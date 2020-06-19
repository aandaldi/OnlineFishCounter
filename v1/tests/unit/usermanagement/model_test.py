from unittest import TestCase
from app import create_app, db, guard
from app.usermanagement.models import UserModel
from datetime import datetime as dt


class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config.from_object('config.TestingConfig')

    def setUp(self):
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        with self.app_context:
            db.create_all()
        self.user = UserModel("aan", guard.hash_password("aldi"), "admin", "admin", dt.now(), "admin")
        print("oke")

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        pass


class TestUsermanagement(BaseTest):
    def test_save_to_db(self):
        with self.app_context:
            self.user.save_to_db()
            user_db = UserModel.lookup(self.user.username)
            self.assertEqual(self.user.username, user_db.username)


    def test_to_json(self):
        with self.app_context:
            self.user.save_to_db()
            uuid = self.user.uuid
            created_at = self.user.date_created
            modified_at = self.user.date_modified
            expect = {
                'uuid': uuid,
                'username': 'aan',
                'roles': 'admin',
                'created_by': 'admin',
                'created_at': created_at,
                'modified_by': 'admin',
                'modified_at': modified_at,
                'last_login': None,
                'is_active': True
            }

            self.assertEqual(self.user.to_json(), expect)
