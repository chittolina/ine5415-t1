# -*- coding: utf-8 -*-
from collections import namedtuple


class Utils:
    """Helper to try apply DRY across the project"""

    TRANSITION = namedtuple('Transition', ['state', 'char'])
    EPSILON = '&'
    NEW_FINAL_STATE = '$'  # used in grammar to automaton conversion

    def __init__(self):
        pass
