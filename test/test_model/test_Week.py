import unittest

from src.leeger.exception.InvalidWeekFormatException import InvalidWeekFormatException
from src.leeger.model.Matchup import Matchup
from src.leeger.model.Week import Week


class TestWeek(unittest.TestCase):
    def test_week_init(self):
        matchup = Matchup(teamAId="", teamBId="", teamAScore=0, teamBScore=0)
        week1 = Week(
            weekNumber=1,
            isPlayoffWeek=False,
            isChampionshipWeek=False,
            matchups=[matchup],
        )
        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=True, matchups=[])

        self.assertEqual(1, week1.weekNumber)
        self.assertFalse(week1.isPlayoffWeek)
        self.assertFalse(week1.isChampionshipWeek)
        self.assertTrue(week2.isPlayoffWeek)
        self.assertTrue(week2.isChampionshipWeek)
        self.assertEqual(1, len(week1.matchups))
        self.assertEqual(matchup.id, week1.matchups[0].id)

    def test_week_postInit(self):
        matchup = Matchup(teamAId="", teamBId="", teamAScore=0, teamBScore=0)
        # valid week
        Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup])
        # valid week
        Week(weekNumber=1, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup])
        # valid week
        Week(weekNumber=1, isPlayoffWeek=True, isChampionshipWeek=True, matchups=[matchup])

        with self.assertRaises(InvalidWeekFormatException) as context:
            # invalid week
            Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=True, matchups=[matchup])
        self.assertEqual("A championship week must be a playoff week.", str(context.exception))
