# The names of battlefields and characters in this game are randomly generated using the random generator in the link
# below.
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
    This class contains data of a battle which takes place in this game.
    """
    battle_number: int = 0

    def __init__(self):
        # type: () -> None
        self.battle_number += 1
        BattleRecord.battle_number += 1
        self.kills: int = 0
        self.assists: int = 0
        self.times_died: int = 0
        self.rating: float = self.calculate_rating()

    def calculate_rating(self):
        # type: () -> float
        self.rating = 6.0 + 0.5 * self.kills + 0.5 * self.assists - 0.5 * self.times_died
        return self.rating

    def increment_kills(self):
        # type: () -> None
        self.kills += 1

    def increment_assists(self):
        # type: () -> None
        self.assists += 1

    def increment_times_died(self):
        # type: () -> None
        self.times_died += 1

    def to_string(self):
        # type: () -> str
        res = ""  # initial value
        res += "Battle #" + str(self.battle_number) + "\n"
        res += "Number of kills: " + str(self.kills) + "\n"
        res += "Number of assists: " + str(self.assists) + "\n"
        res += "Number of times dies: " + str(self.times_died) + "\n"
        res += "Rating: " + str(self.calculate_rating()) + "\n"
        return res


class Battle:
    """
    This class contains attributes of battles in this game.
    """

    def __init__(self, player, ai, battlefield):
        # type: (Player, AI, Battlefield) -> None
        self.player: Player = player
        self.ai: AI = ai
        self.battlefield: Battlefield = battlefield
        self.turn: int = 0  # initial value
        self.starter: Player or None = None  # initial value
        self.whose_turn: Player or None = None  # initial value
        self.is_finished: bool = False  # initial value
        self.winner: Player or None = None  # initial value

    def get_mvp(self):
        # type: () -> Character or Transport or Building or None
        """
        This function is used to get the most valuable participant in the battle.
        :return:
        """
        if self.is_finished:
            # Looking for the value of the highest rating
            participants_and_ratings: dict = {}  # initial value
            for character in self.player.deck.characters:
                participants_and_ratings[character] = character.battle_records[-1].calculate_rating()

            for transport in self.player.deck.transports:
                participants_and_ratings[transport] = transport.battle_records[-1].calculate_rating()

            for building in self.player.deck.transports:
                participants_and_ratings[building] = building.battle_records[-1].calculate_rating()

            for character in self.ai.deck.characters:
                participants_and_ratings[character] = character.battle_records[-1].calculate_rating()

            for transport in self.ai.deck.transports:
                participants_and_ratings[transport] = transport.battle_records[-1].calculate_rating()

            for building in self.ai.deck.transports:
                participants_and_ratings[building] = building.battle_records[-1].calculate_rating()

            participants: list = [i for i in participants_and_ratings.keys()]
            ratings: list = [i for i in participants_and_ratings.values()]
            highest_rating: float = max(ratings)
            for participant in participants:
                if participants_and_ratings[participant] == highest_rating:
                    return participant

            return None  # Unreachable code
        return None

    def to_string(self):
        # type: () -> str
        res = ""  # initial value
        res += "Player: \n"
        res += str(self.player.to_string()) + "\n"
        res += "AI: \n"
        res += str(self.ai.to_string()) + "\n"
        res += "Turn #" + str(self.turn) + "\n"
        return res

    def respawn_character(self, character):
        # type: (Character) -> None
        """
        This function is used to respawn a character that died in the battlefield.
        :param character:
        :return:
        """
        assert isinstance(character, Character), "'character' must be a Character class object."
        if character in self.player.deck.characters:
            # Respawn the character at the left side of the battlefield
            character.respawn(Position(random.randint(0, self.battlefield.width / 2), random.randint(0,
                                                                                                     self.battlefield.height - 1)))
        elif character in self.ai.deck.characters:
            # Respawn the character at the right side of the battlefield
            character.respawn(
                Position(random.randint(self.battlefield.width / 2, self.battlefield.width - 1), random.randint(0,
                                                                                                                self.battlefield.height - 1)))

    def respawn_transport(self, transport):
        # type: (Transport) -> None
        """
        This function is used to respawn a transport that died in the battlefield.
        :param transport:
        :return:
        """
        assert isinstance(transport, Transport), "'transport' must be a Transport class object."
        if transport in self.player.deck.transports:
            # Respawn the transport at the left side of the battlefield
            transport.respawn(Position(random.randint(0, self.battlefield.width / 2), random.randint(0,
                                                                                                     self.battlefield.height - 1)))
        elif transport in self.ai.deck.transports:
            # Respawn the transport at the right side of the battlefield
            transport.respawn(
                Position(random.randint(self.battlefield.width / 2, self.battlefield.width - 1), random.randint(0,
                                                                                                                self.battlefield.height - 1)))

    def get_starter(self):
        # type: () -> Player
        self.starter = self.player if random.random() <= 0.5 else self.ai
        return self.starter

    def get_whose_turn(self):
        # type: () -> Player
        self.turn += 1
        if self.starter == self.player:
            self.whose_turn = self.player if self.turn % 2 == 1 else self.ai
        else:
            self.whose_turn = self.ai if self.turn % 2 == 1 else self.player

        return self.whose_turn

    def end_battle(self):
        # type: () -> None
        # Ending the battle once there is a winner
        if self.is_finished:
            # Restoring the levels of everything in the decks brought to the battle and clearing runes from the
            # characters brought to the battle
            for character in self.player.deck.characters:
                character.clear_runes()
                character.restore_level()

            for transport in self.player.deck.transports:
                transport.restore_level()

            for building in self.player.deck.buildings:
                building.restore_level()

            for character in self.ai.deck.characters:
                character.clear_runes()
                character.restore_level()

            for transport in self.ai.deck.transports:
                transport.restore_level()

            for building in self.ai.deck.buildings:
                building.restore_level()

            # Giving rewards to the winner of the battle
            if self.winner == self.player:
                self.player.exp += Decimal("10") ** ((self.player.level + self.ai.level) ** 2)
                self.player.level_up()
                self.player.coins += Decimal("10") ** ((self.player.level + self.ai.level) ** 2)
                self.player.diamonds += Decimal("10") ** (self.player.level + self.ai.level)
            else:
                self.ai.exp += Decimal("10") ** ((self.player.level + self.ai.level) ** 2)
                self.ai.level_up()
                self.ai.coins += Decimal("10") ** ((self.player.level + self.ai.level) ** 2)
                self.ai.diamonds += Decimal("10") ** (self.player.level + self.ai.level)

    def clone(self):
        # type: () -> Battle
        return copy.deepcopy(self)


class Position:
    """
    This class is used to initialise positions in this game.
    """

    def __init__(self, x, y):
        # type: (int, int) -> None
        self.x: int = x
        self.y: int = y

    def calc_dist(self, other):
        # type: (Position) -> int
        return abs(self.x - other.x) + abs(self.y - other.y)

    def to_string(self):
        # type: () -> str
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def clone(self):
        # type: () -> Position
        return copy.deepcopy(self)


class Character:
    """
    This class is used to initialise characters used in battles in this game.
    """
    MIN_CRIT_RATE: float = 0.15
    MAX_CRIT_RATE: float = 1
    MIN_CRIT_DAMAGE: float = 2

    def __init__(self, character_id, name, character_type, character_class, max_hp, attack, defense, attack_speed,
                 max_magic_points, max_energy, crit_rate, crit_damage, attacking_range, max_moving_distance,
                 curr_battle,
                 battlefield, skills, special_powers, corresponding_deck,
                 position):
        # type: (str, str, CharacterType, CharacterClass, Decimal, Decimal, Decimal, int or float, Decimal, Decimal, float, float, int, int, Battle, Battlefield, list, list, Deck or None, Position) -> None
        self.character_id: str = character_id
        self.name: str = name
        self.character_type: CharacterType = character_type
        self.character_class: CharacterClass = character_class
        self.level: int = 1  # This is the level of the character whenever it starts a battle
        self.exp: Decimal = Decimal("0e0")
        self.required_exp: Decimal = Decimal("1e6")
        self.curr_hp: Decimal = max_hp
        self.max_hp: Decimal = max_hp
        self.attack: Decimal = attack
        self.defense: Decimal = defense
        self.attack_speed: int or float = attack_speed
        self.max_magic_points: Decimal = max_magic_points
        self.curr_magic_points: Decimal = max_magic_points
        self.max_energy: Decimal = max_energy
        self.curr_energy: Decimal = max_energy
        self.crit_rate: float = crit_rate if self.MIN_CRIT_RATE <= crit_rate <= self.MAX_CRIT_RATE else \
            self.MIN_CRIT_RATE if crit_rate < self.MIN_CRIT_RATE else self.MAX_CRIT_RATE
        self.crit_damage: float = crit_damage if self.crit_damage >= self.MIN_CRIT_DAMAGE else self.MIN_CRIT_DAMAGE
        self.attacking_range: int = attacking_range
        self.max_moving_distance: int = max_moving_distance
        self.curr_battle: Battle = curr_battle
        self.battlefield: Battlefield = battlefield
        self.skills: list = skills  # a list of Skill class objects
        self.special_powers: list = special_powers  # a list of SpecialPower class objects
        self.position: Position = position
        self.researches_applied: list = []  # initial value
        self.has_moved: bool = False
        self.corresponding_deck: Deck = corresponding_deck
        self.runes: list = []  # initial value whenever the character enters a battle
        self.battle_records: list = []  # initial value
        self.attackers: list = []  # a list of attackers used to indicate who is doing the assist and the kill
        self.strength: Decimal = self.calculate_strength()

    def attack(self, skill_used, special_power, target):
        # type: (Skill or None, SpecialPower or None, Character or Transport or Building) -> bool
        if self.has_moved:
            if self.position.calc_dist(target.position) <= self.attacking_range and skill_used.does_attack:
                multiplier: float = self.crit_damage if random.random() <= self.crit_rate else 1
                num_allies_deaths: int = 0  # initial value
                for character in self.corresponding_deck.characters:
                    num_allies_deaths += character.battle_records[-1].times_died

                for transport in self.corresponding_deck.transports:
                    num_allies_deaths += transport.battle_records[-1].times_died

                for building in self.corresponding_deck.buildings:
                    num_allies_deaths += building.battle_records[-1].times_died

                num_enemies_deaths: int = 0  # initial value
                for character in target.corresponding_deck.characters:
                    num_enemies_deaths += character.battle_records[-1].times_died

                for transport in target.corresponding_deck.transports:
                    num_enemies_deaths += transport.battle_records[-1].times_died

                for building in target.corresponding_deck.buildings:
                    num_enemies_deaths += building.battle_records[-1].times_died

                self_current_hp_percentage: float = self.curr_hp/self.max_hp * 100
                self_hp_percentage_loss: float = 100 - self_current_hp_percentage
                enemy_current_hp_percentage: float = target.curr_hp/target.max_hp * 100
                enemy_hp_percentage_loss: float = 100 - enemy_current_hp_percentage

                raw_damage: Decimal = self.max_hp * skill_used.damage_multiplier_to_self_max_hp + target.max_hp * \
                             skill_used.damage_multiplier_to_enemies_max_hp + self.attack * \
                             (
                                         skill_used.damage_multiplier_to_self_attack + skill_used.damage_multiplier_to_self_attack_speed) + \
                             self.defense * skill_used.damage_multiplier_to_self_defense + \
                             self.max_magic_points * skill_used.damage_multiplier_to_self_max_magic_points + \
                             self.max_energy * skill_used.damage_multiplier_to_self_max_energy * (num_allies_deaths *
                             skill_used.damage_multiplier_to_number_of_allies_deaths) * (num_enemies_deaths *
                             skill_used.damage_multiplier_to_number_of_enemies_deaths) * (self.curr_battle.turn *
                             skill_used.damage_multiplier_to_number_of_turns) * (self_hp_percentage_loss *
                             skill_used.damage_percentage_up_per_self_hp_percentage_loss) * (self_current_hp_percentage *
                             skill_used.damage_percentage_up_per_self_current_hp_percentage) * (enemy_hp_percentage_loss *
                             skill_used.damage_percentage_up_per_enemies_hp_percentage_loss) * (enemy_current_hp_percentage *
                             skill_used.damage_percentage_up_per_enemies_current_hp_percentage) * multiplier if skill_used is not None else \
                self.max_hp * special_power.damage_multiplier_to_self_max_hp + target.max_hp * \
                special_power.damage_multiplier_to_enemies_max_hp + self.attack * \
                (
                        special_power.damage_multiplier_to_self_attack + special_power.damage_multiplier_to_self_attack_speed) + \
                self.defense * special_power.damage_multiplier_to_self_defense + \
                self.max_magic_points * special_power.damage_multiplier_to_self_max_magic_points + \
                self.max_energy * special_power.damage_multiplier_to_self_max_energy * (num_allies_deaths *
                                                                                     special_power.damage_multiplier_to_number_of_allies_deaths) * (
                            num_enemies_deaths *
                            special_power.damage_multiplier_to_number_of_enemies_deaths) * (self.curr_battle.turn *
                                                                                         special_power.damage_multiplier_to_number_of_turns) * (
                            self_hp_percentage_loss *
                            special_power.damage_percentage_up_per_self_hp_percentage_loss) * (self_current_hp_percentage *
                                                                                            special_power.damage_percentage_up_per_self_current_hp_percentage) * (
                            enemy_hp_percentage_loss *
                            special_power.damage_percentage_up_per_enemies_hp_percentage_loss) * (enemy_current_hp_percentage *
                            special_power.damage_percentage_up_per_enemies_current_hp_percentage) * multiplier if special_power is not None else self.attack * multiplier
                damage: Decimal = raw_damage if ((skill_used is not None and skill_used.does_ignore_enemies_defense) or
                                        (special_power is not None and special_power.does_ignore_enemies_defense)) \
                    else raw_damage - target.defense
                target.curr_hp -= damage
                target.attackers.append(self)
                if target.curr_hp <= 0:
                    target.battle_records[-1].times_died += 1
                    self.battle_records[-1].kills += 1.
                    if len(target.attackers) > 1:
                        target.attackers[-2].battle_records[-1].assists += 1

                    target.attackers = []
                    self.curr_battle.respawn_character(target)

                return True  # attack success

            return False

        return False  # attack failed

    def add_battle_record(self, battle_record):
        # type: (BattleRecord) -> None
        self.battle_records.append(battle_record)

    def respawn(self, position):
        # type: (Position) -> None
        if self.curr_hp <= 0:
            self.curr_hp = self.max_hp
            self.position = position

    def apply_research(self, research):
        # type: (Research) -> None
        self.max_hp *= 1 + research.character_max_hp_percentage_up
        self.attack *= 1 + research.character_attack_percentage_up
        self.defense *= 1 + research.character_defense_percentage_up
        self.attack_speed += research.character_attack_speed_percentage_up
        self.max_magic_points *= 1 + research.character_max_magic_points_percentage_up
        self.max_energy *= 1 + research.character_max_energy_percentage_up
        self.researches_applied.append(research)

    def add_rune(self, rune):
        # type: (Rune) -> None
        self.runes.append(rune)
        self.max_hp += rune.max_hp_up
        self.max_hp *= 1 + rune.max_hp_percentage_up / 100
        self.attack += rune.attack_up
        self.attack *= 1 + rune.attack_percentage_up / 100
        self.defense += rune.defense_up
        self.defense *= 1 + rune.defense_percentage_up / 100
        self.attack_speed += rune.attack_speed_up
        self.max_magic_points += rune.max_magic_points_up
        self.max_magic_points *= 1 + rune.max_magic_points_percentage_up
        self.max_energy += rune.max_energy_up
        self.max_energy *= 1 + rune.max_energy_percentage_up
        self.crit_rate += rune.crit_rate_up
        self.crit_damage += rune.crit_damage_up

    def remove_rune(self, rune):
        # type: (Rune) -> bool
        if rune in self.runes:
            self.runes.remove(rune)
            self.max_hp -= rune.max_hp_up
            self.max_hp /= 1 + rune.max_hp_percentage_up / 100
            self.attack -= rune.attack_up
            self.attack /= 1 + rune.attack_percentage_up / 100
            self.defense -= rune.defense_up
            self.defense /= 1 + rune.defense_percentage_up / 100
            self.attack_speed -= rune.attack_speed_up
            self.max_magic_points -= rune.max_magic_points_up
            self.max_magic_points /= 1 + rune.max_magic_points_percentage_up
            self.max_energy -= rune.max_energy_up
            self.max_energy /= 1 + rune.max_energy_percentage_up
            self.crit_rate -= rune.crit_rate_up
            self.crit_damage -= rune.crit_damage_up
            return True

        return False

    def clear_runes(self):
        # type: () -> None
        for rune in self.runes:
            self.remove_rune(rune)

    def level_up(self):
        # type: () -> None
        while self.exp >= self.required_exp:
            self.level += 1
            self.required_exp *= 10 ** (self.level ** 2)
            self.max_hp *= self.level ** 2
            self.curr_hp = self.max_hp
            self.attack *= self.level ** 2
            self.defense *= self.level ** 2
            self.max_magic_points *= self.level ** 2
            self.curr_magic_points = self.max_magic_points
            self.max_energy *= self.level ** 2
            self.curr_energy = self.max_energy

    def __level_down(self):
        # type: () -> None
        self.required_exp /= 10 ** (self.level ** 2)
        self.max_hp /= self.level ** 2
        self.curr_hp = self.max_hp
        self.attack /= self.level ** 2
        self.defense /= self.level ** 2
        self.max_magic_points /= self.level ** 2
        self.curr_magic_points = self.max_magic_points
        self.max_energy /= self.level ** 2
        self.curr_energy = self.max_energy
        self.level -= 1

    def restore_level(self):
        # type: () -> None
        while self.level > 1:
            self.__level_down()

    def move(self, destination_pos):
        # type: (Position) -> bool
        if self.has_moved is False:
            if 0 <= destination_pos.x >= 0 < self.battlefield.width and 0 <= destination_pos.y < self.battlefield.height:
                if isinstance(self.battlefield.tiles[destination_pos.y][destination_pos.x],
                              Land) and 0 <= self.position.calc_dist(destination_pos) <= self.max_moving_distance:
                    self.position = destination_pos
                    self.has_moved = True
                    return True

                return False

            return False

        return False

    def enter_transport(self, transport):
        # type: (Transport) -> bool
        if self.position == transport.position:
            return transport.place_character(self)

        return False

    def exit_transport(self, transport):
        # type: (Transport) -> bool
        if self.position == transport.position:
            return transport.remove_character(self)

        return False

    def calculate_strength(self):
        # type: () -> Decimal
        self.strength = Decimal(5 * (self.max_hp + self.attack + self.defense + self.max_magic_points +
                                     self.max_energy)) * self.attack_speed * (1 + (100 * self.crit_rate)) * (
                                1 + (100 * self.crit_damage)) * \
                        self.attacking_range * self.max_moving_distance
        return self.strength

    def clone(self):
        # type: () -> Character
        return copy.deepcopy(self)


class WildCharacter(Character):
    """
    This class contains attributes of wild characters randomly spawned in battlefields.
    """

    def __init__(self, character_id, name, character_type, character_class, max_hp, attack, defense, attack_speed,
                 max_magic_points, max_energy, crit_rate, crit_damage, attacking_range, max_moving_distance,
                 curr_battle,
                 battlefield, skills, special_powers, corresponding_deck,
                 position):
        # type: (str, str, CharacterType, CharacterClass, Decimal, Decimal, Decimal, int or float, Decimal, Decimal, float, float, int, int, Battle, Battlefield, list, list, Deck or None, Position) -> None
        super(WildCharacter, self).__init__(character_id, name, character_type, character_class, max_hp, attack, defense, attack_speed,
                 max_magic_points, max_energy, crit_rate, crit_damage, attacking_range, max_moving_distance,
                 curr_battle,
                 battlefield, skills, special_powers, corresponding_deck,
                 position)
        self.corresponding_deck = None
        self.position = Position(random.randint(0, self.battlefield.width - 1), random.randint(0,
            self.battlefield.height - 1))


class CharacterType:
    """
    This class contains attributes of types of characters in this game.
    """
    POSSIBLE_TYPES = ["HERO", "LEGENDARY CREATURE", "HUMAN"]

    def __init__(self, value):
        # type: (str) -> None
        self.value = value if value in self.POSSIBLE_TYPES else None

    def clone(self):
        # type: () -> CharacterType
        return copy.deepcopy(self)


class CharacterClass:
    """
    This class contains attributes of classes of characters.
    """
    POSSIBLE_CLASSES = ["LIGHT INFANTRY", "HEAVY INFANTRY", "CAVALRY", "ARCHER", "SIEGE"]

    def __init__(self, value):
        # type: (str) -> None
        self.value = value if value in self.POSSIBLE_CLASSES else None

    def clone(self):
        # type: () -> CharacterClass
        return copy.deepcopy(self)


class Skill:
    """
    This class is used to initialise skills that characters have.
    """

    def __init__(self, skill_id, name, description, max_level, does_attack, does_heal_self, does_heal_allies,
                 does_ignore_enemies_defense, heal_amount_to_self, heal_amount_to_allies, magic_points_cost,
                 energy_cost, damage_multiplier_to_self_max_hp,
                 damage_multiplier_to_enemies_max_hp, damage_multiplier_to_self_attack,
                 damage_multiplier_to_self_defense, damage_multiplier_to_self_attack_speed,
                 damage_multiplier_to_self_max_magic_points, damage_multiplier_to_self_max_energy,
                 damage_multiplier_to_number_of_allies_deaths, damage_multiplier_to_number_of_enemies_deaths,
                 damage_multiplier_to_number_of_turns,
                 damage_percentage_up_per_self_hp_percentage_loss, damage_percentage_up_per_self_current_hp_percentage,
                 damage_percentage_up_per_enemies_hp_percentage_loss,
                 damage_percentage_up_per_enemies_current_hp_percentage, skill_level_up_bonus, max_cooltime):
        # type: (str, str, str, int, bool, bool, bool, bool, Decimal, Decimal, Decimal, Decimal, float, float, float, float, float, float, float, float, float, float, float, float, float, float, SkillLevelUpBonus, int) -> None
        self.skill_id: str = skill_id
        self.name: str = name
        self.description: str = description
        self.level: int = 1
        self.max_level: int = max_level
        self.does_attack: bool = does_attack
        self.does_heal_self: bool = does_heal_self
        self.does_heal_allies: bool = does_heal_allies
        self.does_ignore_enemies_defense: bool = does_ignore_enemies_defense
        self.heal_amount_to_self: Decimal = heal_amount_to_self
        self.heal_amount_to_allies: Decimal = heal_amount_to_allies
        self.magic_points_cost: Decimal = magic_points_cost
        self.energy_cost: Decimal = energy_cost
        self.damage_multiplier_to_self_max_hp: float = damage_multiplier_to_self_max_hp
        self.damage_multiplier_to_enemies_max_hp: float = damage_multiplier_to_enemies_max_hp
        self.damage_multiplier_to_self_attack: float = damage_multiplier_to_self_attack
        self.damage_multiplier_to_self_defense: float = damage_multiplier_to_self_defense
        self.damage_multiplier_to_self_attack_speed = damage_multiplier_to_self_attack_speed
        self.damage_multiplier_to_self_max_magic_points: float = damage_multiplier_to_self_max_magic_points
        self.damage_multiplier_to_self_max_energy: float = damage_multiplier_to_self_max_energy
        self.damage_multiplier_to_number_of_allies_deaths: float = damage_multiplier_to_number_of_allies_deaths
        self.damage_multiplier_to_number_of_enemies_deaths: float = damage_multiplier_to_number_of_enemies_deaths
        self.damage_multiplier_to_number_of_turns: float = damage_multiplier_to_number_of_turns
        self.damage_percentage_up_per_self_hp_percentage_loss: float = damage_percentage_up_per_self_hp_percentage_loss
        self.damage_percentage_up_per_self_current_hp_percentage: float = damage_percentage_up_per_self_current_hp_percentage
        self.damage_percentage_up_per_enemies_hp_percentage_loss: float = damage_percentage_up_per_enemies_hp_percentage_loss
        self.damage_percentage_up_per_enemies_current_hp_percentage: float = \
            damage_percentage_up_per_enemies_current_hp_percentage
        self.skill_level_up_bonus: SkillLevelUpBonus = skill_level_up_bonus
        self.cooltime: int = max_cooltime
        self.max_cooltime: int = max_cooltime

    def clone(self):
        # type: () -> Skill
        return copy.deepcopy(self)


class SkillLevelUpBonus:
    """
    This class contains attributes of levelling up skills.
    """

    def __init__(self, damage_percentage_up, heal_amount_percentage_up, revival_amount_percentage_up,
                 magic_points_cost_percentage_down, energy_cost_percentage_down):
        # type: (float, float, float, float, float) -> None
        self.damage_percentage_up: float = damage_percentage_up
        self.heal_amount_percentage_up: float = heal_amount_percentage_up
        self.revival_amount_percentage_up: float = revival_amount_percentage_up
        self.magic_points_cost_percentage_down: float = magic_points_cost_percentage_down
        self.energy_cost_percentage_down: float = energy_cost_percentage_down

    def clone(self):
        # type: () -> SkillLevelUpBonus
        return copy.deepcopy(self)


class Battlefield:
    """
    This class contains attributes of battlefields in this game.
    """

    def __init__(self, height, width, battlefield_shop):
        # type: (int, int, BattlefieldShop) -> None
        self.height: int = height
        self.width: int = width
        self.tiles: list = []
        for i in range(self.height):
            new: list = []  # initial value
            for j in range(self.width):
                new.append(Tile())

            self.tiles.append(new)

        self.battlefield_shop: BattlefieldShop = battlefield_shop

    def clone(self):
        # type: () -> Battlefield
        return copy.deepcopy(self)


class Transport:
    """
    This class is used to initialise transports used in battles in this game.
    """
    MIN_CRIT_RATE: float = 0.15
    MAX_CRIT_RATE: float = 1
    MIN_CRIT_DAMAGE: float = 2

    def __init__(self, character_id, name, max_hp, attack, defense, attack_speed, max_magic_points, max_energy,
                 crit_rate, crit_damage, attacking_range, max_moving_distance, battlefield, curr_battle,
                 corresponding_deck, position):
        # type: (str, str, Decimal, Decimal, Decimal, int or float, Decimal, Decimal, float, float, int, int, Battlefield, Battle, Deck or None, Position) -> None
        self.character_id: str = character_id
        self.name: str = name
        self.transport_type: TransportType or None = None
        self.description: str or None = None
        self.level: int = 1  # This is the level of the transport whenever it starts a battle
        self.exp: Decimal = Decimal("0e0")
        self.required_exp: Decimal = Decimal("1e6")
        self.curr_hp: Decimal = max_hp
        self.max_hp: Decimal = max_hp
        self.attack: Decimal = attack
        self.defense: Decimal = defense
        self.attack_speed: int or float = attack_speed
        self.max_magic_points: Decimal = max_magic_points
        self.curr_magic_points: Decimal = max_magic_points
        self.max_energy: Decimal = max_energy
        self.curr_energy: Decimal = max_energy
        self.crit_rate: float = crit_rate if self.MIN_CRIT_RATE <= crit_rate <= self.MAX_CRIT_RATE else \
            self.MIN_CRIT_RATE if crit_rate < self.MIN_CRIT_RATE else self.MAX_CRIT_RATE
        self.crit_damage: float = crit_damage if self.crit_damage >= self.MIN_CRIT_DAMAGE else self.MIN_CRIT_DAMAGE
        self.attacking_range: int = attacking_range
        self.max_moving_distance: int = max_moving_distance
        self.battlefield: Battlefield = battlefield
        self.curr_battle: Battle = curr_battle
        self.corresponding_deck: Deck or None = corresponding_deck
        self.position: Position = position
        self.researches_applied: list = []  # initial value
        self.characters_placed: list = []  # initial value
        self.battle_records: list = []  # initial value
        self.attackers: list = []  # a list of attackers used to indicate who is doing the assist and the kill
        self.can_be_placed: bool = False
        self.has_moved: bool = False
        self.strength: Decimal = self.calculate_strength()

    def respawn(self, position):
        # type: (Position) -> None
        if self.curr_hp <= 0:
            self.curr_hp = self.max_hp
            self.position = position

    def attack(self, target):
        # type: (Character or Transport or Building) -> bool
        if self.position.calc_dist(target.position) <= self.attacking_range:
            multiplier: float = self.crit_damage if random.random() <= self.crit_rate else 1
            damage: Decimal = self.attack * multiplier - target.defense
            target.curr_hp -= damage
            target.attackers.append(self)
            if target.curr_hp <= 0:
                target.battle_records[-1].times_died += 1
                self.battle_records[-1].kills += 1.
                if len(target.attackers) > 1:
                    target.attackers[-2].battle_records[-1].assists += 1

                target.attackers = []
                self.curr_battle.respawn_character(target)

            return True  # attack success

        return False  # attack failed

    def add_battle_record(self, battle_record):
        # type: (BattleRecord) -> None
        self.battle_records.append(battle_record)

    def apply_research(self, research):
        # type: (Research) -> None
        self.max_hp *= 1 + research.transport_max_hp_percentage_up
        self.attack *= 1 + research.transport_attack_percentage_up
        self.defense *= 1 + research.transport_defense_percentage_up
        self.attack_speed += research.transport_attack_speed_percentage_up
        self.max_magic_points *= 1 + research.transport_max_magic_points_percentage_up
        self.max_energy *= 1 + research.transport_max_energy_percentage_up
        self.researches_applied.append(research)

    def level_up(self):
        # type: () -> None
        while self.exp >= self.required_exp:
            self.level += 1
            self.required_exp *= 10 ** (self.level ** 2)
            self.max_hp *= self.level ** 2
            self.curr_hp = self.max_hp
            self.attack *= self.level ** 2
            self.defense *= self.level ** 2
            self.max_magic_points *= self.level ** 2
            self.curr_magic_points = self.max_magic_points
            self.max_energy *= self.level ** 2
            self.curr_energy = self.max_energy

    def __level_down(self):
        # type: () -> None
        self.required_exp /= 10 ** (self.level ** 2)
        self.max_hp /= self.level ** 2
        self.curr_hp = self.max_hp
        self.attack /= self.level ** 2
        self.defense /= self.level ** 2
        self.max_magic_points /= self.level ** 2
        self.curr_magic_points = self.max_magic_points
        self.max_energy /= self.level ** 2
        self.curr_energy = self.max_energy
        self.level -= 1

    def restore_level(self):
        # type: () -> None
        while self.level > 1:
            self.__level_down()

    def move(self, destination_pos):
        # type: (Position) -> bool
        if self.has_moved is False:
            if 0 <= destination_pos.x >= 0 < self.battlefield.width and 0 <= destination_pos.y < self.battlefield.height:
                if isinstance(self.battlefield.tiles[destination_pos.y][destination_pos.x],
                              Land) and 0 <= self.position.calc_dist(destination_pos) <= self.max_moving_distance:
                    self.position = destination_pos
                    self.has_moved = True
                    return True

                return False

            return False

        return False

    def place_character(self, character):
        # type: (Character) -> None
        self.characters_placed.append(character)
        self.max_hp += character.max_hp
        self.curr_hp = self.max_hp
        self.attack += character.attack
        self.defense += character.defense
        self.max_magic_points += character.max_magic_points
        self.max_energy += character.max_energy
        self.strength = self.calculate_strength()

    def remove_character(self, character):
        # type: (Character) -> None
        if character in self.characters_placed:
            self.characters_placed.remove(character)
            self.max_hp -= character.max_hp
            self.curr_hp = self.max_hp
            self.attack -= character.attack
            self.defense -= character.defense
            self.max_magic_points -= character.max_magic_points
            self.max_energy -= character.max_energy
            self.strength = self.calculate_strength()

    def calculate_strength(self):
        # type: () -> Decimal
        self.strength = Decimal(5 * (self.max_hp + self.attack + self.defense + self.max_magic_points +
                                     self.max_energy)) * self.attack_speed * (1 + (100 * self.crit_rate)) * (
                                1 + (100 * self.crit_damage)) * \
                        self.attacking_range * self.max_moving_distance
        return self.strength

    def clone(self):
        # type: () -> Transport
        return copy.deepcopy(self)


class Ship(Transport):
    """
    This class contains attributes of ships in this game.
    """

    def __init__(self, character_id, name, max_hp, attack, defense, attack_speed, max_magic_points, max_energy,
                 crit_rate, crit_damage, attacking_range, max_moving_distance, battlefield, curr_battle,
                 corresponding_deck, position):
        # type: (str, str, Decimal, Decimal, Decimal, int or float, Decimal, Decimal, float, float, int, int, Battlefield, Battle, Deck or None, Position) -> None
        super(Ship, self).__init__(character_id, name, max_hp, attack, defense, attack_speed, max_magic_points, max_energy,
                 crit_rate, crit_damage, attacking_range, max_moving_distance, battlefield, curr_battle,
                 corresponding_deck, position)
        self.description: str = "SHIP"
        self.transport_type: TransportType or None = TransportType("WATER")
        self.can_be_placed: bool = isinstance(self.battlefield.tiles[self.position.y][self.position.x], Water)

    def move(self, destination_pos):
        # type: (Position) -> bool
        if self.has_moved is False:
            if 0 <= destination_pos.x >= 0 < self.battlefield.width and 0 <= destination_pos.y < self.battlefield.height:
                if isinstance(self.battlefield.tiles[destination_pos.y][destination_pos.x],
                              Water) and 0 <= self.position.calc_dist(destination_pos) <= self.max_moving_distance:
                    self.position = destination_pos
                    self.has_moved = True
                    return True

                return False

            return False

        return False


class Truck(Transport):
    """
    This class contains attributes of trucks in this game.
    """

    def __init__(self, character_id, name, max_hp, attack, defense, attack_speed, max_magic_points, max_energy,
                 crit_rate, crit_damage, attacking_range, max_moving_distance, battlefield, curr_battle,
                 corresponding_deck, position):
        # type: (str, str, Decimal, Decimal, Decimal, int or float, Decimal, Decimal, float, float, int, int, Battlefield, Battle, Deck or None, Position) -> None
        super(Truck, self).__init__(character_id, name, max_hp, attack, defense, attack_speed, max_magic_points, max_energy,
                 crit_rate, crit_damage, attacking_range, max_moving_distance, battlefield, curr_battle,
                 corresponding_deck, position)
        self.description: str = "TRUCK"
        self.transport_type: TransportType or None = TransportType("LAND")
        self.can_be_placed: bool = isinstance(self.battlefield.tiles[self.position.y][self.position.x], Land)


class Car(Transport):
    """
    This class contains attributes of cars in this game.
    """

    def __init__(self, character_id, name, max_hp, attack, defense, attack_speed, max_magic_points, max_energy,
                 crit_rate, crit_damage, attacking_range, max_moving_distance, battlefield, curr_battle,
                 corresponding_deck, position):
        # type: (str, str, Decimal, Decimal, Decimal, int or float, Decimal, Decimal, float, float, int, int, Battlefield, Battle, Deck or None, Position) -> None
        super(Car, self).__init__(character_id, name, max_hp, attack, defense, attack_speed, max_magic_points,
                                    max_energy,
                                    crit_rate, crit_damage, attacking_range, max_moving_distance, battlefield,
                                    curr_battle,
                                    corresponding_deck, position)
        self.description: str = "CAR"
        self.transport_type: TransportType or None = TransportType("LAND")
        self.can_be_placed: bool = isinstance(self.battlefield.tiles[self.position.y][self.position.x], Land)


class Motorcycle(Transport):
    """
    This class contains attributes of trucks in this game.
    """

    def __init__(self, character_id, name, max_hp, attack, defense, attack_speed, max_magic_points, max_energy,
                 crit_rate, crit_damage, attacking_range, max_moving_distance, battlefield, curr_battle,
                 corresponding_deck, position):
        # type: (str, str, Decimal, Decimal, Decimal, int or float, Decimal, Decimal, float, float, int, int, Battlefield, Battle, Deck or None, Position) -> None
        super(Motorcycle, self).__init__(character_id, name, max_hp, attack, defense, attack_speed, max_magic_points,
                                    max_energy,
                                    crit_rate, crit_damage, attacking_range, max_moving_distance, battlefield,
                                    curr_battle,
                                    corresponding_deck, position)
        self.description: str = "MOTORCYCLE"
        self.transport_type: TransportType or None = TransportType("LAND")
        self.can_be_placed: bool = isinstance(self.battlefield.tiles[self.position.y][self.position.x], Land)


class TransportType:
    """
    This class contains attributes of types of Transports in this game.
    """
    POSSIBLE_TYPES = ["LAND", "WATER"]

    def __init__(self, value):
        # type: (str) -> None
        self.value: str = value if value in self.POSSIBLE_TYPES else None

    def clone(self):
        # type: () -> TransportType
        return copy.deepcopy(self)


class Building:
    """
    This class contains attributes of buildings in this game.
    """
    MIN_CRIT_RATE: float = 0.15
    MAX_CRIT_RATE: float = 1
    MIN_CRIT_DAMAGE: float = 2

    def __init__(self, character_id, name, description, max_hp, attack, defense, attack_speed, max_magic_points,
                 max_energy,
                 crit_rate, crit_damage, attacking_range, battlefield, curr_battle, corresponding_deck, position):
        # type: (str, str, str, Decimal, Decimal, Decimal, float or int, Decimal, Decimal, float, float, int, Battlefield, Battle, Deck or None, Position) -> None
        self.character_id: str = character_id
        self.name: str = name
        self.description: str = description
        self.building_type: BuildingType or None = None
        self.level: int = 1  # This is the level of the building whenever it starts a battle
        self.exp: Decimal = Decimal("0e0")
        self.required_exp: Decimal = Decimal("1e6")
        self.curr_hp: Decimal = max_hp
        self.max_hp: Decimal = max_hp
        self.attack: Decimal = attack
        self.defense: Decimal = defense
        self.attack_speed: float or int = attack_speed
        self.max_magic_points: Decimal = max_magic_points
        self.curr_magic_points: Decimal = max_magic_points
        self.max_energy: Decimal = max_energy
        self.curr_energy: Decimal = max_energy
        self.crit_rate: float = crit_rate if self.MIN_CRIT_RATE <= crit_rate <= self.MAX_CRIT_RATE else \
            self.MIN_CRIT_RATE if crit_rate < self.MIN_CRIT_RATE else self.MAX_CRIT_RATE
        self.crit_damage: float = crit_damage if self.crit_damage >= self.MIN_CRIT_DAMAGE else self.MIN_CRIT_DAMAGE
        self.attacking_range: int = attacking_range
        self.battlefield: Battlefield = battlefield
        self.curr_battle: Battle = curr_battle
        self.corresponding_deck: Deck or None = corresponding_deck
        self.position: Position = position
        self.researches_applied: list = []  # initial value
        self.characters_placed: list = []  # initial value
        self.battle_records: list = []  # initial value
        self.attackers: list = []  # a list of attackers used to indicate who is doing the assist and the kill
        self.strength: Decimal = self.calculate_strength()

    def attack(self, target):
        # type: (Character or Transport or Building) -> bool
        if self.position.calc_dist(target.position) <= self.attacking_range:
            multiplier: float = self.crit_damage if random.random() <= self.crit_rate else 1
            damage: Decimal = self.attack * multiplier - target.defense
            target.curr_hp -= damage
            target.attackers.append(self)
            if target.curr_hp <= 0:
                target.battle_records[-1].times_died += 1
                self.battle_records[-1].kills += 1.
                if len(target.attackers) > 1:
                    target.attackers[-2].battle_records[-1].assists += 1

                target.attackers = []
                self.curr_battle.respawn_character(target)

            return True  # attack success

        return False  # attack failed

    def add_battle_record(self, battle_record):
        # type: (BattleRecord) -> None
        self.battle_records.append(battle_record)

    def apply_research(self, research):
        # type: (Research) -> None
        self.max_hp *= 1 + research.building_max_hp_percentage_up
        self.attack *= 1 + research.building_attack_percentage_up
        self.defense *= 1 + research.building_defense_percentage_up
        self.attack_speed += research.building_attack_speed_percentage_up
        self.max_magic_points *= 1 + research.building_max_magic_points_percentage_up
        self.max_energy *= 1 + research.building_max_energy_percentage_up
        self.researches_applied.append(research)

    def level_up(self):
        # type: () -> None
        while self.exp >= self.required_exp:
            self.level += 1
            self.required_exp *= 10 ** (self.level ** 2)
            self.max_hp *= self.level ** 2
            self.curr_hp = self.max_hp
            self.attack *= self.level ** 2
            self.defense *= self.level ** 2
            self.max_magic_points *= self.level ** 2
            self.curr_magic_points = self.max_magic_points
            self.max_energy *= self.level ** 2
            self.curr_energy = self.max_energy

    def __level_down(self):
        # type: () -> None
        self.required_exp /= 10 ** (self.level ** 2)
        self.max_hp /= self.level ** 2
        self.curr_hp = self.max_hp
        self.attack /= self.level ** 2
        self.defense /= self.level ** 2
        self.max_magic_points /= self.level ** 2
        self.curr_magic_points = self.max_magic_points
        self.max_energy /= self.level ** 2
        self.curr_energy = self.max_energy
        self.level -= 1

    def restore_level(self):
        # type: () -> None
        while self.level > 1:
            self.__level_down()

    def calculate_strength(self):
        # type: () -> Decimal
        self.strength = Decimal(5 * (self.max_hp + self.attack + self.defense + self.max_magic_points +
                                     self.max_energy)) * self.attack_speed * (1 + (100 * self.crit_rate)) * (
                                1 + (100 * self.crit_damage)) * \
                        self.attacking_range
        return self.strength

    def clone(self):
        # type: () -> Building
        return copy.deepcopy(self)


class Barracks(Building):
    """
    This class is used to initialise barracks in this game.
    """

    def __init__(self, character_id, name, description, max_hp, attack, defense, attack_speed, max_magic_points,
                 max_energy,
                 crit_rate, crit_damage, attacking_range, battlefield, curr_battle, corresponding_deck, position):
        # type: (str, str, str, Decimal, Decimal, Decimal, float or int, Decimal, Decimal, float, float, int, Battlefield, Battle, Deck or None, Position) -> None
        super(Barracks, self).__init__(character_id, name, description, max_hp, attack, defense, attack_speed, max_magic_points,
                 max_energy,
                 crit_rate, crit_damage, attacking_range, battlefield, curr_battle, corresponding_deck, position)
        self.building_type: BuildingType or None = BuildingType("BARRACKS")


class Stable(Building):
    """
    This class is used to initialise stables in this game.
    """

    def __init__(self, character_id, name, description, max_hp, attack, defense, attack_speed, max_magic_points,
                 max_energy,
                 crit_rate, crit_damage, attacking_range, battlefield, curr_battle, corresponding_deck, position):
        # type: (str, str, str, Decimal, Decimal, Decimal, float or int, Decimal, Decimal, float, float, int, Battlefield, Battle, Deck or None, Position) -> None
        super(Stable, self).__init__(character_id, name, description, max_hp, attack, defense, attack_speed,
                                       max_magic_points,
                                       max_energy,
                                       crit_rate, crit_damage, attacking_range, battlefield, curr_battle,
                                       corresponding_deck, position)
        self.building_type: BuildingType or None = BuildingType("STABLE")


class SiegeWorks(Building):
    """
    This class is used to initialise siege works in this game.
    """

    def __init__(self, character_id, name, description, max_hp, attack, defense, attack_speed, max_magic_points,
                 max_energy,
                 crit_rate, crit_damage, attacking_range, battlefield, curr_battle, corresponding_deck, position):
        # type: (str, str, str, Decimal, Decimal, Decimal, float or int, Decimal, Decimal, float, float, int, Battlefield, Battle, Deck or None, Position) -> None
        super(SiegeWorks, self).__init__(character_id, name, description, max_hp, attack, defense, attack_speed,
                                       max_magic_points,
                                       max_energy,
                                       crit_rate, crit_damage, attacking_range, battlefield, curr_battle,
                                       corresponding_deck, position)
        self.building_type: BuildingType or None = BuildingType("SIEGE WORKS")


class Shrine(Building):
    """
    This class is used to initialise shrines in this game.
    """

    def __init__(self, character_id, name, description, max_hp, attack, defense, attack_speed, max_magic_points,
                 max_energy,
                 crit_rate, crit_damage, attacking_range, battlefield, curr_battle, corresponding_deck, position, favor_production_rate):
        # type: (str, str, str, Decimal, Decimal, Decimal, float or int, Decimal, Decimal, float, float, int, Battlefield, Battle, Deck or None, Position, Decimal) -> None
        super(Shrine, self).__init__(character_id, name, description, max_hp, attack, defense, attack_speed,
                                       max_magic_points,
                                       max_energy,
                                       crit_rate, crit_damage, attacking_range, battlefield, curr_battle,
                                       corresponding_deck, position)
        self.building_type: BuildingType or None = BuildingType("SHRINE")
        self.favor_production_rate: Decimal = favor_production_rate


class TownCenter(Building):
    """
    This class is used to initialise town centers in this game.
    """

    def __init__(self, character_id, name, description, max_hp, attack, defense, attack_speed, max_magic_points,
                 max_energy,
                 crit_rate, crit_damage, attacking_range, battlefield, curr_battle, corresponding_deck, position,
                 food_production_rate, gold_production_rate, favor_production_rate):
        # type: (str, str, str, Decimal, Decimal, Decimal, float or int, Decimal, Decimal, float, float, int, Battlefield, Battle, Deck or None, Position, Decimal, Decimal, Decimal) -> None
        super(TownCenter, self).__init__(character_id, name, description, max_hp, attack, defense, attack_speed,
                                         max_magic_points, max_energy,
                                         crit_rate, crit_damage, attacking_range, battlefield, curr_battle,
                                         corresponding_deck, position)
        self.building_type: BuildingType or None = BuildingType("TOWN CENTER")
        self.food_production_rate: Decimal = food_production_rate
        self.gold_production_rate: Decimal = gold_production_rate
        self.favor_production_rate: Decimal = favor_production_rate


class Harbor(Building):
    """
    This class is used to initialise barracks in this game.
    """

    def __init__(self, character_id, name, description, max_hp, attack, defense, attack_speed, max_magic_points,
                 max_energy,
                 crit_rate, crit_damage, attacking_range, battlefield, curr_battle, corresponding_deck, position):
        # type: (str, str, str, Decimal, Decimal, Decimal, float or int, Decimal, Decimal, float, float, int, Battlefield, Battle, Deck or None, Position) -> None
        super(Harbor, self).__init__(character_id, name, description, max_hp, attack, defense, attack_speed,
                                         max_magic_points,
                                         max_energy,
                                         crit_rate, crit_damage, attacking_range, battlefield, curr_battle,
                                         corresponding_deck, position)
        self.building_type: BuildingType or None = BuildingType("HARBOR")


class Garage(Building):
    """
    This class is used to initialise garages in this game.
    """

    def __init__(self, character_id, name, description, max_hp, attack, defense, attack_speed, max_magic_points,
                 max_energy,
                 crit_rate, crit_damage, attacking_range, battlefield, curr_battle, corresponding_deck, position):
        # type: (str, str, str, Decimal, Decimal, Decimal, float or int, Decimal, Decimal, float, float, int, Battlefield, Battle, Deck or None, Position) -> None
        super(Garage, self).__init__(character_id, name, description, max_hp, attack, defense, attack_speed,
                                         max_magic_points,
                                         max_energy,
                                         crit_rate, crit_damage, attacking_range, battlefield, curr_battle,
                                         corresponding_deck, position)
        self.building_type: BuildingType or None = BuildingType("GARAGE")


class Mine(Building):
    """
    This class is used to initialise mines in this game.
    """

    def __init__(self, character_id, name, description, max_hp, attack, defense, attack_speed, max_magic_points,
                 max_energy,
                 crit_rate, crit_damage, attacking_range, battlefield, curr_battle, corresponding_deck, position,
                 gold_production_rate):
        # type: (str, str, str, Decimal, Decimal, Decimal, float or int, Decimal, Decimal, float, float, int, Battlefield, Battle, Deck or None, Position, Decimal) -> None
        super(Mine, self).__init__(character_id, name, description, max_hp, attack, defense, attack_speed,
                                     max_magic_points,
                                     max_energy,
                                     crit_rate, crit_damage, attacking_range, battlefield, curr_battle,
                                     corresponding_deck, position)
        self.building_type: BuildingType or None = BuildingType("MINE")
        self.gold_production_rate: Decimal = gold_production_rate


class Farm(Building):
    """
    This class is used to initialise farms in this game.
    """

    def __init__(self, character_id, name, description, max_hp, attack, defense, attack_speed, max_magic_points,
                 max_energy,
                 crit_rate, crit_damage, attacking_range, battlefield, curr_battle, corresponding_deck, position,
                 food_production_rate):
        # type: (str, str, str, Decimal, Decimal, Decimal, float or int, Decimal, Decimal, float, float, int, Battlefield, Battle, Deck or None, Position, Decimal) -> None
        super(Farm, self).__init__(character_id, name, description, max_hp, attack, defense, attack_speed,
                                   max_magic_points,
                                   max_energy,
                                   crit_rate, crit_damage, attacking_range, battlefield, curr_battle,
                                   corresponding_deck, position)
        self.building_type: BuildingType or None = BuildingType("FARM")
        self.food_production_rate: Decimal = food_production_rate


class Wall(Building):
    """
    This class is used to initialise walls in this game.
    """

    def __init__(self, character_id, name, description, max_hp, attack, defense, attack_speed, max_magic_points,
                 max_energy,
                 crit_rate, crit_damage, attacking_range, battlefield, curr_battle, corresponding_deck, position):
        # type: (str, str, str, Decimal, Decimal, Decimal, float or int, Decimal, Decimal, float, float, int, Battlefield, Battle, Deck or None, Position) -> None
        super(Wall, self).__init__(character_id, name, description, max_hp, attack, defense, attack_speed,
                                     max_magic_points,
                                     max_energy,
                                     crit_rate, crit_damage, attacking_range, battlefield, curr_battle,
                                     corresponding_deck, position)
        self.building_type: BuildingType or None = BuildingType("WALL")


class Fort(Building):
    """
    This class is used to initialise forts in this game.
    """

    def __init__(self, character_id, name, description, max_hp, attack, defense, attack_speed, max_magic_points,
                 max_energy,
                 crit_rate, crit_damage, attacking_range, battlefield, curr_battle, corresponding_deck, position):
        # type: (str, str, str, Decimal, Decimal, Decimal, float or int, Decimal, Decimal, float, float, int, Battlefield, Battle, Deck or None, Position) -> None
        super(Fort, self).__init__(character_id, name, description, max_hp, attack, defense, attack_speed,
                                     max_magic_points,
                                     max_energy,
                                     crit_rate, crit_damage, attacking_range, battlefield, curr_battle,
                                     corresponding_deck, position)
        self.building_type: BuildingType or None = BuildingType("FORT")


class Gate(Building):
    """
    This class is used to initialise gates in this game.
    """

    def __init__(self, character_id, name, description, max_hp, attack, defense, attack_speed, max_magic_points,
                 max_energy,
                 crit_rate, crit_damage, attacking_range, battlefield, curr_battle, corresponding_deck, position):
        # type: (str, str, str, Decimal, Decimal, Decimal, float or int, Decimal, Decimal, float, float, int, Battlefield, Battle, Deck or None, Position) -> None
        super(Gate, self).__init__(character_id, name, description, max_hp, attack, defense, attack_speed,
                                     max_magic_points,
                                     max_energy,
                                     crit_rate, crit_damage, attacking_range, battlefield, curr_battle,
                                     corresponding_deck, position)
        self.building_type: BuildingType or None = BuildingType("GATE")


class DefenseTower(Building):
    """
    This class is used to initialise defense towers in this game.
    """

    def __init__(self, character_id, name, description, max_hp, attack, defense, attack_speed, max_magic_points,
                 max_energy,
                 crit_rate, crit_damage, attacking_range, battlefield, curr_battle, corresponding_deck, position):
        # type: (str, str, str, Decimal, Decimal, Decimal, float or int, Decimal, Decimal, float, float, int, Battlefield, Battle, Deck or None, Position) -> None
        super(DefenseTower, self).__init__(character_id, name, description, max_hp, attack, defense, attack_speed,
                                     max_magic_points,
                                     max_energy,
                                     crit_rate, crit_damage, attacking_range, battlefield, curr_battle,
                                     corresponding_deck, position)
        self.building_type: BuildingType or None = BuildingType("DEFENSE TOWER")


class QuizZone(Building):
    """
    This class is used to initialise quiz zones in this game.
    """

    def __init__(self, character_id, name, description, max_hp, attack, defense, attack_speed, max_magic_points,
                 max_energy,
                 crit_rate, crit_damage, attacking_range, battlefield, curr_battle, corresponding_deck, position):
        # type: (str, str, str, Decimal, Decimal, Decimal, float or int, Decimal, Decimal, float, float, int, Battlefield, Battle, Deck or None, Position) -> None
        super(QuizZone, self).__init__(character_id, name, description, max_hp, attack, defense, attack_speed,
                                     max_magic_points,
                                     max_energy,
                                     crit_rate, crit_damage, attacking_range, battlefield, curr_battle,
                                     corresponding_deck, position)
        self.building_type: BuildingType or None = BuildingType("QUIZ ZONE")


class BuildingType:
    """
    This class contains attributes of types of buildings in this game.
    """
    POSSIBLE_TYPES = ["BARRACKS", "STABLE", "SIEGE WORKS", "SHRINE", "TOWN CENTER", "HARBOR", "GARAGE", "MINE", "FARM",
                      "WALL", "FORT", "GATE", "DEFENSE TOWER", "QUIZ ZONE"]

    def __init__(self, value):
        # type: (str) -> None
        self.value: str = value if value in self.POSSIBLE_TYPES else None

    def clone(self):
        # type: () -> BuildingType
        return copy.deepcopy(self)


class QuizQuestion:
    """
    This class contains attributes of quiz questions that the player can answer each turn during battles.
    """

    def __init__(self, number, question, choices, correct_answer, player_coin_prize, player_diamond_prize,
                 player_exp_prize,
                 deck_food_prize, deck_gold_prize, deck_favor_prize):
        # type: (int, str, str, str, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal) -> None
        self.number: int = number
        self.question: str = question
        self.choices: str = choices
        self.correct_answer: str = correct_answer
        self.player_input_answer: str or None = None  # initial value
        self.player_coin_prize: Decimal = player_coin_prize
        self.player_diamond_prize: Decimal = player_diamond_prize
        self.player_exp_prize: Decimal = player_exp_prize
        self.deck_food_prize: Decimal = deck_food_prize
        self.deck_gold_prize: Decimal = deck_gold_prize
        self.deck_favor_prize: Decimal = deck_favor_prize

    def get_answered(self, player_input_answer):
        # type: (str or None) -> None
        self.player_input_answer = player_input_answer

    def give_out_reward(self, player):
        # type: (Player) -> bool
        # Checking whether the input answer from the player is correct or not
        if self.player_input_answer == self.correct_answer:
            player.coins += self.player_coin_prize
            player.diamonds += self.player_diamond_prize
            player.exp += self.player_exp_prize
            player.deck.food += self.deck_food_prize
            player.deck.gold += self.deck_gold_prize
            player.deck.favor += self.deck_favor_prize
            return True
        return False

    def to_string(self):
        # type: () -> str
        res = ""  # initial value
        res += str(self.number) + ". " + str(self.question) + "\n"
        res += "Choices: " + str(self.choices) + "\n"
        res += "Player coin prize: " + str(self.player_coin_prize) + "\n"
        res += "Player diamond prize: " + str(self.player_diamond_prize) + "\n"
        res += "Player EXP prize: " + str(self.player_exp_prize) + "\n"
        res += "Deck food prize: " + str(self.deck_food_prize) + "\n"
        res += "Deck gold prize: " + str(self.deck_gold_prize) + "\n"
        res += "Deck favor prize: " + str(self.deck_favor_prize) + "\n"
        return res

    def clone(self):
        # type: () -> QuizQuestion
        return copy.deepcopy(self)


class Tile:
    """
    This class contains attributes of tiles on a battlefield.
    """

    def __init__(self):
        # type: () -> None
        self.name: str or None = None
        self.description: str or None = None

    def clone(self):
        # type: () -> Tile
        return copy.deepcopy(self)


class Land(Tile):
    """
    This class is used to initialise tiles representing land.
    """

    def __init__(self):
        # type: () -> None
        super(Land, self).__init__()
        self.name: str or None = None
        self.description: str or None = "LAND"


class Plains(Land):
    """
    This class is used to initialise tiles representing plains.
    """

    def __init__(self, name):
        # type: (str) -> None
        super(Plains, self).__init__()
        self.name: str or None = name
        self.description: str or None = "PLAINS"


class Mountain(Land):
    """
    This class is used to initialise tiles representing mountains.
    """

    def __init__(self, name):
        # type: (str) -> None
        super(Mountain, self).__init__()
        self.name: str or None = name
        self.description: str or None = "MOUNTAIN"


class Hill(Land):
    """
    This class is used to initialise tiles representing hills.
    """

    def __init__(self, name):
        # type: (str) -> None
        super(Hill, self).__init__()
        self.name: str or None = name
        self.description: str or None = "HILL"


class Water(Tile):
    """
    This class is used to initialise tiles representing water.
    """

    def __init__(self):
        # type: () -> None
        super(Water, self).__init__()
        self.name: str or None = None
        self.description: str or None = "WATER"


class River(Water):
    """
    This class is used to initialise tiles representing rivers.
    """

    def __init__(self, name):
        # type: (str) -> None
        super(River, self).__init__()
        self.name: str or None = name
        self.description: str or None = "RIVER"


class Lake(Water):
    """
    This class is used to initialise tiles representing lakes.
    """

    def __init__(self, name):
        # type: (str) -> None
        super(Lake, self).__init__()
        self.name: str or None = name
        self.description: str or None = "LAKE"


class Sea(Water):
    """
    This class is used to initialise tiles representing seas.
    """

    def __init__(self, name):
        # type: (str) -> None
        super(Sea, self).__init__()
        self.name: str or None = name
        self.description: str or None = "SEA"


class Ocean(Water):
    """
    This class is used to initialise tiles representing oceans.
    """

    def __init__(self, name):
        # type: (str) -> None
        super(Ocean, self).__init__()
        self.name: str or None = name
        self.description: str or None = "OCEAN"


class SpecialPower:
    """
    This class contains attributes of special powers that characters have.
    """

    def __init__(self, does_ignore_enemies_defense, damage_multiplier_to_self_max_hp,
                 damage_multiplier_to_enemies_max_hp, damage_multiplier_to_self_attack,
                 damage_multiplier_to_self_defense, damage_multiplier_to_self_attack_speed,
                 damage_multiplier_to_self_max_magic_points, damage_multiplier_to_self_max_energy,
                 damage_multiplier_to_number_of_allies_deaths, damage_multiplier_to_number_of_enemies_deaths,
                 damage_multiplier_to_number_of_turns,
                 damage_percentage_up_per_self_hp_percentage_loss, damage_percentage_up_per_self_current_hp_percentage,
                 damage_percentage_up_per_enemies_hp_percentage_loss,
                 damage_percentage_up_per_enemies_current_hp_percentage, max_cooltime):
        # type: (bool, float, float, float, float, float, float, float, float, float, float, float, float, float, float, int) -> None
        self.does_ignore_enemies_defense: float = does_ignore_enemies_defense
        self.damage_multiplier_to_self_max_hp: float = damage_multiplier_to_self_max_hp
        self.damage_multiplier_to_enemies_max_hp: float = damage_multiplier_to_enemies_max_hp
        self.damage_multiplier_to_self_attack: float = damage_multiplier_to_self_attack
        self.damage_multiplier_to_self_defense: float = damage_multiplier_to_self_defense
        self.damage_multiplier_to_self_attack_speed: float = damage_multiplier_to_self_attack_speed
        self.damage_multiplier_to_self_max_magic_points: float = damage_multiplier_to_self_max_magic_points
        self.damage_multiplier_to_self_max_energy: float = damage_multiplier_to_self_max_energy
        self.damage_multiplier_to_number_of_allies_deaths: float = damage_multiplier_to_number_of_allies_deaths
        self.damage_multiplier_to_number_of_enemies_deaths: float = damage_multiplier_to_number_of_enemies_deaths
        self.damage_multiplier_to_number_of_turns: float = damage_multiplier_to_number_of_turns
        self.damage_percentage_up_per_self_hp_percentage_loss: float = damage_percentage_up_per_self_hp_percentage_loss
        self.damage_percentage_up_per_self_current_hp_percentage: float = damage_percentage_up_per_self_current_hp_percentage
        self.damage_percentage_up_per_enemies_hp_percentage_loss: float = damage_percentage_up_per_enemies_hp_percentage_loss
        self.damage_percentage_up_per_enemies_current_hp_percentage: float = \
            damage_percentage_up_per_enemies_current_hp_percentage
        self.cooltime: int = max_cooltime
        self.max_cooltime: int = max_cooltime

    def clone(self):
        # type: () -> SpecialPower
        return copy.deepcopy(self)


class Research:
    """
    This class contains attributes of researches which can be carried out by the player and the AI.
    """

    def __init__(self, research_id, name, description, min_player_level, character_max_hp_percentage_up,
                 character_attack_percentage_up, character_defense_percentage_up, character_attack_speed_percentage_up,
                 character_max_magic_points_percentage_up, character_max_energy_percentage_up,
                 transport_max_hp_percentage_up, transport_attack_percentage_up, transport_defense_percentage_up,
                 transport_attack_speed_percentage_up, transport_max_magic_points_percentage_up,
                 transport_max_energy_percentage_up, building_max_hp_percentage_up, building_attack_percentage_up,
                 building_defense_percentage_up, building_attack_speed_percentage_up,
                 building_max_magic_points_percentage_up, building_max_energy_percentage_up):
        # type: (str, str, str, int, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float) -> None
        self.research_id: str = research_id
        self.name: str = name
        self.description: str = description
        self.level: int = 0
        self.min_player_level: int = min_player_level
        self.is_unlocked: bool = False
        self.character_max_hp_percentage_up: float = character_max_hp_percentage_up
        self.character_attack_percentage_up: float = character_attack_percentage_up
        self.character_defense_percentage_up: float = character_defense_percentage_up
        self.character_attack_speed_percentage_up: float = character_attack_speed_percentage_up
        self.character_max_magic_points_percentage_up: float = character_max_magic_points_percentage_up
        self.character_max_energy_percentage_up: float = character_max_energy_percentage_up
        self.transport_max_hp_percentage_up: float = transport_max_hp_percentage_up
        self.transport_attack_percentage_up: float = transport_attack_percentage_up
        self.transport_defense_percentage_up: float = transport_defense_percentage_up
        self.transport_attack_speed_percentage_up: float = transport_attack_speed_percentage_up
        self.transport_max_magic_points_percentage_up: float = transport_max_magic_points_percentage_up
        self.transport_max_energy_percentage_up: float = transport_max_energy_percentage_up
        self.building_max_hp_percentage_up: float = building_max_hp_percentage_up
        self.building_attack_percentage_up: float = building_attack_percentage_up
        self.building_defense_percentage_up: float = building_defense_percentage_up
        self.building_attack_speed_percentage_up: float = building_attack_speed_percentage_up
        self.building_max_magic_points_percentage_up: float = building_max_magic_points_percentage_up
        self.building_max_energy_percentage_up: float = building_max_energy_percentage_up

    def __gt__(self, other):
        # type: (Research) -> bool
        if self.research_id > other.research_id:
            return True
        else:
            return False

    def __lt__(self, other):
        # type: (Research) -> bool
        if self.research_id < other.research_id:
            return True
        else:
            return False

    def to_string(self):
        # type: () -> str
        res: str = ""  # initial value
        return res

    def clone(self):
        # type: () -> Research
        return copy.deepcopy(self)


class ResearchNode:
    """
    This class contains attributes of research nodes to be placed in a binary search tree data structure.
    """

    def __init__(self, research_instance):
        # type: (Research or None) -> None
        self.left: Research or None = None
        self.right: Research or None = None
        self.parent: Research or None = None
        self.research_instance: Research or None = research_instance

    def insert(self, node):
        # type: (ResearchNode) -> None
        if self.research_instance > node.research_instance:
            if self.left is None:
                self.left = node
                node.parent = self
            else:
                self.left.insert(node)
        elif self.research_instance < node.research_instance:
            if self.right is None:
                self.right = node
                node.parent = self
            else:
                self.right.insert(node)

    def inorder(self):
        # type: () -> None
        if self.left is not None:
            self.left.inorder()

        print(str(self.research_instance.to_string()) + "\n")
        if self.right is not None:
            self.right.inorder()

    def replace_node_of_parent(self, new_node):
        # type: (ResearchNode) -> None
        if self.parent is not None:
            if new_node is not None:
                new_node.parent = self.parent
            if self.parent.left == self:
                self.parent.left = new_node
            elif self.parent.right == self:
                self.parent.right = new_node
        else:
            self.research_instance = new_node.research_instance
            self.left = new_node.left
            self.right = new_node.right
            if new_node.left is not None:
                new_node.left.parent = self
            if new_node.right is not None:
                new_node.right.parent = self

    def find_min(self):
        # type: () -> None
        current = self
        while current.left is not None:
            current = current.left
        return current

    def remove(self):
        # type: () -> None
        if self.left is not None and self.right is not None:
            successor = self.right.find_min()
            self.research_instance = successor.research_instance
            successor.remove()
        elif self.left is not None:
            self.replace_node_of_parent(self.left)
        elif self.right is not None:
            self.replace_node_of_parent(self.right)
        else:
            self.replace_node_of_parent(None)

    def search(self, research_instance):
        # type: (Research) -> Research or None
        if self.research_instance > research_instance:
            if self.left is not None:
                return self.left.search(research_instance)
            else:
                return None
        elif self.research_instance < research_instance:
            if self.right is not None:
                return self.right.search(research_instance)
            else:
                return None
        return self

    def __gt__(self, other):
        # type: (ResearchNode) -> bool
        if self.research_instance > other.research_instance:
            return True
        else:
            return False

    def __lt__(self, other):
        # type: (ResearchNode) -> bool
        if self.research_instance < other.research_instance:
            return True
        else:
            return False

    def clone(self):
        # type: () ->  ResearchNode
        return copy.deepcopy(self)


class ResearchTree:
    """
    This class contains attributes of a binary search tree containing nodes with Research class objects as instances.
    """

    def __init__(self):
        # type: () -> None
        self.root: ResearchNode or None = None

    def inorder(self):
        # type: () -> None
        if self.root is not None:
            self.root.inorder()

    def add(self, research_instance):
        # type: (Research) -> None
        new_node: ResearchNode = ResearchNode(research_instance)
        if self.root is None:
            self.root = new_node
        else:
            self.root.insert(new_node)

    def remove(self, research_instance):
        # type: (Research) -> None
        to_remove: ResearchNode = self.search(research_instance)

        if (self.root == to_remove
                and self.root.left is None and self.root.right is None):
            self.root = None
        else:
            to_remove.remove()

    def search(self, research_instance):
        # type: (Research) -> ResearchNode
        if self.root is not None:
            return self.root.search(research_instance)

    def clone(self):
        # type: () -> ResearchTree
        return copy.deepcopy(self)


class Player:
    """
    This class contains attributes of the player in the game.
    """
    MAX_CHARACTER_INVENTORY_SIZE: int = 5000
    MAX_TRANSPORT_INVENTORY_SIZE: int = 50000
    MAX_BUILDING_INVENTORY_SIZE: int = 5000

    def __init__(self, name):
        # type: (str) -> None
        self.player_id: str = str(random.randint(100000000, 999999999))
        self.name: str = name
        self.level: int = 1
        self.exp: Decimal = Decimal("0e0")
        self.required_exp: Decimal = Decimal("1e9")
        self.coins: Decimal = Decimal("0e0")
        self.diamonds: Decimal = Decimal("0e0")
        self.deck: Deck or None = None  # initial value
        self.character_inventory: list = [characters[i] for i in range(Deck.NUM_CHARACTERS)]  # initial value
        self.transport_inventory: list = [transports[i] for i in range(Deck.NUM_TRANSPORTS)]  # initial value
        self.building_inventory: list = [buildings[i] for i in range(Deck.NUM_BUILDINGS)]  # initial value
        self.box_inventory: list = []  # initial value
        self.treasure_chest_inventory: list = []  # initial value
        self.researches_applied: list = []  # initial value

    def to_string(self):
        # type: () -> str
        res: str = ""  # initial value
        return res

    def level_up(self):
        # type: () -> None
        while self.exp >= self.required_exp:
            self.level += 1
            self.required_exp *= 10 ** (self.level ** 2)

    def clone(self):
        # type: () -> Player
        return copy.deepcopy(self)


class AI(Player):
    """
    This class contains attributes of opponents in the game.
    """

    def __init__(self, name):
        # type: (str) -> None
        super(AI, self).__init__(name)


class Deck:
    """
    This class contains decks that the player and the AIs can bring to battles.
    """
    NUM_CHARACTERS: int = 5
    NUM_TRANSPORTS: int = 2
    NUM_BUILDINGS: int = 14

    def __init__(self, characters, transports, buildings):
        # type: (list, list, list) -> None
        self.characters: list or None = characters if len(characters) == self.NUM_CHARACTERS else None
        self.transports: list or None = transports if len(transports) == self.NUM_TRANSPORTS else None
        self.buildings: list or None = buildings if len(buildings) == self.NUM_BUILDINGS else None
        self.food: Decimal = Decimal("0e0")
        self.gold: Decimal = Decimal("0e0")
        self.favor: Decimal = Decimal("0e0")
        self.strength: Decimal = self.calculate_strength()

    def replace_character(self, character, replacement_character, player):
        # type: (Character, Character, Player) -> bool
        if character in self.characters and replacement_character not in self.characters:
            if character.character_type == replacement_character.character_type and character.character_class == \
                    replacement_character.character_class and replacement_character in player.character_inventory:
                self.characters.remove(character)
                self.characters.append(replacement_character)
                self.strength = self.calculate_strength()
                return True
            return False
        return False

    def replace_transport(self, transport, replacement_transport, player):
        # type: (Transport, Transport, Player) -> bool
        if transport in self.transports and replacement_transport not in self.transports:
            if transport.transport_type == replacement_transport.transport_type and transport.description == \
                    replacement_transport.description and replacement_transport in player.transport_inventory:
                self.transports.remove(transport)
                self.transports.append(replacement_transport)
                self.strength = self.calculate_strength()
                return True
            return False
        return False

    def replace_building(self, building, replacement_building, player):
        # type: (Building, Building, Player) -> bool
        if building in self.buildings and replacement_building not in self.buildings:
            if building.building_type == replacement_building.building_type and building.description == \
                    replacement_building.description and replacement_building in player.building_inventory:
                self.buildings.remove(building)
                self.buildings.append(replacement_building)
                self.strength = self.calculate_strength()
                return True
            return False
        return False

    def calculate_strength(self):
        # type: () -> Decimal
        self.strength = 0  # initial value
        for character in self.characters:
            self.strength += character.calculate_strength()

        for transport in self.transports:
            self.strength += transport.calculate_strength()

        for building in self.buildings:
            self.strength += building.calculate_strength()

        return self.strength

    def clone(self):
        # type: () -> Deck
        return copy.deepcopy(self)


class Shop:
    """
    This class contains attributes of shops in this game.
    """

    def __init__(self, shop_id):
        # type: (str) -> None
        self.shop_id: str = shop_id
        self.name: str or None = None
        self.description: str or None = None

    def clone(self):
        # type: () -> Shop
        return copy.deepcopy(self)


class GlobalShop(Shop):
    """
    This class contains attributes of a global shop where the player can buy items outside the battlefield.
    """

    def __init__(self, shop_id, items_sold):
        # type: (str, list) -> None
        super(GlobalShop, self).__init__(shop_id)
        self.name: str = "GLOBAL SHOP"
        self.description: str = "A shop where the player can buy items outside the battlefield."
        self.items_sold: list = items_sold


class BattlefieldShop(Shop):
    """
    This class contains attributes of a shop in the battlefield which is used for the player and the AI to buy items
    during a battle.
    """

    def __init__(self, shop_id, items_sold):
        # type: (str, list) -> None
        super(BattlefieldShop, self).__init__(shop_id)
        self.name: str = "BATTLEFIELD SHOP"
        self.description: str = "A shop in the battlefield which is used for the player and the AI to buy " \
                                "items during a battle."
        self.items_sold: list = items_sold


class Rune:
    """
    This class is used to initialise runes which can be placed to characters in this game.
    """

    def __init__(self, max_hp_up, max_hp_percentage_up, attack_up, attack_percentage_up, defense_up,
                 defense_percentage_up, attack_speed_up, max_magic_points_up,
                 max_magic_points_percentage_up, max_energy_up, max_energy_percentage_up,
                 crit_rate_up, crit_damage_up):
        # type: (Decimal, float, Decimal, float, Decimal, float, float or int, Decimal, float, Decimal, float, float, float) -> None
        self.max_hp_up: Decimal = max_hp_up
        self.max_hp_percentage_up: float = max_hp_percentage_up
        self.attack_up: Decimal = attack_up
        self.attack_percentage_up: float = attack_percentage_up
        self.defense_up: Decimal = defense_up
        self.defense_percentage_up: float = defense_percentage_up
        self.attack_speed_up: float or int = attack_speed_up
        self.max_magic_points_up: Decimal = max_magic_points_up
        self.max_magic_points_percentage_up: float = max_magic_points_percentage_up
        self.max_energy_up: Decimal = max_energy_up
        self.max_energy_percentage_up: float = max_energy_percentage_up
        self.crit_rate_up: float = crit_rate_up
        self.crit_damage_up: float = crit_damage_up

    def clone(self):
        # type: () -> Rune
        return copy.deepcopy(self)


class Box:
    """
    This class contains attributes of boxes where the player can get random characters, transports, and buildings.
    """

    def __init__(self, box_id, name, description, size, potential_characters, potential_transports, potential_buildings,
                 open_coin_cost, open_diamond_cost):
        # type: (str, str, str, int, list, list, list, Decimal, Decimal) -> None
        self.box_id: str = box_id
        self.name: str = name
        self.description: str = description
        self.size: int = size
        self.potential_characters: list = potential_characters   # a list of Character class objects
        self.potential_transports: list = potential_transports  # a list of Transport class objects
        self.potential_buildings: list = potential_buildings  # a list of Building class objects
        self.open_coin_cost: Decimal = open_coin_cost
        self.open_diamond_cost: Decimal = open_diamond_cost
        self.contents: list = []  # initial value

    def fill(self):
        # type: () -> None
        self.contents = []  # initial value
        for i in range(self.size):
            decision: int = random.randint(1, 3)
            if decision == 1:
                # Randomly add a character
                self.contents.append(self.potential_characters[random.randint(0, len(self.potential_characters) - 1)])
            elif decision == 2:
                # Randomly add a transport
                self.contents.append(self.potential_transports[random.randint(0, len(self.potential_transports) - 1)])
            else:
                # Randomly add a building
                self.contents.append(self.potential_buildings[random.randint(0, len(self.potential_buildings) - 1)])

    def clone(self):
        # type: () -> Box
        return copy.deepcopy(self)


class TreasureChest:
    """
    This class contains attributes of treasure chests where the player can get a random character, transport, or
    building.
    """

    def __init__(self, treasure_chest_id, name, description, potential_characters, potential_transports,
                 potential_buildings, open_coin_cost, open_diamond_cost):
        # type: (str, str, str, list, list, list, Decimal, Decimal) -> None
        self.treasure_chest_id: str = treasure_chest_id
        self.name: str = name
        self.description: str = description
        self.potential_characters: list = potential_characters # a list of Character class objects
        self.potential_transports: list = potential_transports # a list of Transport class objects
        self.potential_buildings: list = potential_buildings # a list of Building class objects
        self.open_coin_cost: Decimal = open_coin_cost
        self.open_diamond_cost: Decimal = open_diamond_cost
        self.content: Character or Transport or Building or None = None  # initial value

    def fill(self):
        # type: () -> None
        self.content = None  # initial value
        decision: int = random.randint(1, 3)
        self.content = self.potential_characters[random.randint(0, len(self.potential_characters) - 1)] if decision == \
                                                                                                           1 else \
        self.potential_transports[random.randint(0, len(self.potential_transports) - 1)] if decision == 2 \
            else self.potential_buildings[random.randint(0, len(self.potential_buildings) - 1)]

    def clone(self):
        # type: () -> TreasureChest
        return copy.deepcopy(self)


class Game:
    """
    This class contains attributes of the saved game data.
    """

    def __init__(self, characters, transports, buildings, battlefields, quiz_questions, researches):
        # type: (list, list, list, list, list, list) -> None
        self.saved_battles: list = []  # a list of battles being saved
        self.characters: list = characters
        self.transports: list = transports
        self.buildings: list = buildings
        self.battlefields: list = battlefields
        self.quiz_questions: list = quiz_questions
        self.researches: list = researches
        self.research_tree: ResearchTree = ResearchTree()
        for research in self.researches:
            self.research_tree.add(research)


# Initialising variables to be stored in the saved game data.


characters: list = [

]

transports: list = [

]

buildings: list = [

]

battlefields: list = [

]

quiz_questions: list = [

]

researches: list = [

]


def main():
    # type: () -> None
    """
    This function is used to run the program.
    :return:
    """


main()
