import unittest

from app import app, db
from app.models import *
from datetime import date


class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username="robb", sciper=123456)
        u.set_password("hoho")
        self.assertFalse(u.check_password("beep"))
        self.assertTrue(u.check_password("hoho"))

    def test_borrowing(self):
        u = User(username="john", email="reuf@example.com")

        i = Item(name="treuficelle", needs_cleaning=False, condition="good")

        db.session.add_all([u, i])
        db.session.commit()

        b = Borrowing(user_id=u.id, item_id=i.id, borrowing_date=date(2022, 8, 13))

        db.session.add(b)
        db.session.commit()

        self.assertEqual(u.get_borrwed_items().all(), [i])
        self.assertEqual(i.get_borrowers().all(), [u])

        i2 = Item(name="ecran olivier")
        db.session.add(i2)
        db.session.commit()

        b2 = u.borrow(i2, date.today(), date.today(), 1)
        self.assertEqual(u.get_borrwed_items().all(), [i2, i])


if __name__ == "__main__":
    unittest.main(verbosity=2)
