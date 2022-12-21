from flask import current_app as app
from flask import request
from .db import get_db
from .util import get_utc_timestamp


@app.route("/jobs", methods=["POST"])
def create_job():
    # create jobs
    db = get_db()
    timestamp = get_utc_timestamp()
    request_data = request.get_json()

    # in the real world we would be doing more in-depth validations with json-schema or something
    # for the sake of this exercise
    if request_data.get("resource") == None:
        return {"payload": "Bad Request"}, 400

    # transaction context
    with db.cursor() as cur:
        try:
            cur.execute(
                "INSERT INTO jobs (timestamp, name, resource_id, status) VALUES (%s, %s, %s, %s);",
                (
                    timestamp,
                    "process_sample",  # in the real world there might be different kinds of jobs
                    request_data[
                        "resource"
                    ],  # ex:"data-10154db7-5c3c-4418-87bf-8e4cbaa312a3.csv",
                    "pending",
                ),
            )
            # notify workers
            cur.execute(
                "NOTIFY jobs_que;",
            )
            db.commit()

        except Exception as e:
            # TODO use more specific error
            # return error to user
            return {"payload": str(e)}, 500

    return {"payload": "job accepted"}, 202


@app.route("/samples", methods=["GET"])
def get_samples():
    db = get_db()

    if "sample_id" not in request.args:
        return {"payload": "Bad Request"}, 400

    print(request.args.get("sample_id"))
    # transaction context
    with db.cursor() as cur:
        SQL = "SELECT * FROM samples WHERE sample_id = %s;"
        cur.execute(SQL, (request.args.get("sample_id"),))
        results = cur.fetchall()
        print(results)

    return {"payload": {"samples": [results]}}, 200
