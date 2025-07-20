import os
import json
import boto3
from monitor import check_events

sns    = boto3.client("sns")
TOPIC  = os.environ["SNS_TOPIC_ARN"]

def lambda_handler(event, context):
    nuevos = check_events()
    if nuevos:
        # Construir mensaje para email
        lines = [f"[{e['category']}] {e['title']} — {e['start']} ({e['country']})"
                 for e in nuevos]
        sns.publish(
            TopicArn=TOPIC,
            Subject=f"{len(nuevos)} eventos nuevos",
            Message="\n".join(lines)
        )
    return {
        "statusCode": 200,
        "body": json.dumps({"new": len(nuevos)})
    }
