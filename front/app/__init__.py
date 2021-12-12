from flask import Flask
from flask_caching import Cache
from flask_login import LoginManager
from . import auth, items, search, categories, users
from .config import AppConfig, cache_config
import calendar


def create_app():
    app = Flask(__name__)
    app.config.from_object(AppConfig)

    app.register_blueprint(auth.bp)
    app.register_blueprint(items.bp)
    app.register_blueprint(search.bp)
    app.register_blueprint(categories.bp)
    app.register_blueprint(users.bp)
    app.add_url_rule('/', endpoint='index')

    app.cache = Cache(app, config=cache_config)
    app.login = LoginManager()
    app.login.login_view = 'auth.login'
    return app


app = create_app()
app.config['FLASK_ENV'] = 'development'


def format_datetime(value, format="%Y-%M-%D"):
    """Format a date time to (Default): YYYY-MM-DD"""
    if value is None:
        return ""
    return value.strftime(format)


@app.template_global()
def month_name(month):
    return calendar.month_name[month]
