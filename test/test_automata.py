import unittest
import os
from src.automata import Automata
from src.utils_automata import Utils


class AutomataTests(unittest.TestCase):
    def test_alright(self):
        fa = self._create_automata()
        self.assertIsInstance(fa, Automata)

    def test_type_check(self):
        self.assertRaises(ValueError, Automata, '', '', 1, '', '')

    def test_size_check(self):
        self.assertRaises(ValueError, Automata,
                          set(), set(), 'a', set(), dict())

    def test_set_check(self):
        transitions = self._create_transitions()
        self.assertRaises(ValueError, Automata,
                          {'a'}, {'A', 'B'}, 'C', {'B', 'D'}, transitions)

    def test_basic_alphabet(self):
        transitions = self._create_transitions()
        self.assertRaises(ValueError, Automata,
                          {'a'}, {'A', 'B', 'a'}, 'A', {'B'}, transitions)

    def test_save_json(self):
        fa = self._create_automata()
        filename = 'test_save_json'
        fa.save_json(filename)
        # clean the disk
        os.remove(filename + '.json')

    def test_e_closure_empty(self):
        pass

    def test_e_closure_book_example(self):
        pass

    def test_e_closure_simple_example(self):
        pass

    def test_read_json(self):
        fa = Automata.read_from_json('./test/data/test_read_json')
        self.assertIsInstance(fa, Automata)

    def _create_automata(self):
        """Helper that create and return a default automata."""
        transitions = self._create_transitions()
        return Automata({'a', 'b'}, {'A', 'B'}, 'A', {'B'}, transitions)

    def _create_transitions(self):
        """Helper that create and return a default transitions."""
        transitions = {}
        t0 = Utils.TRANSITION('A', 'a')
        transitions[t0] = set('B')
        return transitions

if __name__ == '__main__':
    unittest.main()
