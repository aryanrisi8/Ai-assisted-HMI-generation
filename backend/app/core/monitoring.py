import time
from collections import Counter
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response


REQUEST_COUNT: Counter[str] = Counter()
REQUEST_LATENCY_SECONDS: Counter[str] = Counter()


def register_monitoring(app: FastAPI) -> None:
    @app.middleware("http")
    async def metrics_middleware(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        elapsed = time.perf_counter() - start
        route_key = f"{request.method} {request.url.path} {response.status_code}"
        REQUEST_COUNT[route_key] += 1
        REQUEST_LATENCY_SECONDS[route_key] += elapsed
        response.headers["X-Process-Time"] = f"{elapsed:.4f}"
        return response


def render_prometheus_metrics() -> str:
    lines = [
        "# HELP hmi_http_requests_total Total HTTP requests by route/status.",
        "# TYPE hmi_http_requests_total counter",
    ]
    for route_key, count in sorted(REQUEST_COUNT.items()):
        method, path, status_code = route_key.rsplit(" ", 2)
        lines.append(
            'hmi_http_requests_total{'
            f'method="{method}",path="{path}",status_code="{status_code}"'
            f"}} {count}"
        )

    lines.extend(
        [
            "# HELP hmi_http_request_latency_seconds_total Total HTTP request latency by route/status.",
            "# TYPE hmi_http_request_latency_seconds_total counter",
        ]
    )
    for route_key, latency in sorted(REQUEST_LATENCY_SECONDS.items()):
        method, path, status_code = route_key.rsplit(" ", 2)
        lines.append(
            'hmi_http_request_latency_seconds_total{'
            f'method="{method}",path="{path}",status_code="{status_code}"'
            f"}} {latency:.6f}"
        )

    return "\n".join(lines) + "\n"
