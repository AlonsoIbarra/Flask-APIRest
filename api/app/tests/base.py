

import unittest
import os
import sys
from utils.jwt_utils import write_token
parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir_name)
# Set test database enviroment
os.environ['sqlalchemy_database_uri'] = "sqlite:////databasefile.db"


class BaseTest(unittest.TestCase):

    def __init__(self, methodName: str = ...):
        from config import app, database

        self.app = app
        self.database = database

        # Generate a valid token
        self.token = write_token(data={'data': 'any data to encript'})
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': u'Bearer {}'.format(str(self.token))
        }
        super().__init__(methodName)
