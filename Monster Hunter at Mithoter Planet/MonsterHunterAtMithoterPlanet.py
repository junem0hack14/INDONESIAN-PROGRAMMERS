# The names of the monsters in this game are randomly generated using the random generator in the link below.
# https://www.fantasynamegenerators.com/

# Game version: 1 (Command Line Interface Version)


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

getcontext().Emin = -10 * 10000
getcontext().Emax = 10 * 10000
getcontext().traps[Overflow] = 0
getcontext().traps[Underflow] = 0
getcontext().traps[DivisionByZero] = 0
getcontext().traps[InvalidOperation] = 0
getcontext().prec = 100

today = date.today()


class AwakenBonus:
    """
    This class contains attributes of awaken bonus gained for awakening a hero.
    """

    def __init__(self, attack_speed_up, crit_rate_up, crit_damage_up, evasion_chance_up, resistance_up, accuracy_up,
                 extra_turn_chance_up, counterattack_chance_up, new_move, move_to_be_replaced, upgraded_move):
        # type: (float, float, float, float, float, float, float, float, Move, Move, Move) -> None
        self.attack_speed_up: float = attack_speed_up
        self.crit_rate_up: float = crit_rate_up
        self.crit_damage_up: float = crit_damage_up
        self.evasion_chance_up: float = evasion_chance_up
        self.resistance_up: float = resistance_up
        self.accuracy_up: float = accuracy_up
        self.extra_turn_chance_up: float = extra_turn_chance_up
        self.counterattack_chance_up: float = counterattack_chance_up
        self.new_move: Move = new_move  # a Move class object
        self.move_to_be_replaced: Move = move_to_be_replaced  # a Move class object
        self.upgraded_move: Move = upgraded_move  # a Move class object

    def clone(self):
        return copy.deepcopy(self)


class SecondaryAwakenBonus(AwakenBonus):
    """
    This class contains attributes of secondary awaken bonus gained for secondary awakening a character.
    """

    def __init__(self, attack_speed_up, crit_rate_up, crit_damage_up, evasion_chance_up, resistance_up, accuracy_up,
                 extra_turn_chance_up, counterattack_chance_up, new_move, move_to_be_replaced, upgraded_move,
                 second_new_move, second_move_to_be_replaced, second_upgraded_move):
        super(SecondaryAwakenBonus, self).__init__(attack_speed_up, crit_rate_up, crit_damage_up, evasion_chance_up, resistance_up, accuracy_up,
                 extra_turn_chance_up, counterattack_chance_up, new_move, move_to_be_replaced, upgraded_move)
        # type: (float, float, float, float, float, float, float, float, Move, Move, Move, Move, Move, Move) -> None
        self.second_new_move: Move = second_new_move  # a Move class object
        self.second_move_to_be_replaced: Move = second_move_to_be_replaced  # a Move class object
        self.second_upgraded_move: Move = second_upgraded_move  # a Move class object


class Battle:
    """
    This class contains attributes of battles in this game.
    """

    def __init__(self, player):
        # type: (Player) -> None
        self.player: Player = player


class TrainerBattle(Battle):
    """
    This class is used to initialise battles with trainers.
    """

    def __init__(self, player, trainer):
        # type: (Player, Trainer) -> None
        super(TrainerBattle, self).__init__(player)
        self.trainer: Trainer = trainer
        self.winner: Player or None = None  # initial value


class WildBattle(Battle):
    """
    This class is used to initialise battles with wild monsters.
    """

    def __init__(self, player, wild_monster):
        # type: (Player, Monster) -> None
        super(WildBattle, self).__init__(player)
        self.wild_monster: Monster = wild_monster


class BodyOfWater:
    """

    """


class Dam(BodyOfWater):
    """

    """


class Lake(BodyOfWater):
    """

    """


class River(BodyOfWater):
    """

    """


class Sea(BodyOfWater):
    """

    """


class Building:
    """

    """


class Gym(Building):
    """

    """


class Mall(Building):
    """

    """


class Shop(Building):
    """

    """


class BuildingEntrance:
    """

    """


class BuildingExit:
    """

    """


class City:
    """

    """


class CityPortal:
    """

    """


class Equipment:
    """

    """


class Floor:
    """

    """


class Game:
    """

    """


class Habitat:
    """

    """


class Item:
    """

    """


class Ball(Item):
    """

    """


class FishingLine(Item):
    """

    """


class Potion(Item):
    """

    """


class Shard(Item):
    """

    """


class TreasureChest(Item):
    """

    """


class Location:
    """

    """


class Meteorite:
    """

    """


class Monster:
    """

    """


class Move:
    """

    """


class Player:
    """

    """


class Trainer(Player):
    """

    """


class GymLeader(Trainer):
    """

    """


class Question:
    """
    This class is used to initialise questions asked in quiz zones.
    """

    question_number: int = 0

    def __init__(self, question, choices, correct_answer, reward):
        # type: (str, str, str, Reward) -> None
        self.question_number += 1
        Question.question_number += 1
        self.question: str = question
        self.choices: str = choices
        self.player_input_answer: str or None = None
        self.correct_answer: str = correct_answer
        self.reward: Reward = reward


class QuizZone:
    """

    """


class Reward:
    """

    """


class Rune:
    """

    """


class StairsDown:
    """

    """


class StairsUp:
    """

    """


class Team:
    """

    """


# Initialising variables to be stored in the save game data.


# def main()


# main()