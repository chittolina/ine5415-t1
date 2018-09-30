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
ALPHABET = ['a', 'b']

class RegexParser:

    def __init__(self, input):
        if self._validate(input):
            self.input = input
        else:
            raise RuntimeError('Invalid input string.')

    def _validate(self, input):
        return True

    def _peek(self):
        return self.input[0]

    def _eat(self, char):
        if self._peek() != char:
            raise RuntimeError('Invalid input string.')

        self.input = self.input[1:]

    def _more(self):
        return len(self.input) > 0

    def _next(self):
        char = self._peek()
        self._eat(char)
        return char

    def _regex(self):
        return True

    def _base(self):
        char = self._peek()

        if char == '(':
            self._eat('(')
            regex = self._regex()
            self._eat(')')
            return regex
        elif char in ALPHABET:
            node = Node(char, None, None)
            return node
        else:
            raise RuntimeError('Invalid input string.')

    def _factor(self):
        base = self._base()
        char = self._peek()

        while self._more() and self._peek() in ['?', '*', '.']:
            self._eat(self._peek())

        return base

    def _term(self):
        factor = self._factor()

        if self._peek() in ['|', ')']:
            node = Node('.', factor, self._term())
            return node

        return factor
