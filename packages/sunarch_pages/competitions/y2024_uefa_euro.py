# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Competition: UEFA Euro 2024"""

# library
from __future__ import annotations
from datetime import datetime, timedelta
from dataclasses import dataclass, field, InitVar
from enum import Enum

# requirements
from lektor.db import Page

# package
from common.page import set_field

URL_PATH: str = '/culture/sports/soccer/competitions/uefa-euro-2024/'

KEY_FOR_LOCATIONS: str = 'locations'
KEY_FOR_GROUPS: str = 'groups'
KEY_FOR_TEAMS: str = 'teams'
KEY_FOR_MATCHES: str = 'matches'
KEY_FOR_PERIODS: str = 'periods'

QUALIFIER_RANKING_HOST: int = -1


@dataclass
class Group:
    """Group"""

    name: str
    teams: list[str]


GROUPS_DATA = (
    ('A', ['GER', 'SCO', 'HUN', 'SUI']),
    ('B', ['ESP', 'CRO', 'ITA', 'ALB']),
    ('C', ['DEN', 'ENG', 'SRB', 'SLO']),
    ('D', ['AUT', 'NED', 'FRA', 'POL']),
    ('E', ['BEL', 'ROM', 'SVK', 'UKR']),
    ('F', ['CZE', 'GEO', 'TUR', 'POR']),
)

GROUPS: dict[str, Group] = {}

for group_data in GROUPS_DATA:
    GROUPS[group_data[0]] = Group(*group_data)


@dataclass
class Team:
    """Team"""
    # pylint: disable=too-many-instance-attributes

    abbrev: str
    name: str
    qualifier_ranking: int

    group: str | None = None
    group_matches: list[Match] = field(default_factory=list)
    group_matches_won: int = 0
    group_matches_drawn: int = 0
    group_matches_lost: int = 0
    group_goals_for: int = 0
    group_goals_against: int = 0

    further_matches: list[Match] = field(default_factory=list)

    def reset(self):
        """Reset counters"""
        self.group = None
        self.group_matches = []
        self.group_matches_won = 0
        self.group_matches_drawn = 0
        self.group_matches_lost = 0
        self.group_goals_for = 0
        self.group_goals_against = 0
        self.further_matches = []

    @property
    def group_points(self) -> int:
        """Group matches played"""
        return self.group_matches_won * 3 + self.group_matches_drawn * 1

    @property
    def group_matches_played(self) -> int:
        """Group matches played"""
        return self.group_matches_won + self.group_matches_drawn + self.group_matches_lost

    @property
    def group_goal_difference(self) -> int:
        """Group matches: Difference of goals scored and goals received"""
        return self.group_goals_for - self.group_goals_against

    def __lt__(self, other: Team) -> bool:
        """Less-than comparison function, also use for sorted()"""
        # pylint: disable=too-many-return-statements, too-many-branches

        if self.group_points < other.group_points:
            return True
        if self.group_points > other.group_points:
            return False

        # If two or more teams are equal on points on completion of the group matches,
        #     the following tie-breaking criteria are applied:

        game_against_each_other: dict[str, dict[str, int]] = {
            self.abbrev: {
                'points': 0,
                'goals_for': 0,
            },
            other.abbrev: {
                'points': 0,
                'goals_for': 0,
            },
        }
        for match_item in self.group_matches:
            if {match_item.home, match_item.away} == {self.abbrev, other.abbrev}:
                game_against_each_other[match_item.home]['goals_for'] = match_item.home_score
                game_against_each_other[match_item.away]['goals_for'] = match_item.away_score
                if match_item.home_score < match_item.away_score:
                    game_against_each_other[match_item.home]['points'] = 0
                    game_against_each_other[match_item.away]['points'] = 3
                elif match_item.home_score > match_item.away_score:
                    game_against_each_other[match_item.home]['points'] = 3
                    game_against_each_other[match_item.away]['points'] = 0
                else:  # equal score, match drawn
                    game_against_each_other[match_item.home]['points'] = 1
                    game_against_each_other[match_item.away]['points'] = 1

        # 1) Higher number of points obtained in the matches played between the teams in question
        if game_against_each_other[self.abbrev]['points'] < \
                game_against_each_other[other.abbrev]['points']:
            return True
        if game_against_each_other[self.abbrev]['points'] > \
                game_against_each_other[other.abbrev]['points']:
            return False

        # 2) Superior goal difference
        #        resulting from the matches played between the teams in question

        # 3) Higher number of goals scored in the matches played between the teams in question
        if game_against_each_other[self.abbrev]['goals_for'] < \
                game_against_each_other[other.abbrev]['goals_for']:
            return True
        if game_against_each_other[self.abbrev]['goals_for'] > \
                game_against_each_other[other.abbrev]['goals_for']:
            return False

        # 4) If, after having applied criteria 1 to 3, teams still have an equal ranking,
        #     criteria 1 to 3 are reapplied exclusively to the matches between the teams
        #     who are still level to determine their final rankings.
        # If this procedure does not lead to a decision, criteria 5 to 9 will apply

        # 4/1)

        # 4/2)

        # 4/3)

        # 5) Superior goal difference in all group matches
        if self.group_goal_difference < other.group_goal_difference:
            return True
        if self.group_goal_difference > other.group_goal_difference:
            return False

        # 6) Higher number of goals scored in all group matches
        if self.group_goals_for < other.group_goals_for:
            return True
        if self.group_goals_for > other.group_goals_for:
            return False

        # 7) If on the last round of the group stage,
        #     two teams who are facing each other are tied in points,
        #     goal difference and goals scored then they drew their match
        #     their ranking is determined by a penalty shoot-out.
        # (This criterion is not used if more than two teams had the same number of points.)

        # 8) Lower disciplinary points total in all group matches
        #    (1 point for a single yellow card,
        #     3 points for a red card
        #         regardless whether it was a direct red card or two yellow cards,
        #     4 points for a yellow card followed by a direct red card)

        # 9) Higher position in the European Qualifiers overall ranking,
        #     unless the comparison involves hosts Germany,
        #     in which case a drawing of lots will take place.
        if QUALIFIER_RANKING_HOST not in {self.qualifier_ranking, other.qualifier_ranking}:
            if self.qualifier_ranking < other.qualifier_ranking:
                return False  # reversed!
            if self.qualifier_ranking > other.qualifier_ranking:
                return True  # reversed!

        # fallback
        return self.abbrev < other.abbrev

    def __eq__(self, other: Team) -> bool:
        """Equals comparison function, also use for sorted()"""

        return self.abbrev == other.abbrev


TEAMS_DATA = (
    ('GER', 'Germany', QUALIFIER_RANKING_HOST),
    ('SCO', 'Scotland', 13),
    ('HUN', 'Hungary', 6),
    ('SUI', 'Switzerland', 20),
    ('ESP', 'Spain', 3),
    ('CRO', 'Croatia', 14),
    ('ITA', 'Italy', 18),
    ('ALB', 'Albania', 10),
    ('DEN', 'Denmark', 9),
    ('ENG', 'England', 5),
    ('SRB', 'Serbia', 19),
    ('SLO', 'Slovenia', 15),
    ('AUT', 'Austria', 11),
    ('NED', 'Netherlands', 12),
    ('FRA', 'France', 1),
    ('POL', 'Poland', 26),
    ('BEL', 'Belgium', 4),
    ('ROM', 'Romania', 8),
    ('SVK', 'Slovakia', 16),
    ('UKR', 'Ukraine', 21),
    ('CZE', 'Czech Republic', 17),
    ('GEO', 'Georgia', 34),
    ('TUR', 'Turkey', 7),
    ('POR', 'Portugal', 1),
)

TEAMS: dict[str, Team] = {}

for team_data in TEAMS_DATA:
    TEAMS[team_data[0]] = Team(*team_data)


@dataclass
class Location:
    """Location"""
    city: str
    stadium: str
    capacity: int
    index: int


LOCATIONS_DATA = (
    ('Berlin', 'Olympiastadion', 74461),
    ('Leipzig', 'Red Bull Arena', 42959),
    ('Hamburg', 'Volksparkstadion', 52245),
    ('Dortmund', 'Westfalenstadion', 65849),
    ('Gelsenkirchen', 'Arena AufSchalke', 54740),
    ('Düsseldorf', 'Merkur Spiel-Arena', 51031),
    ('Köln', 'RheinEnergieStadion', 49827),
    ('Frankfurt', 'Deutsche Bank Park', 54697),
    ('Stuttgart', 'MHPArena', 54906),
    ('München', 'Allianz Arena', 70076),
)

LOCATIONS: dict[str, Location] = {}

for i_location, location_data in enumerate(LOCATIONS_DATA):
    LOCATIONS[location_data[0]] = Location(*location_data, index=i_location)


@dataclass
class Broadcaster:
    """Broadcaster"""
    name: str
    name_short: str


class Broadcasters(Enum):
    """All broadcasters"""
    M4_SPORT = Broadcaster('M4 Sport', 'M4 Sport')
    DUNA_WORLD = Broadcaster('Duna World', 'Duna W.')
    M4_SPORT_PLUSZ = Broadcaster('M4 Sport+', 'M4 Sport+')


@dataclass
class Match:
    """Match"""
    # pylint: disable=too-many-instance-attributes

    number: int
    home: str
    home_score: int | None
    away: str
    away_score: int | None
    date_time: datetime
    location: Location
    broadcaster: Broadcaster

    number_sorted: int = 0

    def __post_init__(self):
        self.number_sorted = self.number

    @property
    def date(self) -> str:
        """Matches played"""
        return self.date_time.strftime('%Y-%m-%d')

    @property
    def time(self) -> str:
        """Matches played"""
        return self.date_time.strftime('%H:%M')

    def __lt__(self, other) -> bool:
        """Less-than comparison function, also use for sorted()"""

        if self.date_time == other.date_time:
            return self.number < other.number

        return self.date_time < other.date_time

    def __eq__(self, other) -> bool:
        """Equals comparison function, also use for sorted()"""

        return self.number == other.number


MATCHES: list[Match] = [
    # Group Round 1 ====================================================
    Match(1,
          'GER', 5, 'SCO', 1,
          datetime.fromisoformat('2024-06-14 21:00'),
          LOCATIONS['München'],
          Broadcasters.M4_SPORT.value),
    Match(2,
          'HUN', 1, 'SUI', 3,
          datetime.fromisoformat('2024-06-15 15:00'),
          LOCATIONS['Köln'],
          Broadcasters.M4_SPORT.value),
    Match(3,
          'ESP', 3, 'CRO', 0,
          datetime.fromisoformat('2024-06-15 18:00'),
          LOCATIONS['Berlin'],
          Broadcasters.M4_SPORT.value),
    Match(4,
          'ITA', 2, 'ALB', 1,
          datetime.fromisoformat('2024-06-15 21:00'),
          LOCATIONS['Dortmund'],
          Broadcasters.M4_SPORT.value),
    Match(5,
          'SRB', 0, 'ENG', 1,
          datetime.fromisoformat('2024-06-16 21:00'),
          LOCATIONS['Gelsenkirchen'],
          Broadcasters.M4_SPORT.value),
    Match(6,
          'SLO', 1, 'DEN', 1,
          datetime.fromisoformat('2024-06-16 18:00'),
          LOCATIONS['Stuttgart'],
          Broadcasters.M4_SPORT.value),
    Match(7,
          'POL', 1, 'NED', 2,
          datetime.fromisoformat('2024-06-16 15:00'),
          LOCATIONS['Hamburg'],
          Broadcasters.M4_SPORT.value),
    Match(8,
          'AUT', 0, 'FRA', 1,
          datetime.fromisoformat('2024-06-17 21:00'),
          LOCATIONS['Düsseldorf'],
          Broadcasters.M4_SPORT.value),
    Match(9,
          'BEL', 0, 'SVK', 1,
          datetime.fromisoformat('2024-06-17 18:00'),
          LOCATIONS['Frankfurt'],
          Broadcasters.M4_SPORT.value),
    Match(10,
          'ROM', 3, 'UKR', 0,
          datetime.fromisoformat('2024-06-17 15:00'),
          LOCATIONS['München'],
          Broadcasters.M4_SPORT.value),
    Match(11,
          'TUR', 3, 'GEO', 1,
          datetime.fromisoformat('2024-06-18 18:00'),
          LOCATIONS['Dortmund'],
          Broadcasters.M4_SPORT.value),
    Match(12,
          'POR', 2, 'CZE', 1,
          datetime.fromisoformat('2024-06-18 21:00'),
          LOCATIONS['Leipzig'],
          Broadcasters.M4_SPORT.value),
    # Group Round 2 ====================================================
    Match(13,
          'SCO', None, 'SUI', None,
          datetime.fromisoformat('2024-06-19 21:00'),
          LOCATIONS['Köln'],
          Broadcasters.M4_SPORT.value),
    Match(14,
          'GER', None, 'HUN', None,
          datetime.fromisoformat('2024-06-19 18:00'),
          LOCATIONS['Stuttgart'],
          Broadcasters.M4_SPORT.value),
    Match(15,
          'CRO', None, 'ALB', None,
          datetime.fromisoformat('2024-06-19 15:00'),
          LOCATIONS['Hamburg'],
          Broadcasters.M4_SPORT.value),
    Match(16,
          'ITA', None, 'ESP', None,
          datetime.fromisoformat('2024-06-20 21:00'),
          LOCATIONS['Gelsenkirchen'],
          Broadcasters.M4_SPORT.value),
    Match(17,
          'DEN', None, 'ENG', None,
          datetime.fromisoformat('2024-06-20 18:00'),
          LOCATIONS['Frankfurt'],
          Broadcasters.M4_SPORT.value),
    Match(18,
          'SLO', None, 'SRB', None,
          datetime.fromisoformat('2024-06-20 15:00'),
          LOCATIONS['München'],
          Broadcasters.M4_SPORT.value),
    Match(19,
          'POL', None, 'AUT', None,
          datetime.fromisoformat('2024-06-21 18:00'),
          LOCATIONS['Berlin'],
          Broadcasters.M4_SPORT.value),
    Match(20,
          'FRA', None, 'NED', None,
          datetime.fromisoformat('2024-06-21 21:00'),
          LOCATIONS['Leipzig'],
          Broadcasters.M4_SPORT.value),
    Match(21,
          'SVK', None, 'UKR', None,
          datetime.fromisoformat('2024-06-21 15:00'),
          LOCATIONS['Düsseldorf'],
          Broadcasters.M4_SPORT.value),
    Match(22,
          'BEL', None, 'ROM', None,
          datetime.fromisoformat('2024-06-22 21:00'),
          LOCATIONS['Köln'],
          Broadcasters.M4_SPORT.value),
    Match(23,
          'TUR', None, 'POR', None,
          datetime.fromisoformat('2024-06-22 18:00'),
          LOCATIONS['Dortmund'],
          Broadcasters.M4_SPORT.value),
    Match(24,
          'CZE', None, 'GEO', None,
          datetime.fromisoformat('2024-06-22 15:00'),
          LOCATIONS['Hamburg'],
          Broadcasters.M4_SPORT.value),
    # Group Round 3 ====================================================
    Match(25,
          'SUI', None, 'GER', None,
          datetime.fromisoformat('2024-06-23 21:00'),
          LOCATIONS['Frankfurt'],
          Broadcasters.M4_SPORT_PLUSZ.value),
    Match(26,
          'SCO', None, 'HUN', None,
          datetime.fromisoformat('2024-06-23 21:00'),
          LOCATIONS['Stuttgart'],
          Broadcasters.M4_SPORT.value),
    Match(27,
          'ESP', None, 'ALB', None,
          datetime.fromisoformat('2024-06-24 21:00'),
          LOCATIONS['Düsseldorf'],
          Broadcasters.DUNA_WORLD.value),
    Match(28,
          'ITA', None, 'CRO', None,
          datetime.fromisoformat('2024-06-24 21:00'),
          LOCATIONS['Leipzig'],
          Broadcasters.M4_SPORT.value),
    Match(29,
          'ENG', None, 'SLO', None,
          datetime.fromisoformat('2024-06-25 21:00'),
          LOCATIONS['Köln'],
          Broadcasters.M4_SPORT.value),
    Match(30,
          'DEN', None, 'SRB', None,
          datetime.fromisoformat('2024-06-25 21:00'),
          LOCATIONS['München'],
          Broadcasters.DUNA_WORLD.value),
    Match(31,
          'AUT', None, 'NED', None,
          datetime.fromisoformat('2024-06-25 18:00'),
          LOCATIONS['Berlin'],
          Broadcasters.DUNA_WORLD.value),
    Match(32,
          'POL', None, 'FRA', None,
          datetime.fromisoformat('2024-06-25 18:00'),
          LOCATIONS['Dortmund'],
          Broadcasters.M4_SPORT.value),
    Match(33,
          'SVK', None, 'ROM', None,
          datetime.fromisoformat('2024-06-26 18:00'),
          LOCATIONS['Frankfurt'],
          Broadcasters.DUNA_WORLD.value),
    Match(34,
          'BEL', None, 'UKR', None,
          datetime.fromisoformat('2024-06-26 18:00'),
          LOCATIONS['Stuttgart'],
          Broadcasters.M4_SPORT.value),
    Match(35,
          'POR', None, 'GEO', None,
          datetime.fromisoformat('2024-06-26 21:00'),
          LOCATIONS['Gelsenkirchen'],
          Broadcasters.M4_SPORT.value),
    Match(36,
          'CZE', None, 'TUR', None,
          datetime.fromisoformat('2024-06-26 21:00'),
          LOCATIONS['Hamburg'],
          Broadcasters.DUNA_WORLD.value),
    # Round of 16 ======================================================
    Match(37,
          'G:A1', None, 'G:C2', None,
          datetime.fromisoformat('2024-06-29 21:00'),
          LOCATIONS['Dortmund'],
          Broadcasters.M4_SPORT.value),
    Match(38,
          'G:A2', None, 'G:B2', None,
          datetime.fromisoformat('2024-06-29 18:00'),
          LOCATIONS['Berlin'],
          Broadcasters.M4_SPORT.value),
    Match(39,
          'G:B1', None, 'S:A3/D3/E3/F3', None,
          datetime.fromisoformat('2024-06-30 21:00'),
          LOCATIONS['Köln'],
          Broadcasters.M4_SPORT.value),
    Match(40,
          'G:C1', None, 'S:D2/E2/F2', None,
          datetime.fromisoformat('2024-06-30 18:00'),
          LOCATIONS['Gelsenkirchen'],
          Broadcasters.M4_SPORT.value),
    Match(41,
          'G:F1', None, 'S:A3/B3/C3', None,
          datetime.fromisoformat('2024-07-01 21:00'),
          LOCATIONS['Frankfurt'],
          Broadcasters.M4_SPORT.value),
    Match(42,
          'G:D2', None, 'G:E2', None,
          datetime.fromisoformat('2024-07-01 18:00'),
          LOCATIONS['Düsseldorf'],
          Broadcasters.M4_SPORT.value),
    Match(43,
          'G:E1', None, 'S:A3/B3/C3/D3', None,
          datetime.fromisoformat('2024-07-02 18:00'),
          LOCATIONS['München'],
          Broadcasters.M4_SPORT.value),
    Match(44,
          'G:D1', None, 'G:F2', None,
          datetime.fromisoformat('2024-07-02 21:00'),
          LOCATIONS['Leipzig'],
          Broadcasters.M4_SPORT.value),
    # Quarter-Finals ===================================================
    Match(45,
          'W:39', None, 'W:37', None,
          datetime.fromisoformat('2024-07-05 21:00'),
          LOCATIONS['Stuttgart'],
          Broadcasters.M4_SPORT.value),
    Match(46,
          'W:41', None, 'W:42', None,
          datetime.fromisoformat('2024-07-05 21:00'),
          LOCATIONS['Hamburg'],
          Broadcasters.M4_SPORT.value),
    Match(47,
          'W:43', None, 'W:44', None,
          datetime.fromisoformat('2024-07-06 21:00'),
          LOCATIONS['Berlin'],
          Broadcasters.M4_SPORT.value),
    Match(48,
          'W:40', None, 'W:38', None,
          datetime.fromisoformat('2024-07-06 21:00'),
          LOCATIONS['Düsseldorf'],
          Broadcasters.M4_SPORT.value),
    # Semi-Finals ======================================================
    Match(49,
          'W:45', None, 'W:46', None,
          datetime.fromisoformat('2024-07-09 21:00'),
          LOCATIONS['München'],
          Broadcasters.M4_SPORT.value),
    Match(50,
          'W:47', None, 'W:48', None,
          datetime.fromisoformat('2024-07-10 21:00'),
          LOCATIONS['Dortmund'],
          Broadcasters.M4_SPORT.value),
    # Final ============================================================
    Match(51,
          'W:49', None, 'W:50', None,
          datetime.fromisoformat('2024-07-14 21:00'),
          LOCATIONS['Berlin'],
          Broadcasters.M4_SPORT.value),
]
MATCHES = sorted(MATCHES)
for i_match, match in enumerate(MATCHES):
    match.number_sorted = i_match + 1


@dataclass
class PeriodDay:
    """Period day"""
    date_time: datetime

    @property
    def date(self) -> str:
        """Matches played"""
        return self.date_time.strftime('%Y-%m-%d')

    @property
    def display_date(self) -> str:
        """Matches played"""
        return self.date_time.strftime('%m.%d.')

    @property
    def display_day(self) -> str:
        """Matches played"""
        return self.date_time.strftime('%a')


@dataclass
class Period:
    """Period"""

    first_match: int | None
    first_day: InitVar[str]

    last_match: int | None
    last_day: InitVar[str]

    name: str
    css_class: str | None

    contained_rest_days: int = 0
    name_short: str = ""
    day_list: list[PeriodDay] = field(default_factory=list)

    def __post_init__(self, first_day: str, last_day: str) -> None:
        """Post-init hook"""
        self.name_short = self.name

        date_format: str = '%Y-%m-%d'
        first_day_date = datetime.strptime(first_day, date_format)
        last_day_date = datetime.strptime(last_day, date_format)
        current_date: datetime = first_day_date
        while True:
            if current_date > last_day_date:
                break
            self.day_list.append(PeriodDay(current_date))
            current_date += timedelta(days=1)

    def reinit_name_short(self, name_short: str) -> Period:
        """Set short name and return self"""
        self.name_short = name_short
        return self

    @property
    def days(self) -> int:
        """How many days is the period"""
        return len(self.day_list)

    @property
    def rowspan(self) -> int:
        """How many rows to span in a table"""
        return (self.last_match - self.first_match + 1) + self.days - self.contained_rest_days


@dataclass
class PeriodDefinitions:
    """Period"""

    big: list[Period]
    small: list[Period]


PERIODS = PeriodDefinitions(
    [
        Period(1, '2024-06-14', 36, '2024-06-26', 'Csoportkörök', None),
        Period(None, '2024-06-27', None, '2024-06-28', 'Pihenőnap', None),
        Period(37, '2024-06-29', 51, '2024-07-14', 'Egyenes kieséses szakasz', None,
               contained_rest_days=7),
    ],
    [
        Period(1, '2024-06-14', 12, '2024-06-18', '1. csoportkör', None)
        .reinit_name_short('1. kör'),

        Period(13, '2024-06-19', 24, '2024-06-22', '2. csoportkör', None)
        .reinit_name_short('2. kör'),

        Period(25, '2024-06-23', 36, '2024-06-26', '3. csoportkör', None)
        .reinit_name_short('3. kör'),

        Period(None, '2024-06-27', None, '2024-06-28', 'Pihenőnap', None),
        Period(37, '2024-06-29', 44, '2024-07-02', 'Nyolcaddöntők', 'RoundOf16'),
        Period(None, '2024-07-03', None, '2024-07-04', 'Pihenőnap', None),
        Period(45, '2024-07-05', 48, '2024-07-06', 'Negyeddöntő', 'QuarterFinal'),
        Period(None, '2024-07-07', None, '2024-07-08', 'Pihenőnap', None),
        Period(49, '2024-07-09', 50, '2024-07-10', 'Elődöntő', 'SemiFinal'),
        Period(None, '2024-07-11', None, '2024-07-13', 'Pihenőnap', None),
        Period(51, '2024-07-14', 51, '2024-07-14', 'Döntő', 'Final'),
    ],
)


def setup(page: Page, debug: int = 0) -> None:
    """Set up competition page"""

    print('PAGE SETUP START : Competition - UEFA Euro 2024')

    for team in TEAMS.values():
        team.reset()
        for group in GROUPS.values():
            if team.abbrev in group.teams:
                team.group = group.name

    for match_item in MATCHES:

        if debug > 0:
            print('  - match', match_item.number)

        if (match_item.home_score is None) or (match_item.away_score is None):
            continue

        if PERIODS.big[0].first_match <= match_item.number <= PERIODS.big[0].last_match:
            TEAMS[match_item.home].group_matches.append(match_item)
            TEAMS[match_item.away].group_matches.append(match_item)
        else:
            TEAMS[match_item.home].further_matches.append(match_item)
            TEAMS[match_item.away].further_matches.append(match_item)

        TEAMS[match_item.home].group_goals_for += match_item.home_score
        TEAMS[match_item.home].group_goals_against += match_item.away_score

        TEAMS[match_item.away].group_goals_for += match_item.away_score
        TEAMS[match_item.away].group_goals_against += match_item.home_score

        if match_item.home_score > match_item.away_score:
            TEAMS[match_item.home].group_matches_won += 1
            TEAMS[match_item.away].group_matches_lost += 1
        elif match_item.home_score < match_item.away_score:
            TEAMS[match_item.away].group_matches_won += 1
            TEAMS[match_item.home].group_matches_lost += 1
        else:  # scores equal => undecided
            TEAMS[match_item.home].group_matches_drawn += 1
            TEAMS[match_item.away].group_matches_drawn += 1

    for group in GROUPS.values():
        teams: list[Team] = [TEAMS[abbrev] for abbrev in group.teams]
        group.teams = [team.abbrev for team in sorted(teams, reverse=True)]

    set_field(page, KEY_FOR_LOCATIONS, LOCATIONS)
    set_field(page, KEY_FOR_GROUPS, GROUPS)
    set_field(page, KEY_FOR_TEAMS, TEAMS)
    set_field(page, KEY_FOR_MATCHES, MATCHES)
    set_field(page, KEY_FOR_PERIODS, PERIODS)

    print('PAGE SETUP END   : Competition - UEFA Euro 2024')
