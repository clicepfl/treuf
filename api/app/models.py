import base64
import os
from datetime import date, datetime, timedelta
from enum import Enum
from typing import Union

from flask import current_app, url_for
from sqlalchemy.orm import Query
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.email import send_email


class Role(Enum):
    """Defines roles that allow or not certain routes and actions
    - REUF_ADMIN: whether this user is an admin (logistics manager, president for example) of the real world inventory or not. Can manage items users and only be upgraded by admin
    - REUF: whether this user is a reuf (member of logistics team for example) of the real world inventory. Can manage items and only be upgraded by admin
    """

    REUF_ADMIN = "reuf_admin"
    REUF = "reuf"


class PaginatedAPIMixin(object):
    """Defines a trait for objects from the model. Aims to be inherited by objects to be returned as a jsonified paginated collection."""

    @staticmethod
    def to_collection_dict(
        query: Query,
        page: int,
        per_page: int,
        endpoint: str,
        reuf_view: bool = False,
        **kwargs,
    ) -> dict:
        """Returns a dict representing a collection of items from the query that are to be paginated.

        Args:
            - query: the query containing for the items to be paginated. Should query a table inheriting PaginatedAPIMixin.
            - page: the page to return for this paginated set of items
            - per_page: the number of items per page
            - reuf_view: whether the to_dict called should be made for an admin view or not
            - endpoint: the current route endpoint, where the 'next' and 'previous' links will point to"""
        if not (
            isinstance(query, Query)
            and isinstance(page, int)
            and isinstance(per_page, int)
            and isinstance(reuf_view, bool)
            and isinstance(endpoint, str)
        ):
            raise TypeError("Bad arguments type")
        resources = query.paginate(page, per_page, False)
        data = {
            "elements": [element.to_dict(reuf_view) for element in resources.items],
            "_meta": {
                "page": page,
                "per_page": per_page,
                "total_pages": resources.pages,
                "total_elements": resources.total,
            },
            "_links": {
                "self": url_for(endpoint, page=page, per_page=per_page, **kwargs),
                "next": url_for(endpoint, page=page + 1, per_page=per_page, **kwargs)
                if resources.has_next
                else None,
                "prev": url_for(endpoint, page=page - 1, per_page=per_page, **kwargs)
                if resources.has_prev
                else None,
            },
        }
        return data


class User(PaginatedAPIMixin, db.Model):
    """Represents a user of the system. This is the actor that can borrow items.

    - id: their unique id in the database (set automatically)
    - username: their username to log in
    - email: their email
    - password_hash: the salted hash of their password
    - sciper: their sciper number
    - unit: description of their service at EPFL (student, collaborator, ...)
    - roles: Python list with the roles held by this user. See Roles class
    - token: this user's valid token
    - token_expiration: the expiration date time for the current token

    - borrowings_they_made: relationship query containing the borrowing made by this user"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(96), index=True, unique=True)
    password_hash = db.Column(db.String(102))
    sciper = db.Column(db.Integer, unique=True)
    unit = db.Column(db.String(16))
    roles = db.Column(db.PickleType, default=[], index=True)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    borrowings_they_made = db.relationship(
        "Borrowing",
        backref="borrower",
        foreign_keys="Borrowing.user_id",
        lazy="dynamic",
    )

    def set_password(self, password: str) -> None:
        """Sets the password for this user"""
        # basically hashes with random salt using PBKDF2, see https://werkzeug.palletsprojects.com/en/2.0.x/utils/#module-werkzeug.security
        if not isinstance(password, str):
            raise TypeError("Bad argument type")
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Checks whether the given password matches the one stored in the database"""
        return isinstance(password, str) and check_password_hash(
            self.password_hash, password
        )

    def get_roles(self) -> list[Role]:
        """Returns the Roles for this user. Method required by HTTPauth for RBAC"""
        return self.roles

    def has_one_of_roles(self, roles: list[Role]) -> bool:
        """Returns whether this user one of the given roles in their roles or not"""
        if not (
            isinstance(roles, list) and all([isinstance(r, Role) for r in roles])
        ) or len(roles) > len(Role):
            # checking lengths prevents having undesired long for loop
            raise TypeError("Bad arguments type")
        if self.roles:
            for r in roles:
                if r in self.roles:
                    return True
        return False

    def from_dict(self, data: dict, new_user: bool = False) -> None:
        """Sets attributes for a user from a dict object. Fields to fill are explicitly whitelisted to avoid undesired escalation. Expects already sanitized inputs."""
        if not (isinstance(data, dict) and isinstance(new_user, bool)):
            raise TypeError("Bad arguments type")
        for field in ["username", "email", "sciper", "unit"]:
            if field in data:
                setattr(self, field, data[field])
        if "roles" in data and not new_user:
            # we assume access control has been performed. Also we still refuse to set role at user creation
            send_email(
                subject="A reuf role is being set",
                recipients=current_app.config["ADMIN"],
                text_body=f"Hello my reufs\nThe user {self.username} is being changed their role status account to {data['roles']}. Make sure it's desired",
            )
            # Values should have been sanitized beforehand for not raising ValueError
            self.roles = [Role(r) for r in data["roles"]]
        if new_user and "password" in data:
            self.set_password(data["password"])

    def get_token(self, expires_in: int = 3600) -> str:
        """Retrieves a token for this user. If the current token does not exist or expired, sets a new one. Tokens are by default valid for 1 hour."""
        if not isinstance(expires_in, int):
            raise TypeError("Bad arguments type")
        with current_app.app_context():
            # we need the app context to access the configuration
            expires_in *= current_app.config["TOKEN_LIFETIME"]
        now = datetime.utcnow()
        # we check if the token expires in more than 60 seconds
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        # This test is not necessary. There is a 2^192 bits token but we still make explicitly sure that there is not collision as token should uniquely identify a user
        test_token = base64.b64encode(os.urandom(24)).decode("utf-8")
        while User.query.filter_by(token=test_token).count() > 0:
            test_token = base64.b64encode(os.urandom(24)).decode("utf-8")
        # we explicitly make a string copy that way
        self.token = "" + test_token
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self) -> None:
        """Revokes the token of this user"""
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token: str) -> Union["User", None]:
        """Verifies if the given token corresponds to any user. If yes, returns the user it actually corresponds to"""
        if not isinstance(token, str):
            raise TypeError("Bad arguments type")
        # we explicitly made sure in token generation that those uniquely identify a user
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    def get_borrowed_items(self) -> Query:
        """Returns a query storing the items borrowed by this user, in decreasing order of the borrowings timestamps"""
        return (
            db.session.query(Item)
            .join(Borrowing, Item.id == Borrowing.item_id)
            .filter(Borrowing.user_id == self.id)
            .order_by(Borrowing.timestamp.desc())
        )

    def borrow(
        self,
        item: "Item",
        borrowing_date: date,
        return_date: date,
        borrowed_quantity: int,
        borrowing_description: str = "",
        remarks: str = "",
    ) -> "Borrowing":
        """Creates a new borrowing for an item for this user. Performs checks on the inputs to have a valid borrowing. Tests should be added depending on logistical requirements."""
        if not (
            isinstance(item, Item)
            and isinstance(borrowing_date, date)
            and isinstance(return_date, date)
            and isinstance(borrowed_quantity, int)
            and isinstance(borrowing_description, str)
            and isinstance(remarks, str)
        ):
            raise TypeError("Bad argument type")

        if Item.query.get(item.id) != item:
            raise ValueError("Item not in database")
        if borrowed_quantity < 1:
            raise ValueError("Cannot borrow less that one unit of the item")
        if borrowing_date > return_date or borrowing_date < date.today():
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
        return b

    def __repr__(self) -> str:
        return "<User {} (id: {})>".format(self.username, self.id)

    def to_dict(self, reuf_view: bool = False) -> dict:
        """Converts the value to a dictionary ready to be jsonified. We should make sure to set the correct view depending on the user status with 'reuf view'."""
        data = {
            "id": self.id,
            "username": self.username,
            "_links": {
                "self": url_for("api.get_user", id=self.id),
                "borrowings": url_for("api.get_borrowings_for_user", id=self.id),
                "update": url_for("api.update_user", id=self.id),
                "revoke_token": url_for("api.revoke_token", id=self.id),
            },
        }
        if reuf_view:
            data.update(
                {
                    "email": self.email,
                    "sciper": self.sciper,
                    "unit": self.unit,
                    "roles": [r.value for r in self.roles],
                }
            )
            data["_links"].update({"delete": url_for("api.delete_user", id=self.id)})
        return data


class Item(PaginatedAPIMixin, db.Model):
    """Represents an item of the database. These are to be borrowed by users eventually.

    - id: their if in the database (set automatically)
    - name: their short name
    - description: a description of this object, eventual usage etc
    - box_name: name of this item's box in the real world inventory
    - location: location of this item's box in the real world inventory
    - unit: unit for measuring quantity of this item (litter, meter, 1, ...)
    - quantity: the amount of existing unit of this item
    - expiry_date: the expiry date of this item if any
    - power: the power consumed by this item (in Watts)
    - value: the value of this item (in CHF)
    - needs_cleaning: whether this item has to be cleaned or not
    - condition: condition of this item (good, damaged. ...)
    - remarks: any extra remarks on this item
    - access_control_list: the set of roles that are required to view this item

    - borrowings_it_s_in: relationship query containing the borrowing in which this item is present"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(128))
    box_name = db.Column(db.String(16))
    location = db.Column(db.String(2))
    unit = db.Column(db.String(16))
    quantity = db.Column(db.Integer)
    expiry_date = db.Column(db.Date)
    power = db.Column(db.Integer)
    value = db.Column(db.Integer)
    needs_cleaning = db.Column(db.Boolean)
    condition = db.Column(db.String(16))
    remarks = db.Column(db.String(128))
    access_control_list = db.Column(db.PickleType, default=[], index=True)

    borrowings_it_s_in = db.relationship(
        "Borrowing",
        backref="borrowed_item",
        foreign_keys="Borrowing.item_id",
        lazy="dynamic",
    )

    def get_borrowers(self) -> Query:
        """Returns a query for users that have a borrowing with this item, in decreasing order of the borrowing timestamp"""
        return (
            db.session.query(User)
            .join(Borrowing, User.id == Borrowing.user_id)
            .filter(Borrowing.user_id == self.id)
            .order_by(Borrowing.timestamp.desc())
        )

    def accessible_by_roles(self, roles: list[Role]) -> bool:
        """Returns whether this item can be accessed by a user having the given roles."""
        if not (
            isinstance(roles, list) and all([isinstance(r, Role) for r in roles])
        ) or len(roles) > len(Role):
            # checking lengths prevents having undesired long for loop
            raise TypeError("Bad arguments type")
        if not self.access_control_list or len(self.access_control_list) == 0:
            # no role is required to access this item
            return True
        for required_role in self.access_control_list:
            if not required_role in roles:
                return False
        return True

    def from_dict(
        self,
        data: dict,
    ) -> None:
        """Sets attributes for an item from a dict object. Fields to fill are explicitly whitelisted to avoid undesired escalation. Expects already sanitized inputs.

        Dates are expected in the format '%d.%m.%y' see https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes. For example 22.01.24 is valid for 22nd of january year 2024, while 1.4.2025 is not: days and months should be 0 padded and 21st century prefix omitted."""
        if not isinstance(data, dict):
            raise TypeError("Bad argument type")
        for field in [
            "quantity",
            "power",
            "value",
            "needs_cleaning",
            "name",
            "description",
            "box_name",
            "location",
            "unit",
            "condition",
            "remarks",
        ]:
            if field in data:
                setattr(self, field, data[field])
        if "expiry_date" in data:
            self.expiry_date = datetime.strptime(data["expiry_date"], "%d.%m.%y")
        if "access_control_list" in data:
            self.access_control_list = [Role(r) for r in data["access_control_list"]]

    def __repr__(self) -> str:
        return "<Item {} (id: {})>".format(self.name, self.id)

    def to_dict(self, reuf_view: bool = False) -> dict:
        data = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "unit": self.unit,
            "quantity": self.quantity,
            "expiry_date": self.expiry_date,
            "condition": self.condition,
            "remarks": self.remarks,
            "_links": {
                "self": url_for("api.get_item", id=self.id),
                "borrowings": url_for("api.get_borrowings_with_item", id=self.id),
                "image": url_for("api.get_item_image", id=self.id),
                "borrow": url_for("api.borrow_item", id=self.id),
            },
        }
        if reuf_view:
            data.update(
                {
                    "box_name": self.box_name,
                    "location": self.location,
                    "value": self.value,
                    "needs_cleaning": self.needs_cleaning,
                    "access_control_list": [r.value for r in self.access_control_list],
                }
            )
            data["_links"].update(
                {
                    "update": url_for("api.edit_item", id=self.id),
                    "update_item": url_for("api.modify_item", id=self.id),
                    "update_item_image": url_for("api.modify_item_image", id=self.id),
                    "delete_item": url_for("api.delete_item", id=self.id),
                }
            )
        return data


class Borrowing(PaginatedAPIMixin, db.Model):
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

    def to_dict(self, reuf_view: bool = False) -> dict:
        data = {
            "id": self.id,
            "user": self.borrower.to_dict(reuf_view),  # uses backref
            "item": self.borrowed_item.to_dict(reuf_view),  # uses backref
            "timestamp": self.timestamp.isoformat()
            + "Z",  # uses timezoned date format. See https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxiii-application-programming-interfaces-apis
            "borrowing_date": self.borrowing_date.isoformat() + "Z",
            "return_date": self.return_date.isoformat() + "Z",
            "borrowed_quantity": self.borrowed_quantity,
            "borrowing_description": self.borrowing_description,
            "remarks": self.remarks,
            "_links": {
                "self": url_for("api.get_borrowing", id=self.id),
            },
        }
        return data
