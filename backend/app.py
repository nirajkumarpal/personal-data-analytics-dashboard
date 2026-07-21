from flask import Flask, send_from_directory
from flask_cors import CORS
from config import Config
from models import db


def create_app():
    app = Flask(
        __name__,
        static_folder='../frontend',
        template_folder='../frontend'
    )

    # Allow local frontend dev servers and same-origin backend access.
    CORS(
        app,
        origins=[
            "http://127.0.0.1:5001",
            "http://localhost:5001",
            "http://127.0.0.1:5500",
            "http://localhost:5500"
        ],
        supports_credentials=True
    )
    app.config.from_object(Config)

    db.init_app(app)

    # Register Blueprints
    from routes.auth_routes import auth_bp
    from routes.log_routes import log_bp
    from routes.analytics_routes import analytics_bp
    from routes.goal_routes import goals_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(log_bp, url_prefix='/api/logs')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
    app.register_blueprint(goals_bp, url_prefix='/api/goals')

    @app.route('/')
    def serve_login():
        return send_from_directory('../frontend', 'login.html')

    @app.route('/<path:path>')
    def serve_static(path):
        """Serve frontend files (index, css, js, etc.)."""
        try:
            return send_from_directory('../frontend', path)
        except Exception:
            return send_from_directory('../frontend', 'index.html')

    @app.route('/api/test-connection')
    def test_connection():
        return {"message": "Backend is running and connected to MySQL!"}

    with app.app_context():
        db.create_all()
        print("All tables created successfully.")

    return app


if __name__ == '__main__':
    app = create_app()
    print("Personal Analytics App is running.")
    print("Open this link in browser -> http://127.0.0.1:5001/")
    print("Press CTRL+C to stop")
    app.run(host='127.0.0.1', port=5001, debug=True)
