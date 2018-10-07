import unittest
import os
from src.automata import Automata
from src.utils_automata import Utils


class AutomataTests(unittest.TestCase):
    def test_alright(self):
        fa = self._create_automata()
        self.assertIsInstance(fa, Automata)
        self.assertFalse(fa.deterministic)

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

    def test_read_json(self):
        fa = Automata.read_from_json('./test/data/test_read_json')
        self.assertIsInstance(fa, Automata)

    def test_e_closure_empty(self):
        fa = self._create_automata()
        self.assertSetEqual(set(fa.q0), fa._e_closure([fa.q0]))

    def test_e_closure_book_example(self):
        fa = Automata.read_from_json('./test/data/' +
                                     'test_e_closure_book_aho_example_334')
        self.assertSetEqual({'0', '1', '2', '4', '7'}, fa._e_closure([fa.q0]))
        self.assertFalse(fa.deterministic)

    def test_e_closure_simple_example(self):
        t0 = Utils.TRANSITION('q0', Utils.EPSILON)
        t1 = Utils.TRANSITION('q1', '0')
        transitions = {t0: {'q1'}, t1: {'q2'}}
        fa = Automata({'0'}, {'q0', 'q1', 'q2'}, 'q0', {'q2'}, transitions)
        self.assertSetEqual({'q0', 'q1'}, fa._e_closure([fa.q0]))

    def test_move_empty(self):
        fa = self._create_automata()
        self.assertCountEqual([], fa._move({'B'}, 'a'))

    def test_move_book_example(self):
        fa = Automata.read_from_json('./test/data/' +
                                     'test_e_closure_book_aho_example_334')
        self.assertCountEqual(['3'], fa._move({'0', '1', '2', '4'}, 'a'))

    def test_move_simple_example(self):
        t0 = Utils.TRANSITION('0', Utils.EPSILON)
        t1 = Utils.TRANSITION('1', Utils.EPSILON)
        t2 = Utils.TRANSITION('2', 'a')
        transitions = {t0: {'1'}, t1: {'2'}, t2: {'1', '2'}}
        fa = Automata({'a'}, {'0', '1', '2'}, '0', {'1'}, transitions)
        self.assertCountEqual(['1', '2'], fa._move({'2'}, 'a'))

    def test_nfa_to_dfa_01(self):
        # from https://goo.gl/jHyfwd
        # without epsilon
        t0 = Utils.TRANSITION('q0', '0')
        t1 = Utils.TRANSITION('q0', '1')
        t2 = Utils.TRANSITION('q1', '0')
        transitions = {t0: {'q0'}, t1: {'q0', 'q1'}, t2: {'q2'}}
        nfa = Automata({'0', '1'}, {'q0', 'q1', 'q2'}, 'q0', {'q2'},
                       transitions)
        dfa = nfa.to_dfa()
        # transition by transition was checked by hand with print :|
        # cannot check transition by transition because of the randomness
        self.assertEqual(3, len(dfa.states))
        self.assertEqual(1, len(dfa.final_states))
        self.assertEqual(6, len(dfa.transitions))
        self.assertTrue(dfa.deterministic)

    def test_nfa_to_dfa_02(self):
        # from https://goo.gl/dYbXRr
        # with epsilon
        nfa = Automata.read_from_json('./test/data/test_nfa_to_dfa_02')
        dfa = nfa.to_dfa()
        # transition by transition was checked by hand with print :|
        # cannot check transition by transition because of the randomness
        self.assertEqual(5, len(dfa.states))
        self.assertEqual(4, len(dfa.final_states))
        self.assertEqual(10, len(dfa.transitions))
        self.assertTrue(dfa.deterministic)

    def test_nfa_to_dfa_03(self):
        # from https://goo.gl/Qk8GSk
        # without epsilon
        t0 = Utils.TRANSITION('A', '0')
        t1 = Utils.TRANSITION('A', '1')
        transitions = {t0: {'A'}, t1: {'A', 'B'}}
        nfa = Automata({'0', '1'}, {'A', 'B'}, 'A', {'B'}, transitions)
        dfa = nfa.to_dfa()
        # transition by transition was checked by hand with print :|
        # cannot check transition by transition because of the randomness
        self.assertEqual(2, len(dfa.states))
        self.assertEqual(1, len(dfa.final_states))
        self.assertEqual(4, len(dfa.transitions))
        self.assertTrue(dfa.deterministic)

    def test_nfa_to_dfa_04(self):
        # from https://goo.gl/fFZp7b
        # without epsilon
        t0 = Utils.TRANSITION('A', '0')
        t1 = Utils.TRANSITION('A', '1')
        t2 = Utils.TRANSITION('B', '1')
        transitions = {t0: {'A', 'B'}, t1: {'A'}, t2: {'C'}}
        nfa = Automata({'0', '1'}, {'A', 'B', 'C'}, 'A', {'C'}, transitions)
        dfa = nfa.to_dfa()
        # transition by transition was checked by hand with print :|
        # cannot check transition by transition because of the randomness
        self.assertEqual(3, len(dfa.states))
        self.assertEqual(1, len(dfa.final_states))
        self.assertEqual(6, len(dfa.transitions))
        self.assertTrue(dfa.deterministic)

    def test_nfa_to_dfa_05(self):
        # from https://goo.gl/Ymsc8D
        # with epsilon
        nfa = Automata.read_from_json('./test/data/test_nfa_to_dfa_05')
        dfa = nfa.to_dfa()
        # transition by transition was checked by hand with print :|
        # cannot check transition by transition because of the randomness
        self.assertEqual(6, len(dfa.states))
        self.assertEqual(2, len(dfa.final_states))
        self.assertEqual(12, len(dfa.transitions))
        self.assertTrue(dfa.deterministic)

    def test_define_unreachable_with_few_state(self):
        transitions = {Utils.TRANSITION('A', '0'): {'A'},
                       Utils.TRANSITION('B', '0'): {'B'}}
        dfa = Automata({'0'}, {'A', 'B'}, 'A', {'A'}, transitions)
        unreachable = dfa._define_unreachable()
        self.assertSetEqual({'B'}, unreachable)

    def test_define_unreachable_with_more_state(self):
        dfa = Automata.read_from_json('./test/data/test_define_unreachable')
        unreachable = dfa._define_unreachable()
        self.assertSetEqual({'q2', 'q3', 'q4'}, unreachable)

    def test_merge_nondistinguishable_with_few_state(self):
        transitions = {Utils.TRANSITION('A', '0'): {'B'},
                       Utils.TRANSITION('A', '1'): {'C'},
                       Utils.TRANSITION('B', '0'): {'A'},
                       Utils.TRANSITION('B', '1'): {'B'},
                       Utils.TRANSITION('C', '0'): {'A'},
                       Utils.TRANSITION('C', '1'): {'A'}}
        dfa = Automata({'0', '1'}, {'A', 'B', 'C'}, 'A', {'B', 'C'},
                       transitions)
        result = dfa._merge_nondistinguishable(dfa.states, dfa.final_states)
        self.assertCountEqual([{'A'}, {'B'}, {'C'}], result)

    def test_merge_nondistinguishable_from_class(self):
        dfa = Automata.read_from_json('./test/data/'
                                      'test_merge_nondistinguishable')
        result = dfa._merge_nondistinguishable(dfa.states, dfa.final_states)
        self.assertCountEqual([{'PA'}, {'PC', 'IC'}, {'PB', 'IB'}, {'IA'},
                               {'T'}], result)

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
