from datetime import datetime
from typing import Any

from flask_login import UserMixin
from sqlalchemy.orm import Query
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(96), index=True, unique=True)
    password_hash = db.Column(db.String(102))
    sciper = db.Column(db.Integer, unique=True)

    def set_password(self, password: str) -> None:
        # basically hashes with random salt using PBKDF2, see https://werkzeug.palletsprojects.com/en/2.0.x/utils/#module-werkzeug.security
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return "<User {} (id: {})>".format(self.username, self.id)


@login.user_loader
def load_user(id: int) -> User:
    return User.query.get(int(id))
