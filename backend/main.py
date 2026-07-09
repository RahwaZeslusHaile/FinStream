from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from routes.brokers import router as broker_router  # noqa: E402
from routes.etl import router as etl_router  # noqa: E402
from routes.positions import router as position_router  # noqa: E402

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
