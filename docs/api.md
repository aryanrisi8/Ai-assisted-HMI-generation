# API Documentation

Base path: `/api/v1`

Interactive docs are available from FastAPI at:

- Swagger UI: `/docs`
- OpenAPI JSON: `/openapi.json`

## Health And Monitoring

- `GET /health`: liveness check.
- `GET /health/ready`: readiness check with database connectivity.
- `GET /health/metrics`: Prometheus-style request metrics.

## Authentication

- `POST /auth/register`: register a user and return a JWT.
- `POST /auth/login`: JSON login endpoint.
- `POST /auth/token`: OAuth2 password-form token endpoint.
- `GET /auth/me`: current authenticated user.

## Metadata

- `POST /metadata`: create system, sensors, signals, and alarm thresholds.
- `GET /metadata`: list metadata aggregates.
- `GET /metadata/{id}`: read one metadata aggregate.
- `PUT /metadata/{id}`: update one metadata aggregate.
- `DELETE /metadata/{id}`: delete one metadata aggregate.

## Templates

- `POST /templates`: create a reusable template.
- `GET /templates`: search by `q`, `industry`, `category_id`, and `is_active`.
- `GET /templates/{id}`: read one template.
- `PUT /templates/{id}`: update one template.
- `DELETE /templates/{id}`: delete one template.
- `POST /templates/{id}/clone`: clone a template.

Template shape:

```json
{
  "name": "Cooling Overview",
  "slug": "cooling-overview",
  "industry": "manufacturing",
  "category_id": "uuid",
  "layout": {},
  "components": []
}
```

## Template Categories

- `POST /template-categories`
- `GET /template-categories`
- `PUT /template-categories/{id}`
- `DELETE /template-categories/{id}`

## Dashboards

- `POST /dashboards`: create dashboard and persist editor layout JSON.
- `GET /dashboards`: list saved dashboards.
- `GET /dashboards/{id}`: restore saved dashboard editor state.
- `PUT /dashboards/{id}`: update dashboard metadata and layout JSON.
- `DELETE /dashboards/{id}`: delete dashboard.
- `POST /dashboards/generate/{metadata_id}`: generate dashboard schema from metadata.
- `GET /dashboards/recommendations/{metadata_id}`: get component recommendations.

## Alarm Intelligence

- `POST /alarm-intelligence/analyze`: analyze without persisting.
- `POST /alarm-intelligence/process`: analyze and persist.
- `GET /alarm-intelligence/results`: list recent persisted results.
- `GET /alarm-intelligence/results/{id}`: read one persisted result.

Example request:

```json
{
  "events": [
    {
      "code": "ALM-COOL-PUMP-01",
      "name": "Cooling Pump Trip",
      "severity": "critical",
      "source": "Cooling Loop A",
      "signal_tag": "PUMP_A_STATUS",
      "message": "Cooling pump failure detected"
    }
  ]
}
```

Example response data:

```json
{
  "root_cause": "Cooling Pump Failure",
  "confidence": 87,
  "affected_signals": ["PUMP_A_STATUS"]
}
```
