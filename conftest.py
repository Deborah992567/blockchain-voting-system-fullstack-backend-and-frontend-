import os
import sys
from pathlib import Path

# Ensure backend package is importable when running pytest from repo root
ROOT = Path(__file__).resolve()
BACKEND = ROOT.joinpath("backend")
if BACKEND.exists() and str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))


def pytest_configure(config):
    # Use a file-backed SQLite DB when running tests from repo root. Using
    # a file avoids the per-connection isolation that comes with
    # sqlite:///:memory: and makes tests more reliable across threads.
    os.environ.setdefault("DATABASE_URL", "sqlite:///./.pytest_test.db")
    os.environ.setdefault("METRICS_ENABLED", "0")
    os.environ.setdefault("SECRET_KEY", "test-secret")
    os.environ.setdefault("TESTING", "1")


import pytest


@pytest.fixture(autouse=True)
def ensure_tables():
    """Create (and later drop) all tables for each test when running from repo root.

    This ensures tests discovered at the repository root (e.g., `tests/`) have a
    clean in-memory database available and avoids "no such table" errors.
    """
    try:
        # Import models so metadata is populated when running tests from repo root
        try:
            import importlib

            importlib.import_module("app.models.user")
            importlib.import_module("app.models.election")
            importlib.import_module("app.models.candidate")
            importlib.import_module("app.models.vote")
        except Exception:
            pass

        from app.database.base import Base
        from app.database.session import engine

        # Reset DB when running tests from repo root so runs are hermetic
        try:
            Base.metadata.drop_all(bind=engine)
        except Exception:
            pass

        Base.metadata.create_all(bind=engine)
    except Exception:
        # If creation fails, let tests handle it (useful when running with a real DB)
        pass

    yield

    try:
        Base.metadata.drop_all(bind=engine)
    except Exception:
        pass
