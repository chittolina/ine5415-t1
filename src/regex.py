# -*- coding: utf-8 -*-

class Regex:
    OPERATORS = ['|', '*', '+', '{', '}', '(', ')', 'ˆ']

    def __init__(self, string):
        if self._validate(string):
            self.string = string
        else:
            raise ValueError('Invalid input string.')

    def _validate(self, string):
        return True
