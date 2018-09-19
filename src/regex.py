# -*- coding: utf-8 -*-

class Regex:
    OPERATORS = ['|', '*', '+', '{', '}', '(', ')', '^']

    def __init__(self, string):
        if self._validate(string):
            self.string = string
        else:
            raise ValueError('Invalid input string.')

    def _validate(self, string):
        return True
