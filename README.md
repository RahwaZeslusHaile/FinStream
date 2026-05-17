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
* **Week 1:** Local MVP working
* **Week 2:** Deploy FastAPI to Lambda, connect API Gateway
* **Week 3:** Deploy React to S3 + CloudFront
* **Week 4:** Add RDS or DynamoDB, replace SQLite
* **Week 5:** Add EventBridge ETL automation
