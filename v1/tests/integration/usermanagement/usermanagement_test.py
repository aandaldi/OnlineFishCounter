from tests.base_tests import BaseTest
from app import guard
from datetime import datetime as dt
from app.usermanagement.models import UsermanagementModel


class UserModelIntegrationTest(BaseTest):
    def test_create_and_read(self):
        with self.app_context:
            user = UsermanagementModel(
                username="aan",
                password=guard.hash_password("aldi"),
                roles="admin",
                created_by="admin",
                date_modified=dt.now(),
                modified_by="admin"
            )

            self.assertIsNone(UsermanagementModel.lookup("aan"))
            user.save_to_db()
            self.assertIsNotNone(UsermanagementModel.lookup("aan"))

    def test_update_data(self):
        with self.app_context:
            user = UsermanagementModel(
                username="aan",
                password=guard.hash_password("aldi"),
                roles="admin",
                created_by="admin",
                date_modified=dt.now(),
                modified_by="admin"
            )

            user.save_to_db()

            self.assertEqual(user.username, "aan")

            user.username = "aldi"

            self.assertNotEqual(user.username, "aan")

            user.update_on_db()

            self.assertEqual(user.username, "aldi")
