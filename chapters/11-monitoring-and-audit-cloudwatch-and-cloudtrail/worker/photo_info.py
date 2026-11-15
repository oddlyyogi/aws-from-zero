"""Photo info worker: reads queued S3 events, records each PNG's size next to it."""
import json
import struct

import boto3

s3 = boto3.client("s3")


def png_size(head):
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    return struct.unpack(">II", head[16:24])


def handler(event, context):
    failures = []
    for record in event["Records"]:
        try:
            detail = json.loads(record["body"])["detail"]
            bucket, key = detail["bucket"]["name"], detail["object"]["key"]
            head = s3.get_object(Bucket=bucket, Key=key, Range="bytes=0-23")["Body"].read()
            width, height = png_size(head)
            info = {"key": key, "width": width, "height": height}
            s3.put_object(Bucket=bucket, Key=f"info/{key}.json", Body=json.dumps(info),
                          ContentType="application/json")
            print(json.dumps(info))
        except Exception as err:
            print(f"failed {record['messageId']}: {err}")
            failures.append({"itemIdentifier": record["messageId"]})
    return {"batchItemFailures": failures}
