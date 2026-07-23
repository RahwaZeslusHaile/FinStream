import logging

from mangum import Mangum

from main import app
from services.etl import run_etl_sync_logic

logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)

asgi_handler = Mangum(app)

def handler(event, context):
    if isinstance(event, dict) and event.get("is_cron"):
        logger.info("⏰ EventBridge schedule triggered ETL sync...")
        try:
            result = run_etl_sync_logic()
            return {
                "statusCode": 200,
                "message": "ETL sync completed successfully", 
                "data": result
            }
        except Exception:
            logger.exception("❌ ETL Sync Failed")
            return {
                "statusCode": 500,
                "message": "❌ ETL Sync Failed"
            }
    return asgi_handler(event, context)
