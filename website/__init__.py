import os
from flask import Flask

# from flask_sqlalchemy import SQLAlchemy
#
# db = SQLAlchemy()
# DB_NAME = "database.db"


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Import blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views)
    app.register_blueprint(auth)

    from . import db
    db.init_app(app)

    # app = Flask(__name__)
    # app.config['SECRET_KEY'] = 'dev'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # db.init_app(app)
    #
    #
    # from .models import User, Reservation
    #
    # with app.app_context():
    #     db.create_all()

    return app
