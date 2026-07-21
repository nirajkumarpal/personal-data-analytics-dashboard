-- Personal Analytics Database Setup
-- Target DB: personal_analytics

-- CREATE DATABASE IF NOT EXISTS personal_analytics
--   CHARACTER SET utf8mb4
--   COLLATE utf8mb4_unicode_ci;

-- USE personal_analytics;

-- Users
-- CREATE TABLE IF NOT EXISTS users (
--   id INT AUTO_INCREMENT PRIMARY KEY,
--   username VARCHAR(50) NOT NULL,
--   email VARCHAR(120) NOT NULL UNIQUE,
--   password_hash VARCHAR(255) NOT NULL,
--   study_goal FLOAT NOT NULL DEFAULT 6.0,
--   created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--   updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
--   INDEX idx_users_email (email),
--   INDEX idx_users_username (username)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Daily logs
-- CREATE TABLE IF NOT EXISTS daily_logs (
--   id INT AUTO_INCREMENT PRIMARY KEY,
--   user_id INT NOT NULL,
--   date DATE NOT NULL,
--   study_hours FLOAT NOT NULL DEFAULT 0.0,
--   screen_time_hours FLOAT NOT NULL DEFAULT 0.0,
--   mood_score INT NOT NULL DEFAULT 5,
--   created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--   updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
--   CONSTRAINT chk_daily_logs_mood_score CHECK (mood_score >= 1 AND mood_score <= 10),
--   CONSTRAINT uq_daily_logs_user_date UNIQUE (user_id, date),
--   CONSTRAINT fk_daily_logs_user
--     FOREIGN KEY (user_id) REFERENCES users(id)
--     ON DELETE CASCADE
--     ON UPDATE CASCADE,
--   INDEX idx_daily_logs_user_id (user_id),
--   INDEX idx_daily_logs_date (date)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tasks per daily log
-- CREATE TABLE IF NOT EXISTS tasks (
--   id INT AUTO_INCREMENT PRIMARY KEY,
--   log_id INT NOT NULL,
--   task_name VARCHAR(255) NOT NULL,
--   is_completed BOOLEAN NOT NULL DEFAULT FALSE,
--   created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--   updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
--   CONSTRAINT fk_tasks_log
--     FOREIGN KEY (log_id) REFERENCES daily_logs(id)
--     ON DELETE CASCADE
--     ON UPDATE CASCADE,
--   INDEX idx_tasks_log_id (log_id),
--   INDEX idx_tasks_completed (is_completed)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

