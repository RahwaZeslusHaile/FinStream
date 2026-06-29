# Stage 3: Cloud Database Migration & Event-Driven ETL

This document tracks the architecture, configuration, and implementation details for Stage 3 of FinStream: migrating from a local SQLite database to AWS DynamoDB, implementing EventBridge scheduling, and establishing a raw data storage layer (Data Lake).

---

## 🏗️ Architecture Overview

### Previous Architecture (Stage 1 & 2)
```text
React (S3 / Local) ➔ API Gateway ➔ Lambda (FastAPI) ➔ /tmp/SQLite DB (Ephemeral)
```

### Current Architecture (Stage 3 - Core)
```text
React (S3) ➔ API Gateway ➔ Lambda (FastAPI) ➔ DynamoDB Table (Persistent)
                                ↑
EventBridge Cron (5m) ──────────┘
```

### Next Architecture (Stage 3 - Storage Layer / Data Lake)
```text
                                             ┌──> S3 Bucket (Raw JSON payloads)
                                             │         │
EventBridge Cron (5m) ➔ Lambda Ingestion ────┴─────────▼─────> Lambda ETL Transform ➔ DynamoDB (Clean Positions)
```

---

## 🗄️ DynamoDB Schema Configuration

DynamoDB is a NoSQL key-value and document database. Since our financial positions are queried by broker and asset ticker, we use the following key schema:

* **Table Name:** `finstream-backend-PositionsTable-<ID>` (Created via CloudFormation)
* **Primary Key:**
  * **Partition Key (HASH):** `broker` (Type: String `S`) — e.g. `Broker_A`, `Broker_B`
  * **Sort Key (RANGE):** `ticker` (Type: String `S`) — e.g. `AAPL`, `MSFT`
* **Global Secondary Index (GSI):** `TickerBrokerIndex`
  * **Index Partition Key:** `ticker` (Type: String `S`)
  * **Index Sort Key:** `broker` (Type: String `S`)
  * **Projection:** `ALL` attributes. (Allows querying all positions for a specific ticker across different brokers quickly).

---

## ⏰ Automated ETL Synchronization Flow

Instead of relying on the client's browser to send a HTTP POST request to sync data (which is unreliable and doesn't scale), we configured **Amazon EventBridge** (CloudWatch Events) to trigger our Lambda function every 5 minutes automatically.

### 1. The Trigger (EventBridge)
An EventBridge rule runs on a cron schedule (`rate(5 minutes)`). It sends a custom JSON payload target directly to our Lambda function:
```json
{
  "is_cron": true
}
```

### 2. The Custom Handler
In the backend's `main.py`, the Lambda entry point intercepts this payload. If `"is_cron": true` is present, it directly triggers the ETL logic without routing through HTTP. Otherwise, it delegates HTTP request parsing to `Mangum`:

```python
def handler(event, context):
    if isinstance(event, dict) and event.get("is_cron"):
        print("⏰ EventBridge schedule triggered ETL sync...")
        result = run_etl_sync_logic()
        return result
    asgi_handler = Mangum(app)
    return asgi_handler(event, context)
```

---

## 📥 Storage Layer: S3 Ingestion (Data Lake Pattern)

To implement the Data Lake pattern, we will decouple the API ingestion from the database insertion. The pipeline will operate as follows:

1. **Ingest (Extract & Store Raw):** 
   - Fetch the raw data from `Broker_A` and `Broker_B` mock APIs.
   - Save the raw JSON files directly in the raw S3 bucket under `raw/broker-a.json` and `raw/broker-b.json`.
2. **Transform & Load (Process & Store Clean):**
   - Read the raw JSON files back from S3.
   - Run the normalization logic (convert fields, convert quantities/values to `Decimal` objects).
   - Clear existing rows in DynamoDB.
   - Write the fresh positions into the DynamoDB table using `batch_writer()`.

### Why use a S3 Raw Storage Layer?
* **Auditability:** Keeps a historical record of exactly what data the brokers sent us at any given time.
* **Replayability:** If your business logic changes (e.g. you want to calculate exposure differently), you can re-run your transformer over the historical raw files stored in S3.
* **Separation of Concerns:** The ingestion lambda function only cares about successfully fetching and storing raw data. The transformation function only cares about parsing it.

---

## 🛠️ Key CLI Commands for Verification

### Check DynamoDB Content
```bash
aws dynamodb scan --table-name finstream-backend-PositionsTable-<ID>
```

### Check Deployed CloudFormation Stack Resources
```bash
aws cloudformation list-stack-resources --stack-name finstream-backend
```

### Sync Frontend Build to S3
```bash
aws s3 sync frontend/dist/ s3://finstream-dashboard-rahwa/ --delete
```
