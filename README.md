# PzW Kuharica (Cooking App)

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

## Running in production (short note)

Do NOT use the built-in Flask dev server in production. A minimal production start using Gunicorn looks like:

```bash
# from project root, with your virtualenv active
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

On a platform like Render, set environment variables in the dashboard (do NOT commit real secrets). `runtime.txt` is already set to `python-3.11.12` for compatibility.

## Testing / demo notes for school
- To demo: register a user, verify email, create a recipe, show search/pagination and profile -> "My Recipes".
- Admin: create a user and set `is_admin: true` in the `users` collection (or add a small admin seeding script) to access the admin dashboard.

## Security / production reminders
- Keep `DEBUG=False` and `SECRET_KEY` secret in production.
- Use a persistent rate-limit backend (Redis) for real deployments.
- Use TLS (HTTPS) and set `SESSION_COOKIE_SECURE=True` in production.

If you want, I can add a short `Procfile` or a `render.yaml` with recommended build settings — say the word and I’ll scaffold it.

---
Short and simple. Good luck with the project — if you want, I can also add a one-page demo script you can read aloud during your presentation.
