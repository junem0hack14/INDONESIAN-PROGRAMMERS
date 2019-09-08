import copy
import random
from itertools import combinations


class League:
    """
    This class contains attributes of a soccer league.
    """

    def __init__(self, name):
        # type: (str) -> None
        self.name: str = name
        self.teams: list = []  # initial value
        self.matchdays: dict = {}  # initial value

    def add_team(self, team):
        # type: (Team) -> None
        self.teams.append(team)

    def add_matchday(self, matchday_number, matchday):
        # type: (int, Matchday) -> bool
        if matchday_number not in self.matchdays.keys():
            self.matchdays[matchday_number] = matchday
            return True
        return False

    def sort_matchdays(self):
        # type: () -> None
        matchday_list: list = sorted(self.matchdays.values())
        matchday_nums: list = []  # initial value
        for i in self.matchdays.keys():
            matchday_nums.append(i)

        matchday_nums = sorted(matchday_nums)
        self.matchdays = {}  # initial value
        for i in matchday_nums:
            self.matchdays[i] = matchday_list[i - 1]

    def swap_matchdays(self, matchday_num1, matchday_num2):
        # type: (int, int) -> None
        temp1: Matchday = self.matchdays[matchday_num1]
        temp2: Matchday = self.matchdays[matchday_num2]
        num1: int = temp1.number
        num2: int = temp2.number
        temp1.number = num2
        temp2.number = num1
        self.matchdays[matchday_num2] = temp1
        self.matchdays[matchday_num1] = temp2

    def clone(self):
        # type: () -> League
        return copy.deepcopy(self)

    def to_string(self):
        # type: () -> str
        res: str = ""  # initial value
        res += "Below is a list of teams in " + str(self.name) + " league.\n"
        for team in self.teams:
            res += str(team.to_string()) + "\n"

        res += "Below is a list of matchdays in " + str(self.name) + " league.\n"
        for matchday in self.matchdays.values():
            res += str(matchday.to_string()) + "\n"

        return res


class Team:
    """
    This class contains attributes of teams.
    """

    def __init__(self, name):
        # type: (str) -> None
        self.name = name

    def clone(self):
        # type: () -> Team
        return copy.deepcopy(self)

    def to_string(self):
        # type: () -> str
        return str(self.name)


class Matchday:
    """
    This class contains attributes of matchdays in the league.
    """

    def __init__(self, number):
        # type: (int) -> None
        self.number: int = number
        self.fixtures: list = []  # initial value

    def clone(self):
        # type: () -> Matchday
        return copy.deepcopy(self)

    def add_fixture(self, fixture):
        # type: (Fixture) -> None
        self.fixtures.append(fixture)

    def __gt__(self, other):
        # type: (Matchday) -> bool
        if self.number > other.number:
            return True
        else:
            return False

    def __lt__(self, other):
        # type: (Matchday) -> bool
        if self.number < other.number:
            return True
        else:
            return False

    def to_string(self):
        # type: () -> str
        res: str = ""  # initial value
        res += "MATCHDAY " + str(self.number) + "\n"
        for fixture in self.fixtures:
            res += str(fixture.to_string()) + "\n"

        return res


class Fixture:
    """
    This class contains attributes of fixtures.
    """

    def __init__(self, team1, team2):
        # type: (Team, Team) -> None
        self.team1: Team = team1
        self.team2: Team = team2

    def clone(self):
        # type: () -> Fixture
        return copy.deepcopy(self)

    def reverse(self):
        # type: () -> Fixture
        temp1: Team = self.team1
        temp2: Team = self.team2
        self.team1 = temp2
        self.team2 = temp1
        return self

    def to_string(self):
        # type: () -> str
        return str(self.team1.to_string()) + " vs. " + str(self.team2.to_string()) + "\n"


def main():
    """
    This function is used to run the program
    :return:
    """
    name: str = input("Please enter name of league: ")
    num_teams: int = int(input("Please enter number of teams in " + str(name) + " league: "))
    while num_teams % 2 == 1 or num_teams <= 0:
        num_teams: int = int(input("Sorry, invalid input! Please enter number of teams in " + str(name) + " league: "))

    new_league: League = League(name)
    existing_team_names: list = []  # initial value
    for i in range(num_teams):
        new_team_name: str = input("Please enter name of team: ")
        while new_team_name.upper() in existing_team_names:
            new_team_name = input("Invalid input! Please enter name of team: ")

        curr_team: Team = Team(new_team_name.upper())
        existing_team_names.append(new_team_name.upper())
        new_league.add_team(curr_team)

    fixtures_list: list = list(list(combinations(new_league.teams, 2)))
    num_fixtures_in_a_season: int = 2 * (num_teams - 1)
    num_fixtures_till_mid_season: int = num_fixtures_in_a_season // 2
    for i in range(num_fixtures_till_mid_season):
        curr_matchday: Matchday = Matchday(i + 1)
        used_teams: list = []  # initial value
        for j in range(num_teams // 2):
            fixture_index: int = random.randint(0, len(fixtures_list) - 1)
            fixture_tuple: tuple = fixtures_list[fixture_index]
            while fixture_tuple[0] in used_teams or fixture_tuple[1] in used_teams:
                fixture_index: int = random.randint(0, len(fixtures_list) - 1)
                fixture_tuple: tuple = fixtures_list[fixture_index]

            first_team: Team = fixture_tuple[0]
            second_team: Team = fixture_tuple[1]
            used_teams.append(first_team)
            used_teams.append(second_team)
            fixtures_list.remove(fixture_tuple)
            curr_fixture: Fixture = Fixture(first_team, second_team)
            curr_matchday.add_fixture(curr_fixture)

        new_league.add_matchday(i + 1, curr_matchday)

    for i in range(num_fixtures_till_mid_season, num_fixtures_in_a_season):
        curr_matchday: Matchday = new_league.matchdays[i + 1 - num_fixtures_till_mid_season].clone()
        curr_matchday.number += num_fixtures_till_mid_season
        temp_fixtures: list = curr_matchday.fixtures
        curr_matchday.fixtures = []  # initial value
        for curr_fixture in temp_fixtures:
            curr_matchday.add_fixture(curr_fixture.reverse())

        new_league.add_matchday(i + 1, curr_matchday)

    # Randomly swapping the matchdays in both halves of the season
    num_swaps: int = (num_teams // 2) ** 2
    for i in range(num_swaps):
        matchday_num1: int = random.randint(1, num_fixtures_till_mid_season)
        matchday_num2: int = random.randint(1, num_fixtures_till_mid_season)
        while matchday_num1 == matchday_num2:
            matchday_num1 = random.randint(1, num_fixtures_till_mid_season)
            matchday_num2 = random.randint(1, num_fixtures_till_mid_season)

        matchday_num3: int = random.randint(num_fixtures_till_mid_season + 1, num_fixtures_in_a_season)
        matchday_num4: int = random.randint(num_fixtures_till_mid_season + 1, num_fixtures_in_a_season)
        while matchday_num3 == matchday_num4:
            matchday_num3 = random.randint(num_fixtures_till_mid_season + 1, num_fixtures_in_a_season)
            matchday_num4 = random.randint(num_fixtures_till_mid_season + 1, num_fixtures_in_a_season)

        new_league.swap_matchdays(matchday_num1, matchday_num2)
        new_league.swap_matchdays(matchday_num3, matchday_num4)

    new_league.sort_matchdays()
    print(new_league.to_string())


main()
