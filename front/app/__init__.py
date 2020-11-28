from flask import Flask
from . import auth, items
from flask_caching import Cache

config = {
    "DEBUG": True,              # some Flask specific configs
    "CACHE_TYPE": "simple",     # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}

def create_cached_app():
    app = Flask(__name__)
    app.config.from_mapping(config)

    app.secret_key = "super secret key"
    app.register_blueprint(auth.bp)
    app.register_blueprint(items.bp)
    app.add_url_rule('/', endpoint='index')

    cache = Cache(app)

    return app, cache


app, cache = create_cached_app()

