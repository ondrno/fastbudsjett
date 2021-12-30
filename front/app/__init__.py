from flask import (session, request, Flask)
from flask_babel import Babel
from flask_caching import Cache
from flask_login import LoginManager
from . import auth, items, search, categories, users, utils
from .config import AppConfig, cache_config
import calendar
from .config import cache_config


babel = Babel()


def create_app():
    app = Flask(__name__)
    app.config.from_object(AppConfig)

    app.register_blueprint(auth.mod_auth)
    app.register_blueprint(items.mod_items)
    app.register_blueprint(search.mod_search)
    app.register_blueprint(categories.mod_categories)
    app.register_blueprint(users.mod_users)
    app.add_url_rule('/', endpoint='items.index')

    # app.cache = Cache(app, config=cache_config)
    app.login = LoginManager()
    app.login.login_view = 'auth.login'
    babel.init_app(app)

    return app


app = create_app()


@babel.localeselector
def get_locale():
    if 'locale' in session:
        print(f"found session locale={session['locale']}")
        return session['locale']
    best_match = request.accept_languages.best_match(app.config['LANGUAGES'])
    return best_match


def format_datetime(value, format="%Y-%M-%D"):
    """Format a date time to (Default): YYYY-MM-DD"""
    if value is None:
        return ""
    return value.strftime(format)


@app.template_global()
def month_name(month_no: int, abbr: bool = False, locale: str = None) -> str:
    return utils.month_name(month_no, abbr, locale)


@app.template_global()
def day_name(dow: int, abbr: bool = True, locale: str = None) -> str:
    return utils.day_name(dow, abbr, locale)
