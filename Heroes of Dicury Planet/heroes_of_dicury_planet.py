# The names of the monsters in this game are randomly generated using the random generator in the link below.
# https://www.fantasynamegenerators.com/

# Game version: pre-release 4 (Command Line Interface Version)


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
    return int(n * (n + 1) / 2)


def all_died(team):
    # type: (Team) -> bool
    for hero in team.heroes:
        if hero.get_is_alive():
            return False

    return True


class Action:
    """
    This class contains attributes of actions in this game.
    """

    POSSIBLE_NAMES: list = ["NORMAL ATTACK", "NORMAL HEAL", "USE SKILL"]

    def __init__(self, user, name, target, skill_to_use=None):
        # type: (Hero, str, Hero, Skill or None) -> None
        self.user: Hero = user
        self.name: str or None = name if name in self.POSSIBLE_NAMES else None
        self.target: Hero = target
        self.skill_to_use: Skill or None = skill_to_use

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
            if self.skill_to_use is not None:
                if (self.skill_to_use.does_attack and self.user.corresponding_team != self.target.corresponding_team) \
                        or (self.skill_to_use.does_heal and self.user.corresponding_team == self.target.corresponding_team):
                    self.user.use_skill(self.skill_to_use, self.target)
                    return True
                return False
            return False
        else:
            return False

    def clone(self):
        # type: () -> Action
        return copy.deepcopy(self)


class Hero:
    """
    This class contains attributes of heroes in this game.
    """
    MIN_LEVEL: int = 1
    MIN_RATING: int = 1
    MAX_RATING: int = 6
    MIN_CRIT_RATE: float = 0.15
    MAX_CRIT_RATE: float = 1
    MIN_CRIT_DAMAGE: float = 2
    MIN_RESISTANCE: float = 0
    MAX_RESISTANCE: float = 1
    MIN_ACCURACY: float = 0
    MAX_ACCURACY: float = 1
    MIN_BUFFS: int = 0
    MAX_BUFFS: int = 10
    MIN_DEBUFFS: int = 0
    MAX_DEBUFFS: int = 10

    def __init__(self, name, rating, max_hp, attack_power, defense, skills):
        # type: (str, int, Decimal, Decimal, Decimal, list) -> None
        self.name: str = name
        self.rating: int = rating if self.MIN_RATING <= rating <= self.MAX_RATING else 1
        self.level: int = 1
        self.max_level: int = triangulation(self.rating) * 10
        self.curr_hp: Decimal = max_hp
        self.max_hp: Decimal = max_hp
        self.attack_power: Decimal = attack_power
        self.defense: Decimal = defense
        self.crit_rate: float = self.MIN_CRIT_RATE
        self.crit_damage: float = self.MIN_CRIT_DAMAGE
        self.resistance: float = self.MIN_RESISTANCE
        self.accuracy: float = self.MIN_ACCURACY
        self.skills: list = skills
        self.buffs: list = []
        self.debuffs: list = []
        self.is_alive = True
        self.corresponding_team: Team or None = None  # initial value

    def clone(self):
        # type: () -> Hero
        return copy.deepcopy(self)

    def get_is_alive(self):
        # type: () -> bool
        self.is_alive = self.curr_hp > 0
        return self.is_alive

    def resistance_accuracy_rule(self, other):
        # type: (Hero) -> float
        if self.accuracy >= other.resistance:
            return 0.15
        elif self.accuracy < other.resistance and other.resistance - self.accuracy <= 0.15:
            return 0.15
        else:
            return other.resistance - self.accuracy

    def to_string(self) -> str:
        res: str = ""  # initial value
        res += "Name: " + str(self.name) + "\n"
        res += "Rating: " + str(self.rating) + "\n"
        res += "Level: " + str(self.level) + "\n"
        res += "Max level: " + str(self.max_level) + "\n"
        res += "HP: " + str(self.curr_hp) + "/" + str(self.max_hp) + "\n"
        res += "Attack power: " + str(self.attack_power) + "\n"
        res += "Defense: " + str(self.defense) + "\n"
        res += "Crit rate: " + str(100*self.crit_rate) + "%\n"
        res += "Crit damage: " + str(100 * self.crit_damage) + "%\n"
        res += "Resistance: " + str(100 * self.resistance) + "%\n"
        res += "Accuracy: " + str(100 * self.accuracy) + "%\n"
        res += "Below is a list of skills this hero has.\n"
        for skill in self.skills:
            res += str(skill.to_string()) + "\n"

        res += "Below is a list of buffs that this hero has.\n"
        for buff in self.buffs:
            res += str(buff.to_string()) + "\n"

        res += "Below is a list of debuffs that this hero has.\n"
        for debuff in self.debuffs:
            res += str(debuff.to_string()) + "\n"

        res += "Is it alive? " + str(self.get_is_alive()) + "\n"
        return res

    def add_buff(self, buff):
        # type: (Buff) -> bool
        if len(self.buffs) < self.MAX_BUFFS:
            buff_name_list: list = [curr_buff.name for curr_buff in self.buffs]
            if buff.name not in buff_name_list or buff.is_stackable:
                self.buffs.append(buff)
                self.attack_power *= Decimal(1 + buff.attack_percentage_up/100)
                self.defense *= Decimal(1 + buff.defense_percentage_up/100)
                return True
            return False
        return False

    def remove_buff(self, buff):
        # type: (Buff) -> bool
        if buff in self.buffs:
            self.buffs.remove(buff)
            self.attack_power /= Decimal(1 + buff.attack_percentage_up / 100)
            self.defense /= Decimal(1 + buff.defense_percentage_up / 100)
            return True
        return False

    def add_debuff(self, debuff):
        # type: (Debuff) -> bool
        if len(self.debuffs) < self.MAX_DEBUFFS:
            debuff_name_list: list = [curr_debuff.name for curr_debuff in self.debuffs]
            if debuff.name not in debuff_name_list or debuff.is_stackable:
                self.debuffs.append(debuff)
                self.attack_power *= Decimal(1 - debuff.attack_percentage_down / 100)
                self.defense *= Decimal(1 - debuff.defense_percentage_down / 100)
                return True
            return False
        return False

    def remove_debuff(self, debuff):
        # type: (Debuff) -> bool
        if debuff in self.debuffs:
            self.debuffs.remove(debuff)
            self.attack_power /= Decimal(1 - debuff.attack_percentage_down / 100)
            self.defense /= Decimal(1 - debuff.defense_percentage_down / 100)
            return True
        return False

    def reduce_buffs_count(self):
        # type: () -> None
        for buff in self.buffs:
            buff.duration -= 1
            if buff.duration == 0:
                self.remove_buff(buff)

    def reduce_debuffs_count(self):
        # type: () -> None
        for debuff in self.debuffs:
            debuff.duration -= 1
            if debuff.duration == 0:
                self.remove_debuff(debuff)

    def attack(self, other):
        # type: (Hero) -> str
        return_string: str = ""  # initial value
        is_crit: bool = random.random() <= self.crit_rate
        damage: Decimal = self.attack_power * Decimal(self.crit_damage) - other.defense if is_crit else self.attack_power - \
                                                                                               other.defense
        other.curr_hp -= damage
        return_string += str(self.name) + " did " + str(damage) + " damage on " + str(other.name)
        if other.curr_hp <= 0:
            return_string += str(self.name) + " killed " + str(other.name)

        return_string += "\n"
        return return_string

    def heal(self, other):
        # type: (Hero) -> str
        return_string: str = ""  # initial value
        heal_amount: Decimal = other.max_hp * Decimal(0.2)
        other.curr_hp += heal_amount
        other.curr_hp = other.curr_hp if other.curr_hp <= other.max_hp else other.max_hp
        return_string += str(self.name) + " healed " + str(other.name) + " with amount of " + str(
            heal_amount) + " HP.\n"
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
            is_crit: bool = random.random() <= self.crit_rate
            damage: Decimal = self.attack_power * Decimal(skill.damage_multiplier) * Decimal(self.crit_damage) - target.defense \
                if is_crit else self.attack_power * Decimal(skill.damage_multiplier) - target.defense
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

    def __init__(self, name, does_heal, does_attack, heal_amount, damage_multiplier, buffs_to_allies,
                 debuffs_to_enemies):
        # type: (str, bool, bool, Decimal, float, list, list) -> None
        self.name: str = name
        self.does_heal: bool = does_heal
        self.does_attack: bool = does_attack
        self.heal_amount: Decimal = heal_amount if self.does_heal else 0
        self.damage_multiplier: float = damage_multiplier if self.does_attack else 0
        self.buffs_to_allies: list = buffs_to_allies
        self.debuffs_to_enemies: list = debuffs_to_enemies

    def to_string(self) -> str:
        res: str = ""  # initial value
        res += "Name: " + str(self.name) + "\n"
        res += "Does it heal? " + str(self.does_heal) + "\n"
        res += "Does it attack? " + str(self.does_attack) + "\n"
        res += "Heal amount: " + str(self.heal_amount) + "\n"
        res += "Damage multiplier: " + str(self.damage_multiplier) + "\n"
        res += "Below is a list of buffs that the skill gives to allies.\n"
        for buff in self.buffs_to_allies:
            res += str(buff.to_string()) + "\n"

        res += "Below is a list of debuffs that the skill gives to enemies.\n"
        for debuff in self.debuffs_to_enemies:
            res += str(debuff.to_string()) + "\n"

        return res

    def clone(self):
        # type: () -> Skill
        return copy.deepcopy(self)


class Buff:
    """
    This class contains attributes of beneficial effects.
    """
    POSSIBLE_NAMES = ["ATTACK_UP", "DEFENSE_UP"]

    def __init__(self, name, duration):
        # type: (str, int) -> None
        self.name: str or None = name if name in self.POSSIBLE_NAMES else None
        self.attack_percentage_up: float = 50 if self.name == "ATTACK_UP" else 0
        self.defense_percentage_up: float = 50 if self.name == "DEFENSE_UP" else 0
        self.duration: int = duration
        self.is_stackable: bool = False

    def to_string(self):
        # type: () -> str
        res: str = ""  # initial value
        res += "Name: " + str(self.name) + "\n"
        res += "Attack percentage up: " + str(self.attack_percentage_up) + "%\n"
        res += "Defense percentage up: " + str(self.defense_percentage_up) + "%\n"
        res += "Duration: " + str(self.duration) + " turns\n"
        res += "Is it stackable? " + str(self.is_stackable) + "\n"
        return res

    def clone(self):
        # type: () -> Buff
        return copy.deepcopy(self)


class Debuff:
    """
        This class contains attributes of harmful effects.
        """
    POSSIBLE_NAMES = ["ATTACK_DOWN", "DEFENSE_DOWN"]

    def __init__(self, name, duration):
        # type: (str, int) -> None
        self.name: str or None = name if name in self.POSSIBLE_NAMES else None
        self.attack_percentage_down: float = 50 if self.name == "ATTACK_DOWN" else 0
        self.defense_percentage_down: float = 50 if self.name == "DEFENSE_DOWN" else 0
        self.duration: int = duration
        self.is_stackable: bool = False

    def to_string(self):
        # type: () -> str
        res: str = ""  # initial value
        res += "Name: " + str(self.name) + "\n"
        res += "Attack percentage down: " + str(self.attack_percentage_down) + "%\n"
        res += "Defense percentage down: " + str(self.defense_percentage_down) + "%\n"
        res += "Duration: " + str(self.duration) + " turns\n"
        res += "Is it stackable? " + str(self.is_stackable) + "\n"
        return res

    def clone(self):
        # type: () -> Debuff
        return copy.deepcopy(self)


class Team:
    """
    This class contains attributes of teams brought to battles.
    """
    MAX_TEAM_SIZE = 5

    def __init__(self):
        # type: () -> None
        self.heroes: list = []  # initial value

    def add_hero_(self, hero):
        # type: (Hero) -> bool
        if len(self.heroes) < self.MAX_TEAM_SIZE:
            self.heroes.append(hero)
            return True
        return False

    def remove_hero(self, hero):
        # type: (Hero) -> bool
        if hero in self.heroes:
            self.heroes.remove(hero)
            return True
        return False

    def to_string(self):
        # type: () -> str
        res: str = ""  # initial value
        res += "Below is a list of heroes in the team.\n"
        for hero in self.heroes:
            res += str(hero.to_string()) + "\n"

        return res

    def clone(self):
        # type: () -> Team
        return copy.deepcopy(self)


def main():
    """
    This function is used to run the program.
    :return:
    """
    heroes_list: list = [
        Hero("Hydra", 1, Decimal("5e4"), Decimal("2.5e3"), Decimal("2.47e3"),
             [Skill("Strike", False, True, Decimal("0e0"), 3.5, [], [Debuff("ATTACK_DOWN", 3)]),
              Skill("Dispel", True, False, Decimal("1e4"), 0, [Buff("ATTACK_UP", 2), Buff("DEFENSE_UP", 2)], []),
              Skill("Smother", False, True, Decimal("0e0"), 8, [], [Debuff("DEFENSE_DOWN", 3)])]),
        Hero("Cygrus", 1, Decimal("4.78e4"), Decimal("2.7e3"), Decimal("2.11e3"),
             [Skill("Strike", False, True, Decimal("0e0"), 3.5, [], [Debuff("ATTACK_DOWN", 3)]),
              Skill("Dispel", True, False, Decimal("1e4"), 0, [Buff("ATTACK_UP", 2), Buff("DEFENSE_UP", 2)], []),
              Skill("Smother", False, True, Decimal("0e0"), 8, [], [Debuff("DEFENSE_DOWN", 3)])])
    ]

    player_team: Team = Team()
    enemy_team: Team = Team()

    for i in range(5):
        player_team.add_hero_(heroes_list[random.randint(0, len(heroes_list) - 1)].clone())
        enemy_team.add_hero_(heroes_list[random.randint(0, len(heroes_list) - 1)].clone())

    for hero in player_team.heroes:
        hero.corresponding_team = player_team

    for hero in enemy_team.heroes:
        hero.corresponding_team = enemy_team

    print("Enter 1 to battle.")
    print("Enter 2 to quit.")
    option: int = int(input("Please enter a number: "))
    while option < 1 or option > 2:
        option: int = int(input("Sorry, invalid input! Please enter a number: "))

    while option != 2:
        if option == 1:
            print(player_team.to_string())
            print(enemy_team.to_string())
            turn: int = 0  # initial value
            while not all_died(player_team) and not all_died(enemy_team):
                turn += 1
                if turn % 2 == 1:
                    print("It's player's turn.")
                    hero_index: int = (turn // 2) % len(player_team.heroes)
                    moving_hero: Hero = player_team.heroes[hero_index]
                    while not moving_hero.get_is_alive():
                        hero_index += 1
                        if hero_index >= len(player_team.heroes):
                            hero_index -= len(player_team.heroes)

                        moving_hero = player_team.heroes[hero_index]

                    moving_hero.reduce_buffs_count()
                    moving_hero.reduce_debuffs_count()
                    print("Type in NORMAL ATTACK, NORMAL HEAL, or USE SKILL")
                    action_name: str = input("What do you want to do? ")
                    target: Hero or None = None  # initial value
                    skill_to_use: Skill or None = None  # initial value
                    while action_name not in Action.POSSIBLE_NAMES:
                        action_name: str = input("Invalid input! What do you want to do? ")

                    if action_name == "NORMAL ATTACK":
                        enemy_target_index: int = int(input("Please enter index of enemy's hero: "))
                        while enemy_target_index < 0 or enemy_target_index >= len(enemy_team.heroes):
                            enemy_target_index: int = int(input("Sorry, invalid input! "
                                                                "Please enter index of enemy's hero: "))

                        while not enemy_team.heroes[enemy_target_index].get_is_alive():
                            enemy_target_index: int = int(input("Sorry, invalid input! "
                                                                "Please enter index of enemy's hero: "))

                        target = enemy_team.heroes[enemy_target_index]
                    elif action_name == "NORMAL HEAL":
                        ally_target_index: int = int(input("Please enter index of ally's hero: "))
                        while ally_target_index < 0 or ally_target_index >= len(player_team.heroes):
                            ally_target_index: int = int(input("Sorry, invalid input! "
                                                               "Please enter index of ally's hero: "))

                        while not player_team.heroes[ally_target_index].get_is_alive():
                            ally_target_index: int = int(input("Sorry, invalid input! "
                                                               "Please enter index of ally's hero: "))

                        target = player_team.heroes[ally_target_index]

                    elif action_name == "USE SKILL":
                        skill_index: int = int(input("Please enter the index of the skill you want to use: "))
                        while skill_index < 0 or skill_index >= len(moving_hero.skills):
                            skill_index: int = int(input("Invalid input! "
                                                         "Please enter the index of the skill you want to use: "))

                        skill_to_use = moving_hero.skills[skill_index]

                        if skill_to_use.does_attack:
                            enemy_target_index: int = int(input("Please enter index of enemy's hero: "))
                            while enemy_target_index < 0 or enemy_target_index >= len(enemy_team.heroes):
                                enemy_target_index: int = int(input("Sorry, invalid input! "
                                                                    "Please enter index of enemy's hero: "))

                            while not enemy_team.heroes[enemy_target_index].get_is_alive():
                                enemy_target_index: int = int(input("Sorry, invalid input! "
                                                                    "Please enter index of enemy's hero: "))

                            target = enemy_team.heroes[enemy_target_index]
                            for debuff in skill_to_use.debuffs_to_enemies:
                                if random.random() > moving_hero.resistance_accuracy_rule(target):
                                    target.add_debuff(debuff.clone())

                        elif skill_to_use.does_heal:
                            ally_target_index: int = int(input("Please enter index of ally's hero: "))
                            while ally_target_index < 0 or ally_target_index >= len(player_team.heroes):
                                ally_target_index: int = int(input("Sorry, invalid input! "
                                                                   "Please enter index of ally's hero: "))

                            while not player_team.heroes[ally_target_index].get_is_alive():
                                ally_target_index: int = int(input("Sorry, invalid input! "
                                                                   "Please enter index of ally's hero: "))

                            target = player_team.heroes[ally_target_index]
                            for buff in skill_to_use.buffs_to_allies:
                                target.add_buff(buff.clone())

                    action: Action = Action(moving_hero, action_name, target, skill_to_use) \
                        if skill_to_use is not None else Action(moving_hero, action_name, target)
                    action.execute()
                    print("Current status of player's heroes in the battle are as below.\n")
                    print(player_team.to_string())
                    print("Current status of enemy's heroes in the battle are as below.\n")
                    print(enemy_team.to_string())

                    if all_died(player_team):
                        print("You lose!")

                    if all_died(enemy_team):
                        print("You win!")

                else:
                    print("It's enemy's turn.")
                    hero_index: int = ((turn // 2) - 1) % len(enemy_team.heroes)
                    moving_hero: Hero = enemy_team.heroes[hero_index]
                    while not moving_hero.get_is_alive():
                        hero_index += 1
                        if hero_index >= len(enemy_team.heroes):
                            hero_index -= len(enemy_team.heroes)

                        moving_hero = enemy_team.heroes[hero_index]

                    moving_hero.reduce_buffs_count()
                    moving_hero.reduce_debuffs_count()
                    action_name: str = Action.POSSIBLE_NAMES[random.randint(0, len(Action.POSSIBLE_NAMES) - 1)]
                    skill_to_use: Skill or None = None  # initial value
                    target: Hero or None = None  # initial value
                    if action_name == "NORMAL ATTACK":
                        target = player_team.heroes[random.randint(0, len(player_team.heroes) - 1)]
                        while not target.get_is_alive():
                            target = player_team.heroes[random.randint(0, len(player_team.heroes) - 1)]

                    elif action_name == "NORMAL HEAL":
                        target = enemy_team.heroes[random.randint(0, len(enemy_team.heroes) - 1)]
                        while not target.get_is_alive():
                            target = enemy_team.heroes[random.randint(0, len(enemy_team.heroes) - 1)]

                    elif action_name == "USE SKILL":
                        skill_index: int = random.randint(0, len(moving_hero.skills) - 1)
                        skill_to_use = moving_hero.skills[skill_index]
                        if skill_to_use.does_attack:
                            target = player_team.heroes[random.randint(0, len(player_team.heroes) - 1)]
                            while not target.get_is_alive():
                                target = player_team.heroes[random.randint(0, len(player_team.heroes) - 1)]

                            for debuff in skill_to_use.debuffs_to_enemies:
                                if random.random() > moving_hero.resistance_accuracy_rule(target):
                                    target.add_debuff(debuff.clone())

                        elif skill_to_use.does_heal:
                            target = enemy_team.heroes[random.randint(0, len(enemy_team.heroes) - 1)]
                            while not target.get_is_alive():
                                target = enemy_team.heroes[random.randint(0, len(enemy_team.heroes) - 1)]

                            for buff in skill_to_use.buffs_to_allies:
                                target.add_buff(buff.clone())

                    action: Action = Action(moving_hero, action_name, target, skill_to_use) \
                        if skill_to_use is not None else Action(moving_hero, action_name, target)
                    action.execute()
                    print("Current status of player's heroes in the battle are as below.\n")
                    print(player_team.to_string())
                    print("Current status of enemy's heroes in the battle are as below.\n")
                    print(enemy_team.to_string())

                    if all_died(player_team):
                        print("You lose!")

                    if all_died(enemy_team):
                        print("You win!")

        option: int = int(input("Please enter a number: "))
        while option < 1 or option > 2:
            option: int = int(input("Sorry, invalid input! Please enter a number: "))

    sys.exit()


main()
