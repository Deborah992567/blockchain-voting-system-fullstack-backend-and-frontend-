from fastapi import FastAPI, Depends
from app.deps.timing import timing_dependency
from app.routes import election, candidate, test, auth
from app.routes import vote, results
from app.database.base import Base
from app.database.session import engine
import uvicorn
from app.models import user, election as election_model, candidate as candidate_model, vote as vote_model, otp, email_job  # import all models (including OTP and EmailJob)
from app.utils.logger import logger as base_logger
from app.tasks.scheduler import start_scheduler, stop_scheduler

logger = base_logger.bind(context="app")

app = FastAPI(dependencies=[Depends(timing_dependency)])

# Register request timing middleware to log latency & processing time
from app.middleware.request_timing import request_timing_middleware
app.middleware('http')(request_timing_middleware)

# CORS
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Metrics endpoint
from fastapi.responses import Response
from app.metrics import metrics_response, METRICS_ENABLED


@app.get('/metrics')
def metrics():
    if not METRICS_ENABLED:
        return Response('metrics disabled', status_code=503)
    resp = metrics_response()
    return Response(content=resp, media_type="text/plain; version=0.0.4; charset=utf-8")

app.include_router(auth.router)
app.include_router(election.router)
app.include_router(candidate.router)
app.include_router(test.router)
app.include_router(vote.router)
app.include_router(results.router)


@app.get("/")
def root():
    return {"message": "Backend is alive!"}


def init_db():
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")


@app.on_event("startup")
def _startup():
    init_db()
    # Warn if critical secrets are missing in env
    if not settings.SECRET_KEY:
        logger.warning("SECRET_KEY is not set. Set SECRET_KEY in your environment or .env for secure tokens.")
    if not settings.DATABASE_URL:
        logger.error("DATABASE_URL is not set. Configure DATABASE_URL to point to your Postgres instance.")
    # Database connectivity check
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        logger.info("Database connected", url=str(settings.DATABASE_URL))
    except Exception:
        logger.exception("Database connection failed; ensure DATABASE_URL is correct and Postgres is reachable")

    # SendGrid configuration notice
    if not settings.SENDGRID_API_KEY:
        logger.warning("SendGrid API key not configured. Email sending will be disabled until SENDGRID_API_KEY is set.")
    else:
        logger.info("SendGrid configured (key present)")
        if not settings.EMAIL_FROM:
            logger.warning("SENDGRID_API_KEY is present but EMAIL_FROM is not configured. Set EMAIL_FROM to a valid sender address.")

    if not settings.ADMIN_PRIVATE_KEY:
        logger.info("ADMIN_PRIVATE_KEY not set; on-chain admin operations will be disabled unless provided")
    start_scheduler(app)
    logger.info("Application startup complete")


@app.on_event("shutdown")
def _shutdown():
    stop_scheduler(app)
    logger.info("Application shutdown complete")


if __name__ == "__main__":
    init_db()
    print("Database tables created!")
    uvicorn.run(app, host="0.0.0.0", port=8000)