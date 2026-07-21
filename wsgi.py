"""WSGI entrypoint for Gunicorn and platforms like Render.

Creates the Flask application using the application factory and exposes the
WSGI callable `app` that Gunicorn will use: `gunicorn wsgi:app`.
"""
from backend.app import create_app


app = create_app()
