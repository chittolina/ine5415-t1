import json

class Grammar(object):

    def __init__(self, productions, initial_symbol):
        """Assumes initial_symbol is a char and productions has the following form:
        {
            <upper_case_letter> : [
                (<lower_case_letter>, <upper_case_letter> or <blank>),
                ...
            ]
            ...
        }"""
        self._initial_symbol = initial_symbol
        self._productions = productions
        self._nonterminals = self._getNonterminals()
        self._terminals = self._getTerminals()

    def save_json(self, filename):
        data = {
            'nonterminals': self._nonterminals,
            'terminals': self._terminals,
            'productions': self._productions,
            'initial_symbol': self._initial_symbol
        }
        with open(filename + '.json', 'w') as write_file:
            json.dump(data, write_file, indent=4)

    def _getNonterminals(self):
        nonterminals = set(self._initial_symbol)
        for nonterminal in self._productions.keys():
            nonterminals.add(nonterminal)
        return list(nonterminals)

    def _getTerminals(self):
        terminals = set()
        for body in self._productions.values():
            for production in body:
                terminals.add(production[0])
        return list(terminals)

    def read_from_json(filename):
        with open(filename + '.json', 'r') as read_file:
            data = json.load(read_file)
        return Grammar(data['productions'], data['initial_symbol'])
