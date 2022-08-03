import unittest

from leeger.model.league.Owner import Owner


class TestOwner(unittest.TestCase):
    def test_owner_init(self):
        owner = Owner(name="name")

        self.assertEqual("name", owner.name)

    def test_owner_eq_equal(self):
        # create Owner 1
        owner_1 = Owner(name="owner")

        # create Owner 2
        owner_2 = Owner(name="owner")

        self.assertEqual(owner_1, owner_2)

    def test_owner_eq_notEqual(self):
        # create Owner 1
        owner_1 = Owner(name="owner")

        # create Owner 2
        owner_2 = Owner(name="ownerDIF")

        self.assertNotEqual(owner_1, owner_2)
