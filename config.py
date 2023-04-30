"""Flask configuration."""
from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    """Base config."""

    SECRET_KEY = environ.get("SECRET_KEY")
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"


class ProdConfig(Config):
    """Production config."""

    FLASK_ENV = "production"
    FLASK_DEBUG = False
    DATABASE_URI = environ.get("PROD_DATABASE_URI")
    SQLALCHEMY_DATABASE_URI = DATABASE_URI  # Given by the hosting platform

    BASIC_AUTH_USERNAME = environ.get("BASIC_AUTH_USERNAME")
    BASIC_AUTH_PASSWORD = environ.get("BASIC_AUTH_PASSWORD")


class DevConfig(Config):
    """Development config."""

    FLASK_ENV = "development"
    FLASK_DEBUG = True
    DATABASE_URI = environ.get("DB_URI")
    SQLALCHEMY_DATABASE_URI = DATABASE_URI

    BASIC_AUTH_USERNAME = environ.get("BASIC_AUTH_USERNAME")
    BASIC_AUTH_PASSWORD = environ.get("BASIC_AUTH_PASSWORD")
