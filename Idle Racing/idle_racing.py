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


class Car:
	"""
	This class contains attributes of cars.
	"""
	
	def __init__(self, id, name, top_speed):
		# type: (str, str, Decimal) -> None
		self.id: str = id
		self.name: str = name
		self.level: int = 1
		self.level_up_coin_cost: Decimal = Decimal("1e6")
		self.speed: Decimal = Decimal("0e0")
		self.top_speed: Decimal = top_speed
		self.distance_travelled: Decimal = Decimal("0e0")
		
	def to_string(self):
		# type: () -> str
		res: str = ""  # initial value
		res += "ID: " + str(self.id) + "\n"
		res += "Name: " + str(self.name) + "\n"
		res += "Level: " + str(self.level) + "\n"
		res += "Level up coin cost: " + str(self.level_up_coin_cost) + "\n"
		res += "Speed: " + str(self.speed) + " metres per second.\n"
		res += "Top speed: " + str(self.top_speed) + " metres per second.\n"
		res += "Distance travelled: " + str(self.distance_travelled) + " metres.\n"
		return res
		
	def accelerate(self):
		self.speed += self.top_speed * Decimal("0.1")
		self.speed = self.speed if self.speed <= self.top_speed else self.top_speed
		
	def level_up(self, player):
		# type: (Player) -> bool
		if player.coins >= self.level_up_coin_cost:
			self.level += 1
			player.coins -= self.level_up_coin_cost
			self.level_up_coin_cost *= 2
			self.top_speed *= 2
			return True
		return False
		
		
class Player:
	"""
	This class contains attributes of the player in the game.
	"""
	
	def __init__(self, name):
		# type: (str) -> None
		self.player_id: str = str(random.randint(100000000, 999999999))
		self.name: str = name
		self.car: Car or None = None  # initial value
		self.coins: Decimal = Decimal("0e0")
		self.distance_travelled: Decimal = Decimal("0e0")
		
	def level_up_car(self):
		# type: () -> bool
		return self.car.level_up(self)
		
	def move_car(self, seconds):
		# type: (int) -> bool
		if self.car is not None:
			self.distance_travelled += self.car.speed * seconds
			self.car.distance_travelled += self.car.speed * seconds
			self.coins += self.car.speed * 100 * seconds
			return True
		return False
		
	def to_string(self):
		# type: () -> str
		res: str = ""  # initial value
		res += "Player ID: " + str(self.player_id) + "\n"
		res += "Name: " + str(self.name) + "\n"
		res += "Car: \n" + str(self.car.to_string()) + "\n"
		res += "Coins: " + str(self.coins) + "\n"
		res += "Distance travelled: " + str(self.distance_travelled) + " metres.\n"
		return res
		
		
def main():
	"""
	This function is used to run the program.
	:return:
	"""
	
	new_player: Player or None = None  # initial value
	print("Enter Y for yes.")
	print("Enter anything else for no.")
	filename: str = "Saved Idle Racing Progress"
	load_ask: str = input("Do you want to load game progress? ")
	if load_ask == "Y":
		saved: Player = pickle.load(open(filename, "rb"))
		new_player = saved
		print("Current player data: ", new_player.to_string())
	else:
		name: str = input("Please enter your name: ")
		new_player = Player(name)
		new_player.car = Car("000001", "PW-35", 400)
		
	now = datetime.now()
	print(now)
	print("Type Y for yes.")
	print("Type anything else for no.")
	cont: str = input("Do you want to continue playing? ")
	while cont == "Y":
		new_now = datetime.now()
		time_diff = new_now - now
		seconds: int = time_diff.seconds
		now = new_now
		new_player.move_car(seconds)
		print("Type 1 to level up your car.")
		print("Type 2 to accelerate your car.")
		print("Type 3 to see your stats.")
		print("Type 4 to save and quit.")
		option: int = int(input("Please enter a number: "))
		while option < 1 or option > 4:
			option = int(input("Sorry, invalid input! Please enter a number: "))
			
		if option == 1:
			new_player.level_up_car()
			
		elif option == 2:
			new_player.car.accelerate()
			
		elif option == 3:
			print(new_player.to_string())
			
		elif option == 4:
			pickle.dump(new_player, open(filename, "wb"))
			sys.exit()
			
		cont = input("Do you want to continue playing? ")
		
	pickle.dump(new_player, open(filename, "wb"))
	sys.exit()
	
	
main()