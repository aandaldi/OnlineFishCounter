from unittest import TestCase
from app.auth.user_session_models import UserSessionModel


class BaseTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass


class TestSessionModel(BaseTest):
    def test_create_session_user(self):
        user_session = UserSessionModel(
            access_token="access_token_string",
            usermanagement_uuid="uuid-user-random-val"
        )
        self.assertEqual(user_session.access_token, "access_token_string")

