import unittest

from utils.login_utils import create_signature
from .base import BaseTest
import json
from config import Client


class LoginViewTest(BaseTest):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.url = '/v1/login'

    def setUp(self):
        Client(
            name='user',
            first_surname='first_surname',
            second_surname='second_surname',
            birthdate='02-02-1980',
            gender='F',
            email='mail@mail.com',
            phone='5512345678',
            postal_code='00100',
            password=create_signature('password')
        ).save_to_db()
        return super().setUp()

    def tearDown(self):
        self.database.session.query(Client).delete()
        self.database.session.commit()
        return super().tearDown()

    def test_missing_params(self):
        tester = self.app.test_client(self)

        response = tester.post(
            self.url,
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'Name and password are required',
            str(response.data)
        )

        response = tester.post(
            self.url,
            headers={'Content-Type': 'application/json'},
            data=json.dumps(
                {'password': 'passwords'}
            )
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'Name field is required',
            str(response.data)
        )

        response = tester.post(
            self.url,
            headers={'Content-Type': 'application/json'},
            data=json.dumps(
                {'name': 'users'}
            )
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'Password field is required',
            str(response.data)
        )

    def test_incorrect_credentials(self):
        tester = self.app.test_client(self)

        response = tester.post(
            self.url,
            data=json.dumps(
                {'name': 'usersd', 'password': 'passwordsd'}
            ),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'User not found',
            str(response.data)
        )

        response = tester.post(
            self.url,
            data=json.dumps(
                {'name': 'user', 'password': 'wrong-password'}
            ),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'Wrong password',
            str(response.data)
        )

    def test_correct_credentials(self):
        tester = self.app.test_client(self)

        response = tester.post(
            self.url,
            data=json.dumps(
                {'name': 'user', 'password': 'password'}
            ),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'data',
            str(response.data)
        )


if __name__ == '__main__':
    unittest.main()
