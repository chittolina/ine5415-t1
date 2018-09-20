import unittest
from collections import namedtuple
from src.automata import Automata

class AutomataTests(unittest.TestCase):
    def test_alright(self):
        transitions = self._create_transitions()
        fa = Automata({'a', 'b'}, {'A', 'B'}, 'A', {'B'}, transitions)
        self.assertIsInstance(fa, Automata)

    def test_type_check(self):
        self.assertRaises(ValueError, Automata, '', '', 1, '', '')

    def test_size_check(self):
        self.assertRaises(ValueError, Automata, set(), set(), 'a', set(), dict())

    def test_set_check(self):
        transitions = self._create_transitions()
        self.assertRaises(ValueError, Automata, {'a'}, {'A', 'B'}, 'C', {'B', 'D'} , transitions)

    def test_basic_alphabet(self):
        transitions = self._create_transitions()
        self.assertRaises(ValueError, Automata, {'a'}, {'A', 'B', 'a'}, 'A', {'B'}, transitions)

    def _create_transitions(self):
        """Helper that create and return a default transitions."""
        transitions = {}
        Transition = namedtuple('Transition', ['state', 'char'])
        t0 = Transition('A', 'a')
        transitions[t0] = 'B'
        return transitions

if __name__ == '__main__':
    unittest.main()
