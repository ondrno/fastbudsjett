import os


class AppConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'


cache_config = {
    "DEBUG": True,              # some Flask specific configs
    "CACHE_TYPE": "simple",     # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
