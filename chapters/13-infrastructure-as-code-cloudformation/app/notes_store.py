"""Notes in DynamoDB: one partition per user, sorted by creation time."""
import time
import uuid

import boto3

ddb = boto3.client("dynamodb", region_name="us-east-2")
TABLE = "photo-notes"


def add_note(user, title, body, tags=()):
    note_id = uuid.uuid4().hex[:8]
    sk = f"NOTE#{int(time.time())}#{note_id}"
    item = {"pk": {"S": f"USER#{user}"}, "sk": {"S": sk}, "title": {"S": title},
            "body": {"S": body}, "photos": {"N": "0"}}
    if tags:
        item["tags"] = {"SS": list(tags)}
    ddb.put_item(TableName=TABLE, Item=item, ConditionExpression="attribute_not_exists(sk)")
    return sk


def list_notes(user, limit=10):
    values = {":u": {"S": f"USER#{user}"}, ":n": {"S": "NOTE#"}}
    resp = ddb.query(TableName=TABLE, KeyConditionExpression="pk = :u AND begins_with(sk, :n)",
                     ExpressionAttributeValues=values, ScanIndexForward=False, Limit=limit)
    return [(i["title"]["S"], int(i["photos"]["N"])) for i in resp["Items"]]


def add_photo(user, sk):
    ddb.update_item(TableName=TABLE, Key={"pk": {"S": f"USER#{user}"}, "sk": {"S": sk}},
                    UpdateExpression="ADD photos :one",
                    ExpressionAttributeValues={":one": {"N": "1"}})
