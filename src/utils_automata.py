# -*- coding: utf-8 -*-
from collections import namedtuple


class Utils:

    TRANSITION = namedtuple('Transition', ['state', 'char'])
    EPSILON = '&'

    def __init__(self):
        pass
