# -*- coding: utf-8 -*-
"""INE 5421 - Linguagem Formais e Compiladores - Trabalho 01

Universidade Federal de Santa Catarina

Departamento de Informática e Estatística (INE)

Alunos:

- Filipe Oliveira de Borba
- Gabriel Leal Chittolina Amaral
- Lucas João Martins
"""
import json

from .utils import Utils


class Grammar:
    """Representation of a grammar

    Assumes each production "A -> aB", where B is optional, is of the form:
    ("A", "a"[, "B"])
    """

    def __init__(self, productions, initial_symbol):
        """Constructs a regular grammar

        From a list of productions and the initial symbol.
        """
        self._initial_symbol = initial_symbol
        self._productions = set(productions)
        self._nonterminals = self._get_nonterminals()
        self._terminals = self._get_terminals()

    def to_automaton(self):
        """Return an automata from the self grammar"""
        from .automata import Automata
        transitions = self._make_transitions()
        final_states = set(Utils.NEW_FINAL_STATE)
        q0 = self._initial_symbol
        states = self._nonterminals | final_states
        alphabet = self._terminals
        return Automata(alphabet, states, q0, final_states, transitions)

    def save_json(self, filename):
        """Save in filesystem a json file from a grammar

        The path in filename don't need contain the '.json' extension.
        """
        data = {
            'nonterminals': list(self._nonterminals),
            'terminals': list(self._terminals),
            'productions': list(self._productions),
            'initial_symbol': self._initial_symbol
        }
        with open(filename + '.json', 'w') as write_file:
            json.dump(data, write_file, indent=4)

    def _get_nonterminals(self):
        """Helper to grammar constructor"""
        nonterminals = set()
        nonterminals.add(self._initial_symbol)
        for production in self._productions:
            nonterminals.add(production[0])
            if len(production) == 3:
                nonterminals.add(production[2])
        return nonterminals

    def _get_terminals(self):
        """Helper to grammar constructor"""
        terminals = set()
        for production in self._productions:
            if production[1] != Utils.EPSILON:
                terminals.add(production[1])
        return terminals

    def _make_transitions(self):
        """Helper to conversion from a grammar to an automata"""
        transitions = dict()
        for production in self._productions:
            src = Utils.TRANSITION(production[0], production[1])
            output = self._get_next_state(production)
            self._include_transition(transitions, src, output)
        return transitions

    def _get_next_state(self, production):
        """Helper to conversion from a grammar to an automata"""
        if len(production) == 3:
            return production[2]
        return Utils.NEW_FINAL_STATE

    def _include_transition(self, transitions, src, output):
        """Helper to conversion from a grammar to an automata"""
        if src not in transitions.keys():
            transitions[src] = list()
        transitions[src].append(output)

    @staticmethod
    def read_from_json(filename):
        """Return an grammar from a json file

        The path in filename don't need contain the '.json' extension.
        """
        with open(filename + '.json', 'r') as read_file:
            data = json.load(read_file)
        productions = [tuple(production) for production in data['productions']]
        initial_symbol = data['initial_symbol']
        return Grammar(productions, initial_symbol)
