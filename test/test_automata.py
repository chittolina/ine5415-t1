import unittest
from collections import namedtuple
from src.automata import Automata

class AutomataTests(unittest.TestCase):
    def test_alright(self):
        # create one transition
        transitions = {}
        Transition = namedtuple('Transition', ['state', 'char'])
        t0 = Transition('A', 'a')
        transitions[t0] = 'B'

        fa = Automata({'a', 'b'}, {'A', 'B'}, 'A', {'B'}, transitions)
        self.assertIsInstance(fa, Automata)

    def test_type_check(self):
        self.assertRaises(ValueError, Automata, '', '', 1, '', '')

    def test_size_check(self):
        self.assertRaises(ValueError, Automata, set(), set(), 'a', set(), dict())

    def test_set_check(self):
        # TODO: make a helper method
        # create one transition
        transitions = {}
        Transition = namedtuple('Transition', ['state', 'char'])
        t0 = Transition('A', 'a')
        transitions[t0] = 'B'

        self.assertRaises(ValueError, Automata, {'a'}, {'A', 'B'}, 'C', {'B', 'D'} , transitions)

if __name__ == '__main__':
    unittest.main()
