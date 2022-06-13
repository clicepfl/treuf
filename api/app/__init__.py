import logging
import os
from logging.handlers import RotatingFileHandler, SMTPHandler

from config import Config
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate(db)
mail = Mail()


def create_app(config_class=Config):
    """Factory pattern for app instance construction. Constructs the app from a Config objects and registers the blueprint modules."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    from app.api import bp as api_bp

    app.register_blueprint(api_bp, url_prefix="/api")

    from app.errors import bp as error_bp

    app.register_blueprint(error_bp)

    """Handles application logs by mail and in files when deployed."""
    if not app.debug and not app.testing:
        # we cannot yet have mail logs with a SMTP over SSL connection
        # https://docs.python.org/3/library/logging.handlers.html#logging.handlers.SMTPHandler
        # There exists code to circumvent this https://github.com/dycw/ssl-smtp-handler but not widely adopted
        if app.config["MAIL_SERVER"] and not app.config["MAIL_USE_SSL"]:
            auth = None
            if app.config["MAIL_USERNAME"] or app.config["MAIL_PASSWORD"]:
                auth = (app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])
            secure = None
            if app.config["MAIL_USE_TLS"]:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config["MAIL_SERVER"], app.config["MAIL_PORT"]),
                fromaddr="tom.demont@protonmail.com",
                toaddrs=app.config["ADMIN"],
                subject="Treuf Failure",
                credentials=auth,
                secure=secure,
            )
            mail_handler.setLevel(logging.INFO)
            app.logger.addHandler(mail_handler)

        if not os.path.exists("logs"):
            os.mkdir("logs")
        file_handler = RotatingFileHandler(
            "logs/treuf.log", maxBytes=10240, backupCount=10
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s " "[in %(pathname)s:%(lineno)d]"
            )
        )
        file_handler.setLevel(logging.ERROR)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info("Treuf startup")

    return app


# imports at the bottom to avoid circular dependencies
from app import models, email
