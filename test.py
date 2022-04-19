import unittest

from app import app, db
from app.models import *


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


if __name__ == "__main__":
    unittest.main(verbosity=2)
