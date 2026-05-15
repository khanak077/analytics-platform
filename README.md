# Real-Time Analytics Platform

Production-grade multi-tenant analytics platform built with FastAPI, PostgreSQL, SQLAlchemy Async, and Docker.

---

# Features

- JWT Authentication
- Multi-Tenancy
- Role-Based Access Control
- API Key Management
- Event Ingestion APIs
- Batch Event Processing
- Analytics Aggregation APIs
- Async SQLAlchemy Architecture
- Alembic Database Migrations

---

# Tech Stack

## Backend
- FastAPI
- PostgreSQL
- SQLAlchemy 2.0 Async
- Alembic
- Docker
- JWT Authentication

---

# Setup

## Clone Repository

```bash
git clone <repo_url>
```

---

## Backend Setup

```bash
cd apps/backend

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

---

## Run PostgreSQL

```bash
docker compose up -d
```

---

## Run Migrations

```bash
alembic upgrade head
```

---

## Start Server

```bash
python -m uvicorn app.main:app --reload
```

---

# API Documentation

Swagger UI:

```txt
http://127.0.0.1:8000/docs
```

---

# Architecture

Clean layered architecture:

- Routes
- Dependencies
- Services
- Models
- Schemas
- Core Infrastructure

---

# Future Improvements

- Redis caching
- Celery async workers
- WebSocket live updates
- Dashboard CRUD
- Scheduled reports
- Alerting system
