# The names of battlefields and characters in this game are randomly generated using the random generator in the link
# below.
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

getcontext().Emin = -10 * 10000
getcontext().Emax = 10 * 10000
getcontext().traps[Overflow] = 0
getcontext().traps[Underflow] = 0
getcontext().traps[DivisionByZero] = 0
getcontext().traps[InvalidOperation] = 0
getcontext().prec = 100

today = date.today()


def get_index(elem, a_list):
    # type: (object, list) -> int
    """
    This function is used to get the index of an element in a list.
    :param elem: an element to be searched
    :param a_list: a list to search from
    :return: the index of elem in a_list
    """

    if len(a_list) > 0:
        for i in range(len(a_list)):
            if a_list[i] == elem:
                return i

    return -1  # element not in list



class BattleRecord:
	"""
	This class contains attributes of battle records of heroes.
	"""
	battle_number: int = 0  # initial value
	
	def __init__(self):
		# type: () -> None
		self.battle_number += 1
		BattleRecord.battle_number += 1


# class Battle


# class Position


# class Hero


# class HeroElement


# class Skill


# class SkillLevelUpBonus


# class Battlefield


# class Building


# class TownCenter(Building)


# class DefenseTower(Building)


# class QuizZone(Building)


# class BuildingType


# class QuizQuestion


# class Tile


# class SpecialPower


# class Research


# class Player


# class AI(Player)


# class Deck


# class Shop


# class GlobalShop(Shop)


# class BattlefieldShop(Shop)


# class Rune


# class Box


# class TreasureChest


# class Game


# Initialising variables to be stored in the saved game data.


characters: list = [

]

buildings: list = [

]

battlefields: list = [

]

quiz_questions: list = [

]

researches: list = [

]


# def main()


# main()
