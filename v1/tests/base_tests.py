from unittest import TestCase
from app import create_app, db, guard
from datetime import datetime as dt
from app.usermanagement.models import UsermanagementModel


class BaseTest(TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config.from_object('config.TestingConfig')
        self.app_context = self.app.app_context()
        with self.app_context:
            db.create_all()

    def tearDown(self):
        with self.app_context:
            db.session.remove()
            db.drop_all()
            pass


class TestInsertAdmin:
    def insert_admin():
        admin = UsermanagementModel(
            username="admin",
            password=guard.hash_password("admin"),
            roles="admin",
            created_by="admin",
            date_modified=dt.now(),
            modified_by="admin"
        )
        admin.save_to_db()
        return "admin inserted"
