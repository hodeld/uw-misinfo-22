from django.db import connections
from django.db.utils import OperationalError
import unittest


class TestDataBaseConnection(unittest.TestCase):

    def test_db(self):
        db_conn = connections['earth_semanticscholar']
        try:
            db_conn.cursor()
        except OperationalError:
            connected = False
            print('check vpn connection to CIP')
        else:
            connected = True
        self.assertTrue(connected)
