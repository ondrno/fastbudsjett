from flask import Flask
from flask_babel import Babel
from flask_caching import Cache
from flask_login import LoginManager
from . import auth, items, search, categories, users
from .config import AppConfig, cache_config
import calendar
from .config import cache_config


app = Flask(__name__)
app.config.from_object(AppConfig)

app.register_blueprint(auth.mod_auth)
app.register_blueprint(items.mod_items)
app.register_blueprint(search.mod_search)
app.register_blueprint(categories.mod_categories)
app.register_blueprint(users.mod_users)
app.add_url_rule('/', endpoint='items.index')

app.cache = Cache(app, config=cache_config)
app.login = LoginManager()
app.login.login_view = 'auth.login'

app.config['FLASK_ENV'] = 'development'
babel = Babel(app)
cache = Cache(app, config=cache_config)


def format_datetime(value, format="%Y-%M-%D"):
    """Format a date time to (Default): YYYY-MM-DD"""
    if value is None:
        return ""
    return value.strftime(format)


@app.template_global()
def month_name(month):
    return calendar.month_name[month]

