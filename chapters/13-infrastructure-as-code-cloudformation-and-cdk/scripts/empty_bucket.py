"""Delete every version and delete marker in a bucket, so the bucket itself can be deleted."""
import sys

import boto3

bucket = sys.argv[1]
s3 = boto3.client("s3", region_name="us-east-2")
pages = s3.get_paginator("list_object_versions").paginate(Bucket=bucket)
removed = 0
for page in pages:
    items = page.get("Versions", []) + page.get("DeleteMarkers", [])
    batch = [{"Key": i["Key"], "VersionId": i["VersionId"]} for i in items]
    if batch:
        s3.delete_objects(Bucket=bucket, Delete={"Objects": batch, "Quiet": True})
        removed += len(batch)
print("removed", removed, "versions and markers")
