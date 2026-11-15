"""A tiny API behind CloudFront: answers /api/ requests."""
import json


def handler(event, context):
    body = {"notes": [{"title": "Beach day"}], "path": event.get("rawPath")}
    return {"statusCode": 200, "headers": {"content-type": "application/json"},
            "body": json.dumps(body)}
