import unittest
from src.automata import Automata

class AutomataTests(unittest.TestCase):
    def test_alright(self):
        fa = Automata(set(), set(), '', set(), dict())
        self.assertIsInstance(fa, Automata)

    def test_type_check(self):
        self.assertRaises(ValueError, Automata, '', '', 1, '', '')

if __name__ == '__main__':
    unittest.main()
