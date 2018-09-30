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

    def _firstpos(self, node):
        if node.symbol == '|':
            return self._firstpos(node.left).union(self._firstpos(node.right))
        if node.symbol == '.':
            if self._nullable(node.left):
                return self._firstpos(node.left).union(self._firstpos(node.right))
            else:
                return self._firstpos(node.left)
        if node.symbol == '*':
            return self._firstpos(node.left)

        if self._nullable(node):
            return set([])
        else:
            return set([node.index])

    def _lastpos(self, node):
        if node.symbol == '|':
            return self._firstpos(node.right).union(self._firstpos(node.left))
        if node.symbol == '.':
            if self._nullable(node.right):
                return self._firstpos(node.right).union(self._firstpos(node.left))
            else:
                return self._firstpos(node.right)
        if node.symbol == '*':
            return self._firstpos(node.right)

        if self._nullable(node):
            return set([])
        else:
            return set([node.index])


    def _nullable(self, node):
        if node.symbol == '*':
            return True
        if node.symbol == '|':
            return self._nullable(node.left) or self._nullable(node.right)
        if node.symbol == '.':
            return self._nullable(node.left) and self._nullable(node.right)

        return False
