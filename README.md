# Zoula Air - Backend API

This is the core flight management system for **Zoula Air**, built with a modern Python stack focused on performance, type safety, and scalability.

## Tech Stack

- **Python 3.12+**
- **FastAPI** - High-performance web framework.
- **uv** - Ultra-fast Python package manager.
- **PostgreSQL** - Relational database.
- **SQLAlchemy 2.0** - SQL Toolkit and ORM.
- **Docker & Docker Compose** - Containerized database environment.
- **Alembic** - Database migration management.

---

## Local Setup Guide

Follow these steps to get your development environment up and running.

### 1. Clone the Repository

```bash
git clone https://github.com/AlexT878/zoula-air-app
cd zoula-air-app
```

### 2\. Environment Configuration

Copy the example environment file to create your local config. The default values are pre-configured for the Docker setup.

```bash
cp backend/.env.example backend/.env
```

### 3\. Start Database (Docker)

Ensure Docker Desktop is running, then start the PostgreSQL container:

```bash
docker-compose up -d
```

_This will spin up a Postgres instance at localhost:5432 with the credentials defined in your .env._

### 4\. Install Dependencies

Use uv to sync and install the project dependencies:

```bash
cd backend
uv sync
```

### 6\. Launch the API

Start the FastAPI development server with auto-reload enabled:

```bash
uv run uvicorn app.main:app --reload
```

---

Developed with ❤️ for the **Zoula Air** team.
