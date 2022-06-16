import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
# loads environment variables from a .env files. This .env file should not be versioned
load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    """
    ###################
    TECHNICAL
    ###################
    """

    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    """
    ###################
    MAIL SUPPORT
    ###################
    """
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 25)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") is not None
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL") is not None
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    ADMIN = [os.environ.get("ADMIN")]
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")

    """
    ###################
    AUTHENTICATION
    ###################
    """
    TOKEN_LIFETIME = int(os.environ.get("TOKEN_LIFETIME") or 1)  # lifetime in hours
    USER_CREATION_TOKEN = os.environ.get(
        "USER_CREATION_TOKEN"
    )  # token required for creating a new account
