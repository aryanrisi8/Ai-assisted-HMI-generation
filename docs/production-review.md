# Production Architecture Review

## Current Strengths

- Clear FastAPI modular layering: routers, services, repositories, models, schemas, auth, and core utilities.
- Frontend has a real dashboard editor using React Grid Layout with drag, resize, add, delete, save, and restore behavior.
- Template management supports create, update, delete, clone, search, and categorization.
- Alarm intelligence pipeline covers severity ranking, duplicate suppression, grouping, root-cause suggestions, and clustering.
- JWT auth and protected routes are present.
- Health, readiness, metrics, JSON logging, Dockerfiles, Docker Compose, Vercel config, and Render blueprint are present.

## Production Gaps To Address Before Launch

### Database Migrations

Alembic migration files are not present. Production deploys need deterministic migrations for current models, including `sensors`, dashboard editor persistence, template JSON columns, and alarm intelligence results.

### Authentication Hardening

- Add refresh-token rotation or short-lived access tokens plus refresh sessions.
- Add password reset flow and email verification if public registration remains enabled.
- Add rate limiting on login and registration.
- Consider account lockout after repeated failed login attempts.

### Authorization Model

- Current route protection mostly checks authenticated users.
- Add permission dependencies for admin, engineer, operator, and viewer capabilities.
- Enforce ownership or project-level access on dashboards, templates, and metadata.

### Data Validation And Schema Versioning

- Dashboard layout JSON and component JSON should be validated against a registry schema.
- Template schema versions should be explicit and migratable.
- Alarm intelligence input should support stream source IDs and ingestion timestamps.

### Observability

- The current metrics hook is intentionally lightweight.
- For production, add OpenTelemetry traces and structured request IDs.
- Send logs to Render log streams or an external provider.
- Add alerting for readiness failures, 5xx rates, and database latency.

### Testing

- Add API tests for auth, metadata, templates, dashboards, and alarm intelligence.
- Add frontend editor tests for add, delete, drag, save, and restore flows.
- Add contract tests around JSON schema rendering.

### Security

- Disable permissive CORS in production.
- Keep `.env` files out of Git.
- Add security headers on the frontend host where applicable.
- Run dependency scanning in CI.
- Avoid logging sensitive request payloads.

### Runtime Performance

- Pandas and Scikit-learn are acceptable for request-sized analysis, but high-volume alarm streams should move to a worker queue.
- Add background jobs for incident clustering if payloads grow.
- Add database indexes based on observed dashboard/template/alarm query patterns.

## Recommended Next Steps

1. Add Alembic and create the initial production migration.
2. Add CI workflow for backend syntax/tests and frontend build.
3. Add RBAC enforcement dependencies.
4. Add request ID middleware and OpenTelemetry export.
5. Add seed data for roles and starter template categories.
6. Add production smoke-test script for deployed Vercel and Render URLs.
