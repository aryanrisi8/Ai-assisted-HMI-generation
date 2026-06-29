# Deployment Instructions

## Targets

- Frontend: Vercel
- Backend: Render Python Web Service
- Database: PostgreSQL

## Frontend On Vercel

Project root: `frontend`

Build settings:

```text
Framework Preset: Vite
Build Command: npm run build
Output Directory: dist
Install Command: npm ci
```

Environment variables:

```text
VITE_API_BASE_URL=https://your-render-backend.onrender.com/api/v1
VITE_API_TIMEOUT=30000
```

The app includes `frontend/vercel.json` with an SPA rewrite to `index.html`.

## Backend On Render

Use either `render.yaml` or manual service creation.

Manual settings:

```text
Root Directory: backend
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
Health Check Path: /api/v1/health
```

Environment variables:

```text
APP_ENV=production
DEBUG=false
LOG_FORMAT=json
LOG_LEVEL=INFO
API_V1_PREFIX=/api/v1
DATABASE_URL=<PostgreSQL connection string>
JWT_SECRET_KEY=<strong generated secret>
BACKEND_CORS_ORIGINS=["https://your-frontend.vercel.app"]
```

## PostgreSQL

The backend accepts these URL forms and normalizes them for `psycopg`:

```text
postgres://...
postgresql://...
postgresql+psycopg://...
```

## Local Docker

```bash
docker compose up --build
```

This starts PostgreSQL, the FastAPI backend, and an Nginx-hosted frontend build.

## Production Checklist

1. Set a strong `JWT_SECRET_KEY`.
2. Set `BACKEND_CORS_ORIGINS` to exact Vercel domains.
3. Add database migrations before first production deploy.
4. Run backend syntax/tests and frontend build in CI.
5. Verify `/api/v1/health`, `/api/v1/health/ready`, and `/api/v1/health/metrics`.
6. Enable Render service logs and alerts.
7. Enable Vercel preview deployments for pull requests.
8. Configure backups and retention for PostgreSQL.

## References

- Vercel Vite deployment docs: https://vercel.com/docs/frameworks/frontend/vite
- Render FastAPI deployment docs: https://render.com/docs/deploy-fastapi
- Render PostgreSQL docs: https://render.com/docs/postgresql-creating-connecting
