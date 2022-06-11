import unittest
from decimal import Decimal

from src.leeger.util.Deci import Deci


class TestDeci(unittest.TestCase):
    def test_init_happyPath(self):
        deci1 = Deci(1.1)
        deci2 = Deci(2.2)
        sum = deci1 + deci2

        self.assertIsInstance(deci1, Deci)
        self.assertIsInstance(deci1, Decimal)
        self.assertEqual(Deci("1.1"), deci1)
        self.assertEqual(Deci("2.2"), deci2)
        self.assertEqual(Deci("3.3"), sum)
