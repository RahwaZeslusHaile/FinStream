---
marp: true
theme: default
class: invert
paginate: true
style: |
  section {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    background-color: #0d0e15;
    color: #e2e8f0;
    padding: 50px;
    font-size: 26px;
  }
  h1 {
    color: #00f2fe;
    font-size: 1.8em;
    border-bottom: 2px solid rgba(0, 242, 254, 0.2);
    padding-bottom: 10px;
  }
  h2 {
    color: #3b82f6;
  }
  h3 {
    color: #a855f7;
  }
  footer {
    font-size: 0.5em;
    color: #64748b;
  }
  code {
    background-color: #1e1b4b;
    color: #a5b4fc;
  }
---

# FinStream
## Prime Broker Data Aggregation Platform

### Rahwa Haile
**Full stack project**

---

# Project Overview

## What is FinStream?

FinStream is a full stack application that aggregates portfolio positions from multiple prime brokers into a single standardized format.

The project demonstrates how financial institutions can:

- Ingest portfolio data from multiple brokers
- Normalize different broker payloads
- Store standardized positions
- Expose REST APIs
- Serve data to downstream applications such as dashboards

---

# Why I Built This Project

- Learn backend development using FastAPI
- Design an ETL pipeline
- Learn AWS serverless services
- Practice clean software architecture
- Understand financial data normalization

---

# Technologies

## Backend

- Python
- FastAPI
- Pydantic
- Boto3

## AWS

- Lambda
- API Gateway
- DynamoDB
- S3

## Frontend

- React
- TypeScript
- Vite

---

# High-Level Architecture

```text
          Broker A
               │
               │
          Broker B
               │
               ▼
        Broker Clients
               │
               ▼
          ETL Service
               │
               ▼
        Data Normalization
               │
               ▼
          DynamoDB
               │
               ▼
          FastAPI API
               │
               ▼
        React Dashboard
```

---

# Project Structure

```text
app/

routes/
services/
repositories/
clients/
mappers/
schemas/
domain/
integrations/
```

Each layer has a single responsibility.

---

# Clean Architecture

```text
Client Request

      │

      ▼

Routes

      │

      ▼

Services

      │

      ▼

Repositories

      │

      ▼

DynamoDB
```

Benefits

- Separation of concerns
- Easier testing
- Better maintainability
- Easier scalability

---

# Responsibilities

## Routes

- Receive HTTP requests
- Validate input
- Call services
- Return responses

---

## Services

Contain business logic.

Examples:

- ETL orchestration
- Position retrieval
- Broker coordination
- Error handling

---

## Repositories

Responsible only for database operations.

Examples:

- Scan all positions
- Query by broker
- Get one position
- Persist normalized positions

This layer isolates DynamoDB from the rest of the application.

---

## Clients

Broker clients communicate with external broker APIs.

Responsibilities

- Fetch Broker A data
- Fetch Broker B data

If a broker API changes, only the client changes.

---

## Mappers

Broker payloads have different formats.

The mapper converts them into one common model.

Example

Broker A

```json
{
  "symbol": "AAPL",
  "qty": 10,
  "price": 200
}
```

Broker B

```json
{
  "ticker": "AAPL",
  "amount": 10,
  "market_value": 2000
}
```

↓

Common Position Model

```text
broker
ticker
quantity
market_value
```

---

# ETL Pipeline

```text
Broker APIs

      │

      ▼

Fetch Raw Data

      │

      ▼

Archive Raw JSON to S3

      │

      ▼

Load Raw Data

      │

      ▼

Normalize Broker Formats

      │

      ▼

Persist Positions

      │

      ▼

Expose REST API
```

---

# DynamoDB Design

## Partition Key

```text
broker
```

## Sort Key

```text
ticker
```

Supported Operations

- Scan → all positions
- Query → positions by broker
- GetItem → one position

---

# Design Decisions

## Broker Registry

Instead of

```python
if broker == BrokerName.broker_a:
```

I use

```python
BROKER_REGISTRY = {
    BrokerName.broker_a: get_broker_a_data,
    BrokerName.broker_b: get_broker_b_data,
}
```

Benefits

- Removes branching
- Easier to extend
- Cleaner code

---

# Repository Pattern

Instead of allowing services to communicate directly with DynamoDB,

Services call repositories.

```text
Service

↓

Repository

↓

DynamoDB
```

Benefits

- Database abstraction
- Easier testing
- Easier migration to PostgreSQL or another database

---

# Challenges

## AWS

- Understanding DynamoDB partition and sort keys
- Learning S3 storage architecture
- Working with Lambda and EventBridge

## Backend

- Designing a clean ETL workflow
- Refactoring into layered architecture
- Separating business logic from persistence
- Resolving circular imports

---

# Future Improvements

- Integrate real broker APIs
- Add Broker C, D and E
- Introduce a Normalizer Registry
- Increase Pytest coverage
- Deploy infrastructure using Terraform
- Add authentication
- Add CloudWatch monitoring

---

# Key Learnings

Through this project I learned:

- FastAPI backend development
- REST API design
- ETL pipeline architecture
- AWS services
- DynamoDB data modelling
- Data normalization
- Repository Pattern
- Clean Architecture
- Financial data aggregation

---

# Thank You

## Questions?