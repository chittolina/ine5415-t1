import json

class Grammar(object):

    def __init__(self, productions, initial_symbol):
        """Constructs a regular grammar from a list of productions and the initial symbol.

        Assumes each production "A -> aB", where B is optional, is of the form:
            ("A", "a"[, "B"])
        """
        self._initial_symbol = initial_symbol
        self._productions = set(productions)
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
        for production in self._productions:
            nonterminals.add(production[0])
        return nonterminals

    def _getTerminals(self):
        terminals = set()
        for production in self._productions:
            terminals.add(production[1])
        return terminals

    def read_from_json(filename):
        with open(filename + '.json', 'r') as read_file:
            data = json.load(read_file)
        productions = [tuple(production) for production in data['productions']]
        initial_symbol = data['initial_symbol']
        return Grammar(productions, initial_symbol)
