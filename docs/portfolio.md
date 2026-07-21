# Portfolio Assets: Resume, LinkedIn, Interview Q&A, Review

Resume Project Description

Personal Analytics — personal-analytics
- Built a full-stack personal analytics dashboard to track study hours, screen time, mood, and tasks. Implemented a Flask backend with SQLAlchemy, a responsive static frontend, and analytics routines to generate productivity scores and actionable insights.

ATS-friendly bullets
- Built RESTful APIs with Flask and SQLAlchemy; designed normalized data models and relationships.
- Implemented user authentication, secure password hashing, and per-user goals and progress tracking.
- Developed analytics module to compute productivity scores, weekly summaries, and time-series chart data.
- Containerized the application with Docker and provided CI linting workflow using GitHub Actions.

LinkedIn Post (short)

Just shipped a polished Personal Analytics dashboard: tracks study habits, mood, and tasks with smart insights. Built with Flask, SQLAlchemy, and a minimal JS frontend. Docker-ready and documented. Feedback welcome! #Python #Flask #DataScience

Interview Questions (select)

1. How does your Flask app scale for many users?
- Answer: Discuss WSGI servers, horizontal scaling, managed DB, connection pooling, caching layers (Redis), and async workers.

2. How would you secure the API in production?
- Answer: Use HTTPS, JWT or server-side sessions, CSRF protection, input validation, rate limiting, and secret management.

Project review scores (out of 10)

- Code quality: 7/10 — Solid structure, but needs tests and migrations.
- Documentation: 8/10 — Good start; add diagrams and examples.
- Architecture: 7/10 — Clear separation; improve validation and migration strategy.
- Professionalism: 7/10 — Needs CI tests, release process, and issue templates (added).
