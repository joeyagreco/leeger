import unittest
from leeger.model.league.Division import Division


class TestDivision(unittest.TestCase):
    def test_division_init(self):
        division = Division(name="name")

        self.assertEqual("name", division.name)

    def test_division_eq_equal(self):
        # create division 1
        division_1 = Division(name="division")

        # create division 2
        division_2 = Division(name="division")

        self.assertEqual(division_1, division_2)

    def test_division_eq_notEqual(self):
        # create division 1
        division_1 = Division(name="division")

        # create division 2
        division_2 = Division(name="divisionDIF")

        self.assertNotEqual(division_1, division_2)
        
    def test_toFromJson(self):
        division = Division(name="division")
        self.assertEqual(division, Division.fromJson(division.toJson()))
