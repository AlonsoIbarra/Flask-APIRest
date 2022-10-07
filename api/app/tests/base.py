

import unittest
import os
import sys
from utils.jwt_utils import write_token
parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir_name)
from config import app, database


class BaseTest(unittest.TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:////databasefile.db"

    def __init__(self, methodName: str = ...):
        self.app = app
        self.database = database

        # Generate a valid token
        self.token = write_token(data={'data': 'any data to encript'})
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': u'Bearer {}'.format(str(self.token))
        }
        super().__init__(methodName)

    def setUp(self):
        # Set test database
        os.environ['sqlalchemy_database_uri'] = self.SQLALCHEMY_DATABASE_URI
        return super().setUp()
