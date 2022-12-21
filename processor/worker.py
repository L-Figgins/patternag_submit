import io
import csv
from os import getenv
import psycopg
import uuid
from google.cloud import storage

conn = psycopg.connect(
    host=getenv("PGHOST", ""),
    dbname=getenv("PGDATABASE", ""),
    user=getenv("PGUSER", ""),
    password=getenv("PGPASSWORD"),
    autocommit=True,
)

BUCKET_NAME = getenv("GS_BUCKET", "patternag-backend-coding-challenge")


def download_public_file_into_memory(bucket_name, source_blob_name):
    """Downloads a public blob from the bucket."""

    storage_client = storage.Client.create_anonymous_client()
    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(source_blob_name)
    # download_as_string is deprecated even though its still in the docs
    contents = blob.download_as_bytes().decode()

    print(
        "Downloaded public blob {} from bucket {}.".format(
            source_blob_name, bucket.name
        )
    )

    return contents


def insert_samples(content, cur):
    """Inserts abundance sample data to sample table based on rows in content"""
    # convert to file object to be used by dict reader
    f = io.StringIO(content)

    reader = csv.DictReader(f)
    SQL = "INSERT INTO samples (id, sample_id, kegg_ortholog, lineage_rank, read_count, relative_abundance, total_filtered_reads, rank, taxon_name) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s);"
    for row in reader:
        cur.execute(
            SQL,
            (
                uuid.uuid4().hex,
                row["sample_id"],
                row["kegg_ortholog"],
                row["lineage_rank"],
                row["read_count"],
                row["relative_abundance"],
                row["total_filtered_reads"],
                row["rank"],
                row["taxon_name"],
            ),
        )
    f.close()


worker_id = uuid.uuid4().hex

print("starting processor", worker_id)
conn.execute("LISTEN jobs_que")
gen = conn.notifies()
for notify in gen:
    print("job notification received")
    sql = "SELECT id, timestamp, resource_id, name, status FROM jobs WHERE status = %s ORDER BY timestamp LIMIT 1 FOR UPDATE SKIP LOCKED;"
    with conn.cursor() as cur:
        # transaction context
        try:
            cur.execute(sql, ("pending",))
            id, timestamp, resource_id, name, status = cur.fetchall()[0]
        except Exception as e:
            # TODO use some exceptions
            print(str(e))

        # download resource content
        try:
            content = download_public_file_into_memory(
                bucket_name=BUCKET_NAME, source_blob_name=resource_id
            )

            # insert into samples table
            insert_samples(content, cur)
            # if no error occured mark job as success
            cur.execute("UPDATE jobs SET status = %s WHERE id= %s", ("success", id))
            print(f"job id:{id} success for resource:{resource_id}")

        except Exception as e:
            # TODO catch specfic exception
            # mark job failed if unable to download file
            print(f"job id:{id} failed for resource:{resource_id}")
            print(str(e))
            cur.execute("UPDATE jobs SET status = %s WHERE id= %s", ("failed", id))

    if notify.payload == "stop":
        gen.close()
