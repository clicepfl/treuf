import json
import unittest
from datetime import date

from app import create_app, db
from app.models import User, Role, Borrowing, Item
from datetime import datetime, timedelta
import base64
import os
from config import Config


class TestConfig(Config):
    """Generic config for testing purposes"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SERVER_NAME = "localhost.local"
    SECRET_KEY = "my-test-very-secret-key"


class AppCase(unittest.TestCase):
    """Test case to be used by all classes testing Flask app module"""

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


class UserModelCase(AppCase):
    def test_password_hashing(self):
        u = User(username="robb", email="robb@example.com", sciper=123456)
        u.set_password("hoho")
        self.assertFalse(u.check_password("hoha"))
        self.assertTrue(u.check_password("hoho"))
        self.assertRaises(TypeError, u.set_password, 1234)
        self.assertFalse(u.check_password(1234))

    def test_roles(self):
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
        self.assertFalse(u.has_one_of_roles([Role.REUF, Role.REUF_ADMIN]))
        u.from_dict({"roles": ["reuf_admin"]})
        self.assertEqual(u.get_roles(), [Role.REUF_ADMIN])
        self.assertTrue(u.has_one_of_roles([Role.REUF_ADMIN, Role.REUF]))
        self.assertFalse(u.has_one_of_roles([Role.REUF]))
        self.assertRaises(TypeError, u.has_one_of_roles, ["reuf"])
        self.assertRaises(
            TypeError, u.has_one_of_roles, [Role.REUF_ADMIN, Role.REUF, Role.REUF]
        )

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
        # we created a user with expected attributes
        self.assertEqual(
            u,
            User.query.filter_by(
                username="robb", email="tom.demont+example@epfl.ch"
            ).first(),
        )
        self.assertTrue(
            User.query.filter_by(username="robb", email="tom.demont+example@epfl.ch")
            .first()
            .sciper
            == 123456
        )
        # we cannot change password of non-new users
        u.from_dict({"password": "4567"}, new_user=False)
        self.assertFalse(u.check_password("4567"))
        # we cannot add role to fresh new user
        u.from_dict({"roles": ["reuf"]}, new_user=True)
        self.assertFalse(u.has_one_of_roles([Role.REUF]))
        # we can append role to created user
        u.from_dict({"roles": ["reuf"]})
        self.assertTrue(u.has_one_of_roles([Role.REUF]))

    def test_tokens(self):
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
        t = u.get_token()
        # checks the default expiration time is indeed in 3600 seconds (with an
        # accepted 2s of delta)
        self.assertAlmostEqual(
            u.token_expiration.timestamp(),
            (datetime.utcnow() + timedelta(seconds=3600)).timestamp(),
            delta=2000.0,
        )
        # check our token gives expected access and only this one does
        self.assertEqual(u.check_token(t), u)
        self.assertIsNone(
            u.check_token(base64.b64encode(os.urandom(24)).decode("utf-8"))
        )
        # test revoking token
        u.revoke_token()
        self.assertIsNone(u.check_token(t))

    def test_borrowing(self):
        u = User(username="john", email="reuf@example.com")

        i = Item(name="treuficelle", needs_cleaning=False, condition="good")

        db.session.add_all([u, i])
        db.session.commit()

        b = Borrowing(user_id=u.id, item_id=i.id, borrowing_date=date(2022, 8, 13))

        db.session.add(b)
        db.session.commit()

        # test cross referencing functions
        self.assertEqual(u.get_borrowed_items().all(), [i])
        self.assertEqual(i.get_borrowers().all(), [u])

        i2 = Item(name="ecran olivier")
        db.session.add(i2)
        db.session.commit()

        b2 = u.borrow(i2, date.today(), date.today(), 1)
        db.session.add(b2)
        db.session.commit()
        self.assertEqual(u.get_borrowed_items().all(), [i2, i])

        # test deleting a user and observing residual borrowings
        db.session.delete(u)
        db.session.commit()
        self.assertEqual(b.borrower, None)
        self.assertEqual(i.get_borrowers().all(), [])

    def test_jsonify(self):
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
        u.from_dict({"roles": ["reuf_admin"]})
        db.session.add(u)
        db.session.commit()
        print(u.to_dict(True))
        print(u.to_dict())
        self.assertEqual(
            u.to_dict(True),
            {
                "id": 1,
                "username": "robb",
                "_links": {
                    "self": "http://localhost.local/api/users/1",
                    "borrowings": "http://localhost.local/api/borrowings/for_user/1",
                    "update": "http://localhost.local/api/users/1",
                    "revoke_token": "http://localhost.local/api/tokens/1",
                    "delete": "http://localhost.local/api/users/1",
                },
                "email": "tom.demont+example@epfl.ch",
                "sciper": 123456,
                "unit": "student",
                "roles": ["reuf_admin"],
            },
        )
        self.assertEqual(
            u.to_dict(),
            {
                "id": 1,
                "username": "robb",
                "_links": {
                    "self": "http://localhost.local/api/users/1",
                    "borrowings": "http://localhost.local/api/borrowings/for_user/1",
                    "update": "http://localhost.local/api/users/1",
                    "revoke_token": "http://localhost.local/api/tokens/1",
                },
            },
        )
        v = User()
        v.from_dict(
            {
                "username": "hugo",
                "email": "tom.demont+hugo@epfl.ch",
                "sciper": 234567,
                "unit": "student",
                "password": "4567",
            },
            new_user=True,
        )
        v.from_dict({"roles": ["reuf", "reuf_admin"]})
        db.session.add(v)
        db.session.commit()
        print(User.to_collection_dict(db.session.query(User), 1, 2, "api.get_users"))
        print(
            User.to_collection_dict(db.session.query(User), 1, 2, "api.get_users", True)
        )
        self.assertEqual(
            User.to_collection_dict(db.session.query(User), 1, 2, "api.get_users"),
            {
                "elements": [
                    {
                        "id": 1,
                        "username": "robb",
                        "_links": {
                            "self": "http://localhost.local/api/users/1",
                            "borrowings": "http://localhost.local/api/borrowings/"
                            + "for_user/1",
                            "update": "http://localhost.local/api/users/1",
                            "revoke_token": "http://localhost.local/api/tokens/1",
                        },
                    },
                    {
                        "id": 2,
                        "username": "hugo",
                        "_links": {
                            "self": "http://localhost.local/api/users/2",
                            "borrowings": "http://localhost.local/api/borrowings/"
                            + "for_user/2",
                            "update": "http://localhost.local/api/users/2",
                            "revoke_token": "http://localhost.local/api/tokens/2",
                        },
                    },
                ],
                "_meta": {
                    "page": 1,
                    "per_page": 2,
                    "total_pages": 1,
                    "total_elements": 2,
                },
                "_links": {
                    "self": "http://localhost.local/api/users?page=1&per_page=2",
                    "next": None,
                    "prev": None,
                },
            },
        )
        self.assertEqual(
            User.to_collection_dict(
                db.session.query(User), 1, 2, "api.get_users", True
            ),
            {
                "elements": [
                    {
                        "id": 1,
                        "username": "robb",
                        "_links": {
                            "self": "http://localhost.local/api/users/1",
                            "borrowings": "http://localhost.local/api/borrowings/"
                            + "for_user/1",
                            "update": "http://localhost.local/api/users/1",
                            "revoke_token": "http://localhost.local/api/tokens/1",
                            "delete": "http://localhost.local/api/users/1",
                        },
                        "email": "tom.demont+example@epfl.ch",
                        "sciper": 123456,
                        "unit": "student",
                        "roles": ["reuf_admin"],
                    },
                    {
                        "id": 2,
                        "username": "hugo",
                        "_links": {
                            "self": "http://localhost.local/api/users/2",
                            "borrowings": "http://localhost.local/api/borrowings/"
                            + "for_user/2",
                            "update": "http://localhost.local/api/users/2",
                            "revoke_token": "http://localhost.local/api/tokens/2",
                            "delete": "http://localhost.local/api/users/2",
                        },
                        "email": "tom.demont+hugo@epfl.ch",
                        "sciper": 234567,
                        "unit": "student",
                        "roles": ["reuf", "reuf_admin"],
                    },
                ],
                "_meta": {
                    "page": 1,
                    "per_page": 2,
                    "total_pages": 1,
                    "total_elements": 2,
                },
                "_links": {
                    "self": "http://localhost.local/api/users?page=1&per_page=2",
                    "next": None,
                    "prev": None,
                },
            },
        )


class UserRoutesCase(AppCase):
    def setUp(self):
        super().setUp()
        # adds test users
        u = User()
        u.from_dict(
            {
                "username": "robb",
                "email": "tom.demont+admin@epfl.ch",
                "sciper": 123456,
                "unit": "student",
                "password": "1234",
            },
            new_user=True,
        )
        db.session.add(u)
        db.session.commit()
        u.from_dict({"roles": [Role.REUF_ADMIN]})
        v = User()
        v.from_dict(
            {
                "username": "john",
                "email": "tom.demont+john@epfl.ch",
                "sciper": 234567,
                "unit": "student",
                "password": "4567",
            },
            new_user=True,
        )
        db.session.add_all([u, v])
        db.session.commit()

    def get_token(self, logins: str = "robb:1234"):
        """Utility function for retrieving a token using the basic auth route"""
        creds = base64.b64encode(logins.encode()).decode("utf-8")
        response = json.loads(
            self.client.post(
                "/api/tokens", headers={"Authorization": "Basic " + creds}
            ).data.decode()
        )
        if "token" in response:
            return response["token"]
        raise ValueError("invalid credentials")

    def test_basic_auth(self):
        creds = base64.b64encode(b"robb:1234").decode("utf-8")
        self.assertTrue(
            "token"
            in json.loads(
                self.client.post(
                    "/api/tokens", headers={"Authorization": "Basic " + creds}
                ).data.decode()
            )
        )
        creds = base64.b64encode(b"robb:4321").decode("utf-8")
        response = self.client.post(
            "/api/tokens", headers={"Authorization": "Basic " + creds}
        )
        self.assertEqual(response.status_code, 401)

    def test_delete_token(self):
        token = self.get_token()
        response = self.client.delete(
            "/api/tokens/1", headers={"Authorization": "Bearer " + token}
        )
        self.assertEqual(response.data, b"")
        self.assertEqual(response.status_code, 204)
        creds = base64.b64encode(b"robb:1234").decode("utf-8")
        self.client.post("/api/tokens", headers={"Authorization": "Basic " + creds})
        response = self.client.delete(
            "/api/tokens/1", headers={"Authorization": "Basic " + creds}
        )
        self.assertEqual(response.status_code, 401)
        tokens = [u.get_token() for u in User.query.all()]
        response = self.client.delete(
            "/api/tokens/", headers={"Authorization": "Bearer " + tokens[0]}
        )
        self.assertEqual(response.status_code, 204)
        self.assertTrue(all([User.check_token(t) is None for t in tokens]))

    def test_create_user(self):
        response = self.client.post(
            "/api/users",
            json={
                "username": "bobby",
                "email": "tom.demont+bobby@epfl.ch",
                "sciper": 124598,
                "unit": "student",
                "password": "6789",
            },
        )
        bobby = User.query.filter_by(username="bobby").first()
        self.assertEqual(bobby.id, json.loads(response.data)["id"])
        self.assertEqual(response.status_code, 201)
        fail_response = self.client.post(
            "/api/users",
            json={
                "email": "tom.demont+bobby@epfl.ch",
                "sciper": 124598,
                "unit": "student",
                "password": "6789",
            },
        )
        self.assertEqual(fail_response.status_code, 400)

    def test_modify_user(self):
        token_john = self.get_token("john:4567")
        response = self.client.put(
            "/api/users/2",
            json={"username": "johnny", "password": "8901"},
            headers={"Authorization": "Bearer " + token_john},
        )
        self.assertEqual(json.loads(response.data.decode())["username"], "johnny")
        self.assertRaises(ValueError, self.get_token, "john:4567")
        token_robb = self.get_token()
        response = self.client.put(
            "/api/users/2",
            json={"username": "johnny-johnny", "unit": "staff"},
            headers={"Authorization": "Bearer " + token_robb},
        )
        self.assertEqual(
            json.loads(response.data.decode())["username"], "johnny-johnny"
        )
        fail_response = self.client.put(
            "/api/users/1",
            json={"username": "robby"},
            headers={"Authorization": "Bearer " + token_john},
        )
        self.assertEqual(fail_response.status_code, 401)
        fail_response = self.client.put(
            "/api/users/2",
            json={"username": "robb"},
            headers={"Authorization": "Bearer " + token_john},
        )
        self.assertEqual(fail_response.status_code, 400)
        response = self.client.put(
            "/api/users/2",
            json={"roles": ["reuf"]},
            headers={"Authorization": "Bearer " + token_robb},
        )
        self.assertEqual(User.query.get(2).roles, [Role.REUF])

    def test_delete_user(self):
        self.client.post(
            "/api/users",
            json={
                "username": "bobby",
                "email": "tom.demont+bobby@epfl.ch",
                "sciper": 124598,
                "unit": "student",
                "password": "6789",
            },
        )
        self.assertIsNotNone(User.query.filter_by(username="bobby").first())
        token = self.get_token()
        response = self.client.delete(
            "/api/users/3",
            headers={"Authorization": "Bearer " + token},
        )
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(User.query.filter_by(username="bobby").first())


if __name__ == "__main__":
    unittest.main(verbosity=2)
