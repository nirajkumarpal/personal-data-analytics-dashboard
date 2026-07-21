import os


class Config:
    """Application configuration.

    Uses environment variables in production. Defaults are safe for local development.
    """
    # Database: allow override via DATABASE_URL environment variable (Render uses DATABASE_URL)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///personal_analytics.db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'super-secret-key-for-sessions')

    # Debugging
    DEBUG = os.environ.get('FLASK_DEBUG', '0') == '1' or os.environ.get('DEBUG', '0') == '1'

    # Production-ready defaults
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', '1') == '1'
    REMEMBER_COOKIE_SECURE = os.environ.get('REMEMBER_COOKIE_SECURE', '1') == '1'
