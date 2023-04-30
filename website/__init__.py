import os
from flask import Flask
from sqlalchemy import select
from werkzeug.security import generate_password_hash


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object("config.DevConfig")

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Import blueprints
    from .views import views
    from .auth import auth
    from .gym import gym

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(gym, url_prefix="/gym")

    from .models import db

    db.init_app(app)

    from .admin import admin, basic_auth, MyAdminIndexView

    admin.init_app(app, index_view=MyAdminIndexView())

    basic_auth.init_app(app)

    @app.shell_context_processor
    def shell_imports():
        return dict(
            select=select,
            generate_password_hash=generate_password_hash,
        )

    return app
