from fastapi import FastAPI,APIRouter
from fastapi.middleware.cors import CORSMiddleware
from routes.brokers import router as broker_router
from routes.positions import router as position_router
from routes.etl import router as etl_router

app = FastAPI(title="FinStream API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(broker_router)
app.include_router(position_router)
app.include_router(etl_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}










