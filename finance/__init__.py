import os

from flask import Flask
from flask_session import Session

from cachelib.file import FileSystemCache

from finance.helpers import usd


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # used by flask and extensions to keep data safe
        SECRET_KEY="dev",
        # path to SQLite database - it's under app.instance_path
        DATABASE=os.path.join(app.instance_path, "finance.db"),
        # Configure session to use cachelib (instead of signed cookies)
        SESSION_COOKIE_SAMESITE="Strict",
        SESSION_PERMANENT=False,
        SESSION_TYPE="cachelib",
        SESSION_SERIALIZATION_FORMAT="json",
        SESSION_CACHELIB=FileSystemCache(threshold=500, cache_dir=app.instance_path),
    )

    if test_config is None:
        # load the instance config if exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # the test config passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Custom filter
    app.jinja_env.filters["usd"] = usd

    # Session
    Session(app)

    # Register blueprints
    from . import auth
    from . import stock

    app.register_blueprint(auth.bp)
    app.register_blueprint(stock.bp)

    # Register close_db and init_db_command
    from . import db

    db.init_app(app)

    app.add_url_rule("/", endpoint="index")

    return app
