import unittest
from leeger.model.league.Division import Division


class TestDivision(unittest.TestCase):
    def test_division_init(self):
        division = Division(name="name")

        self.assertEqual("name", division.name)

    def test_division_eq_callsEqualsMethod(self):
        # create division 1
        division_1 = Division(name="division")

        # create division 2
        division_2 = Division(name="division")
        division_2.id = division_1.id

        result = division_1 == division_2

        self.assertTrue(result)

    def test_division_eq_equal(self):
        # create division 1
        division_1 = Division(name="division")

        # create division 2
        division_2 = Division(name="division")

        result = division_1.equals(division_2, ignoreBaseId=True)

        self.assertTrue(result)

    def test_division_eq_notEqual(self):
        # create division 1
        division_1 = Division(name="division")

        # create division 2
        division_2 = Division(name="divisionDIF")

        result = division_1.equals(division_2, ignoreBaseId=True)

        self.assertFalse(result)

    def test_toFromJson(self):
        division = Division(name="division")
        self.assertEqual(division, Division.fromJson(division.toJson()))
