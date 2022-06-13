import json
import unittest
from datetime import date

from app import create_app, db
from app.models import *
from config import Config


class TestConfig(Config):
    """Generic config for testing purposes"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SERVER_NAME = "localhost"


class AppModelCase(unittest.TestCase):
    """Test case to be used by all classes testing Flask app module"""

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


class UserModelCase(AppModelCase):
    def test_password_hashing(self):
        u = User(username="robb", email="robb@example.com", sciper=123456)
        u.set_password("hoho")
        self.assertFalse(u.check_password("hoha"))
        self.assertTrue(u.check_password("hoho"))

    def test_from_dict(self):
        u = User()
        u.from_dict(
            {
                "username": "robb",
                "email": "tom.demont+example@epfl.ch",
                "sciper": 123456,
                "unit": "student",
                "password": "1234",
            },
            new_user=True,
        )
        db.session.add(u)
        db.session.commit()
        self.assertEqual(
            u,
            User.query.filter_by(
                username="robb", email="tom.demont+example@epfl.ch"
            ).first(),
        )

    def test_borrowing(self):
        u = User(username="john", email="reuf@example.com")

        i = Item(name="treuficelle", needs_cleaning=False, condition="good")

        db.session.add_all([u, i])
        db.session.commit()

        b = Borrowing(user_id=u.id, item_id=i.id, borrowing_date=date(2022, 8, 13))

        db.session.add(b)
        db.session.commit()

        self.assertEqual(u.get_borrowed_items().all(), [i])
        self.assertEqual(i.get_borrowers().all(), [u])

        i2 = Item(name="ecran olivier")
        db.session.add(i2)
        db.session.commit()

        b2 = u.borrow(i2, date.today(), date.today(), 1)
        db.session.add(b2)
        db.session.commit()
        self.assertEqual(u.get_borrowed_items().all(), [i2, i])

    def test_jsonify(self):
        i = Item(
            name="xbox360",
            needs_cleaning=False,
            unit="1m",
            quantity=10,
            condition="good",
        )

        db.session.add(i)
        db.session.commit()

        # self.assertEqual(
        #     json.dumps(i.to_dict()),
        #     '{"id": 1, "name": "xbox360", "image": null, "description": null, "box_name": null, "location": null, "unit": "1m", "quantity": 10, "expiry_date": null, "value": null, "needs_cleaning": false, "condition": "good", "remarks": null}',
        # )
        # self.assertEqual(
        #     json.dumps(i.to_dict(["name", "quantity"])),
        #     '{"name": "xbox360", "quantity": 10}',
        # )


if __name__ == "__main__":
    unittest.main(verbosity=2)
