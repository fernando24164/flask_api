from unittest import TestCase
from app import create_app, db
from app.api.models import User
from base64 import b64encode
import json
import os
from config import basedir
from flask_migrate import upgrade


class UserModelTestCase(TestCase):

    @staticmethod
    def create_database(name):
        complete_path = os.path.join(basedir, name)
        with open(complete_path, 'a'):
            os.utime(complete_path, None)

    @staticmethod
    def remove_database(name):
        complete_path = os.path.join(basedir, name)
        os.remove(complete_path)

    @classmethod
    def setUpClass(cls):
        cls.create_database('test.sqlite')
        upgrade()

    @classmethod
    def tearDownClass(cls):
        cls.remove_database('test.sqlite')

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self, name, passwd):
        return {
            'Authorization': 'Basic ' + b64encode(
                (name + ':' + passwd).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_password(self):
        user = User(name='admin', pwd='admin')
        self.assertTrue(user.verify_password('admin'))

    def test_endpoint(self):
        response = self.client.get('/api/test')
        self.assertTrue(response.status_code == 200)

    def test_secret_endpoint(self):
        response = self.client.get('/api/secret')
        self.assertTrue(response.status_code == 403)

    def test_token_based_authentication(self):
        u = User(name='Donald Trump', pwd='1234')
        db.session.add(u)
        db.session.commit()

        response = self.client.get('/api/secret',
                                   headers=self.get_api_headers('Donald Trump',
                                                                '1234'))
        self.assertTrue(response.status_code == 200)

        response = self.client.get('/api/secret',
                                   headers=self.get_api_headers('hack',
                                                                '1234'))
        self.assertTrue(response.status_code == 403)

        response = self.client.get(
            '/api/token',
            headers=self.get_api_headers('Donald Trump', '1234'))
        self.assertTrue(response.status_code == 200)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertIsNotNone(json_response.get('token'))
        token = json_response['token']

        response = self.client.get(
            '/api/secret',
            headers=self.get_api_headers(token, ''))
        self.assertTrue(response.status_code == 200)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertIsNotNone(json_response.get('message'))
        message = json_response['message']
        self.assertEqual(first=message, second='Secret message!')
