from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.utils.logger import logger as base_logger

logger = base_logger.bind(context="db.session")

DATABASE_URL = settings.DATABASE_URL
if not DATABASE_URL:
    # In development/test environments `DATABASE_URL` may be unset. Use a
    # local SQLite file as a safe fallback to avoid crashing on import.
    logger.warning("DATABASE_URL not set; falling back to local SQLite (sqlite:///./dev.db). Set DATABASE_URL in env for Postgres.")
    DATABASE_URL = "sqlite:///./dev.db"

# Tune engine for PostgreSQL and enable optional SQL logging
engine_kwargs = dict(pool_pre_ping=True)
if DATABASE_URL.startswith("postgresql"):
    # reasonable defaults for Postgres; can be overridden by env
    engine_kwargs.update(pool_size=10, max_overflow=20)

engine = create_engine(DATABASE_URL, **engine_kwargs)

# If enabled, attach SQL logging to funnel queries into our logger
if getattr(settings, "DATABASE_LOGGING", False):
    try:
        @event.listens_for(engine, "before_cursor_execute")
        def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            logger.debug("SQL Executing", statement=statement, parameters=str(parameters)[:200])

        @event.listens_for(engine, "handle_error")
        def handle_error(context):
            logger.exception("SQL Error", error=str(context.original_exception))
    except Exception:
        logger.exception("Failed to attach SQL logging listeners")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    logger.debug("DB session opened")
    try:
        yield db
    finally:
        db.close()
        logger.debug("DB session closed")
