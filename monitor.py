import os
import time
import requests
import boto3

# Configuración PredictHQ
TOKEN   = os.environ["PREDICTHQ_TOKEN"]
HEADERS = {"Authorization": f"Bearer {TOKEN}"}
PARAMS  = {
    "category": "concerts,sports",
    "active.gte": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "limit": 100
}
API_URL = "https://api.predicthq.com/v1/events/"

# DynamoDB
dynamo = boto3.resource("dynamodb")
table  = dynamo.Table(os.environ["DDB_TABLE"])

def check_events():
    resp = requests.get(API_URL, headers=HEADERS, params=PARAMS)
    resp.raise_for_status()
    nuevos = []

    for ev in resp.json().get("results", []):
        ev_id = ev["id"]
        if "Item" not in table.get_item(Key={"id": ev_id}):
            # Nuevo: guardar en DynamoDB
            item = {
                "id":       ev_id,
                "title":    ev["title"],
                "category": ev["category"],
                "start":    ev["start"],
                "country":  ev["location"]["country"]
            }
            table.put_item(Item=item)
            nuevos.append(item)
    return nuevos
