
from contextlib import asynccontextmanager
import logging
import os
from typing import Any, Dict

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from db.base import get_db
from utils.logging import configure_logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context: runs on startup and shutdown.

    - Configures logging.
    - Logs startup / shutdown events.

    In later phases, we'll also:
      - Initialize DB schemas/migrations
      - Warm up models
      - Connect to external services
    """
    configure_logging()
    logger.info("=== IS Cardiac Agent Backend starting up ===")
    yield
    logger.info("=== IS Cardiac Agent Backend shutting down ===")


app = FastAPI(
    title=os.getenv("APP_NAME", "IS Cardiac Agent Backend"),
    version="0.0.1",
    lifespan=lifespan,
)


@app.exception_handler(Exception)
async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Catch-all exception handler so the API never leaks raw tracebacks.

    Returns a simple JSON 500 response and logs details server-side.
    """
    logger.exception("Unhandled exception for path %s", request.url.path, exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


@app.get("/health", tags=["system"])
def health_check(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Basic health check endpoint.

    - Verifies the API process is alive.
    - Attempts a simple SELECT 1 against the database.
    """
    try:
        db.execute(text("SELECT 1"))
        db_status = "reachable"
    except Exception as exc:  # noqa: BLE001
        logger.exception("Database health check failed", exc_info=exc)
        raise HTTPException(
            status_code=503,
            detail="Database unavailable",
        ) from exc

    return {
        "status": "ok",
        "db": db_status,
        "env": os.getenv("APP_ENV", "unknown"),
    }

