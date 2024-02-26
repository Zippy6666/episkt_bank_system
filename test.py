import unittest

class MyTest(unittest.TestCase):
    def test_addition(self):
        result = 1 + 2
        self.assertEqual(result, 3)

if __name__ == '__main__':
    unittest.main()