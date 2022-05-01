from datetime import datetime, date

from sqlalchemy.orm import Query
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from flask import url_for
from app import db


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    image = db.Column(db.LargeBinary)
    description = db.Column(db.String(128))
    box_name = db.Column(db.String(16))
    location = db.Column(db.String(2))
    unit = db.Column(db.String(16))
    quantity = db.Column(db.Integer)
    expiry_date = db.Column(db.Date)
    value = db.Column(db.Integer)
    needs_cleaning = db.Column(db.Boolean)
    condition = db.Column(db.String(16))
    remarks = db.Column(db.String(128))

    borrowings_it_s_in = db.relationship(
        "Borrowing",
        backref="borrowed_item",
        foreign_keys="Borrowing.item_id",
        lazy="dynamic",
    )

    def get_borrowers(self) -> Query:
        return (
            db.session.query(User)
            .join(Borrowing, User.id == Borrowing.user_id)
            .filter(Borrowing.user_id == self.id)
            .order_by(Borrowing.timestamp.desc())
        )

    def __repr__(self) -> str:
        return "<Item {} (id: {})>".format(self.name, self.id)

    def to_dict(self, show: list = None) -> dict:
        columns = (
            list(filter(lambda x: x in show, self.__table__.columns.keys()))
            if show is not None
            else self.__table__.columns.keys()
        )
        ret_dict = dict()
        for key in columns:
            ret_dict[key] = getattr(self, key)
        return ret_dict


class Borrowing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    item_id = db.Column(db.Integer, db.ForeignKey("item.id"))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    borrowing_date = db.Column(db.Date)
    return_date = db.Column(db.Date)
    borrowed_quantity = db.Column(db.Integer)
    borrowing_description = db.Column(db.String(64))
    remarks = db.Column(db.String(128))

    def __repr__(self) -> str:
        return "<Borrowing of {} by {} (id: {})>".format(
            self.borrowed_item, self.borrower, self.id
        )

    def to_dict(self, show: list = None) -> dict:
        columns = (
            list(filter(lambda x: x in show, self.__table__.columns.keys()))
            if show is not None
            else self.__table__.columns.keys()
        )
        ret_dict = dict()
        for key in columns:
            ret_dict[key] = getattr(self, key)
        return ret_dict


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(96), index=True, unique=True)
    password_hash = db.Column(db.String(102))
    sciper = db.Column(db.Integer, unique=True)
    unit = db.Column(db.String(16))

    borrowings_they_made = db.relationship(
        "Borrowing",
        backref="borrower",
        foreign_keys="Borrowing.user_id",
        lazy="dynamic",
    )

    def get_borrwed_items(self) -> Query:
        return (
            db.session.query(Item)
            .join(Borrowing, Item.id == Borrowing.item_id)
            .filter(Borrowing.user_id == self.id)
            .order_by(Borrowing.timestamp.desc())
        )

    def borrow(
        self,
        item: Item,
        borrowing_date: date,
        return_date: date,
        borrowed_quantity: int,
        borrowing_description: str = None,
        remarks: str = None,
    ) -> Borrowing:
        if isinstance(item, Item):
            if Item.query.get(item.id) != item:
                raise ValueError("Item not in database")
            if borrowed_quantity < 1:
                raise ValueError("Cannot borrow less that one unit of the item")
            if (
                not isinstance(borrowing_date, date)
                or not isinstance(return_date, date)
                or borrowing_date > return_date
                or borrowing_date < date.today()
            ):
                raise ValueError(
                    "Error on date: should have return date later than borrow date and borrow date not before today"
                )
            b = Borrowing(
                user_id=self.id,
                item_id=item.id,
                borrowing_date=borrowing_date,
                return_date=return_date,
                borrowed_quantity=borrowed_quantity,
                borrowing_description=borrowing_description,
                remarks=remarks,
            )
            db.session.add(b)
            db.session.commit()
            return b
        else:
            raise ValueError("User can only borrow items")

    def set_password(self, password: str) -> None:
        # basically hashes with random salt using PBKDF2, see https://werkzeug.palletsprojects.com/en/2.0.x/utils/#module-werkzeug.security
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return "<User {} (id: {})>".format(self.username, self.id)

    def to_dict(self) -> dict:
        # TODO
        data = {
            "id": self.id,
            "username": self.username,
            "_links": {
                "self": url_for("api.get_user", id=self.id),
            },
        }
        return data
