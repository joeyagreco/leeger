import unittest

from src.leeger.model.Owner import Owner


class TestOwner(unittest.TestCase):
    def test_owner_init(self):
        owner = Owner(name="name")

        self.assertEqual("name", owner.name)
