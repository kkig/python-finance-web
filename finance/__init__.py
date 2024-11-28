import os

from flask import Flask
from flask_session import Session

# import requests

from finance.helpers import usd


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # used by flask and extensions to keep data safe
        SECRET_KEY="dev",
        # path to SQLite database - it's under app.instance_path
        DATABASE=os.path.join(app.instance_path, "finance.sqlite"),
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

    # Configure session to use filesystem (instead of signed cookies)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    from . import stock

    app.register_blueprint(stock.bp)

    # Register close_db and init_db_command
    from . import db

    db.init_app(app)

    return app
