# PzW Kuharica (FamilyRecipes)

Small Flask + MongoDB recipe app used for a school project. It includes user registration, email verification, recipe CRUD with image uploads (GridFS), admin tools and basic rate-limiting.

This README is intentionally short — just what you need to run the project locally and a couple of deployment hints.

## Quick start (local)

1. Create and activate a virtual environment (Python 3.11+ recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy the example env and edit it:

```bash
cp .env.example .env
# Edit .env and set MONGO_URI, SECRET_KEY, MAIL_*, etc.
```

4. Run the app (development):

```bash
python run.py
```

Open http://127.0.0.1:5000 in your browser.

## Important env variables
- `SECRET_KEY` — set a long random secret for session security.
- `MONGO_URI` — MongoDB connection string. Include the database name, e.g. `mongodb+srv://user:pass@host/mydb?...`.
- `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_DEFAULT_SENDER` — SMTP settings for verification emails.
- `RATELIMIT_STORAGE_URI` (optional) — set to a Redis URI in production (recommended) to make Flask-Limiter work across multiple processes/instances.

See `.env.example` for full placeholders.

