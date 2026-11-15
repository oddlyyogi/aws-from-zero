"""Print a presigned PUT URL so a browser can upload one photo straight to S3."""
import sys

import boto3

bucket, key = sys.argv[1], sys.argv[2]
s3 = boto3.client("s3", region_name="us-east-2",
                  endpoint_url="https://s3.us-east-2.amazonaws.com",
                  config=boto3.session.Config(s3={"addressing_style": "virtual"}))
url = s3.generate_presigned_url(
    "put_object",
    Params={"Bucket": bucket, "Key": key, "ContentType": "image/png"},
    ExpiresIn=600,
)
print(url)
