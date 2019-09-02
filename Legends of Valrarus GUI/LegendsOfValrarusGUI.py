# The names of battlefields and characters in this game are randomly generated using the random generator in the link
# below.
# https://www.fantasynamegenerators.com/

# Game version: 1 (Graphical User Interface Version)


import pygame
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

getcontext().Emin = -999999999999999999
getcontext().Emax = 999999999999999999
getcontext().traps[Overflow] = 0
getcontext().traps[Underflow] = 0
getcontext().traps[DivisionByZero] = 0
getcontext().traps[InvalidOperation] = 0
getcontext().prec = 100

today = date.today()
