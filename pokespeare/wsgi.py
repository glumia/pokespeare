"""Flask WSGI application factory."""
from flask import Flask


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)

    @app.route("/ping")
    def ping():
        return "pong"

    # Register blueprints to the app
    # from .views import my_module
    # app.register_blueprint(my_module.bp)

    return app
