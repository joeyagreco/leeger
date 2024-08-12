import unittest
from typing import Optional
from unittest.mock import Mock, patch

from sleeper.enum import PlayoffRoundType as SleeperPlayoffRoundType
from sleeper.enum import SeasonStatus as SleeperSeasonStatus
from sleeper.model import Matchup as SleeperMatchup
from sleeper.model import PlayoffMatchup as SleeperPlayoffMatchup
from sleeper.model import Roster as SleeperRoster
from sleeper.model import RosterSettings as SleeperRosterSettings
from sleeper.model import SportState as SleeperSportState
from sleeper.model import User as SleeperUser

from leeger.enum.MatchupType import MatchupType
from leeger.exception.LeagueLoaderException import LeagueLoaderException
from leeger.league_loader import SleeperLeagueLoader
from leeger.model.league.Division import Division
from leeger.model.league.League import League
from leeger.model.league.Matchup import Matchup
from leeger.model.league.Owner import Owner
from leeger.model.league.Team import Team
from leeger.model.league.Week import Week
from leeger.model.league.Year import Year
from leeger.model.league.YearSettings import YearSettings


class TestSleeperLeagueLoader(unittest.TestCase):
    # helper methods
    def __generateMockSleeperUser(
        self, *, displayName: str, userId: str, metadata: Optional[dict] = None
    ) -> SleeperUser:
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
            metadata=metadata,
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

    def __generateMockSleeperRoster(
        self, *, ownerId: str, rosterId: str, division: int
    ) -> SleeperRoster:
        rosterSettings = SleeperRosterSettings(
            division=division,
            fpts=None,
            fpts_against=None,
            fpts_against_decimal=None,
            fpts_decimal=None,
            losses=None,
            ppts=None,
            ppts_decimal=None,
            ties=None,
            total_moves=None,
            waiver_adjusted=None,
            waiver_budget_used=None,
            waiver_position=None,
            wins=None,
        )
        return SleeperRoster(
            co_owners=None,
            league_id=None,
            metadata=None,
            owner_id=ownerId,
            players=None,
            player_map=None,
            reserve=None,
            roster_id=rosterId,
            settings=rosterSettings,
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

    def __generateMockSleeperSportState(
        self, *, season: str, leg: int
    ) -> SleeperSportState:
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

    def __generateMockSleeperPlayoffMatchup(
        self,
        *,
        round: int,
        team1RosterId: int,
        team2RosterId: int,
        winningRosterId: int,
        p: int,
        matchupId: int,
    ) -> SleeperPlayoffMatchup:
        return SleeperPlayoffMatchup(
            losing_roster_id=None,
            matchup_id=matchupId,
            round=round,
            team_1_from=None,
            team_1_roster_id=team1RosterId,
            team_2_from=None,
            team_2_roster_id=team2RosterId,
            winning_roster_id=winningRosterId,
            p=p,
        )

    @patch("sleeper.api.LeagueAPIClient.get_league")
    def test_loadLeague_invalidSeasonStatus(self, mockGetLeague):
        # create mock SleeperLeague object
        mockSleeperLeague2022 = Mock()
        mockSleeperLeague2022.season = "2022"
        mockSleeperLeague2022.status = SleeperSeasonStatus.DRAFTING
        mockGetLeague.side_effect = [mockSleeperLeague2022]
        with self.assertRaises(LeagueLoaderException) as context:
            leagueLoader = SleeperLeagueLoader("1", [2022])
            leagueLoader.loadLeague()
        self.assertEqual(
            "Year 2022 has a status that is not supported: 'SeasonStatus.DRAFTING'",
            str(context.exception),
        )
        # edit mock SleeperLeague object
        mockSleeperLeague2022.status = SleeperSeasonStatus.POSTPONED
        mockGetLeague.side_effect = [mockSleeperLeague2022]
        with self.assertRaises(LeagueLoaderException) as context:
            leagueLoader = SleeperLeagueLoader("1", [2022])
            leagueLoader.loadLeague()
        self.assertEqual(
            "Year 2022 has a status that is not supported: 'SeasonStatus.POSTPONED'",
            str(context.exception),
        )
        # edit mock SleeperLeague object
        mockSleeperLeague2022.status = SleeperSeasonStatus.PRE_DRAFT
        mockGetLeague.side_effect = [mockSleeperLeague2022]
        with self.assertRaises(LeagueLoaderException) as context:
            leagueLoader = SleeperLeagueLoader("1", [2022])
            leagueLoader.loadLeague()
        self.assertEqual(
            "Year 2022 has a status that is not supported: 'SeasonStatus.PRE_DRAFT'",
            str(context.exception),
        )

    @patch("sleeper.api.LeagueAPIClient.get_league")
    @patch("sleeper.api.LeagueAPIClient.get_users_in_league")
    @patch("sleeper.api.LeagueAPIClient.get_rosters")
    @patch("sleeper.api.LeagueAPIClient.get_matchups_for_week")
    @patch("sleeper.api.LeagueAPIClient.get_sport_state")
    @patch("sleeper.api.LeagueAPIClient.get_winners_bracket")
    def test_load_league_happyPath(
        self,
        mockGetWinnersBracket,
        mockGetSportState,
        mockGetMatchupsForWeek,
        mockGetRosters,
        mockGetUsersInLeague,
        mockGetLeague,
    ):
        # create mock SleeperLeague objects

        mockSleeperLeague2022 = Mock()
        mockSleeperLeague2022.season = "2022"
        mockSleeperLeague2022.status = SleeperSeasonStatus.COMPLETE
        mockSleeperLeague2022.playoff_matchups = []
        mockSleeperLeague2022.name = "Test League 2022"
        mockSleeperLeague2022.settings.playoff_week_start = 3
        mockSleeperLeague2022.settings.league_average_match = 0
        mockSleeperLeague2022.settings.divisions = 2
        mockSleeperLeague2022.settings.playoff_round_type_enum = (
            SleeperPlayoffRoundType.ONE_WEEK_PER_ROUND
        )
        mockSleeperLeague2022.metadata.division_1 = "d1_2022"
        mockSleeperLeague2022.metadata.division_2 = "d2_2022"

        mockSleeperLeague2023 = Mock()
        mockSleeperLeague2023.season = "2023"
        mockSleeperLeague2023.status = SleeperSeasonStatus.IN_SEASON
        mockSleeperLeague2023.playoff_matchups = []
        mockSleeperLeague2023.name = "Test League 2023"
        mockSleeperLeague2023.settings.playoff_week_start = 3
        mockSleeperLeague2023.settings.league_average_match = 0
        mockSleeperLeague2023.settings.divisions = 2
        mockSleeperLeague2023.settings.playoff_round_type_enum = (
            SleeperPlayoffRoundType.ONE_WEEK_PER_ROUND
        )
        mockSleeperLeague2023.metadata.division_1 = "d1_2023"
        mockSleeperLeague2023.metadata.division_2 = "d2_2023"

        # create mock SleeperUser objects
        mockSleeperUsers2022 = [
            self.__generateMockSleeperUser(displayName="User 1", userId="1"),
            self.__generateMockSleeperUser(displayName="User 2", userId="2"),
            self.__generateMockSleeperUser(displayName="User 3", userId="3"),
            self.__generateMockSleeperUser(displayName="User 4", userId="4"),
            self.__generateMockSleeperUser(
                displayName="User 5", userId="5", metadata={"team_name": "Team 5"}
            ),
            self.__generateMockSleeperUser(
                displayName="User 6", userId="6", metadata={"team_name": "Team 6"}
            ),
            self.__generateMockSleeperUser(
                displayName="User 7", userId="7", metadata={"team_name": "Team 7"}
            ),
            self.__generateMockSleeperUser(
                displayName="User 8", userId="8", metadata={"team_name": "Team 8"}
            ),
        ]

        mockSleeperUsers2023 = [
            self.__generateMockSleeperUser(displayName="User 1", userId="1"),
            self.__generateMockSleeperUser(displayName="User 2", userId="2"),
            self.__generateMockSleeperUser(displayName="User 3", userId="3"),
            self.__generateMockSleeperUser(displayName="User 4", userId="4"),
            self.__generateMockSleeperUser(
                displayName="User 5", userId="5", metadata={"team_name": "Team 5"}
            ),
            self.__generateMockSleeperUser(
                displayName="User 6", userId="6", metadata={"team_name": "Team 6"}
            ),
            self.__generateMockSleeperUser(
                displayName="User 7", userId="7", metadata={"team_name": "Team 7"}
            ),
            self.__generateMockSleeperUser(
                displayName="User 8", userId="8", metadata={"team_name": "Team 8"}
            ),
        ]

        # create mock SleeperRoster objects
        # roster id will be YYYY (year) RR (roster number)
        mockSleeperRosters2022 = [
            self.__generateMockSleeperRoster(ownerId="1", rosterId=202201, division=1),
            self.__generateMockSleeperRoster(ownerId="2", rosterId=202202, division=1),
            self.__generateMockSleeperRoster(ownerId="3", rosterId=202203, division=1),
            self.__generateMockSleeperRoster(ownerId="4", rosterId=202204, division=1),
            self.__generateMockSleeperRoster(ownerId="5", rosterId=202205, division=2),
            self.__generateMockSleeperRoster(ownerId="6", rosterId=202206, division=2),
            self.__generateMockSleeperRoster(ownerId="7", rosterId=202207, division=2),
            self.__generateMockSleeperRoster(ownerId="8", rosterId=202208, division=2),
        ]

        mockSleeperRosters2023 = [
            self.__generateMockSleeperRoster(ownerId="1", rosterId=202301, division=1),
            self.__generateMockSleeperRoster(ownerId="2", rosterId=202302, division=1),
            self.__generateMockSleeperRoster(ownerId="3", rosterId=202303, division=1),
            self.__generateMockSleeperRoster(ownerId="4", rosterId=202304, division=1),
            self.__generateMockSleeperRoster(ownerId="5", rosterId=202305, division=2),
            self.__generateMockSleeperRoster(ownerId="6", rosterId=202306, division=2),
            self.__generateMockSleeperRoster(ownerId="7", rosterId=202307, division=2),
            self.__generateMockSleeperRoster(ownerId="8", rosterId=202308, division=2),
        ]

        # create mock SleeperMatchup objects
        # matchup id will be YYYY (year) WW (week number) MM (matchup number)
        mockSleeperMatchups2022_1 = [
            self.__generateMockSleeperMatchup(
                matchupId=20220101, rosterId=202201, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220101, rosterId=202202, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220102, rosterId=202203, points=90.5
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220102, rosterId=202204, points=70.5
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220103, rosterId=202205, points=110
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220103, rosterId=202206, points=60
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220104, rosterId=202207, points=120
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220104, rosterId=202208, points=50
            ),
        ]

        mockSleeperMatchups2022_2 = [
            self.__generateMockSleeperMatchup(
                matchupId=20220201, rosterId=202201, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220201, rosterId=202202, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220202, rosterId=202203, points=90.5
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220202, rosterId=202204, points=70.5
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220203, rosterId=202205, points=110
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220203, rosterId=202206, points=60
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220204, rosterId=202207, points=120
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220204, rosterId=202208, points=50
            ),
        ]

        # playoffs
        mockSleeperMatchups2022_3 = [
            self.__generateMockSleeperMatchup(
                matchupId=20220301, rosterId=202202, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220301, rosterId=202203, points=90.5
            ),
        ]

        # championship
        mockSleeperMatchups2022_4 = [
            self.__generateMockSleeperMatchup(
                matchupId=20220401, rosterId=202201, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220401, rosterId=202202, points=99
            ),
        ]

        mockSleeperMatchups2023_1 = [
            self.__generateMockSleeperMatchup(
                matchupId=20230101, rosterId=202301, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230101, rosterId=202302, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230102, rosterId=202303, points=90.5
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230102, rosterId=202304, points=70.5
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230103, rosterId=202305, points=110
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230103, rosterId=202306, points=60
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230104, rosterId=202307, points=120
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230104, rosterId=202308, points=50
            ),
        ]

        mockSleeperMatchups2023_2 = [
            self.__generateMockSleeperMatchup(
                matchupId=20230201, rosterId=202301, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230201, rosterId=202302, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230202, rosterId=202303, points=90.5
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230202, rosterId=202304, points=70.5
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230203, rosterId=202305, points=110
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230203, rosterId=202306, points=60
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230204, rosterId=202307, points=120
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230204, rosterId=202308, points=50
            ),
        ]

        # playoffs
        mockSleeperMatchups2023_3 = [
            self.__generateMockSleeperMatchup(
                matchupId=20230301, rosterId=202302, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230301, rosterId=202303, points=90.5
            ),
        ]

        # championship
        mockSleeperMatchups2023_4 = [
            self.__generateMockSleeperMatchup(
                matchupId=20230401, rosterId=202301, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230401, rosterId=202302, points=99
            ),
        ]

        # create mock SleeperSportState objects
        mockSleeperSportState2022 = self.__generateMockSleeperSportState(
            season="2022", leg=5
        )
        mockSleeperSportState2023 = self.__generateMockSleeperSportState(
            season="2023", leg=5
        )

        # create mock SleeperPlayoffMatchup objects
        mockSleeperPlayoffMatchups2022 = [
            self.__generateMockSleeperPlayoffMatchup(
                round=1,
                team1RosterId=202202,
                team2RosterId=202203,
                winningRosterId=202202,
                p=0,
                matchupId=20220301,
            ),
            self.__generateMockSleeperPlayoffMatchup(
                round=2,
                team1RosterId=202201,
                team2RosterId=202202,
                winningRosterId=202201,
                p=1,
                matchupId=20220401,
            ),
        ]

        mockSleeperPlayoffMatchups2023 = [
            self.__generateMockSleeperPlayoffMatchup(
                round=1,
                team1RosterId=202302,
                team2RosterId=202303,
                winningRosterId=202302,
                p=0,
                matchupId=20230301,
            ),
            self.__generateMockSleeperPlayoffMatchup(
                round=2,
                team1RosterId=202301,
                team2RosterId=202302,
                winningRosterId=202301,
                p=1,
                matchupId=20230401,
            ),
        ]

        mockGetLeague.side_effect = [mockSleeperLeague2022, mockSleeperLeague2023]
        mockGetUsersInLeague.side_effect = [mockSleeperUsers2022, mockSleeperUsers2023]
        mockGetRosters.side_effect = [mockSleeperRosters2022, mockSleeperRosters2023]
        mockGetMatchupsForWeek.side_effect = [
            mockSleeperMatchups2022_1,
            mockSleeperMatchups2022_2,
            mockSleeperMatchups2022_3,
            mockSleeperMatchups2022_4,
            mockSleeperMatchups2023_1,
            mockSleeperMatchups2023_2,
            mockSleeperMatchups2023_3,
            mockSleeperMatchups2023_4,
        ]
        mockGetSportState.side_effect = [
            mockSleeperSportState2022,
            mockSleeperSportState2023,
        ]
        mockGetWinnersBracket.side_effect = [
            mockSleeperPlayoffMatchups2022,
            mockSleeperPlayoffMatchups2023,
        ]

        # create instance of SleeperLeagueLoader and call load_league method
        sleeper_league_loader = SleeperLeagueLoader("123", [2022, 2023])
        league = sleeper_league_loader.loadLeague()

        # expected league

        division1_2022 = Division(name="d1_2022")
        division2_2022 = Division(name="d2_2022")

        division1_2023 = Division(name="d1_2023")
        division2_2023 = Division(name="d2_2023")

        owner1 = Owner(name="User 1")
        owner2 = Owner(name="User 2")
        owner3 = Owner(name="User 3")
        owner4 = Owner(name="User 4")
        owner5 = Owner(name="User 5")
        owner6 = Owner(name="User 6")
        owner7 = Owner(name="User 7")
        owner8 = Owner(name="User 8")

        team1_2022 = Team(
            ownerId=owner1.id, name="User 1", divisionId=division1_2022.id
        )
        team2_2022 = Team(
            ownerId=owner2.id, name="User 2", divisionId=division1_2022.id
        )
        team3_2022 = Team(
            ownerId=owner3.id, name="User 3", divisionId=division1_2022.id
        )
        team4_2022 = Team(
            ownerId=owner4.id, name="User 4", divisionId=division1_2022.id
        )
        team5_2022 = Team(
            ownerId=owner5.id, name="Team 5", divisionId=division2_2022.id
        )
        team6_2022 = Team(
            ownerId=owner6.id, name="Team 6", divisionId=division2_2022.id
        )
        team7_2022 = Team(
            ownerId=owner7.id, name="Team 7", divisionId=division2_2022.id
        )
        team8_2022 = Team(
            ownerId=owner8.id, name="Team 8", divisionId=division2_2022.id
        )

        team1_2023 = Team(
            ownerId=owner1.id, name="User 1", divisionId=division1_2023.id
        )
        team2_2023 = Team(
            ownerId=owner2.id, name="User 2", divisionId=division1_2023.id
        )
        team3_2023 = Team(
            ownerId=owner3.id, name="User 3", divisionId=division1_2023.id
        )
        team4_2023 = Team(
            ownerId=owner4.id, name="User 4", divisionId=division1_2023.id
        )
        team5_2023 = Team(
            ownerId=owner5.id, name="Team 5", divisionId=division2_2023.id
        )
        team6_2023 = Team(
            ownerId=owner6.id, name="Team 6", divisionId=division2_2023.id
        )
        team7_2023 = Team(
            ownerId=owner7.id, name="Team 7", divisionId=division2_2023.id
        )
        team8_2023 = Team(
            ownerId=owner8.id, name="Team 8", divisionId=division2_2023.id
        )

        expectedLeague = League(
            name="Test League 2023",
            owners=[owner1, owner2, owner3, owner4, owner5, owner6, owner7, owner8],
            years=[
                Year(
                    yearNumber=2022,
                    teams=[
                        team1_2022,
                        team2_2022,
                        team3_2022,
                        team4_2022,
                        team5_2022,
                        team6_2022,
                        team7_2022,
                        team8_2022,
                    ],
                    weeks=[
                        Week(
                            weekNumber=1,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2022.id,
                                    teamBId=team2_2022.id,
                                    teamAScore=100,
                                    teamBScore=100,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                                Matchup(
                                    teamAId=team3_2022.id,
                                    teamBId=team4_2022.id,
                                    teamAScore=90.5,
                                    teamBScore=70.5,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                                Matchup(
                                    teamAId=team5_2022.id,
                                    teamBId=team6_2022.id,
                                    teamAScore=110,
                                    teamBScore=60,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                                Matchup(
                                    teamAId=team7_2022.id,
                                    teamBId=team8_2022.id,
                                    teamAScore=120,
                                    teamBScore=50,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                            ],
                        ),
                        Week(
                            weekNumber=2,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2022.id,
                                    teamBId=team2_2022.id,
                                    teamAScore=100,
                                    teamBScore=100,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                                Matchup(
                                    teamAId=team3_2022.id,
                                    teamBId=team4_2022.id,
                                    teamAScore=90.5,
                                    teamBScore=70.5,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                                Matchup(
                                    teamAId=team5_2022.id,
                                    teamBId=team6_2022.id,
                                    teamAScore=110,
                                    teamBScore=60,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                                Matchup(
                                    teamAId=team7_2022.id,
                                    teamBId=team8_2022.id,
                                    teamAScore=120,
                                    teamBScore=50,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                            ],
                        ),
                        Week(
                            weekNumber=3,
                            matchups=[
                                Matchup(
                                    teamAId=team2_2022.id,
                                    teamBId=team3_2022.id,
                                    teamAScore=100,
                                    teamBScore=90.5,
                                    matchupType=MatchupType.PLAYOFF,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                )
                            ],
                        ),
                        Week(
                            weekNumber=4,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2022.id,
                                    teamBId=team2_2022.id,
                                    teamAScore=100,
                                    teamBScore=99,
                                    matchupType=MatchupType.CHAMPIONSHIP,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                )
                            ],
                        ),
                    ],
                    yearSettings=None,
                    divisions=[division1_2022, division2_2022],
                ),
                Year(
                    yearNumber=2023,
                    teams=[
                        team1_2023,
                        team2_2023,
                        team3_2023,
                        team4_2023,
                        team5_2023,
                        team6_2023,
                        team7_2023,
                        team8_2023,
                    ],
                    weeks=[
                        Week(
                            weekNumber=1,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2023.id,
                                    teamBId=team2_2023.id,
                                    teamAScore=100,
                                    teamBScore=100,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                                Matchup(
                                    teamAId=team3_2023.id,
                                    teamBId=team4_2023.id,
                                    teamAScore=90.5,
                                    teamBScore=70.5,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                                Matchup(
                                    teamAId=team5_2023.id,
                                    teamBId=team6_2023.id,
                                    teamAScore=110,
                                    teamBScore=60,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                                Matchup(
                                    teamAId=team7_2023.id,
                                    teamBId=team8_2023.id,
                                    teamAScore=120,
                                    teamBScore=50,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                            ],
                        ),
                        Week(
                            weekNumber=2,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2023.id,
                                    teamBId=team2_2023.id,
                                    teamAScore=100,
                                    teamBScore=100,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                                Matchup(
                                    teamAId=team3_2023.id,
                                    teamBId=team4_2023.id,
                                    teamAScore=90.5,
                                    teamBScore=70.5,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                                Matchup(
                                    teamAId=team5_2023.id,
                                    teamBId=team6_2023.id,
                                    teamAScore=110,
                                    teamBScore=60,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                                Matchup(
                                    teamAId=team7_2023.id,
                                    teamBId=team8_2023.id,
                                    teamAScore=120,
                                    teamBScore=50,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                            ],
                        ),
                        Week(
                            weekNumber=3,
                            matchups=[
                                Matchup(
                                    teamAId=team2_2023.id,
                                    teamBId=team3_2023.id,
                                    teamAScore=100,
                                    teamBScore=90.5,
                                    matchupType=MatchupType.PLAYOFF,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                )
                            ],
                        ),
                        Week(
                            weekNumber=4,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2023.id,
                                    teamBId=team2_2023.id,
                                    teamAScore=100,
                                    teamBScore=99,
                                    matchupType=MatchupType.CHAMPIONSHIP,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                )
                            ],
                        ),
                    ],
                    yearSettings=None,
                    divisions=[division1_2023, division2_2023],
                ),
            ],
        )
        self.assertTrue(
            league.equals(expectedLeague, ignoreBaseIds=True, ignoreIds=True)
        )
        # check multiWeekMatchupIds
        for year in league.years:
            for week in year.weeks:
                for matchup in week.matchups:
                    self.assertIsNone(matchup.multiWeekMatchupId)

    @patch("sleeper.api.LeagueAPIClient.get_league")
    @patch("sleeper.api.LeagueAPIClient.get_users_in_league")
    @patch("sleeper.api.LeagueAPIClient.get_rosters")
    @patch("sleeper.api.LeagueAPIClient.get_matchups_for_week")
    @patch("sleeper.api.LeagueAPIClient.get_sport_state")
    @patch("sleeper.api.LeagueAPIClient.get_winners_bracket")
    def test_load_league_happyPath_withOwnerNamesAndAliases(
        self,
        mockGetWinnersBracket,
        mockGetSportState,
        mockGetMatchupsForWeek,
        mockGetRosters,
        mockGetUsersInLeague,
        mockGetLeague,
    ):
        # create mock SleeperLeague objects
        mockSleeperLeague2022 = Mock()
        mockSleeperLeague2022.season = "2022"
        mockSleeperLeague2022.status = SleeperSeasonStatus.COMPLETE
        mockSleeperLeague2022.playoff_matchups = []
        mockSleeperLeague2022.name = "Test League 2022"
        mockSleeperLeague2022.settings.playoff_week_start = 3
        mockSleeperLeague2022.settings.league_average_match = 0
        mockSleeperLeague2022.settings.divisions = 2
        mockSleeperLeague2022.settings.playoff_round_type_enum = (
            SleeperPlayoffRoundType.ONE_WEEK_PER_ROUND
        )
        mockSleeperLeague2022.metadata.division_1 = "d1_2022"
        mockSleeperLeague2022.metadata.division_2 = "d2_2022"

        # create mock SleeperUser objects
        mockSleeperUsers2022 = [
            self.__generateMockSleeperUser(displayName="User 1", userId="1"),
            self.__generateMockSleeperUser(displayName="User 2", userId="2"),
            self.__generateMockSleeperUser(displayName="User 3", userId="3"),
            self.__generateMockSleeperUser(displayName="User 4", userId="4"),
            self.__generateMockSleeperUser(
                displayName="User 5", userId="5", metadata={"team_name": "Team 5"}
            ),
            self.__generateMockSleeperUser(
                displayName="User 6", userId="6", metadata={"team_name": "Team 6"}
            ),
            self.__generateMockSleeperUser(
                displayName="User 7", userId="7", metadata={"team_name": "Team 7"}
            ),
            self.__generateMockSleeperUser(
                displayName="User 8", userId="8", metadata={"team_name": "Team 8"}
            ),
        ]

        # create mock SleeperRoster objects
        # roster id will be YYYY (year) RR (roster number)
        mockSleeperRosters2022 = [
            self.__generateMockSleeperRoster(ownerId="1", rosterId=202201, division=1),
            self.__generateMockSleeperRoster(ownerId="2", rosterId=202202, division=1),
            self.__generateMockSleeperRoster(ownerId="3", rosterId=202203, division=1),
            self.__generateMockSleeperRoster(ownerId="4", rosterId=202204, division=1),
            self.__generateMockSleeperRoster(ownerId="5", rosterId=202205, division=2),
            self.__generateMockSleeperRoster(ownerId="6", rosterId=202206, division=2),
            self.__generateMockSleeperRoster(ownerId="7", rosterId=202207, division=2),
            self.__generateMockSleeperRoster(ownerId="8", rosterId=202208, division=2),
        ]

        # create mock SleeperMatchup objects
        # matchup id will be YYYY (year) WW (week number) MM (matchup number)
        mockSleeperMatchups2022_1 = [
            self.__generateMockSleeperMatchup(
                matchupId=20220101, rosterId=202201, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220101, rosterId=202202, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220102, rosterId=202203, points=90.5
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220102, rosterId=202204, points=70.5
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220103, rosterId=202205, points=110
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220103, rosterId=202206, points=60
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220104, rosterId=202207, points=120
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220104, rosterId=202208, points=50
            ),
        ]

        mockSleeperMatchups2022_2 = [
            self.__generateMockSleeperMatchup(
                matchupId=20220201, rosterId=202201, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220201, rosterId=202202, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220202, rosterId=202203, points=90.5
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220202, rosterId=202204, points=70.5
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220203, rosterId=202205, points=110
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220203, rosterId=202206, points=60
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220204, rosterId=202207, points=120
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220204, rosterId=202208, points=50
            ),
        ]

        # playoffs
        mockSleeperMatchups2022_3 = [
            self.__generateMockSleeperMatchup(
                matchupId=20220301, rosterId=202202, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220301, rosterId=202203, points=90.5
            ),
        ]

        # championship
        mockSleeperMatchups2022_4 = [
            self.__generateMockSleeperMatchup(
                matchupId=20220401, rosterId=202201, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220401, rosterId=202202, points=99
            ),
        ]

        # create mock SleeperSportState objects
        mockSleeperSportState2022 = self.__generateMockSleeperSportState(
            season="2022", leg=5
        )

        # create mock SleeperPlayoffMatchup objects
        mockSleeperPlayoffMatchups2022 = [
            self.__generateMockSleeperPlayoffMatchup(
                round=1,
                team1RosterId=202202,
                team2RosterId=202203,
                winningRosterId=202202,
                p=0,
                matchupId=20220301,
            ),
            self.__generateMockSleeperPlayoffMatchup(
                round=2,
                team1RosterId=202201,
                team2RosterId=202202,
                winningRosterId=202201,
                p=1,
                matchupId=20220401,
            ),
        ]

        mockGetLeague.side_effect = [mockSleeperLeague2022]
        mockGetUsersInLeague.side_effect = [mockSleeperUsers2022]
        mockGetRosters.side_effect = [mockSleeperRosters2022]
        mockGetMatchupsForWeek.side_effect = [
            mockSleeperMatchups2022_1,
            mockSleeperMatchups2022_2,
            mockSleeperMatchups2022_3,
            mockSleeperMatchups2022_4,
        ]
        mockGetSportState.side_effect = [mockSleeperSportState2022]
        mockGetWinnersBracket.side_effect = [mockSleeperPlayoffMatchups2022]

        # create instance of SleeperLeagueLoader and call load_league method
        sleeper_league_loader = SleeperLeagueLoader(
            "123",
            [2022],
            ownerNamesAndAliases={
                "o1": ["User 1"],
                "o2": ["User 2"],
                "o3": ["User 3"],
                "o4": ["User 4"],
                "o5": ["User 5"],
                "o6": ["User 6"],
                "o7": ["User 7"],
                "o8": ["User 8"],
            },
        )
        league = sleeper_league_loader.loadLeague()

        # expected league

        owner1 = Owner(name="o1")
        owner2 = Owner(name="o2")
        owner3 = Owner(name="o3")
        owner4 = Owner(name="o4")
        owner5 = Owner(name="o5")
        owner6 = Owner(name="o6")
        owner7 = Owner(name="o7")
        owner8 = Owner(name="o8")

        division1_2022 = Division(name="d1_2022")
        division2_2022 = Division(name="d2_2022")

        team1_2022 = Team(ownerId=owner1.id, name="User 1")
        team2_2022 = Team(ownerId=owner2.id, name="User 2")
        team3_2022 = Team(ownerId=owner3.id, name="User 3")
        team4_2022 = Team(ownerId=owner4.id, name="User 4")
        team5_2022 = Team(ownerId=owner5.id, name="Team 5")
        team6_2022 = Team(ownerId=owner6.id, name="Team 6")
        team7_2022 = Team(ownerId=owner7.id, name="Team 7")
        team8_2022 = Team(ownerId=owner8.id, name="Team 8")

        expectedLeague = League(
            name="Test League 2022",
            owners=[owner1, owner2, owner3, owner4, owner5, owner6, owner7, owner8],
            years=[
                Year(
                    yearNumber=2022,
                    teams=[
                        team1_2022,
                        team2_2022,
                        team3_2022,
                        team4_2022,
                        team5_2022,
                        team6_2022,
                        team7_2022,
                        team8_2022,
                    ],
                    weeks=[
                        Week(
                            weekNumber=1,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2022.id,
                                    teamBId=team2_2022.id,
                                    teamAScore=100,
                                    teamBScore=100,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                                Matchup(
                                    teamAId=team3_2022.id,
                                    teamBId=team4_2022.id,
                                    teamAScore=90.5,
                                    teamBScore=70.5,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                                Matchup(
                                    teamAId=team5_2022.id,
                                    teamBId=team6_2022.id,
                                    teamAScore=110,
                                    teamBScore=60,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                                Matchup(
                                    teamAId=team7_2022.id,
                                    teamBId=team8_2022.id,
                                    teamAScore=120,
                                    teamBScore=50,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                            ],
                        ),
                        Week(
                            weekNumber=2,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2022.id,
                                    teamBId=team2_2022.id,
                                    teamAScore=100,
                                    teamBScore=100,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                                Matchup(
                                    teamAId=team3_2022.id,
                                    teamBId=team4_2022.id,
                                    teamAScore=90.5,
                                    teamBScore=70.5,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                                Matchup(
                                    teamAId=team5_2022.id,
                                    teamBId=team6_2022.id,
                                    teamAScore=110,
                                    teamBScore=60,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                                Matchup(
                                    teamAId=team7_2022.id,
                                    teamBId=team8_2022.id,
                                    teamAScore=120,
                                    teamBScore=50,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                            ],
                        ),
                        Week(
                            weekNumber=3,
                            matchups=[
                                Matchup(
                                    teamAId=team2_2022.id,
                                    teamBId=team3_2022.id,
                                    teamAScore=100,
                                    teamBScore=90.5,
                                    matchupType=MatchupType.PLAYOFF,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                )
                            ],
                        ),
                        Week(
                            weekNumber=4,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2022.id,
                                    teamBId=team2_2022.id,
                                    teamAScore=100,
                                    teamBScore=99,
                                    matchupType=MatchupType.CHAMPIONSHIP,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                )
                            ],
                        ),
                    ],
                    yearSettings=None,
                    divisions=[division1_2022, division2_2022],
                )
            ],
        )
        self.assertTrue(
            league.equals(expectedLeague, ignoreBaseIds=True, ignoreIds=True)
        )
        # check multiWeekMatchupIds
        for year in league.years:
            for week in year.weeks:
                for matchup in week.matchups:
                    self.assertIsNone(matchup.multiWeekMatchupId)

    @patch("sleeper.api.LeagueAPIClient.get_league")
    @patch("sleeper.api.LeagueAPIClient.get_users_in_league")
    @patch("sleeper.api.LeagueAPIClient.get_rosters")
    @patch("sleeper.api.LeagueAPIClient.get_matchups_for_week")
    @patch("sleeper.api.LeagueAPIClient.get_sport_state")
    @patch("sleeper.api.LeagueAPIClient.get_winners_bracket")
    def test_load_league_happyPath(
        self,
        mockGetWinnersBracket,
        mockGetSportState,
        mockGetMatchupsForWeek,
        mockGetRosters,
        mockGetUsersInLeague,
        mockGetLeague,
    ):
        # create mock SleeperLeague objects

        mockSleeperLeague2022 = Mock()
        mockSleeperLeague2022.season = "2022"
        mockSleeperLeague2022.status = SleeperSeasonStatus.COMPLETE
        mockSleeperLeague2022.playoff_matchups = []
        mockSleeperLeague2022.name = "Test League 2022"
        mockSleeperLeague2022.settings.playoff_week_start = 3
        mockSleeperLeague2022.settings.league_average_match = 0
        mockSleeperLeague2022.settings.divisions = 2
        mockSleeperLeague2022.settings.playoff_round_type_enum = (
            SleeperPlayoffRoundType.ONE_WEEK_PER_ROUND
        )
        mockSleeperLeague2022.metadata.division_1 = "d1_2022"
        mockSleeperLeague2022.metadata.division_2 = "d2_2022"

        mockSleeperLeague2023 = Mock()
        mockSleeperLeague2023.season = "2023"
        mockSleeperLeague2023.status = SleeperSeasonStatus.IN_SEASON
        mockSleeperLeague2023.playoff_matchups = []
        mockSleeperLeague2023.name = "Test League 2023"
        mockSleeperLeague2023.settings.playoff_week_start = 3
        mockSleeperLeague2023.settings.league_average_match = 0
        mockSleeperLeague2023.settings.divisions = 2
        mockSleeperLeague2023.settings.playoff_round_type_enum = (
            SleeperPlayoffRoundType.ONE_WEEK_PER_ROUND
        )
        mockSleeperLeague2023.metadata.division_1 = "d1_2023"
        mockSleeperLeague2023.metadata.division_2 = "d2_2023"

        # create mock SleeperUser objects
        mockSleeperUsers2022 = [
            self.__generateMockSleeperUser(displayName="User 1", userId="1"),
            self.__generateMockSleeperUser(displayName="User 2", userId="2"),
            self.__generateMockSleeperUser(displayName="User 3", userId="3"),
            self.__generateMockSleeperUser(displayName="User 4", userId="4"),
            self.__generateMockSleeperUser(
                displayName="User 5", userId="5", metadata={"team_name": "Team 5"}
            ),
            self.__generateMockSleeperUser(
                displayName="User 6", userId="6", metadata={"team_name": "Team 6"}
            ),
            self.__generateMockSleeperUser(
                displayName="User 7", userId="7", metadata={"team_name": "Team 7"}
            ),
            self.__generateMockSleeperUser(
                displayName="User 8", userId="8", metadata={"team_name": "Team 8"}
            ),
        ]

        mockSleeperUsers2023 = [
            self.__generateMockSleeperUser(displayName="User 1", userId="1"),
            self.__generateMockSleeperUser(displayName="User 2", userId="2"),
            self.__generateMockSleeperUser(displayName="User 3", userId="3"),
            self.__generateMockSleeperUser(displayName="User 4", userId="4"),
            self.__generateMockSleeperUser(
                displayName="User 5", userId="5", metadata={"team_name": "Team 5"}
            ),
            self.__generateMockSleeperUser(
                displayName="User 6", userId="6", metadata={"team_name": "Team 6"}
            ),
            self.__generateMockSleeperUser(
                displayName="User 7", userId="7", metadata={"team_name": "Team 7"}
            ),
            self.__generateMockSleeperUser(
                displayName="User 8", userId="8", metadata={"team_name": "Team 8"}
            ),
        ]

        # create mock SleeperRoster objects
        # roster id will be YYYY (year) RR (roster number)
        mockSleeperRosters2022 = [
            self.__generateMockSleeperRoster(ownerId="1", rosterId=202201, division=1),
            self.__generateMockSleeperRoster(ownerId="2", rosterId=202202, division=1),
            self.__generateMockSleeperRoster(ownerId="3", rosterId=202203, division=1),
            self.__generateMockSleeperRoster(ownerId="4", rosterId=202204, division=1),
            self.__generateMockSleeperRoster(ownerId="5", rosterId=202205, division=2),
            self.__generateMockSleeperRoster(ownerId="6", rosterId=202206, division=2),
            self.__generateMockSleeperRoster(ownerId="7", rosterId=202207, division=2),
            self.__generateMockSleeperRoster(ownerId="8", rosterId=202208, division=2),
        ]

        mockSleeperRosters2023 = [
            self.__generateMockSleeperRoster(ownerId="1", rosterId=202301, division=1),
            self.__generateMockSleeperRoster(ownerId="2", rosterId=202302, division=1),
            self.__generateMockSleeperRoster(ownerId="3", rosterId=202303, division=1),
            self.__generateMockSleeperRoster(ownerId="4", rosterId=202304, division=1),
            self.__generateMockSleeperRoster(ownerId="5", rosterId=202305, division=2),
            self.__generateMockSleeperRoster(ownerId="6", rosterId=202306, division=2),
            self.__generateMockSleeperRoster(ownerId="7", rosterId=202307, division=2),
            self.__generateMockSleeperRoster(ownerId="8", rosterId=202308, division=2),
        ]

        # create mock SleeperMatchup objects
        # matchup id will be YYYY (year) WW (week number) MM (matchup number)
        mockSleeperMatchups2022_1 = [
            self.__generateMockSleeperMatchup(
                matchupId=20220101, rosterId=202201, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220101, rosterId=202202, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220102, rosterId=202203, points=90.5
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220102, rosterId=202204, points=70.5
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220103, rosterId=202205, points=110
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220103, rosterId=202206, points=60
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220104, rosterId=202207, points=120
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220104, rosterId=202208, points=50
            ),
        ]

        mockSleeperMatchups2022_2 = [
            self.__generateMockSleeperMatchup(
                matchupId=20220201, rosterId=202201, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220201, rosterId=202202, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220202, rosterId=202203, points=90.5
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220202, rosterId=202204, points=70.5
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220203, rosterId=202205, points=110
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220203, rosterId=202206, points=60
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220204, rosterId=202207, points=120
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220204, rosterId=202208, points=50
            ),
        ]

        # playoffs
        mockSleeperMatchups2022_3 = [
            self.__generateMockSleeperMatchup(
                matchupId=20220301, rosterId=202202, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220301, rosterId=202203, points=90.5
            ),
        ]

        # championship
        mockSleeperMatchups2022_4 = [
            self.__generateMockSleeperMatchup(
                matchupId=20220401, rosterId=202201, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220401, rosterId=202202, points=99
            ),
        ]

        mockSleeperMatchups2023_1 = [
            self.__generateMockSleeperMatchup(
                matchupId=20230101, rosterId=202301, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230101, rosterId=202302, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230102, rosterId=202303, points=90.5
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230102, rosterId=202304, points=70.5
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230103, rosterId=202305, points=110
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230103, rosterId=202306, points=60
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230104, rosterId=202307, points=120
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230104, rosterId=202308, points=50
            ),
        ]

        mockSleeperMatchups2023_2 = [
            self.__generateMockSleeperMatchup(
                matchupId=20230201, rosterId=202301, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230201, rosterId=202302, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230202, rosterId=202303, points=90.5
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230202, rosterId=202304, points=70.5
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230203, rosterId=202305, points=110
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230203, rosterId=202306, points=60
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230204, rosterId=202307, points=120
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230204, rosterId=202308, points=50
            ),
        ]

        # playoffs
        mockSleeperMatchups2023_3 = [
            self.__generateMockSleeperMatchup(
                matchupId=20230301, rosterId=202302, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230301, rosterId=202303, points=90.5
            ),
        ]

        # championship
        mockSleeperMatchups2023_4 = [
            self.__generateMockSleeperMatchup(
                matchupId=20230401, rosterId=202301, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230401, rosterId=202302, points=99
            ),
        ]

        # create mock SleeperSportState objects
        mockSleeperSportState2022 = self.__generateMockSleeperSportState(
            season="2022", leg=5
        )
        mockSleeperSportState2023 = self.__generateMockSleeperSportState(
            season="2023", leg=5
        )

        # create mock SleeperPlayoffMatchup objects
        mockSleeperPlayoffMatchups2022 = [
            self.__generateMockSleeperPlayoffMatchup(
                round=1,
                team1RosterId=202202,
                team2RosterId=202203,
                winningRosterId=202202,
                p=0,
                matchupId=20220301,
            ),
            self.__generateMockSleeperPlayoffMatchup(
                round=2,
                team1RosterId=202201,
                team2RosterId=202202,
                winningRosterId=202201,
                p=1,
                matchupId=20220401,
            ),
        ]

        mockSleeperPlayoffMatchups2023 = [
            self.__generateMockSleeperPlayoffMatchup(
                round=1,
                team1RosterId=202302,
                team2RosterId=202303,
                winningRosterId=202302,
                p=0,
                matchupId=20230301,
            ),
            self.__generateMockSleeperPlayoffMatchup(
                round=2,
                team1RosterId=202301,
                team2RosterId=202302,
                winningRosterId=202301,
                p=1,
                matchupId=20230401,
            ),
        ]

        mockGetLeague.side_effect = [mockSleeperLeague2022, mockSleeperLeague2023]
        mockGetUsersInLeague.side_effect = [mockSleeperUsers2022, mockSleeperUsers2023]
        mockGetRosters.side_effect = [mockSleeperRosters2022, mockSleeperRosters2023]
        mockGetMatchupsForWeek.side_effect = [
            mockSleeperMatchups2022_1,
            mockSleeperMatchups2022_2,
            mockSleeperMatchups2022_3,
            mockSleeperMatchups2022_4,
            mockSleeperMatchups2023_1,
            mockSleeperMatchups2023_2,
            mockSleeperMatchups2023_3,
            mockSleeperMatchups2023_4,
        ]
        mockGetSportState.side_effect = [
            mockSleeperSportState2022,
            mockSleeperSportState2023,
        ]
        mockGetWinnersBracket.side_effect = [
            mockSleeperPlayoffMatchups2022,
            mockSleeperPlayoffMatchups2023,
        ]

        # create instance of SleeperLeagueLoader and call load_league method
        sleeper_league_loader = SleeperLeagueLoader(
            "123", [2022, 2023], leagueName="custom name"
        )
        league = sleeper_league_loader.loadLeague()

        self.assertEqual("custom name", league.name)

    @patch("sleeper.api.LeagueAPIClient.get_league")
    @patch("sleeper.api.LeagueAPIClient.get_users_in_league")
    @patch("sleeper.api.LeagueAPIClient.get_rosters")
    @patch("sleeper.api.LeagueAPIClient.get_matchups_for_week")
    @patch("sleeper.api.LeagueAPIClient.get_sport_state")
    @patch("sleeper.api.LeagueAPIClient.get_winners_bracket")
    def test_load_league_happyPath_playoffRoundType_twoWeekChampionshipRound(
        self,
        mockGetWinnersBracket,
        mockGetSportState,
        mockGetMatchupsForWeek,
        mockGetRosters,
        mockGetUsersInLeague,
        mockGetLeague,
    ):
        # create mock SleeperLeague objects
        mockSleeperLeague2022 = Mock()
        mockSleeperLeague2022.season = "2022"
        mockSleeperLeague2022.status = SleeperSeasonStatus.COMPLETE
        mockSleeperLeague2022.playoff_matchups = []
        mockSleeperLeague2022.name = "Test League 2022"
        mockSleeperLeague2022.settings.playoff_week_start = 3
        mockSleeperLeague2022.settings.league_average_match = 0
        mockSleeperLeague2022.settings.divisions = 2
        mockSleeperLeague2022.settings.playoff_round_type_enum = (
            SleeperPlayoffRoundType.TWO_WEEK_CHAMPIONSHIP_ROUND
        )
        mockSleeperLeague2022.metadata.division_1 = "d1_2022"
        mockSleeperLeague2022.metadata.division_2 = "d2_2022"

        # create mock SleeperUser objects
        mockSleeperUsers2022 = [
            self.__generateMockSleeperUser(displayName="User 1", userId="1"),
            self.__generateMockSleeperUser(displayName="User 2", userId="2"),
            self.__generateMockSleeperUser(displayName="User 3", userId="3"),
            self.__generateMockSleeperUser(displayName="User 4", userId="4"),
            self.__generateMockSleeperUser(
                displayName="User 5", userId="5", metadata={"team_name": "Team 5"}
            ),
            self.__generateMockSleeperUser(
                displayName="User 6", userId="6", metadata={"team_name": "Team 6"}
            ),
            self.__generateMockSleeperUser(
                displayName="User 7", userId="7", metadata={"team_name": "Team 7"}
            ),
            self.__generateMockSleeperUser(
                displayName="User 8", userId="8", metadata={"team_name": "Team 8"}
            ),
        ]

        # create mock SleeperRoster objects
        # roster id will be YYYY (year) RR (roster number)
        mockSleeperRosters2022 = [
            self.__generateMockSleeperRoster(ownerId="1", rosterId=202201, division=1),
            self.__generateMockSleeperRoster(ownerId="2", rosterId=202202, division=1),
            self.__generateMockSleeperRoster(ownerId="3", rosterId=202203, division=1),
            self.__generateMockSleeperRoster(ownerId="4", rosterId=202204, division=1),
            self.__generateMockSleeperRoster(ownerId="5", rosterId=202205, division=2),
            self.__generateMockSleeperRoster(ownerId="6", rosterId=202206, division=2),
            self.__generateMockSleeperRoster(ownerId="7", rosterId=202207, division=2),
            self.__generateMockSleeperRoster(ownerId="8", rosterId=202208, division=2),
        ]

        # create mock SleeperMatchup objects
        # matchup id will be YYYY (year) WW (week number) MM (matchup number)
        mockSleeperMatchups2022_1 = [
            self.__generateMockSleeperMatchup(
                matchupId=20220101, rosterId=202201, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220101, rosterId=202202, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220102, rosterId=202203, points=90.5
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220102, rosterId=202204, points=70.5
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220103, rosterId=202205, points=110
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220103, rosterId=202206, points=60
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220104, rosterId=202207, points=120
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220104, rosterId=202208, points=50
            ),
        ]

        mockSleeperMatchups2022_2 = [
            self.__generateMockSleeperMatchup(
                matchupId=20220201, rosterId=202201, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220201, rosterId=202202, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220202, rosterId=202203, points=90.5
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220202, rosterId=202204, points=70.5
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220203, rosterId=202205, points=110
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220203, rosterId=202206, points=60
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220204, rosterId=202207, points=120
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220204, rosterId=202208, points=50
            ),
        ]

        # playoffs
        mockSleeperMatchups2022_3 = [
            self.__generateMockSleeperMatchup(
                matchupId=20220301, rosterId=202202, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220301, rosterId=202203, points=90.5
            ),
        ]

        # championship 1
        mockSleeperMatchups2022_4 = [
            self.__generateMockSleeperMatchup(
                matchupId=20220401, rosterId=202201, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220401, rosterId=202202, points=99
            ),
        ]

        # championship 2
        mockSleeperMatchups2022_5 = [
            self.__generateMockSleeperMatchup(
                matchupId=20220501, rosterId=202201, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220501, rosterId=202202, points=99
            ),
        ]

        # create mock SleeperSportState objects
        mockSleeperSportState2022 = self.__generateMockSleeperSportState(
            season="2022", leg=6
        )

        # create mock SleeperPlayoffMatchup objects
        mockSleeperPlayoffMatchups2022 = [
            self.__generateMockSleeperPlayoffMatchup(
                round=1,
                team1RosterId=202202,
                team2RosterId=202203,
                winningRosterId=202202,
                p=0,
                matchupId=20220301,
            ),
            self.__generateMockSleeperPlayoffMatchup(
                round=2,
                team1RosterId=202201,
                team2RosterId=202202,
                winningRosterId=202201,
                p=1,
                matchupId=20220401,
            ),
            self.__generateMockSleeperPlayoffMatchup(
                round=2,
                team1RosterId=202201,
                team2RosterId=202202,
                winningRosterId=202201,
                p=1,
                matchupId=20220501,
            ),
        ]

        mockGetLeague.side_effect = [mockSleeperLeague2022]
        mockGetUsersInLeague.side_effect = [mockSleeperUsers2022]
        mockGetRosters.side_effect = [mockSleeperRosters2022]
        mockGetMatchupsForWeek.side_effect = [
            mockSleeperMatchups2022_1,
            mockSleeperMatchups2022_2,
            mockSleeperMatchups2022_3,
            mockSleeperMatchups2022_4,
            mockSleeperMatchups2022_5,
        ]
        mockGetSportState.side_effect = [mockSleeperSportState2022]
        mockGetWinnersBracket.side_effect = [mockSleeperPlayoffMatchups2022]

        # create instance of SleeperLeagueLoader and call load_league method
        sleeper_league_loader = SleeperLeagueLoader("123", [2022])
        league = sleeper_league_loader.loadLeague()

        # expected league

        owner1 = Owner(name="User 1")
        owner2 = Owner(name="User 2")
        owner3 = Owner(name="User 3")
        owner4 = Owner(name="User 4")
        owner5 = Owner(name="User 5")
        owner6 = Owner(name="User 6")
        owner7 = Owner(name="User 7")
        owner8 = Owner(name="User 8")

        division1_2022 = Division(name="d1_2022")
        division2_2022 = Division(name="d2_2022")

        team1_2022 = Team(
            ownerId=owner1.id, name="User 1", divisionId=division1_2022.id
        )
        team2_2022 = Team(
            ownerId=owner2.id, name="User 2", divisionId=division1_2022.id
        )
        team3_2022 = Team(
            ownerId=owner3.id, name="User 3", divisionId=division1_2022.id
        )
        team4_2022 = Team(
            ownerId=owner4.id, name="User 4", divisionId=division1_2022.id
        )
        team5_2022 = Team(
            ownerId=owner5.id, name="Team 5", divisionId=division2_2022.id
        )
        team6_2022 = Team(
            ownerId=owner6.id, name="Team 6", divisionId=division2_2022.id
        )
        team7_2022 = Team(
            ownerId=owner7.id, name="Team 7", divisionId=division2_2022.id
        )
        team8_2022 = Team(
            ownerId=owner8.id, name="Team 8", divisionId=division2_2022.id
        )

        expectedLeague = League(
            name="Test League 2022",
            owners=[owner1, owner2, owner3, owner4, owner5, owner6, owner7, owner8],
            years=[
                Year(
                    yearNumber=2022,
                    teams=[
                        team1_2022,
                        team2_2022,
                        team3_2022,
                        team4_2022,
                        team5_2022,
                        team6_2022,
                        team7_2022,
                        team8_2022,
                    ],
                    weeks=[
                        Week(
                            weekNumber=1,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2022.id,
                                    teamBId=team2_2022.id,
                                    teamAScore=100,
                                    teamBScore=100,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team3_2022.id,
                                    teamBId=team4_2022.id,
                                    teamAScore=90.5,
                                    teamBScore=70.5,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team5_2022.id,
                                    teamBId=team6_2022.id,
                                    teamAScore=110,
                                    teamBScore=60,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team7_2022.id,
                                    teamBId=team8_2022.id,
                                    teamAScore=120,
                                    teamBScore=50,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                            ],
                        ),
                        Week(
                            weekNumber=2,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2022.id,
                                    teamBId=team2_2022.id,
                                    teamAScore=100,
                                    teamBScore=100,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team3_2022.id,
                                    teamBId=team4_2022.id,
                                    teamAScore=90.5,
                                    teamBScore=70.5,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team5_2022.id,
                                    teamBId=team6_2022.id,
                                    teamAScore=110,
                                    teamBScore=60,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team7_2022.id,
                                    teamBId=team8_2022.id,
                                    teamAScore=120,
                                    teamBScore=50,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                            ],
                        ),
                        Week(
                            weekNumber=3,
                            matchups=[
                                Matchup(
                                    teamAId=team2_2022.id,
                                    teamBId=team3_2022.id,
                                    teamAScore=100,
                                    teamBScore=90.5,
                                    matchupType=MatchupType.PLAYOFF,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                )
                            ],
                        ),
                        Week(
                            weekNumber=4,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2022.id,
                                    teamBId=team2_2022.id,
                                    teamAScore=100,
                                    teamBScore=99,
                                    matchupType=MatchupType.CHAMPIONSHIP,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                )
                            ],
                        ),
                        Week(
                            weekNumber=5,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2022.id,
                                    teamBId=team2_2022.id,
                                    teamAScore=100,
                                    teamBScore=99,
                                    matchupType=MatchupType.CHAMPIONSHIP,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                )
                            ],
                        ),
                    ],
                    yearSettings=None,
                    divisions=[division1_2022, division2_2022],
                )
            ],
        )
        self.assertTrue(
            league.equals(expectedLeague, ignoreBaseIds=True, ignoreIds=True)
        )
        # check multiWeekMatchupIds
        for year in league.years:
            for week in year.weeks[:3]:
                for matchup in week.matchups:
                    self.assertIsNone(matchup.multiWeekMatchupId)
            for week in year.weeks[3:]:
                for matchup in week.matchups:
                    self.assertEqual(
                        f"{matchup.teamAId}{matchup.teamBId}",
                        matchup.multiWeekMatchupId,
                    )

    @patch("sleeper.api.LeagueAPIClient.get_league")
    @patch("sleeper.api.LeagueAPIClient.get_users_in_league")
    @patch("sleeper.api.LeagueAPIClient.get_rosters")
    @patch("sleeper.api.LeagueAPIClient.get_matchups_for_week")
    @patch("sleeper.api.LeagueAPIClient.get_sport_state")
    @patch("sleeper.api.LeagueAPIClient.get_winners_bracket")
    def test_load_league_happyPath_playoffRoundType_twoWeeksPerRound(
        self,
        mockGetWinnersBracket,
        mockGetSportState,
        mockGetMatchupsForWeek,
        mockGetRosters,
        mockGetUsersInLeague,
        mockGetLeague,
    ):
        # create mock SleeperLeague objects
        mockSleeperLeague2022 = Mock()
        mockSleeperLeague2022.season = "2022"
        mockSleeperLeague2022.status = SleeperSeasonStatus.COMPLETE
        mockSleeperLeague2022.playoff_matchups = []
        mockSleeperLeague2022.name = "Test League 2022"
        mockSleeperLeague2022.settings.playoff_week_start = 3
        mockSleeperLeague2022.settings.league_average_match = 0
        mockSleeperLeague2022.settings.divisions = 2
        mockSleeperLeague2022.settings.playoff_round_type_enum = (
            SleeperPlayoffRoundType.TWO_WEEKS_PER_ROUND
        )
        mockSleeperLeague2022.metadata.division_1 = "d1_2022"
        mockSleeperLeague2022.metadata.division_2 = "d2_2022"

        # create mock SleeperUser objects
        mockSleeperUsers2022 = [
            self.__generateMockSleeperUser(displayName="User 1", userId="1"),
            self.__generateMockSleeperUser(displayName="User 2", userId="2"),
            self.__generateMockSleeperUser(displayName="User 3", userId="3"),
            self.__generateMockSleeperUser(displayName="User 4", userId="4"),
            self.__generateMockSleeperUser(
                displayName="User 5", userId="5", metadata={"team_name": "Team 5"}
            ),
            self.__generateMockSleeperUser(
                displayName="User 6", userId="6", metadata={"team_name": "Team 6"}
            ),
            self.__generateMockSleeperUser(
                displayName="User 7", userId="7", metadata={"team_name": "Team 7"}
            ),
            self.__generateMockSleeperUser(
                displayName="User 8", userId="8", metadata={"team_name": "Team 8"}
            ),
        ]

        # create mock SleeperRoster objects
        # roster id will be YYYY (year) RR (roster number)
        mockSleeperRosters2022 = [
            self.__generateMockSleeperRoster(ownerId="1", rosterId=202201, division=1),
            self.__generateMockSleeperRoster(ownerId="2", rosterId=202202, division=1),
            self.__generateMockSleeperRoster(ownerId="3", rosterId=202203, division=1),
            self.__generateMockSleeperRoster(ownerId="4", rosterId=202204, division=1),
            self.__generateMockSleeperRoster(ownerId="5", rosterId=202205, division=2),
            self.__generateMockSleeperRoster(ownerId="6", rosterId=202206, division=2),
            self.__generateMockSleeperRoster(ownerId="7", rosterId=202207, division=2),
            self.__generateMockSleeperRoster(ownerId="8", rosterId=202208, division=2),
        ]

        # create mock SleeperMatchup objects
        # matchup id will be YYYY (year) WW (week number) MM (matchup number)
        mockSleeperMatchups2022_1 = [
            self.__generateMockSleeperMatchup(
                matchupId=20220101, rosterId=202201, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220101, rosterId=202202, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220102, rosterId=202203, points=90.5
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220102, rosterId=202204, points=70.5
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220103, rosterId=202205, points=110
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220103, rosterId=202206, points=60
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220104, rosterId=202207, points=120
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220104, rosterId=202208, points=50
            ),
        ]

        mockSleeperMatchups2022_2 = [
            self.__generateMockSleeperMatchup(
                matchupId=20220201, rosterId=202201, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220201, rosterId=202202, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220202, rosterId=202203, points=90.5
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220202, rosterId=202204, points=70.5
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220203, rosterId=202205, points=110
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220203, rosterId=202206, points=60
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220204, rosterId=202207, points=120
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220204, rosterId=202208, points=50
            ),
        ]

        # playoffs 1
        mockSleeperMatchups2022_3 = [
            self.__generateMockSleeperMatchup(
                matchupId=20220301, rosterId=202202, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220301, rosterId=202203, points=90.5
            ),
        ]

        # playoffs 2
        mockSleeperMatchups2022_4 = [
            self.__generateMockSleeperMatchup(
                matchupId=20220401, rosterId=202202, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220401, rosterId=202203, points=90.5
            ),
        ]

        # championship 1
        mockSleeperMatchups2022_5 = [
            self.__generateMockSleeperMatchup(
                matchupId=20220501, rosterId=202201, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220501, rosterId=202202, points=99
            ),
        ]

        # championship 2
        mockSleeperMatchups2022_6 = [
            self.__generateMockSleeperMatchup(
                matchupId=20220601, rosterId=202201, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220601, rosterId=202202, points=99
            ),
        ]

        # create mock SleeperSportState objects
        mockSleeperSportState2022 = self.__generateMockSleeperSportState(
            season="2022", leg=7
        )

        # create mock SleeperPlayoffMatchup objects
        mockSleeperPlayoffMatchups2022 = [
            self.__generateMockSleeperPlayoffMatchup(
                round=1,
                team1RosterId=202202,
                team2RosterId=202203,
                winningRosterId=202202,
                p=0,
                matchupId=20220301,
            ),
            self.__generateMockSleeperPlayoffMatchup(
                round=1,
                team1RosterId=202202,
                team2RosterId=202203,
                winningRosterId=202202,
                p=0,
                matchupId=20220401,
            ),
            self.__generateMockSleeperPlayoffMatchup(
                round=2,
                team1RosterId=202201,
                team2RosterId=202202,
                winningRosterId=202201,
                p=1,
                matchupId=20220501,
            ),
            self.__generateMockSleeperPlayoffMatchup(
                round=2,
                team1RosterId=202201,
                team2RosterId=202202,
                winningRosterId=202201,
                p=1,
                matchupId=20220601,
            ),
        ]

        mockGetLeague.side_effect = [mockSleeperLeague2022]
        mockGetUsersInLeague.side_effect = [mockSleeperUsers2022]
        mockGetRosters.side_effect = [mockSleeperRosters2022]
        mockGetMatchupsForWeek.side_effect = [
            mockSleeperMatchups2022_1,
            mockSleeperMatchups2022_2,
            mockSleeperMatchups2022_3,
            mockSleeperMatchups2022_4,
            mockSleeperMatchups2022_5,
            mockSleeperMatchups2022_6,
        ]
        mockGetSportState.side_effect = [mockSleeperSportState2022]
        mockGetWinnersBracket.side_effect = [mockSleeperPlayoffMatchups2022]

        # create instance of SleeperLeagueLoader and call load_league method
        sleeper_league_loader = SleeperLeagueLoader("123", [2022])
        league = sleeper_league_loader.loadLeague()

        # expected league

        owner1 = Owner(name="User 1")
        owner2 = Owner(name="User 2")
        owner3 = Owner(name="User 3")
        owner4 = Owner(name="User 4")
        owner5 = Owner(name="User 5")
        owner6 = Owner(name="User 6")
        owner7 = Owner(name="User 7")
        owner8 = Owner(name="User 8")

        division1_2022 = Division(name="d1_2022")
        division2_2022 = Division(name="d2_2022")

        team1_2022 = Team(
            ownerId=owner1.id, name="User 1", divisionId=division1_2022.id
        )
        team2_2022 = Team(
            ownerId=owner2.id, name="User 2", divisionId=division1_2022.id
        )
        team3_2022 = Team(
            ownerId=owner3.id, name="User 3", divisionId=division1_2022.id
        )
        team4_2022 = Team(
            ownerId=owner4.id, name="User 4", divisionId=division1_2022.id
        )
        team5_2022 = Team(
            ownerId=owner5.id, name="Team 5", divisionId=division2_2022.id
        )
        team6_2022 = Team(
            ownerId=owner6.id, name="Team 6", divisionId=division2_2022.id
        )
        team7_2022 = Team(
            ownerId=owner7.id, name="Team 7", divisionId=division2_2022.id
        )
        team8_2022 = Team(
            ownerId=owner8.id, name="Team 8", divisionId=division2_2022.id
        )

        expectedLeague = League(
            name="Test League 2022",
            owners=[owner1, owner2, owner3, owner4, owner5, owner6, owner7, owner8],
            years=[
                Year(
                    yearNumber=2022,
                    teams=[
                        team1_2022,
                        team2_2022,
                        team3_2022,
                        team4_2022,
                        team5_2022,
                        team6_2022,
                        team7_2022,
                        team8_2022,
                    ],
                    weeks=[
                        Week(
                            weekNumber=1,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2022.id,
                                    teamBId=team2_2022.id,
                                    teamAScore=100,
                                    teamBScore=100,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team3_2022.id,
                                    teamBId=team4_2022.id,
                                    teamAScore=90.5,
                                    teamBScore=70.5,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team5_2022.id,
                                    teamBId=team6_2022.id,
                                    teamAScore=110,
                                    teamBScore=60,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team7_2022.id,
                                    teamBId=team8_2022.id,
                                    teamAScore=120,
                                    teamBScore=50,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                            ],
                        ),
                        Week(
                            weekNumber=2,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2022.id,
                                    teamBId=team2_2022.id,
                                    teamAScore=100,
                                    teamBScore=100,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team3_2022.id,
                                    teamBId=team4_2022.id,
                                    teamAScore=90.5,
                                    teamBScore=70.5,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team5_2022.id,
                                    teamBId=team6_2022.id,
                                    teamAScore=110,
                                    teamBScore=60,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                                Matchup(
                                    teamAId=team7_2022.id,
                                    teamBId=team8_2022.id,
                                    teamAScore=120,
                                    teamBScore=50,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                ),
                            ],
                        ),
                        Week(
                            weekNumber=3,
                            matchups=[
                                Matchup(
                                    teamAId=team2_2022.id,
                                    teamBId=team3_2022.id,
                                    teamAScore=100,
                                    teamBScore=90.5,
                                    matchupType=MatchupType.PLAYOFF,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                )
                            ],
                        ),
                        Week(
                            weekNumber=4,
                            matchups=[
                                Matchup(
                                    teamAId=team2_2022.id,
                                    teamBId=team3_2022.id,
                                    teamAScore=100,
                                    teamBScore=90.5,
                                    matchupType=MatchupType.PLAYOFF,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                )
                            ],
                        ),
                        Week(
                            weekNumber=5,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2022.id,
                                    teamBId=team2_2022.id,
                                    teamAScore=100,
                                    teamBScore=99,
                                    matchupType=MatchupType.CHAMPIONSHIP,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                )
                            ],
                        ),
                        Week(
                            weekNumber=6,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2022.id,
                                    teamBId=team2_2022.id,
                                    teamAScore=100,
                                    teamBScore=99,
                                    matchupType=MatchupType.CHAMPIONSHIP,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                )
                            ],
                        ),
                    ],
                    yearSettings=None,
                    divisions=[division1_2022, division2_2022],
                )
            ],
        )
        self.assertTrue(
            league.equals(expectedLeague, ignoreBaseIds=True, ignoreIds=True)
        )
        # check multiWeekMatchupIds
        for year in league.years:
            for week in year.weeks[:2]:
                for matchup in week.matchups:
                    self.assertIsNone(matchup.multiWeekMatchupId)
            for week in year.weeks[2:]:
                for matchup in week.matchups:
                    self.assertEqual(
                        f"{matchup.teamAId}{matchup.teamBId}",
                        matchup.multiWeekMatchupId,
                    )

    @patch("sleeper.api.LeagueAPIClient.get_league")
    @patch("sleeper.api.LeagueAPIClient.get_users_in_league")
    @patch("sleeper.api.LeagueAPIClient.get_rosters")
    @patch("sleeper.api.LeagueAPIClient.get_matchups_for_week")
    @patch("sleeper.api.LeagueAPIClient.get_sport_state")
    @patch("sleeper.api.LeagueAPIClient.get_winners_bracket")
    def test_load_league_happyPath_playoffRoundType_unsupported_raisesException(
        self,
        mockGetWinnersBracket,
        mockGetSportState,
        mockGetMatchupsForWeek,
        mockGetRosters,
        mockGetUsersInLeague,
        mockGetLeague,
    ):
        # create mock SleeperLeague objects
        mockSleeperLeague2022 = Mock()
        mockSleeperLeague2022.season = "2022"
        mockSleeperLeague2022.status = SleeperSeasonStatus.COMPLETE
        mockSleeperLeague2022.name = "Test League 2022"
        mockSleeperLeague2022.settings.playoff_week_start = 1
        mockSleeperLeague2022.settings.divisions = 2
        mockSleeperLeague2022.settings.playoff_round_type_enum = None
        mockSleeperLeague2022.metadata.division_1 = "d1_2022"
        mockSleeperLeague2022.metadata.division_2 = "d2_2022"

        # create mock SleeperUser objects
        mockSleeperUsers2022 = [
            self.__generateMockSleeperUser(displayName="User 1", userId="1"),
            self.__generateMockSleeperUser(displayName="User 2", userId="2"),
        ]

        # create mock SleeperRoster objects
        # roster id will be YYYY (year) RR (roster number)
        mockSleeperRosters2022 = [
            self.__generateMockSleeperRoster(ownerId="1", rosterId=202201, division=1),
            self.__generateMockSleeperRoster(ownerId="2", rosterId=202202, division=2),
        ]

        # create mock SleeperMatchup objects
        # matchup id will be YYYY (year) WW (week number) MM (matchup number)
        mockSleeperMatchups2022_1 = [
            self.__generateMockSleeperMatchup(
                matchupId=20220101, rosterId=202201, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220101, rosterId=202202, points=100
            ),
        ]
        # create mock SleeperSportState objects
        mockSleeperSportState2022 = self.__generateMockSleeperSportState(
            season="2022", leg=None
        )

        # create mock SleeperPlayoffMatchup objects
        mockSleeperPlayoffMatchups2022 = [
            self.__generateMockSleeperPlayoffMatchup(
                round=1,
                team1RosterId=202202,
                team2RosterId=202203,
                winningRosterId=202202,
                p=0,
                matchupId=20220301,
            )
        ]

        mockGetLeague.side_effect = [mockSleeperLeague2022]
        mockGetUsersInLeague.side_effect = [mockSleeperUsers2022]
        mockGetRosters.side_effect = [mockSleeperRosters2022]
        mockGetMatchupsForWeek.side_effect = [mockSleeperMatchups2022_1]
        mockGetSportState.side_effect = [mockSleeperSportState2022]
        mockGetWinnersBracket.side_effect = [mockSleeperPlayoffMatchups2022]

        with self.assertRaises(LeagueLoaderException) as context:
            sleeper_league_loader = SleeperLeagueLoader("123", [2022])
            sleeper_league_loader.loadLeague()
        self.assertEqual(
            "PlayoffRoundType 'None' is not supported.", str(context.exception)
        )

    @patch("sleeper.api.LeagueAPIClient.get_league")
    @patch("sleeper.api.LeagueAPIClient.get_users_in_league")
    @patch("sleeper.api.LeagueAPIClient.get_rosters")
    @patch("sleeper.api.LeagueAPIClient.get_matchups_for_week")
    @patch("sleeper.api.LeagueAPIClient.get_sport_state")
    @patch("sleeper.api.LeagueAPIClient.get_winners_bracket")
    def test_load_league_happyPath_leagueMedianGames(
        self,
        mockGetWinnersBracket,
        mockGetSportState,
        mockGetMatchupsForWeek,
        mockGetRosters,
        mockGetUsersInLeague,
        mockGetLeague,
    ):
        # create mock SleeperLeague objects
        mockSleeperLeague2022 = Mock()
        mockSleeperLeague2022.season = "2022"
        mockSleeperLeague2022.status = SleeperSeasonStatus.COMPLETE
        mockSleeperLeague2022.playoff_matchups = []
        mockSleeperLeague2022.name = "Test League 2022"
        mockSleeperLeague2022.settings.playoff_week_start = 3
        mockSleeperLeague2022.settings.league_average_match = 1
        mockSleeperLeague2022.settings.divisions = 2
        mockSleeperLeague2022.settings.playoff_round_type_enum = (
            SleeperPlayoffRoundType.ONE_WEEK_PER_ROUND
        )
        mockSleeperLeague2022.metadata.division_1 = "d1_2022"
        mockSleeperLeague2022.metadata.division_2 = "d2_2022"

        mockSleeperLeague2023 = Mock()
        mockSleeperLeague2023.season = "2023"
        mockSleeperLeague2023.status = SleeperSeasonStatus.IN_SEASON
        mockSleeperLeague2023.playoff_matchups = []
        mockSleeperLeague2023.name = "Test League 2023"
        mockSleeperLeague2023.settings.playoff_week_start = 3
        mockSleeperLeague2023.settings.league_average_match = 0
        mockSleeperLeague2023.settings.divisions = 2
        mockSleeperLeague2023.settings.playoff_round_type_enum = (
            SleeperPlayoffRoundType.ONE_WEEK_PER_ROUND
        )
        mockSleeperLeague2023.metadata.division_1 = "d1_2023"
        mockSleeperLeague2023.metadata.division_2 = "d2_2023"

        # create mock SleeperUser objects
        mockSleeperUsers2022 = [
            self.__generateMockSleeperUser(displayName="User 1", userId="1"),
            self.__generateMockSleeperUser(displayName="User 2", userId="2"),
            self.__generateMockSleeperUser(displayName="User 3", userId="3"),
            self.__generateMockSleeperUser(displayName="User 4", userId="4"),
            self.__generateMockSleeperUser(
                displayName="User 5", userId="5", metadata={"team_name": "Team 5"}
            ),
            self.__generateMockSleeperUser(
                displayName="User 6", userId="6", metadata={"team_name": "Team 6"}
            ),
            self.__generateMockSleeperUser(
                displayName="User 7", userId="7", metadata={"team_name": "Team 7"}
            ),
            self.__generateMockSleeperUser(
                displayName="User 8", userId="8", metadata={"team_name": "Team 8"}
            ),
        ]

        mockSleeperUsers2023 = [
            self.__generateMockSleeperUser(displayName="User 1", userId="1"),
            self.__generateMockSleeperUser(displayName="User 2", userId="2"),
            self.__generateMockSleeperUser(displayName="User 3", userId="3"),
            self.__generateMockSleeperUser(displayName="User 4", userId="4"),
            self.__generateMockSleeperUser(
                displayName="User 5", userId="5", metadata={"team_name": "Team 5"}
            ),
            self.__generateMockSleeperUser(
                displayName="User 6", userId="6", metadata={"team_name": "Team 6"}
            ),
            self.__generateMockSleeperUser(
                displayName="User 7", userId="7", metadata={"team_name": "Team 7"}
            ),
            self.__generateMockSleeperUser(
                displayName="User 8", userId="8", metadata={"team_name": "Team 8"}
            ),
        ]

        # create mock SleeperRoster objects
        # roster id will be YYYY (year) RR (roster number)
        mockSleeperRosters2022 = [
            self.__generateMockSleeperRoster(ownerId="1", rosterId=202201, division=1),
            self.__generateMockSleeperRoster(ownerId="2", rosterId=202202, division=1),
            self.__generateMockSleeperRoster(ownerId="3", rosterId=202203, division=1),
            self.__generateMockSleeperRoster(ownerId="4", rosterId=202204, division=1),
            self.__generateMockSleeperRoster(ownerId="5", rosterId=202205, division=2),
            self.__generateMockSleeperRoster(ownerId="6", rosterId=202206, division=2),
            self.__generateMockSleeperRoster(ownerId="7", rosterId=202207, division=2),
            self.__generateMockSleeperRoster(ownerId="8", rosterId=202208, division=2),
        ]

        mockSleeperRosters2023 = [
            self.__generateMockSleeperRoster(ownerId="1", rosterId=202301, division=1),
            self.__generateMockSleeperRoster(ownerId="2", rosterId=202302, division=1),
            self.__generateMockSleeperRoster(ownerId="3", rosterId=202303, division=1),
            self.__generateMockSleeperRoster(ownerId="4", rosterId=202304, division=1),
            self.__generateMockSleeperRoster(ownerId="5", rosterId=202305, division=2),
            self.__generateMockSleeperRoster(ownerId="6", rosterId=202306, division=2),
            self.__generateMockSleeperRoster(ownerId="7", rosterId=202307, division=2),
            self.__generateMockSleeperRoster(ownerId="8", rosterId=202308, division=2),
        ]

        # create mock SleeperMatchup objects
        # matchup id will be YYYY (year) WW (week number) MM (matchup number)
        mockSleeperMatchups2022_1 = [
            self.__generateMockSleeperMatchup(
                matchupId=20220101, rosterId=202201, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220101, rosterId=202202, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220102, rosterId=202203, points=90.5
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220102, rosterId=202204, points=70.5
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220103, rosterId=202205, points=110
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220103, rosterId=202206, points=60
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220104, rosterId=202207, points=120
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220104, rosterId=202208, points=50
            ),
        ]

        mockSleeperMatchups2022_2 = [
            self.__generateMockSleeperMatchup(
                matchupId=20220201, rosterId=202201, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220201, rosterId=202202, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220202, rosterId=202203, points=90.5
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220202, rosterId=202204, points=70.5
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220203, rosterId=202205, points=110
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220203, rosterId=202206, points=60
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220204, rosterId=202207, points=120
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220204, rosterId=202208, points=50
            ),
        ]

        # playoffs
        mockSleeperMatchups2022_3 = [
            self.__generateMockSleeperMatchup(
                matchupId=20220301, rosterId=202202, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220301, rosterId=202203, points=90.5
            ),
        ]

        # championship
        mockSleeperMatchups2022_4 = [
            self.__generateMockSleeperMatchup(
                matchupId=20220401, rosterId=202201, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20220401, rosterId=202202, points=99
            ),
        ]

        mockSleeperMatchups2023_1 = [
            self.__generateMockSleeperMatchup(
                matchupId=20230101, rosterId=202301, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230101, rosterId=202302, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230102, rosterId=202303, points=90.5
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230102, rosterId=202304, points=70.5
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230103, rosterId=202305, points=110
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230103, rosterId=202306, points=60
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230104, rosterId=202307, points=120
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230104, rosterId=202308, points=50
            ),
        ]

        mockSleeperMatchups2023_2 = [
            self.__generateMockSleeperMatchup(
                matchupId=20230201, rosterId=202301, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230201, rosterId=202302, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230202, rosterId=202303, points=90.5
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230202, rosterId=202304, points=70.5
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230203, rosterId=202305, points=110
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230203, rosterId=202306, points=60
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230204, rosterId=202307, points=120
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230204, rosterId=202308, points=50
            ),
        ]

        # playoffs
        mockSleeperMatchups2023_3 = [
            self.__generateMockSleeperMatchup(
                matchupId=20230301, rosterId=202302, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230301, rosterId=202303, points=90.5
            ),
        ]

        # championship
        mockSleeperMatchups2023_4 = [
            self.__generateMockSleeperMatchup(
                matchupId=20230401, rosterId=202301, points=100
            ),
            self.__generateMockSleeperMatchup(
                matchupId=20230401, rosterId=202302, points=99
            ),
        ]

        # create mock SleeperSportState objects
        mockSleeperSportState2022 = self.__generateMockSleeperSportState(
            season="2022", leg=5
        )
        mockSleeperSportState2023 = self.__generateMockSleeperSportState(
            season="2023", leg=5
        )

        # create mock SleeperPlayoffMatchup objects
        mockSleeperPlayoffMatchups2022 = [
            self.__generateMockSleeperPlayoffMatchup(
                round=1,
                team1RosterId=202202,
                team2RosterId=202203,
                winningRosterId=202202,
                p=0,
                matchupId=20220301,
            ),
            self.__generateMockSleeperPlayoffMatchup(
                round=2,
                team1RosterId=202201,
                team2RosterId=202202,
                winningRosterId=202201,
                p=1,
                matchupId=20220401,
            ),
        ]

        mockSleeperPlayoffMatchups2023 = [
            self.__generateMockSleeperPlayoffMatchup(
                round=1,
                team1RosterId=202302,
                team2RosterId=202303,
                winningRosterId=202302,
                p=0,
                matchupId=20230301,
            ),
            self.__generateMockSleeperPlayoffMatchup(
                round=2,
                team1RosterId=202301,
                team2RosterId=202302,
                winningRosterId=202301,
                p=1,
                matchupId=20230401,
            ),
        ]

        mockGetLeague.side_effect = [mockSleeperLeague2022, mockSleeperLeague2023]
        mockGetUsersInLeague.side_effect = [mockSleeperUsers2022, mockSleeperUsers2023]
        mockGetRosters.side_effect = [mockSleeperRosters2022, mockSleeperRosters2023]
        mockGetMatchupsForWeek.side_effect = [
            mockSleeperMatchups2022_1,
            mockSleeperMatchups2022_2,
            mockSleeperMatchups2022_3,
            mockSleeperMatchups2022_4,
            mockSleeperMatchups2023_1,
            mockSleeperMatchups2023_2,
            mockSleeperMatchups2023_3,
            mockSleeperMatchups2023_4,
        ]
        mockGetSportState.side_effect = [
            mockSleeperSportState2022,
            mockSleeperSportState2023,
        ]
        mockGetWinnersBracket.side_effect = [
            mockSleeperPlayoffMatchups2022,
            mockSleeperPlayoffMatchups2023,
        ]

        # create instance of SleeperLeagueLoader and call load_league method
        sleeper_league_loader = SleeperLeagueLoader("123", [2022, 2023])
        league = sleeper_league_loader.loadLeague()

        # expected league

        owner1 = Owner(name="User 1")
        owner2 = Owner(name="User 2")
        owner3 = Owner(name="User 3")
        owner4 = Owner(name="User 4")
        owner5 = Owner(name="User 5")
        owner6 = Owner(name="User 6")
        owner7 = Owner(name="User 7")
        owner8 = Owner(name="User 8")

        division1_2022 = Division(name="d1_2022")
        division2_2022 = Division(name="d2_2022")

        division1_2023 = Division(name="d1_2023")
        division2_2023 = Division(name="d2_2023")

        team1_2022 = Team(
            ownerId=owner1.id, name="User 1", divisionId=division1_2022.id
        )
        team2_2022 = Team(
            ownerId=owner2.id, name="User 2", divisionId=division1_2022.id
        )
        team3_2022 = Team(
            ownerId=owner3.id, name="User 3", divisionId=division1_2022.id
        )
        team4_2022 = Team(
            ownerId=owner4.id, name="User 4", divisionId=division1_2022.id
        )
        team5_2022 = Team(
            ownerId=owner5.id, name="Team 5", divisionId=division2_2022.id
        )
        team6_2022 = Team(
            ownerId=owner6.id, name="Team 6", divisionId=division2_2022.id
        )
        team7_2022 = Team(
            ownerId=owner7.id, name="Team 7", divisionId=division2_2022.id
        )
        team8_2022 = Team(
            ownerId=owner8.id, name="Team 8", divisionId=division2_2022.id
        )

        team1_2023 = Team(
            ownerId=owner1.id, name="User 1", divisionId=division1_2023.id
        )
        team2_2023 = Team(
            ownerId=owner2.id, name="User 2", divisionId=division1_2023.id
        )
        team3_2023 = Team(
            ownerId=owner3.id, name="User 3", divisionId=division1_2023.id
        )
        team4_2023 = Team(
            ownerId=owner4.id, name="User 4", divisionId=division1_2023.id
        )
        team5_2023 = Team(
            ownerId=owner5.id, name="Team 5", divisionId=division2_2023.id
        )
        team6_2023 = Team(
            ownerId=owner6.id, name="Team 6", divisionId=division2_2023.id
        )
        team7_2023 = Team(
            ownerId=owner7.id, name="Team 7", divisionId=division2_2023.id
        )
        team8_2023 = Team(
            ownerId=owner8.id, name="Team 8", divisionId=division2_2023.id
        )

        expectedLeague = League(
            name="Test League 2023",
            owners=[owner1, owner2, owner3, owner4, owner5, owner6, owner7, owner8],
            years=[
                Year(
                    yearNumber=2022,
                    teams=[
                        team1_2022,
                        team2_2022,
                        team3_2022,
                        team4_2022,
                        team5_2022,
                        team6_2022,
                        team7_2022,
                        team8_2022,
                    ],
                    weeks=[
                        Week(
                            weekNumber=1,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2022.id,
                                    teamBId=team2_2022.id,
                                    teamAScore=100,
                                    teamBScore=100,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                                Matchup(
                                    teamAId=team3_2022.id,
                                    teamBId=team4_2022.id,
                                    teamAScore=90.5,
                                    teamBScore=70.5,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                                Matchup(
                                    teamAId=team5_2022.id,
                                    teamBId=team6_2022.id,
                                    teamAScore=110,
                                    teamBScore=60,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                                Matchup(
                                    teamAId=team7_2022.id,
                                    teamBId=team8_2022.id,
                                    teamAScore=120,
                                    teamBScore=50,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                            ],
                        ),
                        Week(
                            weekNumber=2,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2022.id,
                                    teamBId=team2_2022.id,
                                    teamAScore=100,
                                    teamBScore=100,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                                Matchup(
                                    teamAId=team3_2022.id,
                                    teamBId=team4_2022.id,
                                    teamAScore=90.5,
                                    teamBScore=70.5,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                                Matchup(
                                    teamAId=team5_2022.id,
                                    teamBId=team6_2022.id,
                                    teamAScore=110,
                                    teamBScore=60,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                                Matchup(
                                    teamAId=team7_2022.id,
                                    teamBId=team8_2022.id,
                                    teamAScore=120,
                                    teamBScore=50,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                            ],
                        ),
                        Week(
                            weekNumber=3,
                            matchups=[
                                Matchup(
                                    teamAId=team2_2022.id,
                                    teamBId=team3_2022.id,
                                    teamAScore=100,
                                    teamBScore=90.5,
                                    matchupType=MatchupType.PLAYOFF,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                )
                            ],
                        ),
                        Week(
                            weekNumber=4,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2022.id,
                                    teamBId=team2_2022.id,
                                    teamAScore=100,
                                    teamBScore=99,
                                    matchupType=MatchupType.CHAMPIONSHIP,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                )
                            ],
                        ),
                    ],
                    yearSettings=YearSettings(leagueMedianGames=True),
                    divisions=[division1_2022, division2_2022],
                ),
                Year(
                    yearNumber=2023,
                    teams=[
                        team1_2023,
                        team2_2023,
                        team3_2023,
                        team4_2023,
                        team5_2023,
                        team6_2023,
                        team7_2023,
                        team8_2023,
                    ],
                    weeks=[
                        Week(
                            weekNumber=1,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2023.id,
                                    teamBId=team2_2023.id,
                                    teamAScore=100,
                                    teamBScore=100,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                                Matchup(
                                    teamAId=team3_2023.id,
                                    teamBId=team4_2023.id,
                                    teamAScore=90.5,
                                    teamBScore=70.5,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                                Matchup(
                                    teamAId=team5_2023.id,
                                    teamBId=team6_2023.id,
                                    teamAScore=110,
                                    teamBScore=60,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                                Matchup(
                                    teamAId=team7_2023.id,
                                    teamBId=team8_2023.id,
                                    teamAScore=120,
                                    teamBScore=50,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                            ],
                        ),
                        Week(
                            weekNumber=2,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2023.id,
                                    teamBId=team2_2023.id,
                                    teamAScore=100,
                                    teamBScore=100,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                                Matchup(
                                    teamAId=team3_2023.id,
                                    teamBId=team4_2023.id,
                                    teamAScore=90.5,
                                    teamBScore=70.5,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                                Matchup(
                                    teamAId=team5_2023.id,
                                    teamBId=team6_2023.id,
                                    teamAScore=110,
                                    teamBScore=60,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                                Matchup(
                                    teamAId=team7_2023.id,
                                    teamBId=team8_2023.id,
                                    teamAScore=120,
                                    teamBScore=50,
                                    matchupType=MatchupType.REGULAR_SEASON,
                                    teamAHasTiebreaker=False,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                ),
                            ],
                        ),
                        Week(
                            weekNumber=3,
                            matchups=[
                                Matchup(
                                    teamAId=team2_2023.id,
                                    teamBId=team3_2023.id,
                                    teamAScore=100,
                                    teamBScore=90.5,
                                    matchupType=MatchupType.PLAYOFF,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                )
                            ],
                        ),
                        Week(
                            weekNumber=4,
                            matchups=[
                                Matchup(
                                    teamAId=team1_2023.id,
                                    teamBId=team2_2023.id,
                                    teamAScore=100,
                                    teamBScore=99,
                                    matchupType=MatchupType.CHAMPIONSHIP,
                                    teamAHasTiebreaker=True,
                                    teamBHasTiebreaker=False,
                                    multiWeekMatchupId=None,
                                )
                            ],
                        ),
                    ],
                    yearSettings=None,
                    divisions=[division1_2023, division2_2023],
                ),
            ],
        )
        self.assertTrue(
            league.equals(expectedLeague, ignoreBaseIds=True, ignoreIds=True)
        )
        # check multiWeekMatchupIds
        for year in league.years:
            for week in year.weeks:
                for matchup in week.matchups:
                    self.assertIsNone(matchup.multiWeekMatchupId)
