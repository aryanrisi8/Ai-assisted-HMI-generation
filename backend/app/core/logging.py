import logging
import sys
from datetime import datetime, timezone
from json import dumps

from app.core.config import settings


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return dumps(payload)


def configure_logging() -> None:
    log_level = logging.DEBUG if settings.debug else getattr(
        logging,
        settings.log_level.upper(),
        logging.INFO,
    )
    handler = logging.StreamHandler(sys.stdout)
    if settings.log_format.lower() == "json":
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")
        )

    logging.basicConfig(level=log_level, handlers=[handler], force=True)

    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.INFO if settings.debug else logging.WARNING
    )
