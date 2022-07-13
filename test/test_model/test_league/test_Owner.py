import unittest

from leeger.model.league.Owner import Owner


class TestOwner(unittest.TestCase):
    def test_owner_init(self):
        owner = Owner(name="name")

        self.assertEqual("name", owner.name)
