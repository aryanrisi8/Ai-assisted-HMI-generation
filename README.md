# AI-Assisted HMI Generation Platform

Production-oriented platform for adaptive HMI dashboard generation, visual dashboard editing, template management, metadata management, and alarm intelligence.

## Stack

- Frontend: React, Vite, Tailwind CSS, React Router, Axios, React Grid Layout
- Backend: FastAPI, SQLAlchemy, PostgreSQL, JWT authentication
- Intelligence: Pandas, Scikit-learn
- Target hosting: Vercel frontend, Render backend, PostgreSQL database

## Repository Layout

```text
backend/      FastAPI API, SQLAlchemy models, services, repositories
frontend/     React/Vite HMI frontend and visual dashboard editor
docs/         Architecture, database, API, deployment, and production review docs
```

## Local Docker Run

```bash
docker compose up --build
```

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000/api/v1/health`
- API docs: `http://localhost:8000/docs`
- PostgreSQL: `localhost:5432`

## Production Targets

- Deploy `frontend/` to Vercel.
- Deploy `backend/` to Render as a Python web service.
- Use Render PostgreSQL or another managed PostgreSQL provider.

See [deployment.md](docs/deployment.md), [api.md](docs/api.md), and [production-review.md](docs/production-review.md).
