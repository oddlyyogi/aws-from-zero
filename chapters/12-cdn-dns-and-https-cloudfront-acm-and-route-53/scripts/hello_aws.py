"""Say hello to AWS: who we are, what is in our bucket, and a safe error."""
import sys
from botocore.config import Config


import boto3
from botocore.exceptions import ClientError

session = boto3.Session(region_name="us-east-2")
retries = Config(retries={"max_attempts": 5, "mode": "standard"})
sts = session.client("sts")
print("account:", sts.get_caller_identity()["Account"])

s3 = session.client("s3", config=retries)
bucket = sys.argv[1]
pages = s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix="notes/")
for page in pages:
    for obj in page.get("Contents", []):
        print(f"{obj['Key']:<20} {obj['Size']:>4} bytes")

ddb = session.client("dynamodb")
ddb.get_waiter("table_exists").wait(TableName="photo-notes-cli")
ddb.put_item(TableName="photo-notes-cli",
             Item={"note_id": {"S": "n-002"}, "title": {"S": "Harbour walk"}})
item = ddb.get_item(TableName="photo-notes-cli", Key={"note_id": {"S": "n-002"}})["Item"]
print("note:", item["title"]["S"])
try:
    ddb.describe_table(TableName="no-such-table")
except ClientError as err:
    print("handled:", err.response["Error"]["Code"])
