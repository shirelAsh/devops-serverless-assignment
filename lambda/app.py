import json
import os
import boto3
from datetime import datetime, timezone

s3 = boto3.client("s3")
sns = boto3.client("sns")


def lambda_handler(event, context):
    bucket = os.environ["BUCKET_NAME"]
    topic_arn = os.environ["TOPIC_ARN"]

    resp = s3.list_objects_v2(Bucket=bucket)
    objects = [obj["Key"] for obj in resp.get("Contents", [])]

    message = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "bucket": bucket,
        "object_count": len(objects),
        "objects": objects,
    }

    sns.publish(
        TopicArn=topic_arn,
        Subject="Lambda execution report",
        Message=json.dumps(message, indent=2),
    )

    return {"statusCode": 200, "body": json.dumps(message)}