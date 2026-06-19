import json
import os
from datetime import datetime, timezone
from decimal import Decimal

import boto3
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from database import table

app = FastAPI(title = "Fintech Aggregator API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
s3 = boto3.client("s3")
RAW_DATA_BUCKET = os.getenv("RAW_DATA_BUCKET")


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/mock/broker-a")
def get_broker_a_data():
    return {
        "source": "Broker_A",
        "positions": [
            {"symbol": "AAPL", "qty": 100, "price": 150.25},
            {"symbol": "TSLA", "qty": -50, "price": 200.50},
        ]
    }

@app.get("/mock/broker-b")
def get_broker_b_data():
    return [
        {"ticker": "MSFT", "amount": 200, "market_value": 310.00},
        {"ticker": "AMZN", "amount": 150, "market_value": 135.50},
    ]

def clear_positions():
   scan_params = {"ProjectionExpression":"broker, ticker"}
   while True:
        response = table.scan(**scan_params)
        items = response.get("Items",[])

        with table.batch_writer() as batch:
            for item in items:
                batch.delete_item(
                    Key = {
                        "broker": item["broker"],
                        "ticker": item["ticker"]
                    }
                )
        if "LastEvaluatedKey" not in response:
            break
        scan_params["ExclusiveStartKey"] = response["LastEvaluatedKey"]
        
def run_etl_sync_logic():

    dataA = get_broker_a_data()
    dataB = get_broker_b_data()

    if RAW_DATA_BUCKET:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        s3.put_object(
            Bucket=RAW_DATA_BUCKET,
            Key=f"archive/{timestamp}-broker-a.json",
            Body=json.dumps(dataA),
        )
        s3.put_object(
            Bucket=RAW_DATA_BUCKET,
            Key=f"archive/{timestamp}-broker-b.json",
            Body=json.dumps(dataB),
        )
        s3.put_object(
            Bucket=RAW_DATA_BUCKET,
            Key=f"raw/latest-broker-a.json",
            Body=json.dumps(dataA),
        )
        s3.put_object(
            Bucket=RAW_DATA_BUCKET,
            Key=f"raw/latest-broker-b.json",
            Body=json.dumps(dataB),
        )
    positions_a = dataA.get("positions",[])
    broker_a_name = dataA.get("source","broker_A")
    positions_b = dataB

    if RAW_DATA_BUCKET:
        try:
            responseA = s3.get_object(Bucket=RAW_DATA_BUCKET, Key="raw/latest-broker-a.json")
            responseB = s3.get_object(Bucket=RAW_DATA_BUCKET, Key="raw/latest-broker-b.json")
            processed_dataA = json.loads(responseA["Body"].read().decode('utf-8'))
            processed_dataB = json.loads(responseB["Body"].read().decode('utf-8'))
            positions_a = processed_dataA.get("positions",[])
            broker_a_name = processed_dataA.get("source", "broker_A")
            positions_b = processed_dataB
        except Exception as e:
            print(f"Error reading s3 data: {e}")
    
    positions_added = 0
    
    with table.batch_writer() as batch:
        for position in positions_a:
            qty = Decimal(str(position["qty"]))
            price = Decimal(str(position["price"]))
            
            batch.put_item(
                Item={
                    "broker" : broker_a_name,
                    "ticker" : position["symbol"],
                    "quantity" : qty,
                    "market_value" : price * qty,
                }
            )
            positions_added += 1
        
        for position in positions_b:
            qty = Decimal(str(position["amount"]))
            mv = Decimal(str(position["market_value"]))
            
            batch.put_item(
                Item={
                    "broker" : "broker_B",
                    "ticker" : position["ticker"],
                    "quantity" : qty,
                    "market_value" : mv
                }
            )
            positions_added += 1
    return {"message": "ETL Sync Completed","positions_added": positions_added }
        
    
            
        
@app.post("/api/etl-sync")
def sync_data():  
  return run_etl_sync_logic()
@app.get("/api/positions")
def get_positions():
    scan_params = {}
    positions = []
    while True:
        response = table.scan(**scan_params)
        for item in response.get("Items", []):
            positions.append({
                "broker": item.get("broker"),
                "ticker": item.get("ticker"),
                "quantity": item.get("quantity"),
                "market_value": item.get("market_value")
            })

        if "LastEvaluatedKey" not in response:
            break
        scan_params["ExclusiveStartKey"] = response["LastEvaluatedKey"]
        
    return positions

def handler(event, context):
    if isinstance(event, dict) and event.get("is_cron"):
        print("⏰ EventBridge schedule triggered ETL sync...")
        result = run_etl_sync_logic()
        return result
    asgi_handler = Mangum(app)
    return asgi_handler(event,context)