# Database Documentation

Models (see `backend/models.py`)

- `User` (`users`)
  - `id` PK (Integer)
  - `username` (String(50))
  - `email` (String(120)) unique
  - `password_hash` (String(255))
  - `study_goal` (Float) daily goal in hours

- `DailyLog` (`daily_logs`)
  - `id` PK
  - `user_id` FK -> `users.id`
  - `date` (Date)
  - `study_hours` (Float)
  - `screen_time_hours` (Float)
  - `mood_score` (Integer)

- `Task` (`tasks`)
  - `id` PK
  - `log_id` FK -> `daily_logs.id`
  - `task_name` (String(255))
  - `is_completed` (Boolean)

Relationships

- `User` 1:N `DailyLog` (cascade delete-orphan)
- `DailyLog` 1:N `Task` (cascade delete-orphan)

Indexes & constraints

- `users.email` should be indexed and unique (currently unique constraint exists).
- Consider indexes on `daily_logs(user_id, date)` for time-series queries and `tasks(log_id)`.

Design notes

- SQLite is used for development simplicity. For production switch to PostgreSQL/MySQL and set `DATABASE_URL`.
- Use migrations (Alembic / Flask-Migrate) for schema evolution — currently the project creates tables on app start.
