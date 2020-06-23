from unittest import TestCase
from flask import current_app
from app import create_app, db

app = create_app()


class BaseTest(TestCase):
    def setUp(self):
        with app.app_context():
            self.app = app.test_client()

    def tearDown(self):
        pass

class IndexTests(BaseTest):
    def test_status_code_index(self):
        with self.app as client:
            req = client.get('/')
            self.assertEqual(200, req.status_code)
            # self.as