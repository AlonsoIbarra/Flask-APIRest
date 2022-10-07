import json
import os
from utils.jwt_utils import validate_token, expiration_date, write_token
from .base import BaseTest
from datetime import datetime


class JWTUtilsTest(BaseTest):

    def test_expiration_date(self):
        today = datetime.today()

        os.environ['EXPIRATION_DAYS'] = '1'
        expiration_days = expiration_date()
        diff = expiration_days - today
        diff_seconds = diff.total_seconds()
        hours = diff_seconds // 3600
        # Almost one day
        self.assertEqual(hours, 24)

        os.environ['EXPIRATION_DAYS'] = '2'
        expiration_days = expiration_date()
        diff = expiration_days - today
        diff_seconds = diff.total_seconds()
        hours = diff_seconds // 3600
        self.assertEqual(hours, 48)

    def test_write_token(self):
        data = {
            'data': 'some data'
        }
        encoded_data = write_token(data)
        try:
            json.loads(encoded_data)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(isinstance(encoded_data, str))

    def test_validate_token(self):
        data = {
            'data': 'some data'
        }
        token = write_token(data)
        validate_token_result = validate_token(token)
        self.assertIsNone(validate_token_result)
        validate_token_result = validate_token(token, True)
        self.assertIsNotNone(validate_token_result)
