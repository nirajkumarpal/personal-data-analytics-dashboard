# Personal Analytics

![Build](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.11-blue)

## Personal Analytics — Daily Study & Wellbeing Dashboard

A lightweight analytics app to track daily study hours, screen time, mood, and tasks — with smart insights and a productivity score. Designed as a polished portfolio project showcasing full-stack development with Python, Flask, SQLAlchemy, and a vanilla frontend.

Live demo: None (local run / Docker-ready)

Screenshots
- Placeholder dashboard screenshot: docs/assets/screenshot-dashboard.png

Features
- User registration and login (secure password hashing)
- CRUD for daily logs and tasks
- Per-user goals and daily progress
- Analytics: trends, productivity score, weekly summary, and smart insights
- Lightweight SQLite default with optional MySQL/Postgres configuration
- Static frontend served from `frontend/` (HTML/CSS/JS)

Tech stack
- Python 3.11
- Flask 3
- SQLAlchemy (Flask-SQLAlchemy)
- SQLite (development) / MySQL or PostgreSQL (production)
- HTML/CSS/JavaScript (Chart.js for charts)
- Docker + docker-compose for production-ready setup

Repository structure

```
├── backend/
│   ├── app.py           # Flask app factory
│   ├── config.py        # Configuration (env-aware)
│   ├── models.py        # SQLAlchemy models
│   └── routes/          # API blueprints
├── frontend/            # Static front-end (HTML/CSS/JS)
├── docs/                # Project documentation
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

Quickstart (local)

1. Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r "./requirements.txt"
```

2. Run the backend server (dev):

```bash
python backend/app.py
# Open http://127.0.0.1:5001/
```

Docker (production-ish)

```bash
docker build -t personal-analytics:latest .
docker-compose up -d
```

Configuration & environment variables
- `SECRET_KEY` — Flask secret key (default in `backend/config.py`).
- `DATABASE_URL` — Optional production DB URI (overrides default `sqlite:///personal_analytics.db`).
- `FLASK_ENV` — `development` or `production`.

API Overview
- Auth: `POST /api/auth/register`, `POST /api/auth/login`
- Logs: `POST /api/logs/add`, `GET /api/logs/fetch?user_id=...`, `PUT /api/logs/update/<id>`, `DELETE /api/logs/delete/<id>`
- Analytics: `GET /api/analytics/summary?user_id=...`, `GET /api/analytics/insights?user_id=...`
- Goals: `POST /api/goals/set`, `GET /api/goals/get?user_id=...`

Contributing
- Please read [CONTRIBUTING.md](CONTRIBUTING.md).

License
- MIT (see [LICENSE](LICENSE))

## 👨‍💻 Author

**Niraj Kumar Pal**

- GitHub: https://github.com/nirajkumarpal
- LinkedIn: https://www.linkedin.com/in/niraj-pal-245196314/
- Email: nirajkumarpal468@gmail.com