from flask import Flask
from flask_caching import Cache
from . import auth, items
from .config import AppConfig, cache_config


def create_app():
    app = Flask(__name__)
    app.config.from_object(AppConfig)

    app.register_blueprint(auth.bp)
    app.register_blueprint(items.bp)
    app.add_url_rule('/', endpoint='index')

    app.cache = Cache(app, config=cache_config)

    return app


app = create_app()

