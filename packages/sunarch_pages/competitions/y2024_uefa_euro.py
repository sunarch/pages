# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Competition: UEFA Euro 2024"""

# library
from __future__ import annotations
from datetime import datetime, timedelta
from dataclasses import dataclass, field, InitVar
import os

# requirements
from lektor.db import Page, Pad

# package
from common.page import set_field

URL_PATH: str = '/culture/sports/soccer/competitions/uefa-euro-2024/'

KEY_FOR_LOCATIONS: str = 'locations'
KEY_FOR_GROUPS: str = 'groups'
KEY_FOR_TEAMS: str = 'teams'
KEY_FOR_MATCHES: str = 'matches'
KEY_FOR_PERIODS: str = 'periods'

QUALIFIER_RANKING_HOST: int = -1

COMPETITION_START: datetime = datetime.fromisoformat('2024-06-14 00:00')
FORMAT_ICAL_DATE_UTC: str = '%Y%m%dT%H%M00Z'
FORMAT_ICAL_DATE: str = '%Y%m%dT%H%M00'


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


BROADCASTERS_DATA = (
    ('M4 Sport', 'M4 Sport'),
    ('Duna World', 'Duna W.'),
    ('M4 Sport+', 'M4 Sport+'),
)

BROADCASTERS: dict[str, Broadcaster] = {}

for broadcaster_data in BROADCASTERS_DATA:
    BROADCASTERS[broadcaster_data[0]] = Broadcaster(*broadcaster_data)


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

    @property
    def ical_dtstamp(self) -> str:
        """iCal: DateTime for Start"""
        return (self.date_time + timedelta(hours=-2)).strftime(FORMAT_ICAL_DATE_UTC)

    @property
    def ical_dtstart(self) -> str:
        """iCal: DateTime for Start"""
        return self.date_time.strftime(FORMAT_ICAL_DATE)

    @property
    def ical_dtend(self) -> str:
        """iCal: DateTime for End"""
        return (self.date_time + timedelta(hours=2)).strftime(FORMAT_ICAL_DATE)

    @property
    def ical_summary(self) -> str:
        """iCal: Summary"""

        period_display: str = ''
        if self.number <= PERIODS.big[0].last_match:
            period_display: str = f'{TEAMS[self.home].group}'
        else:
            for period in PERIODS.small:
                if period.name_ical is not None:
                    if period.first_match <= self.number <= period.last_match:
                        period_display: str = period.name_ical

        teams: str = f'{self.home} - {self.away}'
        identifier: str = f'(EB/{self.number}:{period_display})'
        broadcaster: str = f'({self.broadcaster.name_short})'

        return f'{teams} {identifier} {broadcaster}'

    @property
    def ical_location(self) -> str:
        """iCal: Location"""

        return f'{self.location.stadium}, {self.location.city}, Germany'

    def __lt__(self, other) -> bool:
        """Less-than comparison function, also use for sorted()"""

        if self.date_time == other.date_time:
            return self.number < other.number

        return self.date_time < other.date_time

    def __eq__(self, other) -> bool:
        """Equals comparison function, also use for sorted()"""

        return self.number == other.number


def load_matches(pad: Pad) -> list[Match]:
    """Load matches"""

    matches: list[Match] = []

    for match_id, match in pad.databags.lookup('uefa_euro_2024.matches').items():
        number: int = int(match_id[1:])
        home_score: int | None = None if match['home_score'] == 'None' else int(match['home_score'])
        away_score: int | None = None if match['away_score'] == 'None' else int(match['away_score'])

        matches.append(
            Match(
                number,
                match['home'], home_score, match['away'], away_score,
                datetime.fromisoformat(match['date_time']),
                LOCATIONS[match['location']],
                BROADCASTERS[match['broadcaster']]
            )
        )

    matches = sorted(matches)

    for i_match, match in enumerate(matches):
        match.number_sorted = i_match + 1

    return matches


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
    # pylint: disable=too-many-instance-attributes

    first_match: int | None
    first_day: InitVar[str]

    last_match: int | None
    last_day: InitVar[str]

    name: str
    css_class: str | None

    name_ical: str | None = None
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
        Period(37, '2024-06-29', 44, '2024-07-02', 'Nyolcaddöntők', 'RoundOf16', name_ical='8d'),
        Period(None, '2024-07-03', None, '2024-07-04', 'Pihenőnap', None),
        Period(45, '2024-07-05', 48, '2024-07-06', 'Negyeddöntő', 'QuarterFinal', name_ical='4d'),
        Period(None, '2024-07-07', None, '2024-07-08', 'Pihenőnap', None),
        Period(49, '2024-07-09', 50, '2024-07-10', 'Elődöntő', 'SemiFinal', name_ical='2d'),
        Period(None, '2024-07-11', None, '2024-07-13', 'Pihenőnap', None),
        Period(51, '2024-07-14', 51, '2024-07-14', 'Döntő', 'Final', name_ical='1d'),
    ],
)


def write_ical(matches: list[Match]) -> None:
    """Write an iCal calandar"""

    filename: str = 'uefa-euro-2024.ics'
    path: str = os.path.join(os.getcwd(), 'content', filename)
    tzid: str = 'UefaEuro2024'

    with open(path, 'wt', encoding='UTF-8') as fh:
        fh.write('BEGIN:VCALENDAR\r\n')
        fh.write('VERSION:2.0\r\n')
        fh.write('PRODID:sunarch.dev\r\n')
        fh.write('BEGIN:VTIMEZONE\r\n')
        fh.write(f'TZID:{tzid}\r\n')
        fh.write(f'LAST-MODIFIED:{COMPETITION_START.strftime(FORMAT_ICAL_DATE_UTC)}\r\n')
        fh.write('BEGIN:STANDARD\r\n')
        fh.write(f'DTSTART:{COMPETITION_START.strftime(FORMAT_ICAL_DATE)}\r\n')
        fh.write('TZOFFSETFROM:0000\r\n')
        fh.write('TZOFFSETTO:+0200\r\n')
        fh.write('END:STANDARD\r\n')
        fh.write('END:VTIMEZONE\r\n')
        for match in matches:
            fh.write('BEGIN:VEVENT\r\n')
            fh.write(f'UID:UEFA-Euro-2024-match-{match.number}\r\n')
            fh.write(f'DTSTAMP:{match.ical_dtstamp}\r\n')
            fh.write(f'DTSTART;TZID={tzid}:{match.ical_dtstart}\r\n')
            fh.write(f'DTEND;TZID={tzid}:{match.ical_dtend}\r\n')
            fh.write(f'SUMMARY:{match.ical_summary}\r\n')
            fh.write(f'LOCATION:{match.ical_location}\r\n')
            fh.write('END:VEVENT\r\n')
        fh.write('END:VCALENDAR\r\n')


def setup(page: Page, debug: int = 0) -> None:
    """Set up competition page"""

    print('PAGE SETUP START : Competition - UEFA Euro 2024')

    matches: list[Match] = load_matches(page.pad)

    for team in TEAMS.values():
        team.reset()
        for group in GROUPS.values():
            if team.abbrev in group.teams:
                team.group = group.name

    for match_item in matches:

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
    set_field(page, KEY_FOR_MATCHES, matches)
    set_field(page, KEY_FOR_PERIODS, PERIODS)

    print('PAGE SETUP END   : Competition - UEFA Euro 2024')

    write_ical(matches)
    print('FINISHED writing iCal: Competition - UEFA Euro 2024')
