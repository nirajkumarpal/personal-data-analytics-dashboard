import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from backend.config import Config
from backend.models import db
from flask_migrate import Migrate

# Create the Migrate instance (initialized with app in create_app)
migrate = Migrate()


def create_app():
    # Resolve absolute path to the frontend directory to avoid path issues under Gunicorn
    frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))

    app = Flask(
        __name__,
        static_folder=frontend_dir,
        template_folder=frontend_dir,
    )

    # Allow local frontend dev servers and same-origin backend access.
    CORS(
        app,
        origins=[
            "http://127.0.0.1:5001",
            "http://localhost:5001",
            "http://127.0.0.1:5500",
            "http://localhost:5500",
        ],
        supports_credentials=True,
    )

    app.config.from_object(Config)

    db.init_app(app)
    # Initialize migration support
    migrate.init_app(app, db)

    # Register Blueprints
    from backend.routes.auth_routes import auth_bp
    from backend.routes.log_routes import log_bp
    from backend.routes.analytics_routes import analytics_bp
    from backend.routes.goal_routes import goals_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(log_bp, url_prefix='/api/logs')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
    app.register_blueprint(goals_bp, url_prefix='/api/goals')

    @app.route('/')
    def serve_login():
        return send_from_directory(frontend_dir, 'login.html')

    @app.route('/<path:path>')
    def serve_static(path):
        """Serve frontend files (index, css, js, etc.)."""
        try:
            return send_from_directory(frontend_dir, path)
        except Exception:
            return send_from_directory(frontend_dir, 'index.html')

    @app.route('/api/test-connection')
    def test_connection():
        return {"message": "Backend is running and connected to the database!"}

    # In development it's convenient to auto-create tables. In production,
    # rely on migrations (Flask-Migrate / Alembic) and do not call create_all()
    run_create_all = (
        app.config.get('DEBUG', False)
        or os.environ.get('FLASK_ENV') == 'development'
        or os.environ.get('AUTO_CREATE_DB', '0') == '1'
    )

    if run_create_all:
        app.logger.info('Running db.create_all() because DEBUG/development is enabled.')
        db.create_all()

    return app


if __name__ == '__main__':
    # Local dev runner; in production use Gunicorn with the WSGI entrypoint
    app = create_app()
    port = int(os.environ.get('PORT', 5001))
    debug = bool(os.environ.get('FLASK_DEBUG', app.config.get('DEBUG', False)))
    print('Personal Analytics App is running.')
    print(f'Open this link in browser -> http://127.0.0.1:{port}/')
    # Configure simple logging for local runs
    import logging

    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
    app.run(host='0.0.0.0', port=port, debug=debug)
