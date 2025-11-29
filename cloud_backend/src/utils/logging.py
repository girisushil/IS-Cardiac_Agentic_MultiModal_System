cat > cloud_backend/src/utils/logging.py << 'EOF'
import logging
import os
from typing import Optional


def configure_logging(level: Optional[str] = None) -> None:
    """
    Configure root logger with a simple, consistent format.

    Parameters
    ----------
    level : Optional[str]
        Logging level name (e.g., "info", "debug"). If None, uses APP_LOG_LEVEL env or INFO.
    """
    level_name = (level or os.getenv("APP_LOG_LEVEL", "info")).upper()
    numeric_level = getattr(logging, level_name, logging.INFO)

    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    # Reduce noise from some noisy libraries if needed later
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
EOF
