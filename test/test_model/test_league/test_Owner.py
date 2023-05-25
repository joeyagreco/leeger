import unittest

from leeger.model.league.Owner import Owner


class TestOwner(unittest.TestCase):
    def test_owner_init(self):
        owner = Owner(name="name")

        self.assertEqual("name", owner.name)

    def test_owner_eq_callsEqualsMethod(self):
        # create Owner 1
        owner_1 = Owner(name="owner")

        # create Owner 2
        owner_2 = Owner(name="owner")

        result = owner_1 == owner_2

        self.assertTrue(result)

    def test_owner_eq_equal(self):
        # create Owner 1
        owner_1 = Owner(name="owner")

        # create Owner 2
        owner_2 = Owner(name="owner")

        self.assertTrue(owner_1.equals(owner_2))

    def test_owner_eq_notEqual(self):
        # create Owner 1
        owner_1 = Owner(name="owner")

        # create Owner 2
        owner_2 = Owner(name="ownerDIF")

        self.assertFalse(owner_1.equals(owner_2))

    def test_owner_toJson(self):
        owner = Owner(name="owner")
        ownerJson = owner.toJson()

        self.assertIsInstance(ownerJson, dict)
        self.assertEqual("owner", ownerJson["name"])

    def test_owner_fromJson(self):
        owner = Owner(name="owner")
        ownerJson = owner.toJson()
        ownerDerived = Owner.fromJson(ownerJson)
        self.assertEqual(owner, ownerDerived)
        self.assertEqual(owner.id, ownerDerived.id)
