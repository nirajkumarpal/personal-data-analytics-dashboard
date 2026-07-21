# Developer Guide

Setting up development environment

1. Create virtualenv and install dependencies (see README).
2. Run `python backend/app.py` to start the dev server.
3. Consider installing `pre-commit`, `black`, and `flake8` for consistent style.

Recommended improvements for production readiness

- Add database migrations with Alembic/Flask-Migrate.
- Add automated tests (unit + integration) and a small test dataset.
- Replace ad-hoc input validation with a schema library.

Running locally with Docker

- Use `docker-compose` to run the app and a production DB during development.
