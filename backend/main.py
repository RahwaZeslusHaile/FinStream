
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, Base, engine
from models import Position
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title = "Fintech Aggregator API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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

@app.post("/api/etl-sync")
def sync_data(db:Session = Depends(get_db)):  
    db.query(Position).delete()
    
    dataA = get_broker_a_data()
    dataB = get_broker_b_data()  
    
    positions_added = 0

    for position in dataA["positions"]:
        db_position = Position(
            ticker=position["symbol"],
            quantity = position["qty"],
            broker = dataA["source"],
            market_value = position["price"] * position["qty"]
        )
        db.add(db_position)
        positions_added += 1

    for position in dataB:
        db_position = Position(
            ticker=position["ticker"],
            quantity = position["amount"],
            broker = "Broker_B",
            market_value = position["market_value"]
        )
        
        db.add(db_position)
        positions_added += 1

    db.commit()
    return {"message": "ETL Sync Completed", "positions_added": positions_added}

@app.get("/api/positions")
def get_positions(db:Session = Depends(get_db)):
    positions = db.query(Position).all()
    return positions
handler = Mangum(app)