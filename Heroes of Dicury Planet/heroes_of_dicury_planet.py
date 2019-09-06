# The names of the monsters in this game are randomly generated using the random generator in the link below.
# https://www.fantasynamegenerators.com/

# Game version: pre-release 1 (Command Line Interface Version)


import sys
import random
import pickle
import copy
from datetime import date
from datetime import timedelta
import calendar

sys.modules['_decimal'] = None
import decimal
from decimal import *
from decimal import Decimal

getcontext().Emin = -10 ** 10000
getcontext().Emax = 10 ** 10000
getcontext().traps[Overflow] = 0
getcontext().traps[Underflow] = 0
getcontext().traps[DivisionByZero] = 0
getcontext().traps[InvalidOperation] = 0
getcontext().prec = 100

today = date.today()


# Creating necessary functions to be used in the entire program


def triangulation(n: int) -> int:
    return int(n * (n - 1) / 2)


def all_died(team_a, team_b):
    # type: (Team, Team) -> bool
    for hero in team_a.heroes[0]:
        if hero.curr_hp > 0:
            return False

    for hero in team_b.heroes[0]:
        if hero.curr_hp > 0:
            return False

    return True


class Action:
    """
    This class contains attributes of actions in this game.
    """

    POSSIBLE_NAMES: list = ["NORMAL ATTACK", "NORMAL HEAL", "USE SKILL"]

    def __init__(self, user, name, target):
        # type: (Hero, str, Hero) -> None
        self.user: Hero = user
        self.name: str or None = name if name in self.POSSIBLE_NAMES else None
        self.target: Hero = target

    def execute(self):
        # type: () -> bool
        if self.name == "NORMAL ATTACK":
            if self.user.corresponding_team != self.target.corresponding_team:
                self.user.attack(self.target)
                return True
            return False
        elif self.name == "NORMAL HEAL":
            if self.user.corresponding_team == self.target.corresponding_team:
                self.user.heal(self.target)
                return True
            return False
        elif self.name == "USE SKILL":
            skill_to_use: Skill = self.user.skills[0]
            if (skill_to_use.does_attack and self.user.corresponding_team != self.target.corresponding_team) \
                    or (skill_to_use.does_heal and self.user.corresponding_team == self.target.corresponding_team):
                self.user.use_skill(skill_to_use, self.target)
                return True
            return False
        else:
            return False


class Hero:
    MIN_LEVEL: int = 1
    MIN_RATING: int = 1
    MAX_RATING: int = 6

    def __init__(self, name, rating, max_hp, attack_power, defense, skills):
        # type: (str, int, Decimal, Decimal, Decimal, list) -> None
        self.name: str = name
        self.rating: int = rating if self.MIN_RATING <= rating <= self.MAX_RATING else 1
        self.level: int = 1
        self.max_level: int = triangulation(self.level)
        self.curr_hp: Decimal = max_hp
        self.max_hp: Decimal = max_hp
        self.attack_power: Decimal = attack_power
        self.defense: Decimal = defense
        self.skills: list = skills
        self.corresponding_team: Team or None = None  # initial value

    def to_string(self) -> str:
        res: str = ""  # initial value
        res += "Name: " + str(self.name) + "\n"
        res += "Rating: " + str(self.rating) + "\n"
        res += "Level: " + str(self.level) + "\n"
        res += "Max level: " + str(self.max_level) + "\n"
        res += "HP: " + str(self.curr_hp) + "/" + str(self.max_hp) + "\n"
        res += "Attack power: " + str(self.attack_power) + "\n"
        res += "Defense: " + str(self.defense) + "\n"
        res += "Below is a list of skills this hero has.\n"
        for skill in self.skills:
            res += str(skill.to_string()) + "\n"
            
        return res

    def attack(self, other):
        # type: (Hero) -> str
        return_string: str = ""  # initial value
        damage: Decimal = self.attack_power - other.defense
        other.curr_hp -= damage
        return_string += str(self.name) + " did " + str(damage) + " damage on " + str(other.name)
        if other.curr_hp <= 0:
            return_string += str(self.name) + " killed " + str(other.name)

        return_string += "\n"
        return return_string

    def heal(self, other):
        # type: (Hero) -> str
        return_string: str = ""  # initial value
        heal_amount: Decimal = other.max_hp * 0.2
        other.curr_hp += heal_amount
        other.curr_hp = other.curr_hp if other.curr_hp <= other.max_hp else other.max_hp
        return_string += str(self.name) + " healed " + str(other.name) + " with amount of " + str(heal_amount) + " HP.\n"
        return return_string

    def use_skill(self, skill, target):
        # type: (Skill, Hero) -> str
        return_string: str = ""  # initial value
        assert skill in self.skills, "'skill' must be one of the hero's skills."
        if skill.does_heal:
            heal_amount: Decimal = skill.heal_amount
            target.curr_hp += heal_amount
            target.curr_hp = target.curr_hp if target.curr_hp <= target.max_hp else target.max_hp
            return_string += str(self.name) + " healed " + str(target.name) + " with amount of " + str(
                heal_amount) + " HP.\n"

        if skill.does_attack:
            damage: Decimal = self.attack_power * skill.damage_multiplier - target.defense
            target.curr_hp -= damage
            return_string += str(self.name) + " did " + str(damage) + " damage on " + str(target.name)
            if target.curr_hp <= 0:
                return_string += str(self.name) + " killed " + str(target.name)

            return_string += "\n"

        return return_string


class Skill:
    """
    This class contains attributes of skills that a hero has.
    """

    def __init__(self, name, does_heal, does_attack, heal_amount, damage_multiplier):
        # type: (str, bool, bool, Decimal, float) -> None
        self.name: str = name
        self.does_heal: bool = does_heal
        self.does_attack: bool = does_attack
        self.heal_amount: Decimal = heal_amount if self.does_heal else 0
        self.damage_multiplier: float = damage_multiplier if self.does_attack else 0

    def to_string(self) -> str:
        res: str = ""  # initial value
        res += "Name: " + str(self.name) + "\n"
        res += "Does it heal? " + str(self.does_heal) + "\n"
        res += "Does it attack? " + str(self.does_attack) + "\n"
        res += "Heal amount: " + str(self.heal_amount) + "\n"
        res += "Damage multiplier: " + str(self.damage_multiplier) + "\n"
        return res


class Team:
    """
    This class contains attributes of teams brought to battles.
    """
    MAX_TEAM_SIZE = 5

    def __init__(self, heroes: list) -> None:
        self.heroes: list = heroes if len(heroes) <= self.MAX_TEAM_SIZE else []


def main():
    """
    This function is used to run the program.
    :return:
    """
    heroes_list: list = [
        Hero("Hydra", 1, Decimal("5e4"), Decimal("2.5e3"), Decimal("2.47e3"),
             [Skill("Strike", False, True, Decimal("0e0"), 3.5), Skill("Dispel", True, False, Decimal("1e4"), 0)]),
        Hero("Cygrus", 1, Decimal("4.78e4"), Decimal("2.7e3"), Decimal("2.11e3"),
             [Skill("Strike", False, True, Decimal("0e0"), 3.5), Skill("Dispel", True, False, Decimal("1e4"), 0)])
    ]

    player_heroes: list = []  # initial value
    enemy_heroes: list = []  # initial value
    for i in range(5):
        player_heroes.append(heroes_list[random.randint(0, len(heroes_list) - 1)])
        enemy_heroes.append(heroes_list[random.randint(0, len(heroes_list) - 1)])

    player_team: Team = Team([player_heroes])
    for hero in player_team.heroes[0]:
        hero.corresponding_team = player_team

    enemy_team: Team = Team([enemy_heroes])
    for hero in enemy_team.heroes[0]:
        hero.corresponding_team = enemy_team

    print("Enter 1 to battle.")
    print("Enter 2 to quit.")
    option: int = int(input("Please enter a number: "))
    while option < 1 or option > 2:
        option: int = int(input("Sorry, invalid input! Please enter a number: "))

    while option != 2:
        if option == 1:
            print("Battle starts. Below is a list of your heroes.\n")
            for hero in player_team.heroes[0]:
                print(hero.to_string())

            print("Below is a list of your enemy's heroes.\n")
            for hero in enemy_team.heroes[0]:
                print(hero.to_string())

            turn: int = 0  # initial value
            while not all_died(player_team, enemy_team):
                turn += 1
                if turn % 2 == 1:
                    print("It's player's turn.")
                    moving_hero: Hero = player_team.heroes[0][(turn // 2) % len(player_team.heroes[0])]
                    print("Type in NORMAL ATTACK, NORMAL HEAL, or USE SKILL")
                    action_name: str = input("What do you want to do? ")
                    target: Hero or None = None  # initial value
                    while action_name not in Action.POSSIBLE_NAMES:
                        action_name: str = input("Invalid input! What do you want to do? ")

                    if action_name == "NORMAL ATTACK":
                        enemy_target_index: int = int(input("Please enter index of enemy's hero: "))
                        while enemy_target_index < 0 or enemy_target_index >= len(enemy_team.heroes[0]):
                            enemy_target_index: int = int(input("Sorry, invalid input! "
                                                                "Please enter index of enemy's hero: "))
                        target = enemy_team.heroes[0][enemy_target_index]
                    elif action_name == "HEAL":
                        ally_target_index: int = int(input("Please enter index of ally's hero: "))
                        while ally_target_index < 0 or ally_target_index >= len(player_team.heroes[0]):
                            ally_target_index: int = int(input("Sorry, invalid input! "
                                                               "Please enter index of ally's hero: "))
                        target = player_team.heroes[0][ally_target_index]

                    elif action_name == "USE SKILL":
                        if moving_hero.skills[0].does_attack:
                            enemy_target_index: int = int(input("Please enter index of enemy's hero: "))
                            while enemy_target_index < 0 or enemy_target_index >= len(enemy_team.heroes[0]):
                                enemy_target_index: int = int(input("Sorry, invalid input! "
                                                                    "Please enter index of enemy's hero: "))
                            target = enemy_team.heroes[0][enemy_target_index]

                        elif moving_hero.skills[0].does_heal:
                            ally_target_index: int = int(input("Please enter index of ally's hero: "))
                            while ally_target_index < 0 or ally_target_index >= len(player_team.heroes[0]):
                                ally_target_index: int = int(input("Sorry, invalid input! "
                                                                   "Please enter index of ally's hero: "))
                            target = player_team.heroes[0][ally_target_index]

                    action: Action = Action(moving_hero, action_name, target)
                    action.execute()

                    print("Current status of player's heroes in the battle are as below.\n")
                    for hero in player_team.heroes[0]:
                        print(hero.to_string())

                    print("Current status of enemy's heroes in the battle are as below.\n")
                    for hero in enemy_team.heroes[0]:
                        print(hero.to_string())

                else:
                    print("It's enemy's turn.")
                    moving_hero: Hero = enemy_team.heroes[0][(turn // 2) % len(enemy_team.heroes[0])]
                    action_name: str = Action.POSSIBLE_NAMES[random.randint(0, len(Action.POSSIBLE_NAMES) - 1)]
                    target: Hero or None = None  # initial value
                    if action_name == "NORMAL ATTACK":
                        target = player_team.heroes[0][random.randint(0, len(player_team.heroes[0]) - 1)]
                    elif action_name == "HEAL":
                        target = enemy_team.heroes[0][random.randint(0, len(enemy_team.heroes[0]) - 1)]

                    elif action_name == "USE SKILL":
                        if moving_hero.skills[0].does_attack:
                            target = player_team.heroes[0][random.randint(0, len(player_team.heroes[0]) - 1)]

                        elif moving_hero.skills[0].does_heal:
                            target = enemy_team.heroes[0][random.randint(0, len(enemy_team.heroes) - 1)]

                    action: Action = Action(moving_hero, action_name, target)
                    action.execute()

                    print("Current status of player's heroes in the battle are as below.\n")
                    for hero in player_team.heroes[0]:
                        print(hero.to_string())

                    print("Current status of enemy's heroes in the battle are as below.\n")
                    for hero in enemy_team.heroes[0]:
                        print(hero.to_string())

        option: int = int(input("Please enter a number: "))
        while option < 1 or option > 2:
            option: int = int(input("Sorry, invalid input! Please enter a number: "))

    sys.exit()


main()
