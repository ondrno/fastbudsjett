import os


class AppConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    LANGUAGES = ['de', 'en']
    BABEL_DEFAULT_LOCALE = 'de'
    # Statement for enabling the development environment
    DEBUG = True
    FLASK_ENV = 'development'
    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2
    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CRSF_SESSION_KEY = os.environ.get('CRSF_SESSION_KEY') or 'you-will-never-guess-it'
    CSRF_ENABLED = True


cache_config = {
    "DEBUG": True,              # some Flask specific configs
    "CACHE_TYPE": "simple",     # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
