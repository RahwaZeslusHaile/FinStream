# FinStream

A Prime Broker Data Aggregator & Treasury Management Dashboard. This project is designed to ingest, normalize, and visualize financial data from various simulated prime brokers.

## Minimum Viable Product (MVP) Scope

### 1. The Backend (FastAPI + SQLite)
* **Database:** Local SQLite database to ensure a streamlined setup and fast querying without complex configuration.
* **Mock APIs:** Routes that return hardcoded, unstandardized JSON data to simulate two distinct Prime Brokers (e.g., Broker A and Broker B).
* **The Normalizer (ETL) Endpoint:** A core endpoint (e.g., `GET /api/etl-sync`) responsible for fetching the raw mock data, normalizing it into a standardized format, and persisting it to the SQLite database.
* **The Client API:** An endpoint (e.g., `GET /api/positions`) that the frontend consumes to retrieve the cleaned, aggregated position data.

### 2. The Frontend (React + TypeScript)
* **Design Aesthetic:** A single dashboard view utilizing a modern, premium dark-mode UI with glassmorphism elements.
* **Key Metric Cards:** High-level metrics calculated by the backend, displayed prominently:
  * **Total Exposure:** The aggregate sum of all market values.
  * **Daily Financing Cost:** The calculated cost to hold current positions.
* **Data Table:** A comprehensive table displaying the normalized data across brokers, detailing the Ticker, Broker, Quantity, Market Value, and Cost.
* **Data Visualization:** A Recharts Donut Chart illustrating how the total exposure is distributed among the different Prime Brokers.

## Tech Stack
* **Frontend:** React, TypeScript, Recharts
* **Backend:** FastAPI, Python, SQLite, SQLAlchemy
* **Deployment (Planned):** AWS Lambda (via Mangum)

---

## 💻 How to Run Locally

You can run both the backend and frontend locally by following these steps:

### 1. Run the Backend (FastAPI)
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```
3. (Optional) Install dependencies if not already set up:
   * If using `uv` (recommended):
     ```bash
     uv sync
     ```
   * If using standard `pip`:
     ```bash
     pip install -e .
     ```
4. Start the FastAPI development server:
   ```bash
   uvicorn main:app --reload
   ```
   The backend will now be running at `http://127.0.0.1:8000`.

*Note: Since the backend accesses DynamoDB and S3, ensure you have your AWS credentials configured locally (e.g., via `aws configure`), or set appropriate mock environment variables if testing offline.*

### 2. Run the Frontend (React + Vite)
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install the frontend dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
   The frontend dashboard will be accessible at `http://localhost:5173` (or the port specified in your terminal).

### 3. Connect Frontend to Local Backend
By default, [api.ts](file:///Users/cyf/Desktop/Rahwa-development/FinStream/frontend/src/api.ts) might point to an AWS API Gateway endpoint. To point it to your local backend server:
* Open [api.ts](file:///Users/cyf/Desktop/Rahwa-development/FinStream/frontend/src/api.ts) and change the base fetch URLs to use `http://127.0.0.1:8000` (e.g. `http://127.0.0.1:8000/api/positions` and `http://127.0.0.1:8000/api/etl-sync`).

---


## 🧭 How FinStream maps to AWS (Learning Goals)

This project is structured to teach 4 real cloud problems:
* **FastAPI backend** ➔ API hosting (Lambda / ECS)
* **ETL sync endpoint** ➔ Event-driven processing
* **SQLite DB** ➔ Database scaling (RDS / DynamoDB)
* **React dashboard** ➔ Static hosting (S3 + CloudFront)

## 🚀 AWS Evolution Plan

To ensure a smooth learning curve, the project will be built in stages:

### 🥉 Stage 1 — "Local MVP"
Keep everything local to make sure the core logic works:
* FastAPI (monolith)
* SQLite
* Mock broker endpoints
* ETL endpoint
* React dashboard
**👉 Goal:** Make everything work locally first.

### 🥈 Stage 2 — "First AWS Deployment (Simple Hosting)"
* **Backend:** Deploy FastAPI using AWS Lambda + API Gateway (using Mangum to adapt FastAPI to Lambda).
  * *What you learn:* Serverless basics, API Gateway routing, Cold starts.
* **Frontend:** Build React to static files and host on S3 (static hosting) + CloudFront (CDN).
  * *What you learn:* CDN concepts, S3 hosting, Cache behavior.

### 🥇 Stage 3 — "Real Cloud Architecture Upgrade"
Now the project becomes a "real fintech-like architecture".
* **Database Upgrade:** Replace SQLite with **Amazon RDS** (recommended for learning SQL systems) or **Amazon DynamoDB** (for event-driven scaling).
* **Proper ETL Pipeline:** Instead of calling `/etl-sync` manually, use an **EventBridge schedule** (runs every X minutes) to trigger a **Lambda ETL function**.
  * *What you learn:* Scheduled cloud jobs, decoupled systems.
* **Storage Layer (Optional):** Store raw broker JSON in Amazon S3, and store normalized data in the database.
  * *What you learn:* Data lake pattern, raw vs processed data separation.

### 🏗 Stage 4 — "Production-Style Architecture"
Simulate real fintech infrastructure:
* **Security & Observability:** Add IAM roles (security), CloudWatch logs (observability), API throttling (API Gateway), and Secrets Manager (for DB credentials).
  * *What you learn:* Security best practices, monitoring, production constraints.

## 🧠 Recommended Architecture (Final Goal)
```text
React (S3 + CloudFront)
        ↓
API Gateway
        ↓
Lambda (FastAPI via Mangum)
        ↓
RDS (normalized data)
        ↑
EventBridge (scheduled ETL Lambda)
        ↑
S3 (raw broker data)
```

**💡 Key Design Insight:** 
Right now the MVP has an "ETL endpoint you manually call". In the AWS version, this becomes an **"event-driven ETL system that runs automatically"**. This is the biggest conceptual shift you will learn.

## 🧪 Suggested Learning Milestones
* [x] **Week 1:** Local MVP working
* [x] **Week 2:** Deploy FastAPI to Lambda, connect API Gateway
* [x] **Week 3:** Deploy React to S3 + CloudFront
* [x] **Week 4:** Add RDS or DynamoDB, replace SQLite
* [x] **Week 5:** Add EventBridge ETL automation
---

## 🧪 Stage 4: Python Backend Testing Strategy

To ensure code quality and robustness of the backend logic, implement the following testing layers in Python.

### 📁 Backend Directory & Test Structure

Here is the updated layout of your backend structure, showing how the new mappers, repositories, services, and tests are organized:

```text
backend/
├── clients/                  # Raw simulated Broker API callers
│   ├── broker_a_client.py
│   └── broker_b_client.py
├── domain/                   # Domain entities and enums (e.g. BrokerName)
│   └── broker.py
├── integrations/             # AWS Database & Storage connection modules
│   ├── dynamodb.py
│   └── s3.py
├── mappers/                  # Normalization logic translating raw data to schemas
│   ├── broker_a.py           # Broker A normalizer
│   ├── broker_b.py           # Broker B normalizer
│   ├── positions.py          # Unified database model mapper
│   └── registery.py          # Normalizer lookup registry
├── repositories/             # Database access and CRUD queries (no logic)
│   ├── etl.py                # Database save/clear queries
│   └── position.py           # Positions DB query logic
├── routes/                   # FastAPI route definitions
│   ├── brokers.py
│   ├── etl.py
│   └── positions.py
├── schemas/                  # Pydantic schemas (data shapes for API responses)
│   └── positions.py
├── services/                 # Business logic orchestrating repositories & clients
│   ├── broker_registery.py
│   ├── brokers.py
│   ├── etl.py                # Main ETL execution flow
│   └── positions.py          # Positions compilation and fetch logic
├── tests/                    # Pytest suite
│   ├── __init__.py
│   ├── conftest.py            # Global fixtures (e.g., mock table clients)
│   ├── unit/
│   │   ├── __init__.py
│   │   └── test_mappers.py    # Tests for normalizers/mappers
│   └── integration/
│       ├── __init__.py
│       ├── test_repos.py      # Tests database repository functions
│       └── test_routes.py     # Tests FastAPI API endpoints
├── handler.py                # Serverless Lambda entrypoint handler
├── main.py                   # FastAPI local runner setup
└── pyproject.toml            # Project dependencies and config
```



### Phase 1: Python Unit Tests — ETL & Data Normalization
Unit tests validating data mapping, conversions, and edge cases inside [mappers/](file:///Users/cyf/Desktop/Rahwa-development/FinStream/backend/mappers/):
* **Broker A Normalization:** Validate `normalize_broker_a` translates symbol to ticker, calculates `market_value = qty * price`, and handles positive/negative quantities correctly.
* **Broker B Normalization:** Validate `normalize_broker_b` maps keys correctly and handles data arrays.
* **Edge Case Mapping:** Validate mappers handle missing fields, null payloads, and zero values gracefully.

### Phase 2: Python Integration Tests — API Endpoints
Tests using `fastapi.testclient.TestClient` to verify the request/response cycle, route status codes, and JSON serialization:
* **GET `/api/positions`:** Verify returns correct schema list.
* **GET `/api/positions/{broker}`:** Verify returns 404 for unknown brokers and 200 with data for valid ones.
* **POST `/api/etl-sync`:** Verify triggers the ETL flow and reports the correct number of persisted records.
* **Exception Handlers:** Verify corrupted position mapping translates to correct HTTP response status codes.

### Phase 3: Python Repository Tests — DynamoDB Operations
Mocked database tests validating CRUD functionality without hitting the live AWS environment:
* **Mocking:** Use `moto` or local mocks to intercept DynamoDB table actions safely.
* **Clear Table:** Validate `delete_all_positions_repo` deletes all entries cleanly.
* **Batch Writes:** Validate `save_positions_repo` persists position records correctly without duplicates.
* **Queries & Scans:** Validate paginated scans (`scan_all_positions`), single queries (`get_position_item`), and partition key queries (`query_positions_by_broker`).

---

## 🛠️ Python Testing Tech Stack

Configure your testing environment using the following standard tools:

* **Framework:** `pytest` (standard Python testing framework)
* **Mocking:** `pytest-mock` (for utility patching) & `moto` (for DynamoDB mock tables)
* **Coverage:** `pytest-cov` (tracks lines executed)
* **FastAPI Client:** `TestClient` (for local route testing)

### Installation
Run within your backend directory:
```bash
pip install pytest pytest-mock moto pytest-cov
```

### Execution
Run tests locally with:
```bash
pytest
```
