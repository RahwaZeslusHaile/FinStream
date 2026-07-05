from mangum import Mangum

from main import app
from services.etl import run_etl_sync_logic


def handler(event, context):
    if isinstance(event, dict) and event.get("is_cron"):
        print("⏰ EventBridge schedule triggered ETL sync...")
        result = run_etl_sync_logic()
        return result
    asgi_handler = Mangum(app)
    return asgi_handler(event, context)
