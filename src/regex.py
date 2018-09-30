# -*- coding: utf-8 -*-

'''
GLC:
<regex>     ::= <term>
                <term> '|' <regex>
<term>      ::=  { <factor> }
<factor>    ::= <base> { '*' }
                <base> { '?' }
                <base> { '.' }
<base>      ::= <char>
                '(' <regex> ')'
'''

import re

class Node:
    count = 0

    def __init__(self, symbol, left, right):
        self.symbol = symbol
        self.left = left
        self.right = right
        self.index = Node.count
        Node.count += 1


END = '#'
OPERATORS = ['|', '*', '.', '?']
ALPHABET = re.compile(r"([A-z0-9&])|(.)")

class RegexParser:

    def __init__(self, input):
        self.input = input
        if not self._validate():
            raise RuntimeError('Invalid input string.')

    def _validate(self):
        node = self._regex()
        self.root = node
        return True

    def _peek(self):
        if self._more():
            return self.input[0]
        else:
            return ''

    def _eat(self, char):
        if self._peek() != char:
            print self._peek()
            print char
            raise RuntimeError('Invalid input string.')

        self.input = self.input[1:]

    def _more(self):
        return len(self.input) > 0

    def _next(self):
        char = self._peek()
        self._eat(char)
        return char

    def _regex(self):
        term = self._term()

        if self._peek() == '|':
            self._next()
            regex = self._regex()
            node = Node('|', term, regex)
            return node

        return term

    def _base(self):
        char = self._peek()

        if char == '(':
            self._eat('(')
            regex = self._regex()
            self._eat(')')
            return regex
        elif ALPHABET.match(char):
            node = Node(self._next(), None, None)
            return node
        else:
            raise RuntimeError('Invalid input string.')

    def _factor(self):
        base = self._base()
        char = self._peek()

        while self._more() and self._peek() in ['?', '*']:
            base = Node(self._next(), base, None)

        return base

    def _term(self):
        factor = self._factor()

        if self._more() and self._peek() not in ['|', ')']:
            factor = Node('.', factor, self._term())

        return factor
