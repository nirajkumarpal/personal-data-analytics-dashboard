# API Documentation

This file documents the public API endpoints implemented in `backend/routes/`.

Auth

- `POST /api/auth/register`
  - Body: `{ "username": string, "email": string, "password": string }`
  - Success: `201` `{ "message": "User registered successfully", "user": { id, username, email } }`
  - Errors: `400` missing fields or email exists.

- `POST /api/auth/login`
  - Body: `{ "email": string, "password": string }`
  - Success: `200` `{ "message": "Login successful", "user": { ... } }`
  - Errors: `400`, `401` for invalid credentials.

Logs

- `POST /api/logs/add`
  - Body: `{ "user_id": int, "date": "YYYY-MM-DD" (optional), "study_hours": float, "screen_time_hours": float, "mood_score": int, "tasks": ["task1","task2"] }`
  - Success: `201` returns created `log` with tasks
  - Errors: `400` for validation errors

- `GET /api/logs/fetch?user_id={id}`
  - Query: `user_id` (required)
  - Success: `200` list of logs (most recent first)

- `PUT /api/logs/update/<log_id>`
  - Body: must include `user_id`. Optional fields: `study_hours`, `screen_time_hours`, `mood_score`.
  - Success: `200` updated log
  - Errors: `400`, `404`

- `DELETE /api/logs/delete/<log_id>?user_id={id}`
  - Success: `200` on deletion

- `PUT /api/logs/<log_id>/tasks/<task_id>/status`
  - Body: `{ "user_id": int, "is_completed": boolean }`
  - Success: `200` updated task

Analytics

- `GET /api/analytics/summary?user_id={id}`
  - Returns chart data (last 30 logs), insights, productivity score, weekly summary.

- `GET /api/analytics/insights?user_id={id}`
  - Returns smart insights and per-log productivity scores.

- `GET /api/analytics/weekly-summary?user_id={id}`
  - Returns aggregation for the last 7 days.

Goals

- `POST /api/goals/set`
  - Body: `{ "user_id": int, "study_goal": float }`
  - Success: `200` with updated `study_goal`

- `GET /api/goals/get?user_id={id}`
  - Returns current `study_goal`, today's study hours and progress percent.

Error handling

- Endpoints return JSON with `error` key and appropriate HTTP status codes.
- Input validation is basic — production should use a schema validation library (e.g., `marshmallow` or `pydantic`).
