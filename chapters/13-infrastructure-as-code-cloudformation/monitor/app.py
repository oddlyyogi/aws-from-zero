"""A talkative function for the monitoring demo: structured logs and one custom metric."""
import json
import random
import time


def log(level, **fields):
    print(json.dumps({"level": level, **fields}))


def metric(name, value, unit="Count"):
    print(json.dumps({
        "_aws": {"Timestamp": int(time.time() * 1000),
                 "CloudWatchMetrics": [{"Namespace": "PhotoNotes", "Dimensions": [["Route"]],
                                        "Metrics": [{"Name": name, "Unit": unit}]}]},
        "Route": "GET /notes", name: value}))


def handler(event, context):
    start = time.perf_counter()
    if event.get("fail"):
        log("ERROR", route="GET /notes", error="storage unavailable")
        raise RuntimeError("storage unavailable")
    time.sleep(random.uniform(0.01, 0.05))
    ms = round((time.perf_counter() - start) * 1000, 1)
    log("INFO", route="GET /notes", ms=ms)
    metric("NotesServed", 1)
    return {"statusCode": 200, "ms": ms}
