from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    study_goal = db.Column(db.Float, nullable=False, default=6.0)  # Daily study goal in hours
    
    # Relationship to DailyLog
    logs = db.relationship('DailyLog', backref='user', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }

class DailyLog(db.Model):
    __tablename__ = 'daily_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    study_hours = db.Column(db.Float, nullable=False, default=0.0)
    screen_time_hours = db.Column(db.Float, nullable=False, default=0.0)
    mood_score = db.Column(db.Integer, nullable=False, default=5) # 1 to 10
    
    # Relationship to Tasks
    tasks = db.relationship('Task', backref='log', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "date": self.date.isoformat() if self.date else None,
            "study_hours": self.study_hours,
            "screen_time_hours": self.screen_time_hours,
            "mood_score": self.mood_score,
            "tasks": [task.to_dict() for task in self.tasks]
        }

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    log_id = db.Column(db.Integer, db.ForeignKey('daily_logs.id'), nullable=False)
    task_name = db.Column(db.String(255), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "log_id": self.log_id,
            "task_name": self.task_name,
            "is_completed": self.is_completed
        }
