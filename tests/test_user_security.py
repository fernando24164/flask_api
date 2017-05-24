from unittest import TestCase
from app import create_app, db
from app.api.models import User


class UserModelTestCase(TestCase):

    def setUp(self):
        self.app = create_app('default')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password(self):
        user = User(name='admin', pwd='admin')
        self.assertTrue(user.verify_password('admin'))
