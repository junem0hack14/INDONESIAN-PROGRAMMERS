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


class Library:
	"""
	This class contains attributes of the library.
	"""
	
	def __init__(self, items, manager):
		# type: (list, Player) -> None
		self.items: list = items
		self.manager: Player = manager
		
	def to_string(self):
		# type: () -> str
		res: str = ""  # initial value
		for item in self.items:
			res += str(item.to_string()) + "\n"
			
		res += "Manager: \n" + str(self.manager.to_string()) + "\n"
		return res
		
	def clone(self):
		# type: () -> Library
		return copy.deepcopy(self)
	
	
class Item:
	"""
	This class contains attributes of items in the library.
	"""
	
	def __init__(self, item_id, name, coin_cost, coin_production_rate):
		# type: (str, str, Decimal, Decimal) -> None
		self.item_id: str = item_id
		self.name: str = name
		self.level: int = 0
		self.coin_cost: Decimal = coin_cost
		self.min_coins_to_activate: Decimal = coin_cost
		self.coin_production_rate: Decimal = coin_production_rate
		self.is_active: bool = False
		
	def produce_resources(self, player, seconds):
		# type: (Player, int) -> None
		player.coins += self.coin_production_rate * seconds if self.is_active else 0
		player.coins_earned += self.coin_production_rate * seconds if self.is_active else 0
		
	def to_string(self):
		# type: () -> str
		res: str = ""  # initial value
		res += "Item ID: " + str(self.item_id) + "\n"
		res += "Name: " + str(self.name) + "\n"
		res += "Level: " + str(self.level) + "\n"
		res += "Coin cost: " + str(self.coin_cost) + "\n"
		res += "Minimum coins to activate this item: " + str(self.min_coins_to_activate) + "\n"
		res += "Coin production rate: " + str(self.coin_production_rate) + "\n"
		res += "Is it active? " + str(self.is_active) + "\n"
		return res
		
	def activate(self, player):
		# type: (Player) -> bool
		if player.coins >= self.coin_cost and player.coins_earned >= self.min_coins_to_activate and not self.is_active:
			self.level += 1
			player.coins -= self.coin_cost
			self.is_active = True
			return True
		return False
		
	def level_up(self, player):
		# type: (Player) -> bool
		if player.coins >= self.coin_cost and self.is_active:
			self.level += 1
			player.coins -= self.coin_cost
			self.coin_cost *= 2
			self.coin_production_rate *= 2
			return True
		return False
		
	def clone(self):
		# type: () -> Item
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
		
	def to_string(self):
		# type: () -> str
		res: str = ""  # initial value
		res += "Player ID: " + str(self.player_id) + "\n"
		res += "Name: " + str(self.name) + "\n"
		res += "Coins: " + str(self.coins) + "\n"
		res += "Coins earned: " + str(self.coins_earned) + "\n"
		return res
		
		
items: list = [
	Item("000001", "CD", Decimal("5e4"), Decimal("5e3")),
	Item("000002", "DVD", Decimal("5e9"), Decimal("5e7")),
	Item("000003", "Children's Book", Decimal("5e15"), Decimal("5e12")),
	Item("000004", "Hobby Book", Decimal("5e22"), Decimal("5e18")),
	Item("000005", "Fantasy Book", Decimal("5e30"), Decimal("5e25")),
	Item("000006", "Autobiography Book", Decimal("5e39"), Decimal("5e33")),
	Item("000007", "Biography Book", Decimal("5e49"), Decimal("5e42")),
	Item("000008", "Trilogy Book", Decimal("5e60"), Decimal("5e52")),
	Item("000009", "Series", Decimal("5e72"), Decimal("5e63")),
	Item("000010", "Prayer Book", Decimal("5e85"), Decimal("5e75")),
	Item("000011", "Journal", Decimal("5e99"), Decimal("5e88")),
	Item("000012", "Diary", Decimal("5e114"), Decimal("5e102")),
	Item("000013", "Cookbook", Decimal("5e130"), Decimal("5e117")),
	Item("000014", "Art Book", Decimal("5e147"), Decimal("5e133")),
	Item("000015", "Comic", Decimal("5e165"), Decimal("5e150")),
	Item("000016", "Dictionary", Decimal("5e184"), Decimal("5e168")),
	Item("000017", "Encyclopaedia", Decimal("5e204"), Decimal("5e187")),
	Item("000018", "Poetry Book", Decimal("5e225"), Decimal("5e207")),
	Item("000019", "Anthology Book", Decimal("5e247"), Decimal("5e228")),
	Item("000020", "Math Book", Decimal("5e270"), Decimal("5e250")),
	Item("000021", "History Book", Decimal("5e294"), Decimal("5e273")),
	Item("000022", "Science Book", Decimal("5e319"), Decimal("5e297")),
	Item("000023", "Information and Technology Book", Decimal("5e345"), Decimal("5e322")),
	Item("000024", "Religion Book", Decimal("5e372"), Decimal("5e348")),
	Item("000025", "Music Book", Decimal("5e400"), Decimal("5e375")),
	Item("000026", "Travel Book", Decimal("5e429"), Decimal("5e403")),
	Item("000027", "Sports Book", Decimal("5e459"), Decimal("5e432")),
	Item("000028", "Automotive Book", Decimal("5e490"), Decimal("5e462")),
	Item("000029", "Architecture Book", Decimal("5e522"), Decimal("5e493")),
	Item("000030", "Guide Book", Decimal("5e555"), Decimal("5e525")),
	Item("000031", "Self Help Book", Decimal("5e589"), Decimal("5e558")),
	Item("000032", "Horror Book", Decimal("5e624"), Decimal("5e592")),
	Item("000033", "Mystery Book", Decimal("5e660"), Decimal("5e627")),
	Item("000034", "Romance Book", Decimal("5e697"), Decimal("5e663")),
	Item("000035", "Action and Adventure Book", Decimal("5e735"), Decimal("5e700")),
	Item("000036", "Drama Book", Decimal("5e774"), Decimal("5e738")),
	Item("000037", "Satire Book", Decimal("5e814"), Decimal("5e777")),
	Item("000038", "Science Fiction Book", Decimal("5e855"), Decimal("5e817"))
]


def main():
	"""
	This function is used to run the program.
	:return:
	"""
	
	new_library: Library = Library(items, None)
	print("Enter Y for yes.")
	print("Enter anything else for no.")
	filename: str = "Saved Library Tycoon Progress"
	load_ask: str = input("Do you want to load game progress? ")
	if load_ask == "Y":
		saved: Library = pickle.load(open(filename, "rb"))
		new_library = saved
		print("Current library data: ", new_library.to_string())
	else:
		name: str = input("Please enter your name: ")
		new_player: Player = Player(name)
		new_library = Library(items, new_player)
		
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
		for item in new_library.items:
			item.produce_resources(new_library.manager, seconds)
			
		print("Type 1 to activate an item.")
		print("Type 2 to level up an item.")
		print("Type 3 to see your library status.")
		print("Type 4 to save and quit.")
		option: int = int(input("Please enter a number: "))
		while option < 1 or option > 4:
			option = int(input("Sorry, invalid input! Please enter a number: "))
			
		if option == 1:
			item_index: int = int(input("Please enter index of item that you want to activate: "))
			while item_index < 0 or item_index >= len(new_library.items):
				item_index = int(input("Please enter index of item that you want to activate: "))
				
			to_be_activated: Item = new_library.items[item_index]
			to_be_activated.activate(new_library.manager)
			
		elif option == 2:
			item_index: int = int(input("Please enter index of item that you want to activate: "))
			while item_index < 0 or item_index >= len(new_library.items):
				item_index = int(input("Please enter index of item that you want to activate: "))
				
			to_be_upgraded: Item = new_library.items[item_index]
			to_be_upgraded.level_up(new_library.manager)
			
		elif option == 3:
			print(new_library.to_string())
			
		elif option == 4:
			pickle.dump(new_library, open(filename, "wb"))
			sys.exit()
			
		cont = input("Do you want to continue playing? ")
		
	pickle.dump(new_library, open(filename, "wb"))
	sys.exit()
	
	
main()
