# -*- coding: utf-8 -*-

'''
GLC:
<regex>     ::= <term>
                <term> '|' <regex>
<term>      ::=  { <factor> }
<factor>    ::= <base> { '*' }
                <base> { '?' }
<base>      ::= <char>
                '(' <regex> ')'

'''
class Regex:
    END = '#'
    OPERATORS = ['|', '*', '.', '?']

    def __init__(self, input):
        if self._validate(input):
            self.input = input
        else:
            raise ValueError('Invalid input string.')

    def _validate(self, input):
        return True

    def _peek(self):
        return self.input[0]

    def _eat(self, char):
        if _peek() != char
            raise RuntimeError('Invalid input string.')

        self.input = self.input[1:]

    def _more(self):
        return len(self.input) > 0

    def _next(self):
        char = _peek()
        _eat(char)
        return char

    def _regex(self):
