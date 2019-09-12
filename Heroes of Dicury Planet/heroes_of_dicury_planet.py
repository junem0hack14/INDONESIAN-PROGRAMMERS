# The names of the monsters in this game are randomly generated using the random generator in the link below.
# https://www.fantasynamegenerators.com/

# Game version: pre-release 6 (Command Line Interface Version)


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


class AwakenBonus:
    """
    This class contains attributes of awaken bonus gained for awakening a hero.
    """

    def __init__(self, attack_speed_up, crit_rate_up, crit_damage_up, evasion_chance_up, resistance_up, accuracy_up,
                 extra_turn_chance_up, counterattack_chance_up, new_skill, skill_to_be_replaced, upgraded_skill):
        # type: (float, float, float, float, float, float, float, float, Skill, Skill, Skill) -> None
        self.attack_speed_up: float = attack_speed_up
        self.crit_rate_up: float = crit_rate_up
        self.crit_damage_up: float = crit_damage_up
        self.evasion_chance_up: float = evasion_chance_up
        self.resistance_up: float = resistance_up
        self.accuracy_up: float = accuracy_up
        self.extra_turn_chance_up: float = extra_turn_chance_up
        self.counterattack_chance_up: float = counterattack_chance_up
        self.new_skill: Skill = new_skill  # a Skill class object
        self.skill_to_be_replaced: Skill = skill_to_be_replaced  # a Skill class object
        self.upgraded_skill: Skill = upgraded_skill  # a Skill class object

    def to_string(self):
        # type: () -> str
        res: str = ""  # initial value
        res += "Attack speed up: " + str(self.attack_speed_up) + "\n"
        res += "Crit rate up: " + str(100 * self.crit_rate_up) + "%\n"
        res += "Crit damage up: " + str(100 * self.crit_damage_up) + "%\n"
        res += "Evasion chance up: " + str(100 * self.evasion_chance_up) + "%\n"
        res += "Resistance up: " + str(100 * self.resistance_up) + "%\n"
        res += "Accuracy up: " + str(100 * self.accuracy_up) + "%\n"
        res += "Extra turn chance up: " + str(100 * self.extra_turn_chance_up) + "%\n"
        res += "Counterattack chance up: " + str(100 * self.counterattack_chance_up) + "%\n"
        res += "New skill gained: \n" + str(self.new_skill.to_string()) + "\n"
        res += "Skill to be replaced: \n" + str(self.skill_to_be_replaced.to_string()) + "\n"
        res += "Upgraded skill: \n" + str(self.upgraded_skill.to_string()) + "\n"
        return res

    def clone(self):
        return copy.deepcopy(self)


class SecondaryAwakenBonus(AwakenBonus):
    """
    This class contains attributes of secondary awaken bonus gained for secondary awakening a character.
    """

    def __init__(self, attack_speed_up, crit_rate_up, crit_damage_up, evasion_chance_up, resistance_up, accuracy_up,
                 extra_turn_chance_up, counterattack_chance_up, new_skill, skill_to_be_replaced, upgraded_skill,
                 second_new_skill, second_skill_to_be_replaced, second_upgraded_skill):
        # type: (float, float, float, float, float, float, float, float, Skill, Skill, Skill, Skill, Skill, Skill) -> None
        AwakenBonus.__init__(self, attack_speed_up, crit_rate_up, crit_damage_up, evasion_chance_up, resistance_up,
                             accuracy_up, extra_turn_chance_up, counterattack_chance_up, new_skill,
                             skill_to_be_replaced, upgraded_skill)
        self.second_new_skill: Skill = second_new_skill  # a Skill class object
        self.second_skill_to_be_replaced: Skill = second_skill_to_be_replaced  # a Skill class object
        self.second_upgraded_skill: Skill = second_upgraded_skill  # a Skill class object

    def to_string(self):
        # type: () -> str
        res: str = AwakenBonus.to_string(self)
        res += "Second new skill gained: \n" + str(self.second_new_skill.to_string()) + "\n"
        res += "Second skill to be replaced: \n" + str(self.second_skill_to_be_replaced) + "\n"
        res += "Second upgraded skill: \n" + str(self.second_upgraded_skill.to_string()) + "\n"
        return res


class Battle:
    """
    This class contains attributes of battles carried out in the game.
    """

    def __init__(self, team1, team2):
        # type: (Team, Team) -> None
        self.team1: Team = team1  # a Team class object
        self.team2: Team = team2  # a Team class object
        self.whose_turn: Hero or None = None  # a Hero class object
        self.winner: Team or None = None  # a Team class object
        self.is_finished: bool = False
        self.turn: int = 0

    def clone(self):
        return copy.deepcopy(self)


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
                        or (
                        self.skill_to_use.does_heal and self.user.corresponding_team == self.target.corresponding_team):
                    self.user.use_skill(self.skill_to_use, self.target)
                    return True
                return False
            return False
        else:
            return False

    def clone(self):
        # type: () -> Action
        return copy.deepcopy(self)


class PrefixStat:
    """
    This class contains attributes of the prefix stat of the rune.
    """
    POSSIBLE_PREFIX_STAT_TYPES = ["MAX_HP_UP", "MAX_HP_PERCENTAGE_UP", "ATTACK_UP", "ATTACK_PERCENTAGE_UP",
                                  "DEFENSE_UP", "DEFENSE_PERCENTAGE_UP", "ATTACK_SPEED_UP", "MAX_MAGIC_POINTS_UP",
                                  "MAX_MAGIC_POINTS_PERCENTAGE_UP", "MAX_ENERGY_UP", "MAX_ENERGY_PERCENTAGE_UP",
                                  "CRIT_RATE_UP", "CRIT_DAMAGE_UP", "EVASION_CHANCE_UP", "RESISTANCE_UP", "ACCURACY_UP"]

    def __init__(self, prefix_stat_type, corresponding_rune):
        # type: (str, Rune) -> None
        self.prefix_stat_type: str = prefix_stat_type if prefix_stat_type in self.POSSIBLE_PREFIX_STAT_TYPES else None
        self.corresponding_rune: Rune = corresponding_rune  # a Rune class object
        self.max_hp_up: Decimal = Decimal("1e10") * 10 ** (10 + self.corresponding_rune.rating ** 2) if \
            self.prefix_stat_type == "MAX_HP_UP" else 0
        self.max_hp_percentage_up: float = 2 * self.corresponding_rune.rating - 1 if \
            self.prefix_stat_type == "MAX_HP_PERCENTAGE_UP" else 0
        self.attack_up: Decimal = Decimal("1e10") * 10 ** (8 + self.corresponding_rune.rating ** 2) if \
            self.prefix_stat_type == "ATTACK_UP" else 0
        self.attack_percentage_up: float = 2 * self.corresponding_rune.rating - 1 if \
            self.prefix_stat_type == "ATTACK_PERCENTAGE_UP" else 0
        self.defense_up: Decimal = Decimal("1e10") * 10 ** (8 + self.corresponding_rune.rating ** 2) if \
            self.prefix_stat_type == "DEFENSE_UP" else 0
        self.defense_percentage_up: float = 2 * self.corresponding_rune.rating - 1 if \
            self.prefix_stat_type == "DEFENSE_PERCENTAGE_UP" else 0
        self.attack_speed_up: float = 2 * self.corresponding_rune.rating - 1 if self.prefix_stat_type == "ATTACK_SPEED_UP" \
            else 0
        self.max_magic_points_up: Decimal = Decimal("1e10") * 10 ** (10 + self.corresponding_rune.rating ** 2) if \
            self.prefix_stat_type == "MAX_MAGIC_POINTS_UP" else 0
        self.max_magic_points_percentage_up: float = 2 * self.corresponding_rune.rating - 1 if \
            self.prefix_stat_type == "MAX_MAGIC_POINTS_PERCENTAGE_UP" else 0
        self.max_energy_up: Decimal = Decimal("1e10") * 10 ** (10 + self.corresponding_rune.rating ** 2) if \
            self.prefix_stat_type == "MAX_ENERGY_UP" else 0
        self.max_energy_percentage_up: float = 2 * self.corresponding_rune.rating - 1 if \
            self.prefix_stat_type == "MAX_ENERGY_PERCENTAGE_UP" else 0
        self.crit_rate_up: float = self.corresponding_rune.rating if self.prefix_stat_type == "CRIT_RATE_UP" else 0
        self.crit_damage_up: float = 2 * self.corresponding_rune.rating - 1 if self.prefix_stat_type == "CRIT_DAMAGE_UP" else 0
        self.evasion_chance_up: float = self.corresponding_rune.rating if self.prefix_stat_type == "EVASION_CHANCE_UP" else 0
        self.resistance_up: float = self.corresponding_rune.rating if self.prefix_stat_type == "RESISTANCE_UP" else 0
        self.accuracy_up: float = self.corresponding_rune.rating if self.prefix_stat_type == "ACCURACY_UP" else 0

    def clone(self):
        # type: () -> PrefixStat
        return copy.deepcopy(self)


class MainStat:
    """
    This class contains attributes of main stats of a rune.
    """

    def __init__(self, max_hp_up, max_hp_percentage_up, attack_up, attack_percentage_up, defense_up,
                 defense_percentage_up, attack_speed_up, max_magic_points_up, max_magic_points_percentage_up,
                 max_energy_up, max_energy_percentage_up, crit_rate_up, crit_damage_up, evasion_chance_up,
                 resistance_up, accuracy_up):
        # type: (Decimal, float, Decimal, float, Decimal, float, float, Decimal, float, Decimal, float, float, float, float, float, float) -> None
        self.max_hp_up: Decimal = max_hp_up
        self.max_hp_percentage_up: float = max_hp_percentage_up
        self.attack_up: Decimal = attack_up
        self.attack_percentage_up: float = attack_percentage_up
        self.defense_up: Decimal = defense_up
        self.defense_percentage_up: float = defense_percentage_up
        self.attack_speed_up: float = attack_speed_up
        self.max_magic_points_up: Decimal = max_magic_points_up
        self.max_magic_points_percentage_up: float = max_magic_points_percentage_up
        self.max_energy_up: Decimal = max_energy_up
        self.max_energy_percentage_up: float = max_energy_percentage_up
        self.crit_rate_up: float = crit_rate_up
        self.crit_damage_up: float = crit_damage_up
        self.evasion_chance_up: float = evasion_chance_up
        self.resistance_up: float = resistance_up
        self.accuracy_up: float = accuracy_up

    def clone(self):
        # type: () -> MainStat
        return copy.deepcopy(self)


class RuneStat:
    """
    This class contains attributes of stats of the rune.
    """

    def __init__(self, max_hp_up, max_hp_percentage_up, attack_up, attack_percentage_up, defense_up,
                 defense_percentage_up, attack_speed_up, max_magic_points_up, max_magic_points_percentage_up,
                 max_energy_up, max_energy_percentage_up, crit_rate_up, crit_damage_up, evasion_chance_up,
                 resistance_up, accuracy_up):
        # type: (Decimal, float, Decimal, float, Decimal, float, float, Decimal, float, Decimal, float, float, float, float, float, float) -> None
        self.max_hp_up: Decimal = max_hp_up
        self.max_hp_percentage_up: float = max_hp_percentage_up
        self.attack_up: Decimal = attack_up
        self.attack_percentage_up: float = attack_percentage_up
        self.defense_up: Decimal = defense_up
        self.defense_percentage_up: float = defense_percentage_up
        self.attack_speed_up: float = attack_speed_up
        self.max_magic_points_up: Decimal = max_magic_points_up
        self.max_magic_points_percentage_up: float = max_magic_points_percentage_up
        self.max_energy_up: Decimal = max_energy_up
        self.max_energy_percentage_up: float = max_energy_percentage_up
        self.crit_rate_up: float = crit_rate_up
        self.crit_damage_up: float = crit_damage_up
        self.evasion_chance_up: float = evasion_chance_up
        self.resistance_up: float = resistance_up
        self.accuracy_up: float = accuracy_up

    def clone(self):
        # type: () -> RuneStat
        return copy.deepcopy(self)


class SetEffect:
    """
    This class is used to initialise set effects of runes.
    """

    def __init__(self, max_hp_percentage_up, attack_percentage_up, defense_percentage_up, attack_speed_percentage_up,
                 max_magic_points_percentage_up, max_energy_percentage_up, crit_rate_up, crit_damage_up,
                 evasion_chance_up, resistance_up, accuracy_up, extra_turn_chance_up, counterattack_chance_up,
                 life_drain_percentage_up, stun_rate_up, allies_attack_percentage_up, allies_defense_percentage_up,
                 allies_max_hp_percentage_up, allies_accuracy_up, allies_resistance_up):
        # type: (float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float ,float) -> None
        self.max_hp_percentage_up: float = max_hp_percentage_up
        self.attack_percentage_up: float = attack_percentage_up
        self.defense_percentage_up: float = defense_percentage_up
        self.attack_speed_percentage_up: float = attack_speed_percentage_up
        self.max_magic_points_percentage_up: float = max_magic_points_percentage_up
        self.max_energy_percentage_up: float = max_energy_percentage_up
        self.crit_rate_up: float = crit_rate_up
        self.crit_damage_up: float = crit_damage_up
        self.evasion_chance_up: float = evasion_chance_up
        self.resistance_up: float = resistance_up
        self.accuracy_up: float = accuracy_up
        self.extra_turn_chance_up: float = extra_turn_chance_up
        self.counterattack_chance_up: float = counterattack_chance_up
        self.life_drain_percentage_up: float = life_drain_percentage_up
        self.stun_rate_up: float = stun_rate_up
        self.allies_attack_percentage_up: float = allies_attack_percentage_up
        self.allies_defense_percentage_up: float = allies_defense_percentage_up
        self.allies_max_hp_percentage_up: float = allies_max_hp_percentage_up
        self.allies_accuracy_up: float = allies_accuracy_up
        self.allies_resistance_up: float = allies_resistance_up

    def clone(self):
        # type: () -> SetEffect
        return copy.deepcopy(self)


class RuneUpgrade:
    """
    This class contains attributes of upgrades of a rune.
    """

    def __init__(self, rune_upgrade_id, name, description, purchase_coin_cost, application_coin_cost, sell_coin_gain):
        # type: (str, str, str, Decimal, Decimal, Decimal) -> None
        self.rune_upgrade_id: str = rune_upgrade_id
        self.name: str = name
        self.description: str = description
        self.purchase_coin_cost: Decimal = purchase_coin_cost
        self.application_coin_cost: Decimal = application_coin_cost
        self.sell_coin_gain: Decimal = sell_coin_gain

    def clone(self):
        # type: () -> RuneUpgrade
        return copy.deepcopy(self)


class EnchantedGem(RuneUpgrade):
    """
    This class contains attributes of enchanted gems to change rune stats.
    """

    def __init__(self, rune_upgrade_id, name, description, purchase_coin_cost, application_coin_cost, sell_coin_gain,
                 max_hp_up_increase, max_hp_percentage_up_increase, attack_up_increase, attack_percentage_up_increase,
                 defense_up_increase, defense_percentage_up_increase, attack_speed_up_increase,
                 max_magic_points_up_increase, max_magic_points_percentage_up_increase, max_energy_up_increase,
                 max_energy_percentage_up_increase, crit_rate_up_increase, crit_damage_up_increase,
                 evasion_chance_up_increase, resistance_up_increase, accuracy_up_increase):
        # type: (str, str, str, Decimal, Decimal, Decimal, Decimal, float, Decimal, float, Decimal, float, float, Decimal, float, Decimal, float, float, float, float, float, float) -> None
        RuneUpgrade.__init__(self, rune_upgrade_id, name, description, purchase_coin_cost, application_coin_cost,
                             sell_coin_gain)
        self.max_hp_up_increase: Decimal = max_hp_up_increase
        self.max_hp_percentage_up_increase: float = max_hp_percentage_up_increase
        self.attack_up_increase: Decimal = attack_up_increase
        self.attack_percentage_up_increase: float = attack_percentage_up_increase
        self.defense_up_increase: Decimal = defense_up_increase
        self.defense_percentage_up_increase: float = defense_percentage_up_increase
        self.attack_speed_up_increase: float = attack_speed_up_increase
        self.max_magic_points_up_increase: Decimal = max_magic_points_up_increase
        self.max_magic_points_percentage_up_increase: float = max_magic_points_percentage_up_increase
        self.max_energy_up_increase: Decimal = max_energy_up_increase
        self.max_energy_percentage_up_increase: float = max_energy_percentage_up_increase
        self.crit_rate_up_increase: float = crit_rate_up_increase
        self.crit_damage_up_increase: float = crit_damage_up_increase
        self.evasion_chance_up_increase: float = evasion_chance_up_increase
        self.resistance_up_increase: float = resistance_up_increase
        self.accuracy_up_increase: float = accuracy_up_increase


class Grindstone(RuneUpgrade):
    """
    This class contains attributes of grindstones which are used to increase rune stats.
    """

    def __init__(self, rune_upgrade_id, name, description, purchase_coin_cost, application_coin_cost, sell_coin_gain,
                 max_hp_up_increase, max_hp_percentage_up_increase, attack_up_increase, attack_percentage_up_increase,
                 defense_up_increase, defense_percentage_up_increase, attack_speed_up_increase,
                 max_magic_points_up_increase, max_magic_points_percentage_up_increase, max_energy_up_increase,
                 max_energy_percentage_up_increase, crit_rate_up_increase, crit_damage_up_increase,
                 evasion_chance_up_increase, resistance_up_increase, accuracy_up_increase):
        # type: (str, str, str, Decimal, Decimal, Decimal, Decimal, float, Decimal, float, Decimal, float, float, Decimal, float, Decimal, float, float, float, float, float, float) -> None
        RuneUpgrade.__init__(self, rune_upgrade_id, name, description, purchase_coin_cost, application_coin_cost,
                             sell_coin_gain)
        self.max_hp_up_increase: Decimal = max_hp_up_increase
        self.max_hp_percentage_up_increase: float = max_hp_percentage_up_increase
        self.attack_up_increase: Decimal = attack_up_increase
        self.attack_percentage_up_increase: float = attack_percentage_up_increase
        self.defense_up_increase: Decimal = defense_up_increase
        self.defense_percentage_up_increase: float = defense_percentage_up_increase
        self.attack_speed_up_increase: float = attack_speed_up_increase
        self.max_magic_points_up_increase: Decimal = max_magic_points_up_increase
        self.max_magic_points_percentage_up_increase: float = max_magic_points_percentage_up_increase
        self.max_energy_up_increase: Decimal = max_energy_up_increase
        self.max_energy_percentage_up_increase: float = max_energy_percentage_up_increase
        self.crit_rate_up_increase: float = crit_rate_up_increase
        self.crit_damage_up_increase: float = crit_damage_up_increase
        self.evasion_chance_up_increase: float = evasion_chance_up_increase
        self.resistance_up_increase: float = resistance_up_increase
        self.accuracy_up_increase: float = accuracy_up_increase


class ReappraisalStone(RuneUpgrade):
    """
    This class contains attributes of reappraisal stones to reroll the rune stats.
    """

    def __init__(self, rune_upgrade_id, name, description, purchase_coin_cost, application_coin_cost, sell_coin_gain,
                 max_hp_up_increase, max_hp_percentage_up_increase, attack_up_increase, attack_percentage_up_increase,
                 defense_up_increase, defense_percentage_up_increase, attack_speed_up_increase,
                 max_magic_points_up_increase, max_magic_points_percentage_up_increase, max_energy_up_increase,
                 max_energy_percentage_up_increase, crit_rate_up_increase, crit_damage_up_increase,
                 evasion_chance_up_increase, resistance_up_increase, accuracy_up_increase):
        # type: (str, str, str, Decimal, Decimal, Decimal, Decimal, float, Decimal, float, Decimal, float, float, Decimal, float, Decimal, float, float, float, float, float, float) -> None
        RuneUpgrade.__init__(self, rune_upgrade_id, name, description, purchase_coin_cost, application_coin_cost,
                             sell_coin_gain)
        self.max_hp_up_increase: Decimal = max_hp_up_increase
        self.max_hp_percentage_up_increase: float = max_hp_percentage_up_increase
        self.attack_up_increase: Decimal = attack_up_increase
        self.attack_percentage_up_increase: float = attack_percentage_up_increase
        self.defense_up_increase: Decimal = defense_up_increase
        self.defense_percentage_up_increase: float = defense_percentage_up_increase
        self.attack_speed_up_increase: float = attack_speed_up_increase
        self.max_magic_points_up_increase: Decimal = max_magic_points_up_increase
        self.max_magic_points_percentage_up_increase: float = max_magic_points_percentage_up_increase
        self.max_energy_up_increase: Decimal = max_energy_up_increase
        self.max_energy_percentage_up_increase: float = max_energy_percentage_up_increase
        self.crit_rate_up_increase: float = crit_rate_up_increase
        self.crit_damage_up_increase: float = crit_damage_up_increase
        self.evasion_chance_up_increase: float = evasion_chance_up_increase
        self.resistance_up_increase: float = resistance_up_increase
        self.accuracy_up_increase: float = accuracy_up_increase


class Rune:
    """
    This class contains attributes of runes which can be placed on heroes.
    """
    MIN_SLOT_NUMBER: int = 1
    MAX_SLOT_NUMBER: int = 6
    MIN_RATING: int = 1
    MAX_RATING: int = 6
    MIN_LEVEL: int = 0
    MAX_LEVEL: int = 100
    POSSIBLE_SET_NAMES: list = ["ENERGY", "FATAL", "RAGE", "GUARD", "BLADE", "DODGE", "MAGIC", "ENDURANCE", "ENDURE", "FOCUS",
                          "SWIFT", "VIOLENT", "REVENGE", "VAMPIRE", "DESPAIR", "FIGHT", "DETERMINATION", "ENHANCE",
                          "ACCURACY", "TOLERANCE"]

    def __init__(self, rune_id, slot_number, rating, set_name, prefix_stat, main_stat, rune_stat, rune_upgrades_applied,
                 purchase_coin_cost):
        # type: (str, int, int, str, PrefixStat, MainStat, RuneStat, list, Decimal) -> None
        self.rune_id: str = rune_id
        self.slot_number: int = slot_number if self.MIN_SLOT_NUMBER <= slot_number <= self.MAX_SLOT_NUMBER else 1
        self.rating: int = rating if self.MIN_RATING <= rating <= self.MAX_RATING else 1
        self.level: int = self.MIN_LEVEL
        self.set_name: str = set_name if set_name in self.POSSIBLE_SET_NAMES else None
        self.complete_set_size: int = 4 if self.set_name == "FATAL" or self.set_name == "RAGE" or \
                                      self.set_name == "MAGIC" or self.set_name == "SWIFT" or self.set_name == "VIOLENT" or \
                                      self.set_name == "VAMPIRE" else 2
        self.set_effect: SetEffect = SetEffect(20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0) \
            if self.set_name == "ENERGY" else SetEffect(0, 35, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0) \
            if self.set_name == "FATAL" else SetEffect(0, 0, 0, 0, 0, 0, 0, 0.4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0) \
            if self.set_name == "RAGE" else SetEffect(0, 0, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0) \
            if self.set_name == "GUARD" else SetEffect(0, 0, 0, 0, 0, 0, 0.12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0) \
            if self.set_name == "BLADE" else SetEffect(0, 0, 0, 0, 0, 0, 0, 0, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0) \
            if self.set_name == "DODGE" else SetEffect(0, 0, 0, 0, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0) \
            if self.set_name == "MAGIC" else SetEffect(0, 0, 0, 0, 0, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0) \
            if self.set_name == "ENDURANCE" else SetEffect(0, 0, 0, 0, 0, 0, 0, 0, 0, 0.2, 0, 0, 0, 0, 0, 0, 0, 0,
                                                           0, 0) if self.set_name == "ENDURE" else SetEffect(0, 0, 0, 0,
                                                                                                             0, 0, 0, 0,
                                                                                                             0, 0, 0.2,
                                                                                                             0, 0, 0, 0,
                                                                                                             0,
                                                                                                             0, 0, 0,
                                                                                                             0) if self.set_name == "FOCUS" else SetEffect(
            0, 0, 0, 25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0) if self.set_name == "SWIFT" else SetEffect(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.22, 0, 0, 0, 0, 0,
                                                                0, 0, 0) if self.set_name == "VIOLENT" else SetEffect(0,
                                                                                                                      0,
                                                                                                                      0,
                                                                                                                      0,
                                                                                                                      0,
                                                                                                                      0,
                                                                                                                      0,
                                                                                                                      0,
                                                                                                                      0,
                                                                                                                      0,
                                                                                                                      0,
                                                                                                                      0,
                                                                                                                      0.15,
                                                                                                                      0,
                                                                                                                      0,
                                                                                                                      0,
                                                                                                                      0,
                                                                                                                      0,
                                                                                                                      0,
                                                                                                                      0) if self.set_name == "REVENGE" else SetEffect(
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 35, 0,
            0, 0, 0, 0, 0) if self.set_name == "VAMPIRE" else SetEffect(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                                        0, 0.25, 0, 0, 0, 0,
                                                                        0) if self.set_name == "DESPAIR" else SetEffect(
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 8, 0, 0, 0, 0) if self.set_name == "FIGHT" else SetEffect(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                                            0, 0, 0, 8, 0, 0,
                                                                            0) if self.set_name == "DETERMINATION" else SetEffect(
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0) if self.set_name == "ENHANCE" else SetEffect(0, 0, 0, 0, 0, 0, 0, 0,
                                                                                             0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                                                             0, 10,
                                                                                             0) if self.set_name == "ACCURACY" else SetEffect(
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10) if self.set_name == "TOLERANCE" else SetEffect(0, 0, 0, 0, 0, 0, 0, 0,
                                                                                                0, 0, 0, 0, 0, 0, 0, 0,
                                                                                                0, 0, 0, 0)
        self.prefix_stat: PrefixStat = prefix_stat
        self.main_stat: MainStat = main_stat
        self.rune_stat: RuneStat = rune_stat
        self.rune_upgrades_applied: list = rune_upgrades_applied
        self.purchase_coin_cost: Decimal = purchase_coin_cost
        self.sell_coin_gain: Decimal = self.purchase_coin_cost / 5
        self.level_up_coin_cost: Decimal = Decimal("10e1") ** (10 * 2 ** (self.rating - 1))
        self.level_up_success_rate: float = 1
        self.set_effect_applied: bool = False
        self.removal_coin_cost: Decimal = Decimal("10e1") ** (15 * 2 ** (self.rating - 1))

    def to_string(self):
        # type: () -> str
        res: str = ""  # initial value
        res += "Slot number: " + str(self.slot_number) + "\n"
        res += "Rating: " + str(self.rating) + "\n"
        res += "Level: " + str(self.level) + "\n"
        return res

    def clone(self):
        # type: () -> Rune
        return copy.deepcopy(self)


class Hero:
    """
    This class contains attributes of heroes in this game.
    """
    MIN_LEVEL: int = 1
    MIN_RATING: int = 1
    MAX_RATING: int = 30
    MIN_CRIT_RATE: float = 0.15
    MAX_CRIT_RATE: float = 1
    MIN_CRIT_DAMAGE: float = 2
    MIN_EVASION_CHANCE = 0
    MAX_EVASION_CHANCE = 0.5
    MIN_RESISTANCE: float = 0.15
    MAX_RESISTANCE: float = 1
    MIN_ACCURACY: float = 0
    MAX_ACCURACY: float = 1
    MIN_EXTRA_TURN_CHANCE: float = 0
    MAX_EXTRA_TURN_CHANCE: float = 0.5
    MIN_COUNTERATTACK_CHANCE: float = 0
    MAX_COUNTERATTACK_CHANCE: float = 1
    MIN_STUN_RATE: float = 0
    MAX_STUN_RATE: float = 1
    MIN_ATTACK_GAUGE: float = 0
    POSSIBLE_TYPES: list = ["MATERIAL", "SUPPORT", "HP", "ATTACK", "DEFENSE"]
    POSSIBLE_ELEMENTS: list = ["LIGHT", "DARK", "MAGIC", "UNDEAD", "WATER", "AIR", "FIRE", "TECH", "EARTH", "LIFE",
                               "NEUTRAL"]
    MIN_BUFFS: int = 0
    MAX_BUFFS: int = 10
    MIN_DEBUFFS: int = 0
    MAX_DEBUFFS: int = 10
    MIN_RUNES: int = 0
    MAX_RUNES: int = 6

    def __init__(self, hero_id, name, type, element, rating, max_hp, attack_power, defense, attack_speed,
                 max_magic_points, max_energy, skills, awaken_bonus, num_awakening_shards_required,
                 secondary_awaken_bonus):
        # type: (str, str, str, str, int, Decimal, Decimal, Decimal, float, Decimal, Decimal, list, AwakenBonus, int, SecondaryAwakenBonus) -> None
        self.hero_id: str = hero_id
        self.name: str = name
        self.type: str or None = type if type in self.POSSIBLE_TYPES else None
        self.element: str or None = element if element in self.POSSIBLE_ELEMENTS else None
        self.rating: int = rating if self.MIN_RATING <= rating <= self.MAX_RATING else 1
        self.level: int = 1
        self.max_level: int = triangulation(self.rating) * 10
        self.curr_hp: Decimal = max_hp
        self.max_hp: Decimal = max_hp
        self.attack_power: Decimal = attack_power
        self.defense: Decimal = defense
        self.attack_speed: float = attack_speed
        self.curr_magic_points: Decimal = max_magic_points
        self.max_magic_points: Decimal = max_magic_points
        self.curr_energy: Decimal = max_energy
        self.max_energy: Decimal = max_energy
        self.crit_rate: float = self.MIN_CRIT_RATE
        self.crit_damage: float = self.MIN_CRIT_DAMAGE
        self.evasion_chance: float = self.MIN_EVASION_CHANCE
        self.resistance: float = self.MIN_RESISTANCE
        self.accuracy: float = self.MIN_ACCURACY
        self.extra_turn_chance: float = self.MIN_EXTRA_TURN_CHANCE
        self.counterattack_chance: float = self.MIN_COUNTERATTACK_CHANCE
        self.glancing_hit_chance: float = 0
        self.normal_hit_chance: float = 0
        self.crushing_hit_chance: float = 0
        self.critical_hit_chance: float = 0
        self.attack_gauge = self.MIN_ATTACK_GAUGE
        self.life_drain_percentage: float = 0
        self.stun_rate: float = self.MIN_STUN_RATE
        self.reflected_damage_percentage: float = 0
        self.additional_damage_percentage_received: float = 0
        self.skills: list = skills
        self.awaken_bonus: AwakenBonus = awaken_bonus
        self.num_awakening_shards_required: int = num_awakening_shards_required
        self.secondary_awaken_bonus: SecondaryAwakenBonus = secondary_awaken_bonus
        self.buffs: list = []
        self.debuffs: list = []
        self.runes: dict = {}
        self.secondary_awakening_exp: Decimal = Decimal("0e0")
        self.is_alive: bool = True
        self.can_move: bool = True
        self.corresponding_team: Team or None = None  # initial value
        self.limit_break_applied: bool = False  # initial value
        self.strength: Decimal = self.calculate_strength()

    def to_string(self) -> str:
        res: str = ""  # initial value
        res += "Name: " + str(self.name) + "\n"
        res += "Type: " + str(self.type) + "\n"
        res += "Element: " + str(self.element) + "\n"
        res += "Rating: " + str(self.rating) + "\n"
        res += "Level: " + str(self.level) + "/" + str(self.max_level) + "\n" if self.max_level != float('inf') \
            else "Level: " + str(self.level) + "\n"
        res += "HP: " + str(self.curr_hp) + "/" + str(self.max_hp) + "\n"
        res += "Attack power: " + str(self.attack_power) + "\n"
        res += "Defense: " + str(self.defense) + "\n"
        res += "Attack speed: " + str(self.attack_speed) + "\n"
        res += "Magic points: " + str(self.curr_magic_points) + "/" + str(self.max_magic_points) + "\n"
        res += "Energy: " + str(self.curr_energy) + "/" + str(self.max_energy) + "\n"
        res += "Crit rate: " + str(100 * self.crit_rate) + "%\n"
        res += "Crit damage: " + str(100 * self.crit_damage) + "%\n"
        res += "Evasion chance: " + str(100 * self.evasion_chance) + "%\n"
        res += "Resistance: " + str(100 * self.resistance) + "%\n"
        res += "Accuracy: " + str(100 * self.accuracy) + "%\n"
        res += "Extra turn chance: " + str(100 * self.extra_turn_chance) + "%\n"
        res += "Counterattack chance: " + str(100 * self.counterattack_chance) + "%\n"
        res += "Glancing hit chance: " + str(100 * self.glancing_hit_chance) + "%\n"
        res += "Normal hit chance: " + str(100 * self.normal_hit_chance) + "%\n"
        res += "Crushing hit chance: " + str(100 * self.crushing_hit_chance) + "%\n"
        res += "Critical hit chance: " + str(100 * self.critical_hit_chance) + "%\n"
        res += "Attack gauge: " + str(100 * self.attack_gauge) + "%\n"
        res += "Life drain percentage: " + str(self.life_drain_percentage) + "%\n"
        res += "Stun rate: " + str(100 * self.stun_rate) + "%\n"
        res += "Reflected damage percentage: " + str(self.reflected_damage_percentage) + "%\n"
        res += "Additional damage percentage received: " + str(self.additional_damage_percentage_received) + "%\n"
        res += "Below is a list of skills this hero has.\n"
        for skill in self.skills:
            res += str(skill.to_string()) + "\n"

        res += "Awaken bonus: \n" + str(self.awaken_bonus.to_string()) + "\n"
        res += "Number of awakening shards required to awaken this hero: " + str(
            self.num_awakening_shards_required) + "\n"
        res += "Secondary awaken bonus: \n" + str(self.secondary_awaken_bonus.to_string()) + "\n"

        res += "Below is a list of buffs that this hero has.\n"
        for buff in self.buffs:
            res += str(buff.to_string()) + "\n"

        res += "Below is a list of debuffs that this hero has.\n"
        for debuff in self.debuffs:
            res += str(debuff.to_string()) + "\n"

        res += "Below is a list of runes equipped to this hero.\n"
        for slot_number in self.runes.keys():
            res += str(self.runes[slot_number].to_string()) + "\n"

        res += "Secondary awakening EXP: " + str(self.secondary_awakening_exp) + "\n"
        res += "Is it alive? " + str(self.get_is_alive()) + "\n"
        res += "Can it move? " + str(self.get_can_move()) + "\n"
        res += "Has limit break been applied to this hero? " + str(self.limit_break_applied) + "\n"
        res += "Strength: " + str(self.calculate_strength()) + "\n"
        return res

    def clone(self):
        # type: () -> Hero
        return copy.deepcopy(self)

    def get_can_move(self):
        self.can_move = True  # initial value
        for debuff in self.debuffs:
            if debuff.prevents_turn:
                self.can_move = False

        return self.can_move

    def calculate_strength(self):
        self.strength = 5 * Decimal(
            self.max_hp + self.attack + self.defense + self.max_magic_points + self.max_energy) * \
                        (1 + 100 * Decimal(self.crit_rate)) * (1 + 100 * Decimal(self.crit_damage)) * (
                                1 + 100 * Decimal(self.evasion_chance)) * \
                        (1 + 100 * Decimal(self.resistance)) * (1 + 100 * Decimal(self.accuracy)) * (
                                1 + 100 * Decimal(self.extra_turn_chance)) * \
                        (1 + 100 * Decimal(self.counterattack_chance)) * (
                                1 + 100 * Decimal(self.life_drain_percentage)) * \
                        (1 + 100 * Decimal(self.reflected_damage_percentage)) * (1 + 100 * Decimal(self.stun_rate))
        return self.strength

    def place_rune(self, slot_number, rune):
        # type: (int, Rune) -> bool
        if slot_number in self.runes.keys():
            self.remove_rune(slot_number)
            self.runes[slot_number] = rune
            self.max_hp += rune.prefix_stat.max_hp_up
            self.max_hp *= Decimal(1 + rune.prefix_stat.max_hp_percentage_up/100)
            self.curr_hp = self.max_hp
            self.attack_power += rune.prefix_stat.attack_up
            self.attack_power *= Decimal(1 + rune.prefix_stat.attack_percentage_up)
            self.defense += rune.prefix_stat.defense_up
            self.defense *= Decimal(1 + rune.prefix_stat.defense_percentage_up)
            self.attack_speed += rune.prefix_stat.attack_speed_up
            self.max_magic_points += rune.prefix_stat.max_magic_points_up
            self.max_magic_points *= Decimal(1 + rune.prefix_stat.max_magic_points_percentage_up)
            self.curr_magic_points = self.max_magic_points
            self.max_energy += rune.prefix_stat.max_energy_up
            self.max_energy *= Decimal(1 + rune.prefix_stat.max_energy_percentage_up)
            self.curr_energy = self.max_energy
            self.crit_rate += rune.prefix_stat.crit_rate_up
            self.crit_rate = self.crit_rate if self.crit_rate <= self.MAX_CRIT_RATE else self.MAX_CRIT_RATE
            self.crit_damage += rune.prefix_stat.crit_damage_up
            self.evasion_chance += rune.prefix_stat.evasion_chance_up
            self.evasion_chance = self.evasion_chance if self.evasion_chance <= self.MAX_EVASION_CHANCE \
                else self.evasion_chance
            self.resistance += rune.prefix_stat.resistance_up
            self.resistance = self.resistance if self.resistance <= self.MAX_RESISTANCE else self.MAX_RESISTANCE
            self.accuracy += rune.prefix_stat.accuracy_up
            self.accuracy = self.accuracy if self.accuracy <= self.MAX_ACCURACY else self.MAX_ACCURACY
            self.max_hp += rune.main_stat.max_hp_up
            self.max_hp *= Decimal(1 + rune.main_stat.max_hp_percentage_up / 100)
            self.curr_hp = self.max_hp
            self.attack_power += rune.main_stat.attack_up
            self.attack_power *= Decimal(1 + rune.main_stat.attack_percentage_up)
            self.defense += rune.main_stat.defense_up
            self.defense *= Decimal(1 + rune.main_stat.defense_percentage_up)
            self.attack_speed += rune.main_stat.attack_speed_up
            self.max_magic_points += rune.main_stat.max_magic_points_up
            self.max_magic_points *= Decimal(1 + rune.main_stat.max_magic_points_percentage_up)
            self.curr_magic_points = self.max_magic_points
            self.max_energy += rune.main_stat.max_energy_up
            self.max_energy *= Decimal(1 + rune.main_stat.max_energy_percentage_up)
            self.curr_energy = self.max_energy
            self.crit_rate += rune.main_stat.crit_rate_up
            self.crit_rate = self.crit_rate if self.crit_rate <= self.MAX_CRIT_RATE else self.MAX_CRIT_RATE
            self.crit_damage += rune.main_stat.crit_damage_up
            self.evasion_chance += rune.main_stat.evasion_chance_up
            self.evasion_chance = self.evasion_chance if self.evasion_chance <= self.MAX_EVASION_CHANCE \
                else self.evasion_chance
            self.resistance += rune.main_stat.resistance_up
            self.resistance = self.resistance if self.resistance <= self.MAX_RESISTANCE else self.MAX_RESISTANCE
            self.accuracy += rune.main_stat.accuracy_up
            self.accuracy = self.accuracy if self.accuracy <= self.MAX_ACCURACY else self.MAX_ACCURACY
            self.max_hp += rune.rune_stat.max_hp_up
            self.max_hp *= Decimal(1 + rune.rune_stat.max_hp_percentage_up / 100)
            self.curr_hp = self.max_hp
            self.attack_power += rune.rune_stat.attack_up
            self.attack_power *= Decimal(1 + rune.rune_stat.attack_percentage_up)
            self.defense += rune.rune_stat.defense_up
            self.defense *= Decimal(1 + rune.rune_stat.defense_percentage_up)
            self.attack_speed += rune.rune_stat.attack_speed_up
            self.max_magic_points += rune.rune_stat.max_magic_points_up
            self.max_magic_points *= Decimal(1 + rune.rune_stat.max_magic_points_percentage_up)
            self.curr_magic_points = self.max_magic_points
            self.max_energy += rune.rune_stat.max_energy_up
            self.max_energy *= Decimal(1 + rune.rune_stat.max_energy_percentage_up)
            self.curr_energy = self.max_energy
            self.crit_rate += rune.rune_stat.crit_rate_up
            self.crit_rate = self.crit_rate if self.crit_rate <= self.MAX_CRIT_RATE else self.MAX_CRIT_RATE
            self.crit_damage += rune.rune_stat.crit_damage_up
            self.evasion_chance += rune.rune_stat.evasion_chance_up
            self.evasion_chance = self.evasion_chance if self.evasion_chance <= self.MAX_EVASION_CHANCE \
                else self.evasion_chance
            self.resistance += rune.rune_stat.resistance_up
            self.resistance = self.resistance if self.resistance <= self.MAX_RESISTANCE else self.MAX_RESISTANCE
            self.accuracy += rune.rune_stat.accuracy_up
            self.accuracy = self.accuracy if self.accuracy <= self.MAX_ACCURACY else self.MAX_ACCURACY
            return True
        else:
            self.runes[slot_number] = rune
            self.max_hp += rune.prefix_stat.max_hp_up
            self.max_hp *= Decimal(1 + rune.prefix_stat.max_hp_percentage_up / 100)
            self.curr_hp = self.max_hp
            self.attack_power += rune.prefix_stat.attack_up
            self.attack_power *= Decimal(1 + rune.prefix_stat.attack_percentage_up)
            self.defense += rune.prefix_stat.defense_up
            self.defense *= Decimal(1 + rune.prefix_stat.defense_percentage_up)
            self.attack_speed += rune.prefix_stat.attack_speed_up
            self.max_magic_points += rune.prefix_stat.max_magic_points_up
            self.max_magic_points *= Decimal(1 + rune.prefix_stat.max_magic_points_percentage_up)
            self.curr_magic_points = self.max_magic_points
            self.max_energy += rune.prefix_stat.max_energy_up
            self.max_energy *= Decimal(1 + rune.prefix_stat.max_energy_percentage_up)
            self.curr_energy = self.max_energy
            self.crit_rate += rune.prefix_stat.crit_rate_up
            self.crit_rate = self.crit_rate if self.crit_rate <= self.MAX_CRIT_RATE else self.MAX_CRIT_RATE
            self.crit_damage += rune.prefix_stat.crit_damage_up
            self.evasion_chance += rune.prefix_stat.evasion_chance_up
            self.evasion_chance = self.evasion_chance if self.evasion_chance <= self.MAX_EVASION_CHANCE \
                else self.evasion_chance
            self.resistance += rune.prefix_stat.resistance_up
            self.resistance = self.resistance if self.resistance <= self.MAX_RESISTANCE else self.MAX_RESISTANCE
            self.accuracy += rune.prefix_stat.accuracy_up
            self.accuracy = self.accuracy if self.accuracy <= self.MAX_ACCURACY else self.MAX_ACCURACY
            self.max_hp += rune.main_stat.max_hp_up
            self.max_hp *= Decimal(1 + rune.main_stat.max_hp_percentage_up / 100)
            self.curr_hp = self.max_hp
            self.attack_power += rune.main_stat.attack_up
            self.attack_power *= Decimal(1 + rune.main_stat.attack_percentage_up)
            self.defense += rune.main_stat.defense_up
            self.defense *= Decimal(1 + rune.main_stat.defense_percentage_up)
            self.attack_speed += rune.main_stat.attack_speed_up
            self.max_magic_points += rune.main_stat.max_magic_points_up
            self.max_magic_points *= Decimal(1 + rune.main_stat.max_magic_points_percentage_up)
            self.curr_magic_points = self.max_magic_points
            self.max_energy += rune.main_stat.max_energy_up
            self.max_energy *= Decimal(1 + rune.main_stat.max_energy_percentage_up)
            self.curr_energy = self.max_energy
            self.crit_rate += rune.main_stat.crit_rate_up
            self.crit_rate = self.crit_rate if self.crit_rate <= self.MAX_CRIT_RATE else self.MAX_CRIT_RATE
            self.crit_damage += rune.main_stat.crit_damage_up
            self.evasion_chance += rune.main_stat.evasion_chance_up
            self.evasion_chance = self.evasion_chance if self.evasion_chance <= self.MAX_EVASION_CHANCE \
                else self.evasion_chance
            self.resistance += rune.main_stat.resistance_up
            self.resistance = self.resistance if self.resistance <= self.MAX_RESISTANCE else self.MAX_RESISTANCE
            self.accuracy += rune.main_stat.accuracy_up
            self.accuracy = self.accuracy if self.accuracy <= self.MAX_ACCURACY else self.MAX_ACCURACY
            self.max_hp += rune.rune_stat.max_hp_up
            self.max_hp *= Decimal(1 + rune.rune_stat.max_hp_percentage_up / 100)
            self.curr_hp = self.max_hp
            self.attack_power += rune.rune_stat.attack_up
            self.attack_power *= Decimal(1 + rune.rune_stat.attack_percentage_up)
            self.defense += rune.rune_stat.defense_up
            self.defense *= Decimal(1 + rune.rune_stat.defense_percentage_up)
            self.attack_speed += rune.rune_stat.attack_speed_up
            self.max_magic_points += rune.rune_stat.max_magic_points_up
            self.max_magic_points *= Decimal(1 + rune.rune_stat.max_magic_points_percentage_up)
            self.curr_magic_points = self.max_magic_points
            self.max_energy += rune.rune_stat.max_energy_up
            self.max_energy *= Decimal(1 + rune.rune_stat.max_energy_percentage_up)
            self.curr_energy = self.max_energy
            self.crit_rate += rune.rune_stat.crit_rate_up
            self.crit_rate = self.crit_rate if self.crit_rate <= self.MAX_CRIT_RATE else self.MAX_CRIT_RATE
            self.crit_damage += rune.rune_stat.crit_damage_up
            self.evasion_chance += rune.rune_stat.evasion_chance_up
            self.evasion_chance = self.evasion_chance if self.evasion_chance <= self.MAX_EVASION_CHANCE \
                else self.evasion_chance
            self.resistance += rune.rune_stat.resistance_up
            self.resistance = self.resistance if self.resistance <= self.MAX_RESISTANCE else self.MAX_RESISTANCE
            self.accuracy += rune.rune_stat.accuracy_up
            self.accuracy = self.accuracy if self.accuracy <= self.MAX_ACCURACY else self.MAX_ACCURACY
            return True

    def remove_rune(self, slot_number):
        # type: (int) -> bool
        if slot_number in self.runes.keys():
            removed_rune: Rune = self.runes.pop(slot_number)
            self.max_hp -= removed_rune.prefix_stat.max_hp_up
            self.max_hp /= Decimal(1 + removed_rune.prefix_stat.max_hp_percentage_up / 100)
            self.curr_hp = self.max_hp
            self.attack_power -= removed_rune.prefix_stat.attack_up
            self.attack_power /= Decimal(1 + removed_rune.prefix_stat.attack_percentage_up)
            self.defense -= removed_rune.prefix_stat.defense_up
            self.defense /= Decimal(1 + removed_rune.prefix_stat.defense_percentage_up)
            self.attack_speed -= removed_rune.prefix_stat.attack_speed_up
            self.max_magic_points -= removed_rune.prefix_stat.max_magic_points_up
            self.max_magic_points /= Decimal(1 + removed_rune.prefix_stat.max_magic_points_percentage_up)
            self.curr_magic_points = self.max_magic_points
            self.max_energy -= removed_rune.prefix_stat.max_energy_up
            self.max_energy /= Decimal(1 + removed_rune.prefix_stat.max_energy_percentage_up)
            self.curr_energy = self.max_energy
            self.crit_rate -= removed_rune.prefix_stat.crit_rate_up
            self.crit_rate = self.crit_rate if self.crit_rate <= self.MAX_CRIT_RATE else self.MAX_CRIT_RATE
            self.crit_damage -= removed_rune.prefix_stat.crit_damage_up
            self.evasion_chance -= removed_rune.prefix_stat.evasion_chance_up
            self.evasion_chance = self.evasion_chance if self.evasion_chance <= self.MAX_EVASION_CHANCE \
                else self.evasion_chance
            self.resistance -= removed_rune.prefix_stat.resistance_up
            self.resistance = self.resistance if self.resistance <= self.MAX_RESISTANCE else self.MAX_RESISTANCE
            self.accuracy -= removed_rune.prefix_stat.accuracy_up
            self.accuracy = self.accuracy if self.accuracy <= self.MAX_ACCURACY else self.MAX_ACCURACY
            self.max_hp -= removed_rune.main_stat.max_hp_up
            self.max_hp /= Decimal(1 + removed_rune.main_stat.max_hp_percentage_up / 100)
            self.curr_hp = self.max_hp
            self.attack_power -= removed_rune.main_stat.attack_up
            self.attack_power /= Decimal(1 + removed_rune.main_stat.attack_percentage_up)
            self.defense -= removed_rune.main_stat.defense_up
            self.defense /= Decimal(1 + removed_rune.main_stat.defense_percentage_up)
            self.attack_speed -= removed_rune.main_stat.attack_speed_up
            self.max_magic_points -= removed_rune.main_stat.max_magic_points_up
            self.max_magic_points /= Decimal(1 + removed_rune.main_stat.max_magic_points_percentage_up)
            self.curr_magic_points = self.max_magic_points
            self.max_energy -= removed_rune.main_stat.max_energy_up
            self.max_energy /= Decimal(1 + removed_rune.main_stat.max_energy_percentage_up)
            self.curr_energy = self.max_energy
            self.crit_rate -= removed_rune.main_stat.crit_rate_up
            self.crit_rate = self.crit_rate if self.crit_rate <= self.MAX_CRIT_RATE else self.MAX_CRIT_RATE
            self.crit_damage -= removed_rune.main_stat.crit_damage_up
            self.evasion_chance -= removed_rune.main_stat.evasion_chance_up
            self.evasion_chance = self.evasion_chance if self.evasion_chance <= self.MAX_EVASION_CHANCE \
                else self.evasion_chance
            self.resistance -= removed_rune.main_stat.resistance_up
            self.resistance = self.resistance if self.resistance <= self.MAX_RESISTANCE else self.MAX_RESISTANCE
            self.accuracy -= removed_rune.main_stat.accuracy_up
            self.accuracy = self.accuracy if self.accuracy <= self.MAX_ACCURACY else self.MAX_ACCURACY
            self.max_hp -= removed_rune.rune_stat.max_hp_up
            self.max_hp /= Decimal(1 + removed_rune.rune_stat.max_hp_percentage_up / 100)
            self.curr_hp = self.max_hp
            self.attack_power -= removed_rune.rune_stat.attack_up
            self.attack_power /= Decimal(1 + removed_rune.rune_stat.attack_percentage_up)
            self.defense -= removed_rune.rune_stat.defense_up
            self.defense /= Decimal(1 + removed_rune.rune_stat.defense_percentage_up)
            self.attack_speed -= removed_rune.rune_stat.attack_speed_up
            self.max_magic_points -= removed_rune.rune_stat.max_magic_points_up
            self.max_magic_points /= Decimal(1 + removed_rune.rune_stat.max_magic_points_percentage_up)
            self.curr_magic_points = self.max_magic_points
            self.max_energy -= removed_rune.rune_stat.max_energy_up
            self.max_energy /= Decimal(1 + removed_rune.rune_stat.max_energy_percentage_up)
            self.curr_energy = self.max_energy
            self.crit_rate -= removed_rune.rune_stat.crit_rate_up
            self.crit_rate = self.crit_rate if self.crit_rate <= self.MAX_CRIT_RATE else self.MAX_CRIT_RATE
            self.crit_damage -= removed_rune.rune_stat.crit_damage_up
            self.evasion_chance -= removed_rune.rune_stat.evasion_chance_up
            self.evasion_chance = self.evasion_chance if self.evasion_chance <= self.MAX_EVASION_CHANCE \
                else self.evasion_chance
            self.resistance -= removed_rune.rune_stat.resistance_up
            self.resistance = self.resistance if self.resistance <= self.MAX_RESISTANCE else self.MAX_RESISTANCE
            self.accuracy -= removed_rune.rune_stat.accuracy_up
            self.accuracy = self.accuracy if self.accuracy <= self.MAX_ACCURACY else self.MAX_ACCURACY
            return True
        return False

    def recover_energy(self):
        self.curr_energy += Decimal(1 / 12) * self.max_energy
        self.curr_energy = self.curr_energy if self.curr_energy <= self.max_energy else self.max_energy

    def recover_magic_points(self):
        self.curr_magic_points += Decimal(1 / 12) * self.max_magic_points
        self.curr_magic_points = self.curr_magic_points if self.curr_magic_points <= \
                                                           self.max_magic_points else self.max_magic_points

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

    def add_buff(self, buff):
        # type: (Buff) -> bool
        if len(self.buffs) < self.MAX_BUFFS:
            buff_name_list: list = [curr_buff.name for curr_buff in self.buffs]
            if buff.name not in buff_name_list or buff.is_stackable:
                self.buffs.append(buff)
                self.attack_power *= Decimal(1 + buff.attack_percentage_up / 100)
                self.defense *= Decimal(1 + buff.defense_percentage_up / 100)
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
        damage: Decimal = self.attack_power * Decimal(
            self.crit_damage) - other.defense if is_crit else self.attack_power - \
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
        self.curr_magic_points -= skill.magic_points_cost
        self.curr_energy -= skill.energy_cost
        if skill.does_heal:
            heal_amount: Decimal = skill.heal_amount
            target.curr_hp += heal_amount
            target.curr_hp = target.curr_hp if target.curr_hp <= target.max_hp else target.max_hp
            for buff in skill.buffs_to_allies:
                target.add_buff(buff.clone())
            return_string += str(self.name) + " healed " + str(target.name) + " with amount of " + str(
                heal_amount) + " HP.\n"

        if skill.does_attack:
            is_crit: bool = random.random() <= self.crit_rate
            damage: Decimal = self.attack_power * Decimal(skill.damage_multiplier) * Decimal(
                self.crit_damage) - target.defense \
                if is_crit else self.attack_power * Decimal(skill.damage_multiplier) - target.defense
            target.curr_hp -= damage
            for debuff in skill.debuffs_to_enemies:
                if random.random() > self.resistance_accuracy_rule(target):
                    target.add_debuff(debuff.clone())
            return_string += str(self.name) + " did " + str(damage) + " damage on " + str(target.name)
            if target.curr_hp <= 0:
                return_string += str(self.name) + " killed " + str(target.name)

            return_string += "\n"

        return return_string


class Skill:
    """
    This class contains attributes of skills that a hero has.
    """

    def __init__(self, skill_id, name, description):
        # type: (str, str, str) -> None
        self.skill_id: str = skill_id
        self.name: str = name
        self.description: str = description

    def to_string(self) -> str:
        res: str = ""  # initial value
        res += "Skill ID: " + str(self.skill_id) + "\n"
        res += "Name: " + str(self.name) + "\n"
        res += "Description: " + str(self.description) + "\n"
        return res

    def clone(self):
        # type: () -> Skill
        return copy.deepcopy(self)


class ActiveSkill(Skill):
    """
    This class is used to initialise active skills that characters have.
    """

    def __init__(self, skill_id, name, description, max_level, does_attack, does_heal_self, does_heal_allies,
                 does_revive_self, does_revive_allies, does_remove_self_debuffs, does_remove_allies_debuffs,
                 does_remove_enemies_buffs, does_increase_self_attack_gauge, does_increase_allies_attack_gauge,
                 does_decrease_enemies_attack_gauge, does_ignore_enemies_defense, is_aoe, heal_amount_to_self,
                 heal_amount_to_allies, revival_amount_to_self, revival_amount_to_allies,
                 attack_gauge_increase_to_self, attack_gauge_increase_to_allies, attack_gauge_decrease_to_enemies,
                 does_decrease_allies_skill_cooltime, does_increase_enemies_skill_cooltime, buffs_to_self,
                 buffs_to_allies, debuffs_to_enemies, magic_points_cost, energy_cost, damage_multiplier_to_self_max_hp,
                 damage_multiplier_to_enemies_max_hp, damage_multiplier_to_self_attack,
                 damage_multiplier_to_self_defense, damage_multiplier_to_self_attack_speed,
                 damage_multiplier_to_number_of_dead_allies, damage_multiplier_to_number_of_dead_enemies,
                 damage_multiplier_to_number_of_debuffs_on_enemies, damage_percentage_up_on_enemies_without_buffs,
                 damage_percentage_up_per_self_hp_percentage_loss, damage_percentage_up_per_self_current_hp_percentage,
                 damage_percentage_up_per_enemies_hp_percentage_loss,
                 damage_percentage_up_per_enemies_current_hp_percentage, max_cooltime, skill_level_up_bonus):
        # type: (str, str, str, int, bool, bool, bool, bool, bool, bool, bool, bool, bool, bool, bool, bool, bool, Decimal, Decimal, Decimal, Decimal, float, float, float, bool, bool, list, list, list, Decimal, Decimal, float, float, float, float, float, float, float, float, float, float, float, float, float, int, SkillLevelUpBonus) -> None
        Skill.__init__(self, skill_id, name, description)
        self.level: int = 1
        self.max_level: int = max_level
        self.does_attack: bool = does_attack
        self.does_heal_self: bool = does_heal_self
        self.does_heal_allies: bool = does_heal_allies
        self.does_revive_self: bool = does_revive_self
        self.does_revive_allies: bool = does_revive_allies
        self.does_remove_self_debuffs: bool = does_remove_self_debuffs
        self.does_remove_allies_debuffs: bool = does_remove_allies_debuffs
        self.does_remove_enemies_buffs: bool = does_remove_enemies_buffs
        self.does_increase_self_attack_gauge: bool = does_increase_self_attack_gauge
        self.does_increase_allies_attack_gauge: bool = does_increase_allies_attack_gauge
        self.does_decrease_enemies_attack_gauge: bool = does_decrease_enemies_attack_gauge
        self.does_ignore_enemies_defense: bool = does_ignore_enemies_defense
        self.is_aoe: bool = is_aoe
        self.heal_amount_to_self: Decimal = heal_amount_to_self
        self.heal_amount_to_allies: Decimal = heal_amount_to_allies
        self.revival_amount_to_self: Decimal = revival_amount_to_self
        self.revival_amount_to_allies: Decimal = revival_amount_to_allies
        self.attack_gauge_increase_to_self: float = attack_gauge_increase_to_self
        self.attack_gauge_increase_to_allies: float = attack_gauge_increase_to_allies
        self.attack_gauge_decrease_to_enemies: float = attack_gauge_decrease_to_enemies
        self.does_decrease_allies_skill_cooltime: float = does_decrease_allies_skill_cooltime
        self.does_increase_enemies_skill_cooltime: float = does_increase_enemies_skill_cooltime
        self.buffs_to_self: list = buffs_to_self  # a list of Buff class objects
        self.buffs_to_allies: list = buffs_to_allies  # a list of Buff class objects
        self.debuffs_to_enemies: list = debuffs_to_enemies  # a list of Debuff class objects
        self.magic_points_cost: Decimal = magic_points_cost
        self.energy_cost: Decimal = energy_cost
        self.damage_multiplier_to_self_max_hp: float = damage_multiplier_to_self_max_hp
        self.damage_multiplier_to_enemies_max_hp: float = damage_multiplier_to_enemies_max_hp
        self.damage_multiplier_to_self_attack: float = damage_multiplier_to_self_attack
        self.damage_multiplier_to_self_defense: float = damage_multiplier_to_self_defense
        self.damage_multiplier_to_self_attack_speed: float = damage_multiplier_to_self_attack_speed
        self.damage_multiplier_to_number_of_dead_allies: float = damage_multiplier_to_number_of_dead_allies
        self.damage_multiplier_to_number_of_dead_enemies: float = damage_multiplier_to_number_of_dead_enemies
        self.damage_multiplier_to_number_of_debuffs_on_enemies: float = damage_multiplier_to_number_of_debuffs_on_enemies
        self.damage_percentage_up_on_enemies_without_buffs: float = damage_percentage_up_on_enemies_without_buffs
        self.damage_percentage_up_per_self_hp_percentage_loss: float = damage_percentage_up_per_self_hp_percentage_loss
        self.damage_percentage_up_per_self_current_hp_percentage: float = damage_percentage_up_per_self_current_hp_percentage
        self.damage_percentage_up_per_enemies_hp_percentage_loss: float = damage_percentage_up_per_enemies_hp_percentage_loss
        self.damage_percentage_up_per_enemies_current_hp_percentage: float = \
            damage_percentage_up_per_enemies_current_hp_percentage
        self.cooltime: int = max_cooltime
        self.max_cooltime: int = max_cooltime
        self.skill_level_up_bonus: SkillLevelUpBonus = skill_level_up_bonus  # a SkillLevelUpBonus class object
        self.is_activated: bool = True


class LeaderSkill(Skill):
    """
    This class contains attributes of leader skills that characters have.
    """

    def __init__(self, skill_id, name, description, max_hp_percentage_up, attack_percentage_up, defense_percentage_up,
                 attack_speed_percentage_up, max_magic_points_percentage_up, max_energy_percentage_up,
                 crit_rate_up, crit_damage_up, evasion_chance_up, resistance_up, accuracy_up):
        # type: (str, str, str, float, float, float, float, float, float, float, float, float, float, float) -> None
        Skill.__init__(self, skill_id, name, description)
        self.max_hp_percentage_up: float = max_hp_percentage_up
        self.attack_percentage_up: float = attack_percentage_up
        self.defense_percentage_up: float = defense_percentage_up
        self.attack_speed_percentage_up: float = attack_speed_percentage_up
        self.max_magic_points_percentage_up: float = max_magic_points_percentage_up
        self.max_energy_percentage_up: float = max_energy_percentage_up
        self.crit_rate_up: float = crit_rate_up
        self.crit_damage_up: float = crit_damage_up
        self.evasion_chance_up: float = evasion_chance_up
        self.resistance_up: float = resistance_up
        self.accuracy_up: float = accuracy_up


class PassiveSkill(Skill):
    """
    This class is used to initialise passive skills that characters have.
    """

    def __init__(self, skill_id, name, description, max_hp_percentage_up, attack_percentage_up, defense_percentage_up,
                 attack_speed_percentage_up, crit_rate_up, crit_damage_up, resistance_up, accuracy_up,
                 extra_turn_chance_up, counterattack_chance_up, damage_multiplier_to_number_of_dead_allies,
                 damage_multiplier_to_number_of_dead_enemies, damage_multiplier_to_number_of_debuffs_on_enemies,
                 damage_percentage_up_on_enemies_without_buffs, damage_percentage_up_per_self_hp_percentage_loss,
                 damage_percentage_up_per_self_current_hp_percentage,
                 damage_percentage_up_per_enemies_hp_percentage_loss,
                 damage_percentage_up_per_enemies_current_hp_percentage, attack_gauge_increase_to_self,
                 attack_gauge_increase_to_allies, attack_gauge_decrease_to_enemies, buffs_to_self,
                 buffs_to_allies, debuffs_to_enemies, special_effects):
        # type: (str, str, str, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, list, list, list, list) -> None
        Skill.__init__(self, skill_id, name, description)
        self.max_hp_percentage_up: float = max_hp_percentage_up
        self.attack_percentage_up: float = attack_percentage_up
        self.defense_percentage_up: float = defense_percentage_up
        self.attack_speed_percentage_up: float = attack_speed_percentage_up
        self.crit_rate_up: float = crit_rate_up
        self.crit_damage_up: float = crit_damage_up
        self.resistance_up: float = resistance_up
        self.accuracy_up: float = accuracy_up
        self.extra_turn_chance_up: float = extra_turn_chance_up
        self.counterattack_chance_up: float = counterattack_chance_up
        self.damage_multiplier_to_number_of_dead_allies: float = damage_multiplier_to_number_of_dead_allies
        self.damage_multiplier_to_number_of_dead_enemies: float = damage_multiplier_to_number_of_dead_enemies
        self.damage_multiplier_to_number_of_debuffs_on_enemies: float = damage_multiplier_to_number_of_debuffs_on_enemies
        self.damage_percentage_up_on_enemies_without_buffs: float = damage_percentage_up_on_enemies_without_buffs
        self.damage_percentage_up_per_self_hp_percentage_loss: float = damage_percentage_up_per_self_hp_percentage_loss
        self.damage_percentage_up_per_self_current_hp_percentage: float = damage_percentage_up_per_self_current_hp_percentage
        self.damage_percentage_up_per_enemies_hp_percentage_loss: float = damage_percentage_up_per_enemies_hp_percentage_loss
        self.damage_percentage_up_per_enemies_current_hp_percentage: float = \
            damage_percentage_up_per_enemies_current_hp_percentage
        self.attack_gauge_increase_to_self: float = attack_gauge_increase_to_self
        self.attack_gauge_increase_to_allies: float = attack_gauge_increase_to_allies
        self.attack_gauge_decrease_to_enemies: float = attack_gauge_decrease_to_enemies
        self.buffs_to_self: list = buffs_to_self  # a list of Buff class objects
        self.buffs_to_allies: list = buffs_to_allies  # a list of Buff class objects
        self.debuffs_to_enemies: list = debuffs_to_enemies  # a list of Debuff class objects
        self.special_effects: list = special_effects  # a list of SpecialEffect class objects
        self.is_activated: bool = True


class SkillLevelUpBonus:
    """
    This class contains attributes of levelling up skills.
    """

    def __init__(self, damage_percentage_up, heal_amount_percentage_up, revival_amount_percentage_up,
                 magic_points_cost_percentage_down, energy_cost_percentage_down, max_cooltime_down):
        # type: (float, float, float, float, float, float) -> None
        self.damage_percentage_up: float = damage_percentage_up
        self.heal_amount_percentage_up: float = heal_amount_percentage_up
        self.revival_amount_percentage_up: float= revival_amount_percentage_up
        self.magic_points_cost_percentage_down: float = magic_points_cost_percentage_down
        self.energy_cost_percentage_down: float = energy_cost_percentage_down
        self.max_cooltime_down: float = max_cooltime_down

    def clone(self):
        # type: () -> SkillLevelUpBonus
        return copy.deepcopy(self)


class SpecialEffect:
    """
    This class is used to initialise special effects that passive skills have.
    """

    def __init__(self, attack_percentage_up, defense_percentage_up, attack_speed_percentage_up, damage_percentage_up,
                 times_accumulated, max_times_accumulated):
        # type: (float, float, float, float, int, int) -> None
        self.attack_percentage_up: float = attack_percentage_up
        self.defense_percentage_up: float = defense_percentage_up
        self.attack_speed_percentage_up: float = attack_speed_percentage_up
        self.damage_percentage_up: float = damage_percentage_up
        self.times_accumulated: int = times_accumulated
        self.max_times_accumulated: int = max_times_accumulated

    def clone(self):
        # type: () -> SpecialEffect
        return copy.deepcopy(self)


class Buff:
    """
    This class contains attributes of beneficial effects.
    """
    POSSIBLE_NAMES = ["INCREASE_ATK", "INCREASE_DEF", "INCREASE_SPD", "INCREASE_CR", "IMMUNITY", "INVINCIBILITY",
                           "ENDURE", "RECOVERY", "COUNTER", "REFLECT", "VAMPIRE"]

    def __init__(self, name, description, duration):
        # type: (str, str, int) -> None
        self.name: str or None = name if name in self.POSSIBLE_NAMES else None
        self.description: str = description
        self.blocks_damage: bool = self.name == "INVINCIBILITY"
        self.blocks_debuffs: bool = self.name == "IMMUNITY"
        self.prevents_death: bool = self.name == "ENDURE"
        self.heal_percentage_per_turn: float = 15 if self.name == "RECOVERY" else 0
        self.attack_percentage_up: float = 50 if self.name == "INCREASE_ATK" else 0
        self.defense_percentage_up: float = 50 if self.name == "INCREASE_DEF" else 0
        self.attack_speed_percentage_up: float = 100 / 3 if self.name == "INCREASE_SPD" else 0
        self.crit_rate_up: float = 1 / 3 if self.name == "INCREASE_CR" else 0
        self.counterattack_chance_up: float = 1 if self.name == "COUNTER" else 0
        self.life_drain_percentage_up: float = 15 if self.name == "VAMPIRE" else 0
        self.reflected_damage_percentage_up: float = 100 / 3 if self.name == "REFLECT" else 0
        self.duration: int = duration
        self.is_stackable: bool = self.name == "RECOVERY"

    def to_string(self):
        # type: () -> str
        res: str = ""  # initial value
        res += "Name: " + str(self.name) + "\n"
        res += "Description: " + str(self.description) + "\n"
        res += "Does it block damage? " + str(self.blocks_damage) + "\n"
        res += "Does it block debuffs? " + str(self.blocks_debuffs) + "\n"
        res += "Does it prevent death? " + str(self.prevents_death) + "\n"
        res += "Heal percentage per turn: " + str(self.heal_percentage_per_turn) + "%\n"
        res += "Attack percentage up: " + str(self.attack_percentage_up) + "%\n"
        res += "Defense percentage up: " + str(self.defense_percentage_up) + "%\n"
        res += "Attack speed percentage up: " + str(self.attack_speed_percentage_up) + "%\n"
        res += "Crit rate up: " + str(self.crit_rate_up) + "\n"
        res += "Counterattack chance up: " + str(self.counterattack_chance_up) + "\n"
        res += "Life drain percentage up: " + str(self.life_drain_percentage_up) + "%\n"
        res += "Reflected damage percentage up: " + str(self.reflected_damage_percentage_up) + "%\n"
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
    POSSIBLE_NAMES = ["DECREASE_ATK", "DECREASE_DEF", "DECREASE_SPD", "GLANCING", "BLOCK_BENEFICIAL_EFFECTS",
                             "BRAND", "UNRECOVERABLE", "DAMAGE_OVER_TIME", "FREEZE", "STUN", "SLEEP", "SILENCE",
                             "OBLIVION"]

    def __init__(self, name, description, duration):
        # type: (str, str, int) -> None
        self.name: str or None = name if name in self.POSSIBLE_NAMES else None
        self.description: str = description
        self.blocks_heal: bool = self.name == "UNRECOVERABLE"
        self.blocks_buffs: bool = self.name == "BLOCK_BENEFICIAL_EFFECTS"
        self.prevents_turn: bool = self.name == "FREEZE" or self.name == "STUN" or self.name == "SLEEP"
        self.silences_skills: bool = self.name == "SILENCE"
        self.blocks_passive_skills: bool = self.name == "OBLIVION"
        self.damage_percentage_per_turn: float = 5 if self.name == "DAMAGE_OVER_TIME" else 0
        self.attack_percentage_down: float = 50 if self.name == "DECREASE_ATK" else 0
        self.defense_percentage_down: float = 50 if self.name == "DECREASE_DEF" else 0
        self.attack_speed_percentage_down: float = 100 / 3 if self.name == "DECREASE_SPD" else 0
        self.glancing_hit_chance_up: float = 0.5 if self.name == "GLANCING" else 0
        self.additional_damage_percentage_received_up: float = 25 if self.name == "BRAND" else 0
        self.duration: int = duration
        self.is_stackable: bool = False

    def to_string(self):
        # type: () -> str
        res: str = ""  # initial value
        res += "Name: " + str(self.name) + "\n"
        res += "Description: " + str(self.description) + "\n"
        res += "Does it block heal? " + str(self.blocks_heal) + "\n"
        res += "Does it block buffs? " + str(self.blocks_buffs) + "\n"
        res += "Does it prevent turn? " + str(self.prevents_turn) + "\n"
        res += "Does it silence skills? " + str(self.silences_skills) + "\n"
        res += "Does it block passive skills? " + str(self.blocks_passive_skills) + "\n"
        res += "Damage percentage per turn: " + str(self.damage_percentage_per_turn) + "%\n"
        res += "Attack percentage down: " + str(self.attack_percentage_down) + "%\n"
        res += "Defense percentage down: " + str(self.defense_percentage_down) + "%\n"
        res += "Attack speed percentage down: " + str(self.attack_speed_percentage_down) + "%\n"
        res += "Glancing hit chance up: " + str(self.glancing_hit_chance_up) + "\n"
        res += "Additional damage percentage received up: " + str(self.additional_damage_percentage_received_up) + "%\n"
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
    MAX_TEAM_SIZE = 20

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

    to_be_printed = str(calendar.day_name[today.weekday()]) + ", " + str(today.day) + " "
    month = "January " if today.month == 1 else "February " if today.month == 2 else "March " \
        if today.month == 3 else "April " if today.month == 4 else "May " if today.month == 5 else \
        "June " if today.month == 6 else "July " if today.month == 7 else "August " if today.month == \
        8 else "September " if today.month == 9 else "October " if today.month == 10 else "November " \
        if today.month == 11 else "December "
    to_be_printed += str(month) + str(today.year) + "\n"
    print(to_be_printed)


main()
