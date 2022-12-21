from os import getenv
import psycopg2

from flask import g


def get_db():
    if "db" not in g:
        g.db = psycopg2.connect(
            host=getenv("PGHOST", ""),
            database=getenv("PGDATABASE", ""),
            user=getenv("PGUSER", ""),
            password=getenv("PGPASSWORD"),
        )
    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_con():
    db = get_db()


def init_app(app):
    app.teardown_appcontext(close_db)
