import os

class Config:
    # Using SQLite for development (no MySQL setup required)
    # To use MySQL instead, uncomment the line below and update credentials:
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:0751@localhost:3306/personal_analytics'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///personal_analytics.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-for-sessions'
