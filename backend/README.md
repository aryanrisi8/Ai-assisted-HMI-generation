# FastAPI Backend Foundation

## Module Layout

```text
backend/
  app/
    main.py
    auth/
      dependencies.py
      schemas.py
      security.py
    core/
      config.py
      exceptions.py
      logging.py
      responses.py
    db/
      base.py
      session.py
    repositories/
      base.py
      role_repository.py
      user_repository.py
    routers/
      api.py
      auth.py
      health.py
      users.py
    services/
      auth_service.py
      user_service.py
    models.py
    schemas.py
```

## Run Locally

```bash
cd backend
python -m venv .venv
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## Configuration

Configuration is loaded from environment variables through `app.core.config.Settings`.

The database URL can be supplied directly:

```text
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/hmi_platform
```

Or assembled from:

```text
POSTGRES_HOST
POSTGRES_PORT
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
```

## Auth Endpoints

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/token`
- `GET /api/v1/auth/me`
- `GET /api/v1/users/me`
- `POST /api/v1/metadata`
- `GET /api/v1/metadata`
- `GET /api/v1/metadata/{id}`
- `PUT /api/v1/metadata/{id}`
- `DELETE /api/v1/metadata/{id}`

## Foundation Boundaries

- Routers handle HTTP concerns only.
- Services own business decisions and transaction flow.
- Repositories own SQLAlchemy query details.
- Auth dependencies own current-user resolution and permission gates.
- Core modules own settings, logging, errors, and response envelopes.
