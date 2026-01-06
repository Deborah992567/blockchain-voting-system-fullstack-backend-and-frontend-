# Blockchain Voting System

This repository contains a demo blockchain voting system (FastAPI backend + static vanilla frontend).

## What I implemented
- Auth: email/password, OTP verification, social login helpers (Google/GitHub)
- Email outbox + SendGrid integration (durable EmailJob model and retry worker)
- OTP model/service with cleanup job via APScheduler
- Redis-backed cache with in-memory fallback
- JWT tokens for auth
- Blockchain contract deploy & vote helpers (Web3)
- Frontend (vanilla): landing, login, register, verify, dashboard with MetaMask signing
- Request timing middleware and handler timing dependency (logs latency + processing time)
- Prometheus metrics (optional) and `/metrics` endpoint
- Alembic migrations and fallback SQL script to apply schema changes
- Tests scaffolding and scripts for local development

## Backend setup (recommended)
1. Create Python virtualenv and install dependencies

```bash
cd backend
./scripts/setup_env.sh
source .venv/bin/activate
```

2. Configure environment variables (recommended via `.env` or shell env):
- `DATABASE_URL` (Postgres)
- `SECRET_KEY` and other OAuth/SendGrid settings (see `app/config.py`)

Example .env values (use your own secure values):

```
DATABASE_URL=postgresql://postgres:YOUR_DB_PASSWORD@localhost:5432/voting-system
SECRET_KEY=your-secret
SENDGRID_API_KEY=your-sendgrid-key
EMAIL_FROM=no-reply@example.com
```

3. Run database migrations (Alembic)

```bash
cd backend
source .venv/bin/activate
alembic upgrade head
```

If Alembic is not available or you prefer a fallback (dev only), run the helper script:

```bash
PYTHONPATH=. python3 app/scripts/apply_migrations.py
```

4. Run the backend

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload
```

5. Run tests

```bash
cd repo_root
PYTHONPATH=backend pytest -q
```

## Frontend (vanilla) notes
- Static files are under `frontend/vanilla`. Open `index.html` in the browser for the demo UI.
- Dashboard supports MetaMask signing and will call `/elections/{id}/details` to get contract info.

## Migrations added
- `alembic/versions/20251229_add_election_admins_and_columns.py` — adds `election_admins` table and election fields
- `alembic/versions/20251230_add_vote_signature_txhash.py` — adds `signature`, `tx_hash`, `wallet_address` columns to `votes`

## Notes & Next steps
- You should **not** store user private keys on the server — the current code supports signed-message verification (and optionally submitting on-chain tx from client). See `POST /votes/submit-signature`.
- Consider adding integration tests that mock Web3 or run against a local Ganache instance for on-chain verification.

## SendGrid & Database logging

- To check SendGrid configuration at runtime use `GET /test/email/check` which returns whether `SENDGRID_API_KEY` is present. An admin-only endpoint `POST /test/email/test?to=you@example.com` will attempt to send a test email.
- A helper script is provided to test SendGrid from the command line: `SENDGRID_API_KEY=KEY TEST_EMAIL=you@example.com python backend/scripts/check_sendgrid.py`
- Database SQL logging can be enabled with `DATABASE_LOGGING=1` (it defaults to enabled when `DATABASE_URL` contains `postgresql`). SQL statements are logged to the `logs/` directory.

## Environment variables and `.env`

Create a `.env` file in `blockchain-voting-system/app/.env` (already used by the app if `python-dotenv` is installed). **Do not commit `.env` to source control.**

Key variables to set in `.env`:

- `DATABASE_URL` — Postgres connection string (e.g., `postgresql://user:pass@localhost:5432/voting-system`)
- `SECRET_KEY` — cryptographic secret for JWTs and other signing
- `SECURITY_PASSWORD_SALT` — salt used for password hashing / reset tokens
- `SENDGRID_API_KEY` — SendGrid API key for transactional email
- `EMAIL_FROM` — sender address for transactional emails
- `ADMIN_ADDRESS` / `ADMIN_PRIVATE_KEY` — admin blockchain wallet (dev only)
- `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` — OAuth for Google
- `GITHUB_CLIENT_ID` / `GITHUB_CLIENT_SECRET` — OAuth for GitHub
- `REDIS_URL` — Redis connection (optional)
- `DATABASE_LOGGING` — `1` or `0` to toggle SQL logging

For local development, a `.env` example is included in `blockchain-voting-system/app/.env`.
