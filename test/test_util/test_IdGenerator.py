import unittest

from leeger.util.IdGenerator import IdGenerator


class TestIdGenerator(unittest.TestCase):
    def test_generateId_happyPath(self):
        response1 = IdGenerator.generateId()
        response2 = IdGenerator.generateId()
        self.assertIsInstance(response1, str)
        self.assertIsInstance(response2, str)
        self.assertEqual(32, len(response1))
        self.assertEqual(32, len(response2))
        self.assertNotEqual(response1, response2)
