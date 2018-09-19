# -*- coding: utf-8 -*-

class Regex:
    OPERATORS = ['|', '*', '+', '{', '}', '(', ')', '^']

    def __init__(self, string):
        if self._validate(string):
            self.string = string
        else:
            raise ValueError('Invalid input string.')

    def _validate(self, string):
        for c in string:
            if c not in self.OPERATORS:
                return False

        return True
