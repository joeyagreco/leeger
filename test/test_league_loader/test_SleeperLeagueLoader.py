import unittest
from leeger.enum.MatchupType import MatchupType

from leeger.league_loader import SleeperLeagueLoader
from unittest.mock import patch, Mock
from sleeper.model import User as SleeperUser
from sleeper.model import Roster as SleeperRoster
from sleeper.model import Matchup as SleeperMatchup
from sleeper.model import SportState as SleeperSportState
from leeger.model.league.League import League
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Owner import Owner

from leeger.model.league.Team import Team
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year


class TestSleeperLeagueLoader(unittest.TestCase):
    """
    # TODO: Add better tests.
    """

    # helper methods
    def __generateMockSleeperUser(self, *, displayName: str, userId: str) -> SleeperUser:
        return SleeperUser(
            avatar=None,
            cookies=None,
            created=None,
            currencies=None,
            data_updated=None,
            deleted=None,
            display_name=displayName,
            email=None,
            is_bot=None,
            is_owner=None,
            league_id=None,
            metadata=None,
            notifications=None,
            pending=None,
            phone=None,
            real_name=None,
            solicitable=None,
            summoner_region=None,
            token=None,
            user_id=userId,
            username=None,
            verification=None,
        )

    def __generateMockSleeperRoster(self, *, ownerId: str, rosterId: str) -> SleeperRoster:
        return SleeperRoster(
            co_owners=None,
            league_id=None,
            metadata=None,
            owner_id=ownerId,
            players=None,
            player_map=None,
            reserve=None,
            roster_id=rosterId,
            settings=None,
            starters=None,
            taxi=None,
        )

    def __generateMockSleeperMatchup(
        self, *, matchupId: int, rosterId: int, points: float
    ) -> SleeperMatchup:
        return SleeperMatchup(
            custom_points=None,
            matchup_id=matchupId,
            players=None,
            players_points=None,
            points=points,
            roster_id=rosterId,
            starters=None,
            starters_points=None,
        )

    def __generateMockSleeperSportState(self, *, season: str, leg: int) -> SleeperSportState:
        return SleeperSportState(
            display_week=None,
            league_create_season=None,
            league_season=None,
            leg=leg,
            previous_season=None,
            season=season,
            season_start_date=None,
            season_type=None,
            week=None,
        )

    def test_loadLeague_intendedFailure(self):
        with self.assertRaises(ValueError) as context:
            leagueLoader = SleeperLeagueLoader("0", [2000])
            leagueLoader.loadLeague()  # 0 is a bad league ID
        self.assertEqual("Could not find years '[2000]' for league.", str(context.exception))

    @patch("sleeper.api.LeagueAPIClient.get_league")
    @patch("sleeper.api.LeagueAPIClient.get_users_in_league")
    @patch("sleeper.api.LeagueAPIClient.get_rosters")
    @patch("sleeper.api.LeagueAPIClient.get_matchups_for_week")
    @patch("sleeper.api.LeagueAPIClient.get_sport_state")
    @patch("sleeper.api.LeagueAPIClient.get_winners_bracket")
    def test_load_league(
        self,
        mockGetWinnersBracket,
        mockGetSportState,
        mockGetMatchupsForWeek,
        mockGetRosters,
        mockGetUsersInLeague,
        mockGetLeague,
    ):
        # create mock SleeperLeague object
        mockSleeperLeague2022 = Mock()
        mockSleeperLeague2022.season = "2022"
        mockSleeperLeague2022.status = "active"
        mockSleeperLeague2022.playoff_matchups = []
        mockSleeperLeague2022.name = "Test League 2022"
        mockSleeperLeague2022.settings.playoff_week_start = 3
        mockSleeperLeague2022.settings.league_average_match = 0

        # create mock SleeperUser objects
        # TODO: mock metadata for team name
        mockSleeperUsers2022 = [
            self.__generateMockSleeperUser(displayName="User 1", userId="1"),
            self.__generateMockSleeperUser(displayName="User 2", userId="2"),
            self.__generateMockSleeperUser(displayName="User 3", userId="3"),
            self.__generateMockSleeperUser(displayName="User 4", userId="4"),
            self.__generateMockSleeperUser(displayName="User 5", userId="5"),
            self.__generateMockSleeperUser(displayName="User 6", userId="6"),
            self.__generateMockSleeperUser(displayName="User 7", userId="7"),
            self.__generateMockSleeperUser(displayName="User 8", userId="8"),
        ]

        # create mock SleeperRoster objects
        # roster id will be YYYY (year) RR (roster number)
        mockSleeperRosters2022 = [
            self.__generateMockSleeperRoster(ownerId="1", rosterId=202201),
            self.__generateMockSleeperRoster(ownerId="2", rosterId=202202),
            self.__generateMockSleeperRoster(ownerId="3", rosterId=202203),
            self.__generateMockSleeperRoster(ownerId="4", rosterId=202204),
            self.__generateMockSleeperRoster(ownerId="5", rosterId=202205),
            self.__generateMockSleeperRoster(ownerId="6", rosterId=202206),
            self.__generateMockSleeperRoster(ownerId="7", rosterId=202207),
            self.__generateMockSleeperRoster(ownerId="8", rosterId=202208),
        ]

        # create mock SleeperMatchup objects
        # matchup id will be YYYY (year) WW (week number) MM (matchup number)
        mockSleeperMatchups2022_1 = [
            self.__generateMockSleeperMatchup(matchupId=20220101, rosterId=202201, points=100),
            self.__generateMockSleeperMatchup(matchupId=20220101, rosterId=202202, points=100),
            self.__generateMockSleeperMatchup(matchupId=20220102, rosterId=202203, points=90.5),
            self.__generateMockSleeperMatchup(matchupId=20220102, rosterId=202204, points=70.5),
            self.__generateMockSleeperMatchup(matchupId=20220103, rosterId=202205, points=110),
            self.__generateMockSleeperMatchup(matchupId=20220103, rosterId=202206, points=60),
            self.__generateMockSleeperMatchup(matchupId=20220104, rosterId=202207, points=120),
            self.__generateMockSleeperMatchup(matchupId=20220104, rosterId=202208, points=50),
        ]

        # create mock SleeperSportState objects
        mockSleeperSportState2022 = self.__generateMockSleeperSportState(season="2022", leg=2)

        mockGetLeague.side_effect = [mockSleeperLeague2022]
        mockGetUsersInLeague.side_effect = [mockSleeperUsers2022]
        mockGetRosters.side_effect = [mockSleeperRosters2022]
        mockGetMatchupsForWeek.side_effect = [mockSleeperMatchups2022_1]
        mockGetSportState.side_effect = [mockSleeperSportState2022]
        mockGetWinnersBracket.side_effect = [[]]

        # create instance of SleeperLeagueLoader and call load_league method
        sleeper_league_loader = SleeperLeagueLoader("123", [2022])
        league = sleeper_league_loader.loadLeague()

        # expected league
        team1 = Team(ownerId=1, name="User 1")
        team2 = Team(ownerId=2, name="User 2")
        team3 = Team(ownerId=3, name="User 3")
        team4 = Team(ownerId=4, name="User 4")
        team5 = Team(ownerId=5, name="User 5")
        team6 = Team(ownerId=6, name="User 6")
        team7 = Team(ownerId=7, name="User 7")
        team8 = Team(ownerId=8, name="User 8")

        expectedLeague = League(
            name="Test League 2022",
            owners=[
                Owner(name="User 1"),
                Owner(name="User 2"),
                Owner(name="User 3"),
                Owner(name="User 4"),
                Owner(name="User 5"),
                Owner(name="User 6"),
                Owner(name="User 7"),
                Owner(name="User 8"),
            ],
            years=[
                Year(
                    yearNumber=2022,
                    teams=[team1, team2, team3, team4, team5, team6, team7, team8],
                    weeks=[
                        Week(
                            weekNumber=1,
                            matchups=[
                                Matchup(
                                    teamAId=team1.id,
                                    teamBId=team2.id,
                                    teamAScore=100,
                                    teamBScore=100,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team3.id,
                                    teamBId=team4.id,
                                    teamAScore=90.5,
                                    teamBScore=70.5,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team5.id,
                                    teamBId=team6.id,
                                    teamAScore=110,
                                    teamBScore=60,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team7.id,
                                    teamBId=team8.id,
                                    teamAScore=120,
                                    teamBScore=50,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                            ],
                        )
                    ],
                    yearSettings=None,
                )
            ],
        )
        self.assertEqual(league, expectedLeague)
