import json

from .utils import Utils

class Grammar(object):

    def __init__(self, productions, initial_symbol):
        """Constructs a regular grammar from a list of productions and the initial symbol.

        Assumes each production "A -> aB", where B is optional, is of the form:
            ("A", "a"[, "B"])
        """
        self._initial_symbol = initial_symbol
        self._productions = set(productions)
        self._nonterminals = self._get_nonterminals()
        self._terminals = self._get_terminals()

    def to_automaton(self):
        from .automata import Automata
        transitions = self._make_transitions()
        final_states = set(Utils.NEW_FINAL_STATE)
        q0 = self._initial_symbol
        states = self._nonterminals | final_states
        alphabet = self._terminals
        return Automata(alphabet, states, q0, final_states, transitions)

    def save_json(self, filename):
        data = {
            'nonterminals': self._nonterminals,
            'terminals': self._terminals,
            'productions': self._productions,
            'initial_symbol': self._initial_symbol
        }
        with open(filename + '.json', 'w') as write_file:
            json.dump(data, write_file, indent=4)

    def _get_nonterminals(self):
        nonterminals = set(self._initial_symbol)
        for production in self._productions:
            nonterminals.add(production[0])
            if len(production) == 3:
                nonterminals.add(production[2])
        return nonterminals

    def _get_terminals(self):
        terminals = set()
        for production in self._productions:
            if production[1] != Utils.EPSILON:
                terminals.add(production[1])
        return terminals

    def _make_transitions(self):
        transitions = dict()
        for production in self._productions:
            input = Utils.TRANSITION(production[0], production[1])
            output = self._get_next_state(production)
            self._include_transition(transitions, input, output)
        return transitions

    def _get_next_state(self, production):
        if len(production) == 3:
            return production[2]
        return Utils.NEW_FINAL_STATE

    def _include_transition(self, transitions, input, output):
        if not input in transitions.keys():
            transitions[input] = list()
        transitions[input].append(output)

    def read_from_json(filename):
        with open(filename + '.json', 'r') as read_file:
            data = json.load(read_file)
        productions = [tuple(production) for production in data['productions']]
        initial_symbol = data['initial_symbol']
        return Grammar(productions, initial_symbol)
