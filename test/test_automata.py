import unittest
import os
from collections import namedtuple
from src.automata import Automata

class AutomataTests(unittest.TestCase):
    def test_alright(self):
        fa = self._create_automata()
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

    def test_save_json(self):
        fa = self._create_automata()
        filename = 'test_save_json'
        fa.save_json(filename)
        # clean the disk
        os.remove(filename + '.json')

    def _create_automata(self):
        """Helper that create and return a default automata."""
        transitions = self._create_transitions()
        return Automata({'a', 'b'}, {'A', 'B'}, 'A', {'B'}, transitions)

    def _create_transitions(self):
        """Helper that create and return a default transitions."""
        transitions = {}
        Transition = namedtuple('Transition', ['state', 'char'])
        t0 = Transition('A', 'a')
        transitions[t0] = set('B')
        return transitions

if __name__ == '__main__':
    unittest.main()
