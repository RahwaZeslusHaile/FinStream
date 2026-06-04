
import os
from decimal import Decimal
import boto3
from fastapi import FastAPI, Depends
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
    clear_positions()

    dataA = get_broker_a_data()
    dataB = get_broker_b_data()
    
    positions_added = 0
    
    with table.batch_writer() as batch:
        for position in dataA["positions"]:
            qty = Decimal(str(position["qty"]))
            price = Decimal(str(position["price"]))
            
            batch.put_item(
                Item={
                    "broker" : dataA["source"],
                    "ticker" : position["symbol"],
                    "quantity" : qty,
                    "market_value" : price * qty,
                }
            )
            positions_added += 1
        
        for position in dataB:
            qty = Decimal(str(position["amount"]))
            mv = Decimal(str(position["market_value"]))
            
            batch.put_item(
                Item={
                    "broker" : "Broker_B",
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