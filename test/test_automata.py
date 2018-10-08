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

    def test_dfa_minimization_01(self):
        # from https://goo.gl/zN5uE3
        transitions = {Utils.TRANSITION('a', '0'): {'b'},
                       Utils.TRANSITION('a', '1'): {'c'},
                       Utils.TRANSITION('b', '0'): {'a'},
                       Utils.TRANSITION('b', '1'): {'d'},
                       Utils.TRANSITION('c', '0'): {'e'},
                       Utils.TRANSITION('c', '1'): {'f'},
                       Utils.TRANSITION('d', '0'): {'e'},
                       Utils.TRANSITION('d', '1'): {'f'},
                       Utils.TRANSITION('e', '0'): {'e'},
                       Utils.TRANSITION('e', '1'): {'f'},
                       Utils.TRANSITION('f', '0'): {'f'},
                       Utils.TRANSITION('f', '1'): {'f'}}
        dfa = Automata({'0', '1'}, {'a', 'b', 'c', 'd', 'e', 'f'}, 'a',
                       {'c', 'd', 'e'}, transitions)
        mdfa = dfa.minimize()
        # transition by transition was checked by hand with print :|
        # cannot check transition by transition because of the randomness
        self.assertEqual(3, len(mdfa.states))
        self.assertEqual(1, len(mdfa.final_states))
        self.assertEqual(6, len(mdfa.transitions))

    def test_dfa_minimization_02(self):
        # example 1 from https://goo.gl/3RWgMn
        dfa = Automata.read_from_json('./test/data/test_dfa_minimization_02')
        mdfa = dfa.minimize()
        # transition by transition was checked by hand with print :|
        # cannot check transition by transition because of the randomness
        self.assertEqual(4, len(mdfa.states))
        self.assertEqual(1, len(mdfa.final_states))
        self.assertEqual(8, len(mdfa.transitions))

    def test_dfa_minimization_03(self):
        # example 2 from https://goo.gl/3RWgMn
        transitions = {Utils.TRANSITION('1', 'a'): {'2'},
                       Utils.TRANSITION('1', 'b'): {'3'},
                       Utils.TRANSITION('2', 'a'): {'2'},
                       Utils.TRANSITION('2', 'b'): {'4'},
                       Utils.TRANSITION('3', 'a'): {'3'},
                       Utils.TRANSITION('3', 'b'): {'3'},
                       Utils.TRANSITION('4', 'a'): {'6'},
                       Utils.TRANSITION('4', 'b'): {'3'},
                       Utils.TRANSITION('5', 'a'): {'5'},
                       Utils.TRANSITION('5', 'b'): {'3'},
                       Utils.TRANSITION('6', 'a'): {'5'},
                       Utils.TRANSITION('6', 'b'): {'4'}}
        dfa = Automata({'a', 'b'}, {'1', '2', '3', '4', '5', '6'}, '1',
                       {'1', '2', '4', '5', '6'}, transitions)
        mdfa = dfa.minimize()
        # transition by transition was checked by hand with print :|
        # cannot check transition by transition because of the randomness
        self.assertEqual(6, len(mdfa.states))
        self.assertEqual(5, len(mdfa.final_states))
        self.assertEqual(12, len(mdfa.transitions))

    def test_dfa_minimization_04(self):
        # example from https://goo.gl/KMxzxm
        dfa = Automata.read_from_json('./test/data/test_dfa_minimization_04')
        mdfa = dfa.minimize()
        # transition by transition was checked by hand with print :|
        # cannot check transition by transition because of the randomness
        self.assertEqual(5, len(mdfa.states))
        self.assertEqual(1, len(mdfa.final_states))
        self.assertEqual(10, len(mdfa.transitions))

    def test_union_01(self):
        # example from https://goo.gl/Rj1T8T
        transitions_01 = {Utils.TRANSITION('1', 'a'): {'2'},
                          Utils.TRANSITION('1', 'b'): {'4'},
                          Utils.TRANSITION('2', 'a'): {'2'},
                          Utils.TRANSITION('2', 'b'): {'3'},
                          Utils.TRANSITION('3', 'a'): {'2'},
                          Utils.TRANSITION('3', 'b'): {'3'},
                          Utils.TRANSITION('4', 'a'): {'4'},
                          Utils.TRANSITION('4', 'b'): {'4'}}
        in_01 = Automata({'a', 'b'}, {'1', '2', '3', '4'}, '1', {'3'},
                         transitions_01)
        transitions_02 = {Utils.TRANSITION('1', 'a'): {'4'},
                          Utils.TRANSITION('1', 'b'): {'2'},
                          Utils.TRANSITION('2', 'a'): {'3'},
                          Utils.TRANSITION('2', 'b'): {'2'},
                          Utils.TRANSITION('3', 'a'): {'3'},
                          Utils.TRANSITION('3', 'b'): {'2'},
                          Utils.TRANSITION('4', 'a'): {'4'},
                          Utils.TRANSITION('4', 'b'): {'4'}}
        in_02 = Automata({'a', 'b'}, {'1', '2', '3', '4'}, '1', {'3'},
                         transitions_02)
        verbose_union = in_01.union(in_02)
        union = verbose_union.minimize()
        # transition by transition was checked by hand with print :|
        # cannot check transition by transition because of the randomness
        self.assertEqual(5, len(union.states))
        self.assertEqual(2, len(union.final_states))
        self.assertEqual(10, len(union.transitions))

    def test_union_02(self):
        # example from https://goo.gl/KEzUNJ
        in_01 = Automata.read_from_json('./test/data/test_union_02_input_01')
        in_02 = Automata.read_from_json('./test/data/test_union_02_input_02')
        verbose_union = in_01.union(in_02)
        union = verbose_union.minimize()
        # transition by transition was checked by hand with print :|
        # cannot check transition by transition because of the randomness
        self.assertEqual(3, len(union.states))
        self.assertEqual(1, len(union.final_states))
        self.assertEqual(6, len(union.transitions))

    def test_union_03(self):
        # example from https://goo.gl/7zdezP
        in_01 = Automata.read_from_json('./test/data/test_union_03_input_01')
        in_02 = Automata.read_from_json('./test/data/test_union_03_input_02')
        verbose_union = in_01.union(in_02)
        union = verbose_union.minimize()
        # transition by transition was checked by hand with print :|
        # cannot check transition by transition because of the randomness
        self.assertEqual(4, len(union.states))
        self.assertEqual(1, len(union.final_states))
        self.assertEqual(8, len(union.transitions))

    def test_union_04(self):
        # example from https://goo.gl/ya52uS
        in_01 = Automata.read_from_json('./test/data/test_union_04_input_01')
        in_02 = Automata.read_from_json('./test/data/test_union_04_input_02')
        union = in_01.union(in_02)
        # transition by transition was checked by hand with print :|
        # cannot check transition by transition because of the randomness
        self.assertEqual(8, len(union.states))
        self.assertEqual(5, len(union.final_states))
        self.assertEqual(16, len(union.transitions))

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

    def _print_automata(self, automata):
        """Helper that print the most importants infos from automata."""
        print('States:')
        print(automata.states)
        print('Alphabet:')
        print(automata.alphabet)
        print('Final states:')
        print(automata.final_states)
        print('q0:')
        print(automata.q0)
        print('Transitions:')
        print(automata.transitions)

if __name__ == '__main__':
    unittest.main()
