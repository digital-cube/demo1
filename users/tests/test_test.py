import unittest
from unittest.mock import patch
import funkcionalnosti

from base import test

class MyTestCase(unittest.TestCase):

    @patch('redis.Redis', test.MockedRedis)
    def test1(self):
        self.assertIsNone(funkcionalnosti.f1())
        self.assertEqual(funkcionalnosti.f2(), b'dada')


if __name__ == '__main__':
    unittest.main()
