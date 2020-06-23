from tests.base_tests import BaseTest
from app import create_app, db, guard
from app.usermanagement.models import UsermanagementModel
from datetime import datetime as dt


class TestUsermanagement(BaseTest):
    def test_create_user(self):
        user = UsermanagementModel(
            username="aan",
            password=guard.hash_password("aldi"),
            roles="admin",
            created_by="admin",
            date_modified=dt.now(),
            modified_by="admin"
        )

        self.assertEqual(user.username, "aan")
        self.assertNotEqual(user.password, "aldi")

    def test_to_json(self):
        user = UsermanagementModel(
            username="aan",
            password=guard.hash_password("aldi"),
            roles="admin",
            created_by="admin",
            date_modified=dt.now(),
            modified_by="admin"
        )

        expect = {
            "uuid": user.uuid,
            "username": "aan",
            "roles": "admin",
            "created_by": "admin",
            "created_at": user.date_created,
            "modified_by": "admin",
            "modified_at": user.date_modified,
            "last_login": user.last_login,
            "is_active": None
        }

        self.assertEqual(user.to_json(), expect)

    def test_to_json_key(self):
        user = UsermanagementModel(
            username="aan",
            password=guard.hash_password("aldi"),
            roles="admin",
            created_by="admin",
            date_modified=dt.now(),
            modified_by="admin"
        )

        user_json_keys = []

        for key, value in user.to_json().items():
            user_json_keys.append(key)

        keys_expect = ['uuid', 'username', 'roles', 'created_by', 'created_at', 'modified_by', 'modified_at',
                       'last_login', 'is_active']

        self.assertEqual(user_json_keys, keys_expect)
