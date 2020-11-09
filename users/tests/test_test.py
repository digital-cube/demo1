import unittest


class MyTestCase(unittest.TestCase):

    def setUp(self):
        print("SETUP")

    def test_nesto(self):
        print("TEST NESTO")
    def test_nesto2(self):
        print("TEST NESTO2")

class Izvedeno(MyTestCase):

    def test_something(self):
        print("TEST_SOMETHING")

    def test_something2(self):
        print("TEST_SOMETHING2")

if __name__ == '__main__':
    unittest.main()
