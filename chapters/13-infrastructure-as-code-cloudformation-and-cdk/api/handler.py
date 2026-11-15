"""Photo Notes API: one Lambda handler behind an HTTP API (payload format 2.0)."""
import json

from app.notes_store import add_note, list_notes


def reply(status, body):
    return {"statusCode": status, "headers": {"content-type": "application/json"},
            "body": json.dumps(body)}


def handler(event, context):
    route = event.get("routeKey", "")
    user = "ana"   # one demo user until sign-in exists
    if route == "GET /notes":
        notes = [{"title": t, "photos": p} for t, p in list_notes(user)]
        return reply(200, {"notes": notes})
    if route == "POST /notes":
        try:
            data = json.loads(event.get("body") or "")
            title = data["title"].strip()
        except (ValueError, KeyError, AttributeError):
            return reply(400, {"error": "send JSON with a title"})
        sk = add_note(user, title, data.get("body", ""), tags=data.get("tags", ()))
        return reply(201, {"created": sk})
    return reply(404, {"error": f"no route {route}", "request": context.aws_request_id})
