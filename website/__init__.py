import os
from flask import Flask
from sqlalchemy import select

DB_NAME = "database.sqlite"
SQLA_DB_URI = f"sqlite:///{DB_NAME}"


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, DB_NAME),
        SQLALCHEMY_DATABASE_URI=SQLA_DB_URI,  # Given by the hosting platform
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Make following imports available in templates
    import datetime

    @app.context_processor
    def add_imports():
        return dict(datetime=datetime.datetime)

    @app.context_processor
    def time_utility_processor():
        def is_same_week(date):
            today = datetime.datetime.today()
            year, week, _ = date.isocalendar()
            current_year, current_week, _ = today.isocalendar()
            return year == current_year and week == current_week

        return dict(
            is_same_week=is_same_week,
        )

    # Import blueprints
    from .views import views
    from .auth import auth
    from .gym import gym

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(gym, url_prefix="/gym")

    from .models import db

    db.init_app(app)

    @app.shell_context_processor
    def shell_imports():
        return dict(select=select)

    return app
