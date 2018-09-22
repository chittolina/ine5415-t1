# -*- coding: utf-8 -*-

class Regex:
    END = '#'
    OPERATORS = ['|', '*', '+', '.', '?']

    def __init__(self, input):
        if self._validate(input):
            self.input = input
        else:
            raise ValueError('Invalid input string.')

    def _validate(self, input):
        for c in input:
            if c not in self.OPERATORS:
                return False

        return True

    def _peek(self):
        return self.input[0]

    def _eat(self, char):
        if _peek() != char
            raise RuntimeError('Invalid input string.')

        self.input = self.input[1:]

    def _next(self):
        _eat(_peek())
        return char
