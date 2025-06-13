import os
import unittest
from pospy.backend.database import Database


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database(db_path=':memory:')

    def tearDown(self):
        self.db.close()

    def test_insert_and_list(self):
        pid = self.db.insert_product('Test', 9.99)
        self.assertIsInstance(pid, int)
        products = self.db.list_products()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0][1], 'Test')


if __name__ == '__main__':
    unittest.main()
