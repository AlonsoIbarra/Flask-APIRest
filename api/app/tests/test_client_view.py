import os
from utils.login_utils import create_signature
from config import Client
from utils.jwt_utils import write_token
from .base import BaseTest
import json


class ClientViewTest(BaseTest):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.url = '/v1/resources/clients'
        # Generate a valid token
        os.environ['EXPIRATION_DAYS'] = '-1'
        self.expiredtoken = write_token(data={'data': 'data to encript'})
        self.headers_expired = {
            'Content-Type': 'application/json',
            'Authorization': u'Bearer {}'.format(str(self.expiredtoken))
        }
        os.environ['EXPIRATION_DAYS'] = '1'

    def test_auth_required(self):
        tester = self.app.test_client(self)
        response = tester.post(
            self.url,
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn('Authentication needed', str(response.data))

    def test_invalid_token(self):
        tester = self.app.test_client(self)
        response = tester.post(
            self.url,
            headers={
                'Content-Type': 'application/json',
                'Authorization': u'Bearer fake_token_123'
            }
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid Token', str(response.data))

    def test_expired_token(self):
        tester = self.app.test_client(self)
        response = tester.post(
            self.url,
            headers=self.headers_expired,
            data=json.dumps(
                {
                    'name': 'name2',
                    'site_client_id': 2,
                    'first_surname': "surname",
                    'second_surname': 'second',
                    'birthdate': '1990-04-28',
                    'gender': 'F',
                    'email': 'mail@mail.com',
                    'phone': '551234678',
                    'postal_code': '12345',
                    'password': 'secret-password'
                }
            )
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn('Token Expired', str(response.data))

    def test_missing_params(self):
        tester = self.app.test_client(self)
        response = tester.post(
            self.url,
            headers=self.headers
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing json params', str(response.data))

        response = tester.post(
            self.url,
            headers=self.headers,
            data=json.dumps(
                {'name': 'name2'}
            )
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'Site client id field is required',
            str(response.data)
        )

        response = tester.post(
            self.url,
            headers=self.headers,
            data=json.dumps(
                {
                    'name': 'name2',
                    'site_client_id': 2,
                }
            )
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('First surname field is required', str(response.data))

        response = tester.post(
            self.url,
            headers=self.headers,
            data=json.dumps(
                {
                    'name': 'name2',
                    'site_client_id': 2,
                    'first_surname': "surname"
                }
            )
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('Second surname field is required', str(response.data))

        response = tester.post(
            self.url,
            headers=self.headers,
            data=json.dumps(
                {
                    'name': 'name2',
                    'site_client_id': 2,
                    'first_surname': "surname",
                    'second_surname': 'second'
                }
            )
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('birthdate', str(response.data))
        self.assertIn('Missing required parameter', str(response.data))

        response = tester.post(
            self.url,
            headers=self.headers,
            data=json.dumps(
                {
                    'name': 'name2',
                    'site_client_id': 2,
                    'first_surname': "surname",
                    'second_surname': 'second',
                    'birthdate': '1990-04-28'
                }
            )
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('gender', str(response.data))
        self.assertIn('Missing required parameter', str(response.data))

        response = tester.post(
            self.url,
            headers=self.headers,
            data=json.dumps(
                {
                    'name': 'name2',
                    'site_client_id': 2,
                    'first_surname': "surname",
                    'second_surname': 'second',
                    'birthdate': '1990-04-28',
                    'gender': 'F'
                }
            )
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', str(response.data))
        self.assertIn('Missing required parameter', str(response.data))

        response = tester.post(
            self.url,
            headers=self.headers,
            data=json.dumps(
                {
                    'name': 'name2',
                    'site_client_id': 2,
                    'first_surname': "surname",
                    'second_surname': 'second',
                    'birthdate': '1990-04-28',
                    'gender': 'F',
                    'email': 'mail@mail.com'
                }
            )
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('phone', str(response.data))
        self.assertIn('Missing required parameter', str(response.data))

        response = tester.post(
            self.url,
            headers=self.headers,
            data=json.dumps(
                {
                    'name': 'name2',
                    'site_client_id': 2,
                    'first_surname': "surname",
                    'second_surname': 'second',
                    'birthdate': '1990-04-28',
                    'gender': 'F',
                    'email': 'mail@mail.com',
                    'phone': '5512345678'
                }
            )
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('postal_code', str(response.data))
        self.assertIn('Missing required parameter', str(response.data))

        response = tester.post(
            self.url,
            headers=self.headers,
            data=json.dumps(
                {
                    'name': 'name2',
                    'site_client_id': 2,
                    'first_surname': "surname",
                    'second_surname': 'second',
                    'birthdate': '1990-04-28',
                    'gender': 'F',
                    'email': 'mail@mail.com',
                    'phone': '5512345678',
                    'postal_code': '12345'
                }
            )
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('Password field is required', str(response.data))

    def test_birthdate_format(self):
        tester = self.app.test_client(self)
        response = tester.post(
            self.url,
            headers=self.headers,
            data=json.dumps(
                {
                    'name': 'name2',
                    'site_client_id': 2,
                    'first_surname': "surname",
                    'second_surname': 'second',
                    'birthdate': '1990/04/28',
                    'gender': 'F',
                    'email': 'mail@mail.com',
                    'phone': '5512345678',
                    'postal_code': '12345',
                    'password': 'secret-password'
                }
            )
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('birthdate', str(response.data))
        self.assertIn(
            'Incorrect data format, should be YYYY-MM-DD',
            str(response.data)
        )

        response = tester.post(
            self.url,
            headers=self.headers,
            data=json.dumps(
                {
                    'name': 'name2',
                    'site_client_id': 2,
                    'first_surname': "surname",
                    'second_surname': 'second',
                    'birthdate': '1990-28-04',
                    'gender': 'F',
                    'email': 'mail@mail.com',
                    'phone': '5512345678',
                    'postal_code': '12345',
                    'password': 'secret-password'
                }
            )
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('birthdate', str(response.data))
        self.assertIn(
            'Incorrect data format, should be YYYY-MM-DD',
            str(response.data)
        )

        response = tester.post(
            self.url,
            headers=self.headers,
            data=json.dumps(
                {
                    'name': 'name2',
                    'site_client_id': 2,
                    'first_surname': "surname",
                    'second_surname': 'second',
                    'birthdate': '28-04-1990',
                    'gender': 'F',
                    'email': 'mail@mail.com',
                    'phone': '5512345678',
                    'postal_code': '12345',
                    'password': 'secret-password'
                }
            )
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('birthdate', str(response.data))
        self.assertIn(
            'Incorrect data format, should be YYYY-MM-DD',
            str(response.data)
        )

        response = tester.post(
            self.url,
            headers=self.headers,
            data=json.dumps(
                {
                    'name': 'name2',
                    'site_client_id': 2,
                    'first_surname': "surname",
                    'second_surname': 'second',
                    'birthdate': '04-28-1990',
                    'gender': 'F',
                    'email': 'mail@mail.com',
                    'phone': '5512345678',
                    'postal_code': '12345',
                    'password': 'secret-password'
                }
            )
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('birthdate', str(response.data))
        self.assertIn(
            'Incorrect data format, should be YYYY-MM-DD',
            str(response.data)
        )

    def test_gender_options(self):
        tester = self.app.test_client(self)
        response = tester.post(
            self.url,
            headers=self.headers,
            data=json.dumps(
                {
                    'name': 'name2',
                    'site_client_id': 2,
                    'first_surname': "surname",
                    'second_surname': 'second',
                    'birthdate': '1990-04-28',
                    'gender': '',
                    'email': 'mail@mail.com',
                    'phone': '5512345678',
                    'postal_code': '12345',
                    'password': 'secret-password'
                }
            )
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('gender', str(response.data))
        self.assertIn('is not a valid choice', str(response.data))

        response = tester.post(
            self.url,
            headers=self.headers,
            data=json.dumps(
                {
                    'name': 'name2',
                    'site_client_id': 2,
                    'first_surname': "surname",
                    'second_surname': 'second',
                    'birthdate': '1990-04-28',
                    'gender': 'f',
                    'email': 'mail@mail.com',
                    'phone': '5512345678',
                    'postal_code': '12345',
                    'password': 'secret-password'
                }
            )
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('gender', str(response.data))
        self.assertIn('is not a valid choice', str(response.data))

        response = tester.post(
            self.url,
            headers=self.headers,
            data=json.dumps(
                {
                    'name': 'name2',
                    'site_client_id': 2,
                    'first_surname': "surname",
                    'second_surname': 'second',
                    'birthdate': '1990-04-28',
                    'gender': 'm',
                    'email': 'mail@mail.com',
                    'phone': '5512345678',
                    'postal_code': '12345',
                    'password': 'secret-password'
                }
            )
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('gender', str(response.data))
        self.assertIn('is not a valid choice', str(response.data))

        response = tester.post(
            self.url,
            headers=self.headers,
            data=json.dumps(
                {
                    'name': 'name2',
                    'site_client_id': 2,
                    'first_surname': "surname",
                    'second_surname': 'second',
                    'birthdate': '1990-04-28',
                    'gender': '1',
                    'email': 'mail@mail.com',
                    'phone': '5512345678',
                    'postal_code': '12345',
                    'password': 'secret-password'
                }
            )
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('gender', str(response.data))
        self.assertIn('is not a valid choice', str(response.data))

        response = tester.post(
            self.url,
            headers=self.headers,
            data=json.dumps(
                {
                    'name': 'name2',
                    'site_client_id': 2,
                    'first_surname': "surname",
                    'second_surname': 'second',
                    'birthdate': '1990-04-28',
                    'gender': 't',
                    'email': 'mail@mail.com',
                    'phone': '5512345678',
                    'postal_code': '12345',
                    'password': 'secret-password'
                }
            )
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('gender', str(response.data))
        self.assertIn('is not a valid choice', str(response.data))

    def test_email_options(self):
        tester = self.app.test_client(self)
        response = tester.post(
            self.url,
            headers=self.headers,
            data=json.dumps(
                {
                    'name': 'name',
                    'site_client_id': 2,
                    'first_surname': "surname",
                    'second_surname': 'second',
                    'birthdate': '1990-04-28',
                    'gender': 'F',
                    'email': 'mailmail.com',
                    'phone': '5512345678',
                    'postal_code': '12345',
                    'password': 'secret-password'
                }
            )
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', str(response.data))
        self.assertIn('Incorrect email format', str(response.data))

        response = tester.post(
            self.url,
            headers=self.headers,
            data=json.dumps(
                {
                    'name': 'name',
                    'site_client_id': 2,
                    'first_surname': "surname",
                    'second_surname': 'second',
                    'birthdate': '1990-04-28',
                    'gender': 'F',
                    'email': 'mail@mailcom',
                    'phone': '5512345678',
                    'postal_code': '12345',
                    'password': 'secret-password'
                }
            )
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', str(response.data))
        self.assertIn('Incorrect email format', str(response.data))

        response = tester.post(
            self.url,
            headers=self.headers,
            data=json.dumps(
                {
                    'name': 'name',
                    'site_client_id': 2,
                    'first_surname': "surname",
                    'second_surname': 'second',
                    'birthdate': '1990-04-28',
                    'gender': 'F',
                    'email': 'mail@@mail.com',
                    'phone': '5512345678',
                    'postal_code': '12345',
                    'password': 'secret-password'
                }
            )
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', str(response.data))
        self.assertIn('Incorrect email format', str(response.data))

        response = tester.post(
            self.url,
            headers=self.headers,
            data=json.dumps(
                {
                    'name': 'name',
                    'site_client_id': 2,
                    'first_surname': "surname",
                    'second_surname': 'second',
                    'birthdate': '1990-04-28',
                    'gender': 'F',
                    'email': 'mail@mail..com',
                    'phone': '5512345678',
                    'postal_code': '12345',
                    'password': 'secret-password'
                }
            )
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', str(response.data))
        self.assertIn('Incorrect email format', str(response.data))

    def test_phone_format(self):
        tester = self.app.test_client(self)
        response = tester.post(
            self.url,
            headers=self.headers,
            data=json.dumps(
                {
                    'name': 'name2',
                    'site_client_id': 2,
                    'first_surname': "surname",
                    'second_surname': 'second',
                    'birthdate': '1990-04-28',
                    'gender': 'F',
                    'email': 'mail@mail.com',
                    'phone': '5512s34678',
                    'postal_code': '12345',
                    'password': 'secret-password'
                }
            )
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('phone', str(response.data))
        self.assertIn(
            'Phone number must not contains letters',
            str(response.data)
        )

        response = tester.post(
            self.url,
            headers=self.headers,
            data=json.dumps(
                {
                    'name': 'name2',
                    'site_client_id': 2,
                    'first_surname': "surname",
                    'second_surname': 'second',
                    'birthdate': '1990-04-28',
                    'gender': 'F',
                    'email': 'mail@mail.com',
                    'phone': '012345678901234567893',
                    'postal_code': '12345',
                    'password': 'secret-password'
                }
            )
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('phone', str(response.data))
        self.assertIn(
            'Phone number must be a maximun of 20 characters long',
            str(response.data)
        )

    def test_postal_code_format(self):
        tester = self.app.test_client(self)
        response = tester.post(
            self.url,
            headers=self.headers,
            data=json.dumps(
                {
                    'name': 'name2',
                    'site_client_id': 2,
                    'first_surname': "surname",
                    'second_surname': 'second',
                    'birthdate': '1990-04-28',
                    'gender': 'F',
                    'email': 'mail@mail.com',
                    'phone': '551234678',
                    'postal_code': '12s45',
                    'password': 'secret-password'
                }
            )
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('postal_code', str(response.data))
        self.assertIn('Postal code must be numbers', str(response.data))

        response = tester.post(
            self.url,
            headers=self.headers,
            data=json.dumps(
                {
                    'name': 'name2',
                    'site_client_id': 2,
                    'first_surname': "surname",
                    'second_surname': 'second',
                    'birthdate': '1990-04-28',
                    'gender': 'F',
                    'email': 'mail@mail.com',
                    'phone': '551234678',
                    'postal_code': '125989876545',
                    'password': 'secret-password'
                }
            )
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('postal_code', str(response.data))
        self.assertIn(
            'Postal code must be a maximun of 5 characters long',
            str(response.data)
        )

    def test_client_twice(self):
        tester = self.app.test_client(self)
        Client(
            name='user-test',
            first_surname='yhsaa',
            second_surname='uytr',
            birthdate='02-02-1980',
            gender='F',
            email='adsd@mail.com',
            phone='5512345678',
            postal_code='00100',
            password=create_signature('password')
        ).save_to_db()

        response = tester.post(
            self.url,
            headers=self.headers,
            data=json.dumps(
                {
                    'name': 'user-test',
                    'site_client_id': 2,
                    'first_surname': "surname",
                    'second_surname': 'second',
                    'birthdate': '1990-04-28',
                    'gender': 'F',
                    'email': 'mail@mail.com',
                    'phone': '551234678',
                    'postal_code': '12345',
                    'password': 'secret-password'
                }
            )
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'is already registered',
            str(response.data))

    def test_create_client_succesfully(self):
        tester = self.app.test_client(self)
        response = tester.post(
            self.url,
            headers=self.headers,
            data=json.dumps(
                {
                    'name': 'name2',
                    'site_client_id': 2,
                    'first_surname': "surname",
                    'second_surname': 'second',
                    'birthdate': '1990-04-28',
                    'gender': 'F',
                    'email': 'mail@mail.com',
                    'phone': '551234678',
                    'postal_code': '12345',
                    'password': 'secret-password'
                }
            )
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn('erp-client-key', str(response.data))
