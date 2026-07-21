# Deployment Guide

This guide explains recommended deployment options: Docker (recommended), or a PaaS (Render, Railway).

Docker

1. Build image:

```bash
docker build -t personal-analytics:latest .
```

2. Run with docker-compose:

```bash
docker-compose up -d
```

Notes
- Use a production WSGI server like `gunicorn` behind a reverse proxy (nginx).
- Configure `DATABASE_URL` to point to managed Postgres/MySQL.
- Manage secrets using environment variables or a secrets manager.

PaaS (Render / Railway)

- Set environment variables (SECRET_KEY, DATABASE_URL) in the service settings.
- Use a managed database and attach it to your service.

CI/CD
- Use GitHub Actions (sample workflow at `.github/workflows/ci.yml`) to run linters and tests.
- Create a release workflow to build and push Docker images to GitHub Container Registry.
