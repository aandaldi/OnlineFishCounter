from tests.base_tests import BaseTest
from datetime import datetime as dt
from app import guard
from app.usermanagement.models import UsermanagementModel
from app.auth.user_session_models import UserSessionModel


class UserSessionTest(BaseTest):
    def test_create_save_user_session(self):
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
            print(UsermanagementModel.lookup("aan"))

            user_session = UserSessionModel(
                access_token="access_token_string",
                usermanagement_uuid=user.uuid
            )
            user_session.save_to_db()
            self.assertIsNotNone(UserSessionModel.lookup(user.uuid))
            self.assertEqual(UserSessionModel.lookup(user.uuid).usermanagement_uuid, user.uuid)

    def test_delete_session(self):
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
            user_session = UserSessionModel(
                access_token="access_token_string",
                usermanagement_uuid=user.uuid
            )
            user_session.save_to_db()
            self.assertIsNotNone(UserSessionModel.lookup(user.uuid))
            user_session.delete_from_db()
            self.assertIsNone(UserSessionModel.lookup(user.uuid))
