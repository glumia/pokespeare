"""Flask WSGI application factory."""
from flask import Flask


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)

    @app.route("/ping")
    def ping():
        return "pong"

    # Register blueprints to the app
    from .views import pokemon

    app.register_blueprint(pokemon.bp)

    # Initialize app's accessors
    from .pokeapi import poke_api_client  # noqa
    from .shakespeare import shakespeare_client  # noqa

    return app
