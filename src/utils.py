# -*- coding: utf-8 -*-
from collections import namedtuple


class Utils:

    TRANSITION = namedtuple('Transition', ['state', 'char'])
    EPSILON = '&'
    NEW_FINAL_STATE = '$' # used in grammar to automaton conversion

    def __init__(self):
        pass
