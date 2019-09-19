import sys
import random
import pickle
import copy

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


class Player:
	"""
	This class contains attributes of the player in the game.
	"""
	
	def __init__(self, name):
		self.name = name
		self.level = 1
		self.curr_hp = Decimal("4.5e4")
		self.max_hp = self.curr_hp
		self.attack = Decimal("1.1e4")
		self.defense = Decimal("7.6e3")
		
	def level_up(self):
		self.level += 1
		self.max_hp *= 2
		self.curr_hp = self.max_hp
		self.attack *= 2
		self.defense *= 2
		
	def stats(self):
		print("Name: ", self.name)
		print("Level: ", self.level)
		print("HP: " + str(self.curr_hp) + "/" + str(self.max_hp))
		print("Attack: ", self.attack)
		print("Defense: ", self.defense)
		
		
class Enemy:
	"""
	This class contains attributes of the enemy in the game.
	"""
	
	def __init__(self, name):
		self.name = name
		self.level = 1
		self.curr_hp = Decimal("5e4")
		self.max_hp = self.curr_hp
		self.attack = Decimal("1e4")
		self.defense = Decimal("8e3")
		
	def level_up(self):
		self.level += 1
		self.max_hp *= 2
		self.curr_hp = self.max_hp
		self.attack *= 2
		self.defense *= 2
		
	def stats(self):
		print("Name: ", self.name)
		print("Level: ", self.level)
		print("HP: " + str(self.curr_hp) + "/" + str(self.max_hp))
		print("Attack: ", self.attack)
		print("Defense: ", self.defense)
		
		
def main():
	"""
	This function is used to run the game.
	"""
	name = input("Please enter your name: ")
	player = Player(name)
	enemy = Enemy("COM")
	
	while True:
		turn = 1
		while player.curr_hp > 0 and enemy.curr_hp > 0:
			if turn % 2 == 1:
				print("Enter ATTACK to attack.")
				print("Enter anything else to quit.")
				action = input("What do you want to do? ")
				if action == "ATTACK":
					enemy.curr_hp -= player.attack - enemy.defense
				else:
					sys.exit()
					
			else:
				print("You are under attack.")
				player.curr_hp -= enemy.attack - player.defense
				
			print("Your current stats: ")
			player.stats()
			print("Your enemy's stats: ")
			enemy.stats()
			turn += 1
			if player.curr_hp <= 0:
				print("GAME OVER! " + str(player.name).upper() + " DIED.")
				sys.exit()
				
			elif enemy.curr_hp < 0:
				print("You won the battle.")
				level_ups_player = random.randint(1, 100)
				level_ups_enemy = random.randint(1, 100)
				for i in range(level_ups_player):
					player.level_up()
					
				for i in range(level_ups_enemy):
					enemy.level_up()
	
	
main()
