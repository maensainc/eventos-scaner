import os
import json
import boto3
from monitor import check_events

# Cliente SNS
sns = boto3.client("sns")
TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]

def lambda_handler(event, context):
    nuevos = check_events()
    if nuevos:
        # Construye el mensaje
        lines = [f"[{e['category']}] {e['title']} — {e['start']} ({e['country']})"
                 for e in nuevos]
        mensaje = "\n".join(lines)
        sns.publish(
            TopicArn=TOPIC_ARN,
            Subject=f"{len(nuevos)} eventos nuevos",
            Message=mensaje
        )
    return {
        "statusCode": 200,
        "body": json.dumps({"new_count": len(nuevos)})
    }
