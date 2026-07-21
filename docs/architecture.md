# Architecture

This document explains the high-level architecture, request lifecycle, and data flow.

High-level overview

- Backend: Flask app (app factory) exposing REST blueprints in `backend/routes/`.
- Database: SQLAlchemy models in `backend/models.py`.
- Frontend: Static HTML/CSS/JS served from `frontend/`.
- Dev/Prod: Local SQLite by default; production can use MySQL/Postgres via `DATABASE_URL`.

Mermaid diagram (high level):

```mermaid
flowchart LR
  A[Browser (frontend)] -->|HTTP| B[Flask backend]
  B --> C[(Database)]
  B --> D[Analytics module]
  D --> C
```

Request lifecycle

1. Browser sends HTTP request to Flask route (e.g., `/api/logs/add`).
2. Flask blueprint parses request and validates inputs.
3. Business logic uses SQLAlchemy models to read/write data.
4. Backend returns JSON; frontend renders charts and UI.

Separation of concerns

- `app.py` constructs the Flask app and registers blueprints.
- Blueprints (`routes/`) handle request/response and basic validation.
- `analytics/insights.py` contains domain logic for productivity scoring and insights.
- `models.py` contains normalized tables with relationships.
