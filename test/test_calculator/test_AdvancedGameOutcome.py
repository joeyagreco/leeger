import unittest
from decimal import Decimal

from src.leeger.calculator.AdvancedGameOutcome import AdvancedGameOutcome
from src.leeger.model.Matchup import Matchup
from src.leeger.model.Owner import Owner
from src.leeger.model.Team import Team
from src.leeger.model.Week import Week
from src.leeger.model.Year import Year


class TestAdvancedGameOutcome(unittest.TestCase):
    def test_getWAL_happyPath(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=1)
        matchup3 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup2])
        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=True, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[team1, team2], weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Decimal("0.5"), response[team1.id])
        self.assertEqual(Decimal("2.5"), response[team2.id])

    def test_getWAL_onlyPostSeasonIsTrue(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup3 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup2])
        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=True, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[team1, team2], weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getWAL(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Decimal("0"), response[team1.id])
        self.assertEqual(Decimal("2"), response[team2.id])

    def test_getWAL_onlyRegularSeasonIsTrue(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup3 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup2])
        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[team1, team2], weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getWAL(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Decimal("0"), response[team1.id])
        self.assertEqual(Decimal("2"), response[team2.id])

    def test_getWAL_weekNumberStartGiven(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup3 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=2, teamBScore=1)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup2])
        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[team1, team2], weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getWAL(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Decimal("1"), response[team1.id])
        self.assertEqual(Decimal("1"), response[team2.id])

    def test_getWAL_weekNumberEndGiven(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup3 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=2, teamBScore=1)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup2])
        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup3])

        year = Year(yearNumber=2000, teams=[team1, team2], weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getWAL(year, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Decimal("0"), response[team1.id])
        self.assertEqual(Decimal("2"), response[team2.id])

    def test_getWAL_weekNumberStartGivenAndWeekNumberEndGiven(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup3 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=2, teamBScore=1)
        matchup4 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=2, teamBScore=1)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup1])
        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False, matchups=[matchup2])
        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup3])
        week4 = Week(weekNumber=4, isPlayoffWeek=True, isChampionshipWeek=False, matchups=[matchup4])

        year = Year(yearNumber=2000, teams=[team1, team2], weeks=[week1, week2, week3, week4])

        response = AdvancedGameOutcome.getWAL(year, weekNumberStart=2, weekNumberEnd=3)

        self.assertIsInstance(response, dict)
        self.assertEqual(2, len(response.keys()))
        self.assertEqual(Decimal("1"), response[team1.id])
        self.assertEqual(Decimal("1"), response[team2.id])

    def test_getAWAL_happyPath(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")
        owner3 = Owner(name="3")
        owner4 = Owner(name="4")
        owner5 = Owner(name="5")
        owner6 = Owner(name="6")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")
        team3 = Team(ownerId=owner3.id, name="3")
        team4 = Team(ownerId=owner4.id, name="4")
        team5 = Team(ownerId=owner5.id, name="5")
        team6 = Team(ownerId=owner6.id, name="6")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team3.id, teamBId=team4.id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=team5.id, teamBId=team6.id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team3.id, teamBId=team4.id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=team5.id, teamBId=team6.id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team3.id, teamBId=team4.id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=team5.id, teamBId=team6.id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[team1, team2, team3, team4, team5, team6], weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getAWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Decimal("0"), response[team1.id])
        self.assertEqual(Decimal("0.6"), response[team2.id])
        self.assertEqual(Decimal("1.2"), response[team3.id])
        self.assertEqual(Decimal("2.1"), response[team4.id])
        self.assertEqual(Decimal("2.1"), response[team5.id])
        self.assertEqual(Decimal("3"), response[team6.id])

    def test_getAWAL_onlyPostSeasonIsTrue(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")
        owner3 = Owner(name="3")
        owner4 = Owner(name="4")
        owner5 = Owner(name="5")
        owner6 = Owner(name="6")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")
        team3 = Team(ownerId=owner3.id, name="3")
        team4 = Team(ownerId=owner4.id, name="4")
        team5 = Team(ownerId=owner5.id, name="5")
        team6 = Team(ownerId=owner6.id, name="6")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team3.id, teamBId=team4.id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=team5.id, teamBId=team6.id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team3.id, teamBId=team4.id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=team5.id, teamBId=team6.id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team3.id, teamBId=team4.id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=team5.id, teamBId=team6.id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=True,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[team1, team2, team3, team4, team5, team6], weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getAWAL(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Decimal("0"), response[team1.id])
        self.assertEqual(Decimal("0.4"), response[team2.id])
        self.assertEqual(Decimal("0.8"), response[team3.id])
        self.assertEqual(Decimal("1.4"), response[team4.id])
        self.assertEqual(Decimal("1.4"), response[team5.id])
        self.assertEqual(Decimal("2"), response[team6.id])

    def test_getAWAL_onlyRegularSeasonIsTrue(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")
        owner3 = Owner(name="3")
        owner4 = Owner(name="4")
        owner5 = Owner(name="5")
        owner6 = Owner(name="6")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")
        team3 = Team(ownerId=owner3.id, name="3")
        team4 = Team(ownerId=owner4.id, name="4")
        team5 = Team(ownerId=owner5.id, name="5")
        team6 = Team(ownerId=owner6.id, name="6")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team3.id, teamBId=team4.id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=team5.id, teamBId=team6.id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team3.id, teamBId=team4.id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=team5.id, teamBId=team6.id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team3.id, teamBId=team4.id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=team5.id, teamBId=team6.id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=True,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[team1, team2, team3, team4, team5, team6], weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getAWAL(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Decimal("0"), response[team1.id])
        self.assertEqual(Decimal("0.2"), response[team2.id])
        self.assertEqual(Decimal("0.4"), response[team3.id])
        self.assertEqual(Decimal("0.7"), response[team4.id])
        self.assertEqual(Decimal("0.7"), response[team5.id])
        self.assertEqual(Decimal("1"), response[team6.id])

    def test_getAWAL_weekNumberStartGiven(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")
        owner3 = Owner(name="3")
        owner4 = Owner(name="4")
        owner5 = Owner(name="5")
        owner6 = Owner(name="6")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")
        team3 = Team(ownerId=owner3.id, name="3")
        team4 = Team(ownerId=owner4.id, name="4")
        team5 = Team(ownerId=owner5.id, name="5")
        team6 = Team(ownerId=owner6.id, name="6")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team3.id, teamBId=team4.id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=team5.id, teamBId=team6.id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team3.id, teamBId=team4.id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=team5.id, teamBId=team6.id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team3.id, teamBId=team4.id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=team5.id, teamBId=team6.id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=True,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[team1, team2, team3, team4, team5, team6], weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getAWAL(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Decimal("0"), response[team1.id])
        self.assertEqual(Decimal("0.4"), response[team2.id])
        self.assertEqual(Decimal("0.8"), response[team3.id])
        self.assertEqual(Decimal("1.4"), response[team4.id])
        self.assertEqual(Decimal("1.4"), response[team5.id])
        self.assertEqual(Decimal("2"), response[team6.id])

    def test_getAWAL_weekNumberEndGiven(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")
        owner3 = Owner(name="3")
        owner4 = Owner(name="4")
        owner5 = Owner(name="5")
        owner6 = Owner(name="6")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")
        team3 = Team(ownerId=owner3.id, name="3")
        team4 = Team(ownerId=owner4.id, name="4")
        team5 = Team(ownerId=owner5.id, name="5")
        team6 = Team(ownerId=owner6.id, name="6")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team3.id, teamBId=team4.id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=team5.id, teamBId=team6.id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team3.id, teamBId=team4.id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=team5.id, teamBId=team6.id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team3.id, teamBId=team4.id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=team5.id, teamBId=team6.id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=True,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[team1, team2, team3, team4, team5, team6], weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getAWAL(year, weekNumberEnd=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Decimal("0"), response[team1.id])
        self.assertEqual(Decimal("0.4"), response[team2.id])
        self.assertEqual(Decimal("0.8"), response[team3.id])
        self.assertEqual(Decimal("1.4"), response[team4.id])
        self.assertEqual(Decimal("1.4"), response[team5.id])
        self.assertEqual(Decimal("2"), response[team6.id])

    def test_getAWAL_weekNumberStartGivenAndWeekNumberEndGiven(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")
        owner3 = Owner(name="3")
        owner4 = Owner(name="4")
        owner5 = Owner(name="5")
        owner6 = Owner(name="6")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")
        team3 = Team(ownerId=owner3.id, name="3")
        team4 = Team(ownerId=owner4.id, name="4")
        team5 = Team(ownerId=owner5.id, name="5")
        team6 = Team(ownerId=owner6.id, name="6")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team3.id, teamBId=team4.id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=team5.id, teamBId=team6.id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team3.id, teamBId=team4.id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=team5.id, teamBId=team6.id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team3.id, teamBId=team4.id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=team5.id, teamBId=team6.id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team3.id, teamBId=team4.id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=team5.id, teamBId=team6.id, teamAScore=4, teamBScore=5)

        week4 = Week(weekNumber=4, isPlayoffWeek=True, isChampionshipWeek=True,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[team1, team2, team3, team4, team5, team6],
                    weeks=[week1, week2, week3, week4])

        response = AdvancedGameOutcome.getAWAL(year, weekNumberStart=2, weekNumberEnd=3)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Decimal("0"), response[team1.id])
        self.assertEqual(Decimal("0.4"), response[team2.id])
        self.assertEqual(Decimal("0.8"), response[team3.id])
        self.assertEqual(Decimal("1.4"), response[team4.id])
        self.assertEqual(Decimal("1.4"), response[team5.id])
        self.assertEqual(Decimal("2"), response[team6.id])

    def test_getAWAL_matchupEndsInTie(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")
        owner3 = Owner(name="3")
        owner4 = Owner(name="4")
        owner5 = Owner(name="5")
        owner6 = Owner(name="6")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")
        team3 = Team(ownerId=owner3.id, name="3")
        team4 = Team(ownerId=owner4.id, name="4")
        team5 = Team(ownerId=owner5.id, name="5")
        team6 = Team(ownerId=owner6.id, name="6")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team3.id, teamBId=team4.id, teamAScore=3, teamBScore=3)
        matchup3 = Matchup(teamAId=team5.id, teamBId=team6.id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[team1, team2, team3, team4, team5, team6], weeks=[week1])

        response = AdvancedGameOutcome.getAWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Decimal("0"), response[team1.id])
        self.assertEqual(Decimal("0.2"), response[team2.id])
        self.assertEqual(Decimal("0.5"), response[team3.id])
        self.assertEqual(Decimal("0.5"), response[team4.id])
        self.assertEqual(Decimal("0.8"), response[team5.id])
        self.assertEqual(Decimal("1"), response[team6.id])

    def test_getAWAL_multipleMatchupsEndInTie(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")
        owner3 = Owner(name="3")
        owner4 = Owner(name="4")
        owner5 = Owner(name="5")
        owner6 = Owner(name="6")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")
        team3 = Team(ownerId=owner3.id, name="3")
        team4 = Team(ownerId=owner4.id, name="4")
        team5 = Team(ownerId=owner5.id, name="5")
        team6 = Team(ownerId=owner6.id, name="6")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=1)
        matchup2 = Matchup(teamAId=team3.id, teamBId=team4.id, teamAScore=3, teamBScore=3)
        matchup3 = Matchup(teamAId=team5.id, teamBId=team6.id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[team1, team2, team3, team4, team5, team6], weeks=[week1])

        response = AdvancedGameOutcome.getAWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Decimal("0.1"), response[team1.id])
        self.assertEqual(Decimal("0.1"), response[team2.id])
        self.assertEqual(Decimal("0.5"), response[team3.id])
        self.assertEqual(Decimal("0.5"), response[team4.id])
        self.assertEqual(Decimal("0.8"), response[team5.id])
        self.assertEqual(Decimal("1"), response[team6.id])

    def test_getAWAL_allMatchupsEndInTie(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")
        owner3 = Owner(name="3")
        owner4 = Owner(name="4")
        owner5 = Owner(name="5")
        owner6 = Owner(name="6")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")
        team3 = Team(ownerId=owner3.id, name="3")
        team4 = Team(ownerId=owner4.id, name="4")
        team5 = Team(ownerId=owner5.id, name="5")
        team6 = Team(ownerId=owner6.id, name="6")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=1)
        matchup2 = Matchup(teamAId=team3.id, teamBId=team4.id, teamAScore=2, teamBScore=2)
        matchup3 = Matchup(teamAId=team5.id, teamBId=team6.id, teamAScore=3, teamBScore=3)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[team1, team2, team3, team4, team5, team6], weeks=[week1])

        response = AdvancedGameOutcome.getAWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Decimal("0.1"), response[team1.id])
        self.assertEqual(Decimal("0.1"), response[team2.id])
        self.assertEqual(Decimal("0.5"), response[team3.id])
        self.assertEqual(Decimal("0.5"), response[team4.id])
        self.assertEqual(Decimal("0.9"), response[team5.id])
        self.assertEqual(Decimal("0.9"), response[team6.id])

    def test_getAWAL_allMatchupsEndInTieAndHaveSameScore(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")
        owner3 = Owner(name="3")
        owner4 = Owner(name="4")
        owner5 = Owner(name="5")
        owner6 = Owner(name="6")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")
        team3 = Team(ownerId=owner3.id, name="3")
        team4 = Team(ownerId=owner4.id, name="4")
        team5 = Team(ownerId=owner5.id, name="5")
        team6 = Team(ownerId=owner6.id, name="6")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=1)
        matchup2 = Matchup(teamAId=team3.id, teamBId=team4.id, teamAScore=1, teamBScore=1)
        matchup3 = Matchup(teamAId=team5.id, teamBId=team6.id, teamAScore=1, teamBScore=1)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[team1, team2, team3, team4, team5, team6], weeks=[week1])

        response = AdvancedGameOutcome.getAWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Decimal("0.5"), response[team1.id])
        self.assertEqual(Decimal("0.5"), response[team2.id])
        self.assertEqual(Decimal("0.5"), response[team3.id])
        self.assertEqual(Decimal("0.5"), response[team4.id])
        self.assertEqual(Decimal("0.5"), response[team5.id])
        self.assertEqual(Decimal("0.5"), response[team6.id])

    def test_getAWAL_sixteenTeams(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")
        owner3 = Owner(name="3")
        owner4 = Owner(name="4")
        owner5 = Owner(name="5")
        owner6 = Owner(name="6")
        owner7 = Owner(name="7")
        owner8 = Owner(name="8")
        owner9 = Owner(name="9")
        owner10 = Owner(name="10")
        owner11 = Owner(name="11")
        owner12 = Owner(name="12")
        owner13 = Owner(name="13")
        owner14 = Owner(name="14")
        owner15 = Owner(name="15")
        owner16 = Owner(name="16")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")
        team3 = Team(ownerId=owner3.id, name="3")
        team4 = Team(ownerId=owner4.id, name="4")
        team5 = Team(ownerId=owner5.id, name="5")
        team6 = Team(ownerId=owner6.id, name="6")
        team7 = Team(ownerId=owner7.id, name="7")
        team8 = Team(ownerId=owner8.id, name="8")
        team9 = Team(ownerId=owner9.id, name="9")
        team10 = Team(ownerId=owner10.id, name="10")
        team11 = Team(ownerId=owner11.id, name="11")
        team12 = Team(ownerId=owner12.id, name="12")
        team13 = Team(ownerId=owner13.id, name="13")
        team14 = Team(ownerId=owner14.id, name="14")
        team15 = Team(ownerId=owner15.id, name="15")
        team16 = Team(ownerId=owner16.id, name="16")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team3.id, teamBId=team4.id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=team5.id, teamBId=team6.id, teamAScore=5, teamBScore=6)
        matchup4 = Matchup(teamAId=team7.id, teamBId=team8.id, teamAScore=7, teamBScore=8)
        matchup5 = Matchup(teamAId=team9.id, teamBId=team10.id, teamAScore=9, teamBScore=10)
        matchup6 = Matchup(teamAId=team11.id, teamBId=team12.id, teamAScore=11, teamBScore=12)
        matchup7 = Matchup(teamAId=team13.id, teamBId=team14.id, teamAScore=13, teamBScore=14)
        matchup8 = Matchup(teamAId=team15.id, teamBId=team16.id, teamAScore=15, teamBScore=16)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3, matchup4, matchup5, matchup6, matchup7, matchup8])

        year = Year(yearNumber=2000,
                    teams=[team1, team2, team3, team4, team5, team6, team7, team8, team9, team10, team11, team12,
                           team13, team14, team15, team16], weeks=[week1])

        response = AdvancedGameOutcome.getAWAL(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(16, len(response.keys()))
        self.assertEqual(Decimal("0"), response[team1.id])
        self.assertEqual(Decimal("0.06666666666666666666666666667"), response[team2.id])
        self.assertEqual(Decimal("0.1333333333333333333333333333"), response[team3.id])
        self.assertEqual(Decimal("0.2"), response[team4.id])
        self.assertEqual(Decimal("0.2666666666666666666666666667"), response[team5.id])
        self.assertEqual(Decimal("0.3333333333333333333333333334"), response[team6.id])
        self.assertEqual(Decimal("0.4"), response[team7.id])
        self.assertEqual(Decimal("0.4666666666666666666666666667"), response[team8.id])
        self.assertEqual(Decimal("0.5333333333333333333333333334"), response[team9.id])
        self.assertEqual(Decimal("0.6"), response[team10.id])
        self.assertEqual(Decimal("0.6666666666666666666666666667"), response[team11.id])
        self.assertEqual(Decimal("0.7333333333333333333333333334"), response[team12.id])
        self.assertEqual(Decimal("0.8"), response[team13.id])
        self.assertEqual(Decimal("0.8666666666666666666666666667"), response[team14.id])
        self.assertEqual(Decimal("0.9333333333333333333333333334"), response[team15.id])
        self.assertEqual(Decimal("1"), response[team16.id])

    def test_getAWALPerGame_happyPath(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")
        owner3 = Owner(name="3")
        owner4 = Owner(name="4")
        owner5 = Owner(name="5")
        owner6 = Owner(name="6")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")
        team3 = Team(ownerId=owner3.id, name="3")
        team4 = Team(ownerId=owner4.id, name="4")
        team5 = Team(ownerId=owner5.id, name="5")
        team6 = Team(ownerId=owner6.id, name="6")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team3.id, teamBId=team4.id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=team5.id, teamBId=team6.id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team3.id, teamBId=team4.id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=team5.id, teamBId=team6.id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team3.id, teamBId=team4.id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=team5.id, teamBId=team6.id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[team1, team2, team3, team4, team5, team6], weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getAWALPerGame(year)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Decimal("0"), response[team1.id])
        self.assertEqual(Decimal("0.2"), response[team2.id])
        self.assertEqual(Decimal("0.4"), response[team3.id])
        self.assertEqual(Decimal("0.7"), response[team4.id])
        self.assertEqual(Decimal("0.7"), response[team5.id])
        self.assertEqual(Decimal("1"), response[team6.id])

    def test_getAWALPerGame_onlyPostSeasonIsTrue(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")
        owner3 = Owner(name="3")
        owner4 = Owner(name="4")
        owner5 = Owner(name="5")
        owner6 = Owner(name="6")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")
        team3 = Team(ownerId=owner3.id, name="3")
        team4 = Team(ownerId=owner4.id, name="4")
        team5 = Team(ownerId=owner5.id, name="5")
        team6 = Team(ownerId=owner6.id, name="6")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team3.id, teamBId=team4.id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=team5.id, teamBId=team6.id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team3.id, teamBId=team4.id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=team5.id, teamBId=team6.id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team3.id, teamBId=team4.id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=team5.id, teamBId=team6.id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=True,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[team1, team2, team3, team4, team5, team6], weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getAWALPerGame(year, onlyPostSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Decimal("0"), response[team1.id])
        self.assertEqual(Decimal("0.2"), response[team2.id])
        self.assertEqual(Decimal("0.4"), response[team3.id])
        self.assertEqual(Decimal("0.7"), response[team4.id])
        self.assertEqual(Decimal("0.7"), response[team5.id])
        self.assertEqual(Decimal("1"), response[team6.id])

    def test_getAWALPerGame_onlyRegularSeasonIsTrue(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")
        owner3 = Owner(name="3")
        owner4 = Owner(name="4")
        owner5 = Owner(name="5")
        owner6 = Owner(name="6")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")
        team3 = Team(ownerId=owner3.id, name="3")
        team4 = Team(ownerId=owner4.id, name="4")
        team5 = Team(ownerId=owner5.id, name="5")
        team6 = Team(ownerId=owner6.id, name="6")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team3.id, teamBId=team4.id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=team5.id, teamBId=team6.id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team3.id, teamBId=team4.id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=team5.id, teamBId=team6.id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team3.id, teamBId=team4.id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=team5.id, teamBId=team6.id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=True,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[team1, team2, team3, team4, team5, team6], weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getAWALPerGame(year, onlyRegularSeason=True)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Decimal("0"), response[team1.id])
        self.assertEqual(Decimal("0.2"), response[team2.id])
        self.assertEqual(Decimal("0.4"), response[team3.id])
        self.assertEqual(Decimal("0.7"), response[team4.id])
        self.assertEqual(Decimal("0.7"), response[team5.id])
        self.assertEqual(Decimal("1"), response[team6.id])

    def test_getAWALPerGame_weekNumberStartGiven(self):
        owner1 = Owner(name="1")
        owner2 = Owner(name="2")
        owner3 = Owner(name="3")
        owner4 = Owner(name="4")
        owner5 = Owner(name="5")
        owner6 = Owner(name="6")

        team1 = Team(ownerId=owner1.id, name="1")
        team2 = Team(ownerId=owner2.id, name="2")
        team3 = Team(ownerId=owner3.id, name="3")
        team4 = Team(ownerId=owner4.id, name="4")
        team5 = Team(ownerId=owner5.id, name="5")
        team6 = Team(ownerId=owner6.id, name="6")

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team3.id, teamBId=team4.id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=team5.id, teamBId=team6.id, teamAScore=4, teamBScore=5)

        week1 = Week(weekNumber=1, isPlayoffWeek=False, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team3.id, teamBId=team4.id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=team5.id, teamBId=team6.id, teamAScore=4, teamBScore=5)

        week2 = Week(weekNumber=2, isPlayoffWeek=True, isChampionshipWeek=False,
                     matchups=[matchup1, matchup2, matchup3])

        matchup1 = Matchup(teamAId=team1.id, teamBId=team2.id, teamAScore=1, teamBScore=2)
        matchup2 = Matchup(teamAId=team3.id, teamBId=team4.id, teamAScore=3, teamBScore=4)
        matchup3 = Matchup(teamAId=team5.id, teamBId=team6.id, teamAScore=4, teamBScore=5)

        week3 = Week(weekNumber=3, isPlayoffWeek=True, isChampionshipWeek=True,
                     matchups=[matchup1, matchup2, matchup3])

        year = Year(yearNumber=2000, teams=[team1, team2, team3, team4, team5, team6], weeks=[week1, week2, week3])

        response = AdvancedGameOutcome.getAWALPerGame(year, weekNumberStart=2)

        self.assertIsInstance(response, dict)
        self.assertEqual(6, len(response.keys()))
        self.assertEqual(Decimal("0"), response[team1.id])
        self.assertEqual(Decimal("0.2"), response[team2.id])
        self.assertEqual(Decimal("0.4"), response[team3.id])
        self.assertEqual(Decimal("0.7"), response[team4.id])
        self.assertEqual(Decimal("0.7"), response[team5.id])
        self.assertEqual(Decimal("1"), response[team6.id])
