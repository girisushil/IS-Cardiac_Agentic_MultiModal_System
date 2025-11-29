import os
import sys
from pathlib import Path

from fastapi.testclient import TestClient

# Configure env BEFORE importing the app
os.environ.setdefault("DATABASE_URL", "sqlite:///./test_health.db")
os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("APP_LOG_LEVEL", "debug")

# Ensure cloud_backend/src is on the Python path so `api.main` is importable.
REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_SRC = REPO_ROOT / "cloud_backend" / "src"
sys.path.append(str(BACKEND_SRC))

from api.main import app  # noqa: E402


def test_health_ok() -> None:
    """
    Basic smoke test that /health responds with 200 and the expected keys.
    """
    client = TestClient(app)

    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    assert data["db"] == "reachable"
    assert data["env"] == "test"

