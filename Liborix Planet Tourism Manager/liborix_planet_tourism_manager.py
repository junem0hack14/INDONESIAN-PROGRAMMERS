import sys
import random
import pickle
import copy
from datetime import datetime
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


# Game version: 1


class Game:
	"""
	This class contains attributes of the game.
	"""
	
	def __init__(self, places, player):
		# type: (list, Player) -> None
		self.places: list = places
		self.player: Player = player
		
	def to_string(self):
		# type: () -> str
		res: str = ""  # initial value
		res += "Places: \n"
		for place in self.places:
			res += str(place.to_string()) +  "\n"
			
		res += "Player: \n" + str(self.player.to_string()) + "\n"
		return res
		
	def clone(self):
		# type: () -> Game
		return copy.deepcopy(self)
	
	
class Place:
	"""
	This class contains attributes of places in Liborix planet where people can visit.
	"""
	
	def __init__(self, place_id, name, description, coin_production_rate, m_cube_production_rate, kwh_production_rate, worker_production_rate, visitor_production_rate, empty_space_production_rate, special_coin_production_rate, coin_cost, m_cube_cost, kwh_cost, worker_cost, visitor_cost, empty_space_cost, special_coin_cost):
		# type: (str, str, str, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal) -> None
		self.place_id: str = place_id
		self.name: str = name
		self.description: str = description
		self.level = 0  # initial value
		self.coin_production_rate: Decimal = coin_production_rate
		self.m_cube_production_rate: Decimal = m_cube_production_rate
		self.kwh_production_rate: Decimal = kwh_production_rate
		self.worker_production_rate: Decimal = worker_production_rate
		self.visitor_production_rate: Decimal = visitor_production_rate
		self.empty_space_production_rate: Decimal = empty_space_production_rate
		self.special_coin_production_rate: Decimal = special_coin_production_rate
		self.coin_cost: Decimal = coin_cost
		self.m_cube_cost: Decimal = m_cube_cost
		self.kwh_cost: Decimal = kwh_cost
		self.worker_cost: Decimal = worker_cost
		self.visitor_cost: Decimal = visitor_cost
		self.empty_space_cost: Decimal = empty_space_cost
		self.special_coin_cost: Decimal = special_coin_cost
		self.is_active: bool = False
		
	def to_string(self):
		# type: () -> str
		res: str = ""  # initial value
		res += "Place ID: " + str(self.place_id) + "\n"
		res += "Name: " + str(self.name) + "\n"
		res += "Description: " + str(self.description) + "\n"
		res += "Level: " + str(self.level) + "\n"
		res += "Coin production rate: " + str(self.coin_production_rate) + "\n"
		return res
		
	def clone(self):
		# type: () -> Place
		return copy.deepcopy(self)
	
	
class Player:
	"""
	This class contains attributes of the player in the game.
	"""
	
	def __init__(self, name):
		# type: (str) -> None
		self.player_id: str = str(random.randint(100000000, 999999999))
		self.name: str = name
		self.coins: Decimal = Decimal("1e6")
		self.coins_earned: Decimal = Decimal("1e6")
		self.m_cube: Decimal = Decimal("1e3")
		self.m_cube_earned: Decimal = Decimal("1e3")
		self.kwh: Decimal = Decimal("1e3")
		self.kwh_earned: Decimal = Decimal("1e3")
		self.workers: Decimal = Decimal("1e3")
		self.workers_earned: Decimal = Decimal("1e3")
		self.visitors: Decimal = Decimal("1e3")
		self.visitors_earned: Decimal = Decimal("1e3")
		self.empty_space: Decimal = Decimal("1e3")
		self.empty_space_earned: Decimal = Decimal("1e3")
		self.special_coins: Decimal = Decimal("1e3")
		self.special_coins_earned: Decimal = Decimal("1e3")
		
	def to_string(self):
		# type: () -> str
		res: str = ""  # initial value
		res += "Player ID: " + str(self.player_id) + "\n"
		res += "Name: " + str(self.name) + "\n"
		res += "Coins: " + str(self.coins) + "\n"
		res += "Coins earned: " + str(self.coins_earned) + "\n"
		res += "Metres cube: " + str(self.m_cube) + "\n"
		res += "Metres cube earned: " + str(self.m_cube_earned) + "\n"
		res += "kWh: " + str(self.kwh) + "\n"
		res += "kWh earned: " + str(self.kwh_earned) + "\n"
		res += "Workers: " + str(self.workers) + "\n"
		res += "Workers earned: " + str(self.workers_earned) + "\n"
		res += "Visitors: " + str(self.visitors) +"\n"
		res += "Visitors earned: " + str(self.visitors_earned) + "\n"
		res += "Empty space: " + str(self.empty_space) + "\n"
		res += "Empty space earned: " + str(self.empty_space_earned) + "\n"
		res += "Special coins: " + str(self.special_coins) + "\n"
		res += "Special coins earned: " + str(self.special_coins_earned) + "\n"
		return res
		
	def clone(self):
		# type: () -> Player
		return copy.deepcopy(self)
