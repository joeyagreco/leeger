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
