# -*- coding: utf-8 -*-
"""INE 5421 - Linguagem Formais e Compiladores - Trabalho 01

Universidade Federal de Santa Catarina

Departamento de Informática e Estatística (INE)

Alunos:

- Filipe Oliveira de Borba
- Gabriel Leal Chittolina Amaral
- Lucas João Martins
"""
from collections import namedtuple


class Utils:
    """Helper to try apply DRY across the project"""

    TRANSITION = namedtuple('Transition', ['state', 'char'])
    EPSILON = '&'
    NEW_FINAL_STATE = '$'  # used in grammar to automaton conversion

    def __init__(self):
        pass
