"""Logging configuration, driven by settings (with optional ANSI colors)."""

import logging
import os
import sys
from logging.config import dictConfig

from app.core.settings import settings

_RESET = "\033[0m"
_LEVEL_COLORS = {
    "DEBUG": "\033[36m",  # cyan
    "INFO": "\033[32m",  # green
    "WARNING": "\033[33m",  # yellow
    "ERROR": "\033[31m",  # red
    "CRITICAL": "\033[1;31m",  # bold red
}


def _colors_enabled() -> bool:
    """Colorize only when enabled, honoring NO_COLOR and a real TTY."""
    if not settings.log_colors:
        return False
    if os.environ.get("NO_COLOR") is not None:
        return False
    return sys.stdout.isatty()


class ColorFormatter(logging.Formatter):
    """Wraps each record in an ANSI color chosen by its level."""

    def __init__(self, *args, use_colors: bool | None = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.use_colors = _colors_enabled() if use_colors is None else use_colors

    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        if self.use_colors:
            color = _LEVEL_COLORS.get(record.levelname)
            if color:
                return f"{color}{message}{_RESET}"
        return message


def configure_logging() -> None:
    """Configure root + uvicorn/SQLAlchemy loggers with a service-tagged formatter."""
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "()": "app.core.logging.ColorFormatter",
                    "format": (
                        f"%(asctime)s %(levelname)s [{settings.service_name}] %(name)s: %(message)s"
                    ),
                    "datefmt": "%Y-%m-%dT%H:%M:%S%z",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "stream": "ext://sys.stdout",
                },
            },
            "root": {
                "level": settings.log_level,
                "handlers": ["console"],
            },
            "loggers": {
                "uvicorn.error": {"level": settings.log_level, "propagate": True},
                "uvicorn.access": {"level": "WARNING", "propagate": True},
                "sqlalchemy.engine": {
                    "level": "INFO" if settings.database.echo else "WARNING",
                    "propagate": True,
                },
            },
        }
    )
