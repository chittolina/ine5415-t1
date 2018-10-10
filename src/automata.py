# -*- coding: utf-8 -*-
import json
import itertools
from .utils import Utils


class Automata:
    """Representation of an automata

    The automata can be deterministic or not. After validation in constructor,
    then this property is defined.
    """

    def __init__(self, alphabet, states, q0, final_states, transitions):
        if self.validate(alphabet, states, q0, final_states, transitions):
            self.alphabet = alphabet  # type is a set of string
            self.states = states  # type is a set of string
            self.q0 = q0  # type is a string
            self.final_states = final_states  # type is a set of string
            # transitions is a dict(namedtuple(state, alphabet): set(state))
            self.transitions = transitions
        else:
            raise ValueError('Invalid input to create an automata.')

        self.deterministic = self._is_deterministic()

    def save_json(self, filename):
        """Save in filesystem a json file from an automata

        The path in filename don't need contain the '.json' extension.
        """
        data = {}
        data['alphabet'] = list(self.alphabet)
        data['states'] = list(self.states)
        data['q0'] = self.q0
        data['final_states'] = list(self.final_states)
        data['transitions'] = [(k[0], k[1], list(v))
                               for k, v in self.transitions.items()]

        with open(filename + '.json', 'w') as write_file:
            json.dump(data, write_file, indent=4)

    def _is_deterministic(self):
        """Check if the automata is deterministic.

        1. There are no moves on input &, and
        2. For each state s and input symbol a, there is exactly one edge out
        of s labeled a.
        """
        if len(self.transitions) != len(self.alphabet) * len(self.states):
            return False

        for key, value in self.transitions.items():
            if key[1] == Utils.EPSILON or len(value) != 1:
                return False

        return True

    def to_dfa(self):
        """Conversion of an NFA to a DFA

        Use the technique known as 'the subset construction' to return the new
        DFA
        """
        if self.deterministic:
            raise Warning('Automata is a DFA. Isnt necessary make conversion.')

        # start determinization process
        new_q0 = frozenset(self._e_closure([self.q0]))
        new_states = [new_q0]
        new_transitions = {}

        states_to_check = 1
        i = 0
        while states_to_check > 0:
            state = new_states[i]
            states_to_check -= 1
            i += 1

            for char in self.alphabet:
                new_state = frozenset(self._e_closure(self._move(state, char)))

                if new_state not in new_states:
                    new_states.append(new_state)
                    states_to_check += 1

                new_transitions[Utils.TRANSITION(state, char)] = new_state

        new_final_states = {s for s in new_states
                            if not s.isdisjoint(self.final_states)}

        # process is done and now its necessary 'normalizar' the new things
        # 'normalizar' -> set of states become a string
        final_names = {}
        normal_states = set()
        i = 0
        for new_state in new_states:
            name = 'q' + str(i)
            final_names[new_state] = name
            normal_states.add(name)
            i += 1

        normal_q0 = final_names[new_q0]
        normal_final_states = {final_names[s] for s in new_final_states}

        normal_transitions = {}
        for trans, target in new_transitions.items():
            normal_from = final_names[trans[0]]
            normal_target = {final_names[target]}
            normal_transitions[Utils.TRANSITION(normal_from, trans[1])] = \
                normal_target

        # all done, just return a new Automata
        return Automata(self.alphabet, normal_states, normal_q0,
                        normal_final_states, normal_transitions)

    def _e_closure(self, states):
        """Return e-closure of states parameter

        Set of NFA states reachable from some NFA state s in set states on
        e-transitions alone.

        Type of parameter 'states' is a list.
        """
        stack = [s for s in states]
        e_closure = states
        while stack:
            top_state = stack.pop()
            transition = Utils.TRANSITION(top_state, Utils.EPSILON)

            # avoid KeyError with state without transition by epsilon
            if transition in self.transitions:
                for state in self.transitions[transition]:
                    if state not in e_closure:
                        e_closure.append(state)
                        stack.append(state)

        return {s for s in e_closure}

    def _move(self, states, char):
        """Return move result by char in states.

        List of NFA states to which there is a transition on input symbol char
        from some state s in states.
        """
        stack = [s for s in states]
        result = []
        while stack:
            top_state = stack.pop()
            transition = Utils.TRANSITION(top_state, char)

            # avoid KeyError with state without transition by epsilon
            if transition in self.transitions:
                for state in self.transitions[transition]:
                    if state not in result:
                        result.append(state)

        return result

    def minimize(self):
        """Minimize a DFA by the Hopcroft's algorithm.

        Hopcroft's algorithm says that to minimize a automata it's necessary
        just two steps:
        1. Remove unreachable states
        2. Merge nondistinguishable states

        Then return a minimized DFA.
        """
        if not self.deterministic:
            raise Warning('Its necessary be a DFA to make minimization.')

        # start steps of minimization
        unreachable_states = self._define_unreachable()

        new_states = self.states - unreachable_states
        new_final_states = self.final_states - unreachable_states

        partition = self._merge_nondistinguishable(new_states,
                                                   new_final_states)

        # two step was done. The next process is similar to 'normalizar'
        # of determinization. Probably, this could be coded better
        normal_states = set()
        normal_final_states = set()
        final_names = {}
        i = 0
        for group in partition:
            name = 'q' + str(i)
            i += 1
            final_names[name] = group
            normal_states.add(name)

            if self.q0 in group:
                normal_q0 = name

            if self.final_states.intersection(group):
                normal_final_states.add(name)

        normal_transitions = {}
        for group in partition:
            old_source = next(iter(group))
            for char in self.alphabet:
                old_target = self.transitions[Utils.TRANSITION(old_source,
                                                               char)]

                new_source = None
                new_target = None
                for name, value in final_names.items():
                    if old_source in value:
                        new_source = name

                    if old_target.intersection(value):
                        new_target = name

                    if new_source is not None and new_target is not None:
                        break

                normal_transitions[Utils.TRANSITION(new_source, char)] = \
                    new_target

        # all done, just return a new Automata
        return Automata(self.alphabet, normal_states, normal_q0,
                        normal_final_states, normal_transitions)

    def _define_unreachable(self):
        """Return unreachable states

        Any state that cannot be reached from the start state, for any input.
        """
        # today this method is only used in minimization, so the next check
        # is a little verbose. On the other hand, the algorithm has an
        # adaptation that make him fail if applied in a NFA
        if not self.deterministic:
            raise Warning('Its necessary be a DFA to define unreachable'
                          ' states.')

        reachable_states = {self.q0}
        new_states = {self.q0}

        while True:
            tmp = set()
            for state in new_states:
                for char in self.alphabet:
                    # only works because its a DFA
                    # solution to the problem of add a set inside other set
                    set_of_target = self.transitions[
                        Utils.TRANSITION(state, char)].copy()
                    tmp.add(set_of_target.pop())

            new_states = tmp - reachable_states
            reachable_states = reachable_states.union(new_states)

            if not new_states:
                break

        return self.states - reachable_states

    def _merge_nondistinguishable(self, new_states, new_final_states):
        """Return partition with the merge of nondistinguishable states

        Based on partition refinement, partiotining the DFA states into groups
        by their behavior. These groups represent equivalence classes of the
        Myhill–Nerode equivalence relation, whereby every two states of the
        same partition are equivalent if they have the same behavior for all
        the input sequences.
        """
        if not self.deterministic:
            raise Warning('Its necessary be a DFA to merge nondistinguishable'
                          ' states.')

        nonaccepting_states = new_states - new_final_states
        partition = [new_final_states, nonaccepting_states]
        work_list = [new_final_states]
        work_partition = partition.copy()

        while work_list:
            group = work_list.pop()
            for char in self.alphabet:
                # create a set of states for which a transition on char leads
                # to a state in group
                sources = set()
                for key, value in self.transitions.items():
                    if key[1] == char and value.intersection(group):
                        sources.add(key[0])

                while work_partition:
                    item = work_partition.pop()
                    intersection_result = sources.intersection(item)
                    relative_complement_result = item - sources
                    if intersection_result and relative_complement_result:
                        partition.remove(item)
                        partition.append(intersection_result)
                        partition.append(relative_complement_result)
                        work_partition.append(intersection_result)
                        work_partition.append(relative_complement_result)

                        if item in work_list:
                            work_list.remove(item)
                            work_list.append(intersection_result)
                            work_list.append(relative_complement_result)
                        else:
                            if len(intersection_result) <= \
                               len(relative_complement_result):
                                work_list.append(intersection_result)
                            else:
                                work_list.append(relative_complement_result)

                work_partition = partition.copy()

        return partition

    def union(self, other):
        """Make union of two DFAs

        Using the Sipser's proof that the class of regular languages is closed
        under the union operation. Return a new automata that is the union of
        the self instance and the dfa passed by parameter.
        """
        return self._helper_union_and_intersection(other, True)

    def intersection(self, other):
        """Make intersection of two DFAs

        Using the Sipser's proof that the class of regular languages is closed
        under the intersection operation. Return a new automata that is the
        intersection of the self instance and the dfa passed by parameter.
        """
        return self._helper_union_and_intersection(other, False)

    def _helper_union_and_intersection(self, other, is_union):
        """Helper to union and intersection of two DFAs

        Since the algorithm to union and intersection of two DFAs are almost
        equal, this helper make all proccess for both operations. The only
        difference is in the creation of final states. This difference is
        managed by the parameter 'is_union'.

        Return a resultant automata.
        """
        if not self.deterministic or not other.deterministic:
            raise Warning('The inputs need to be DFAs to make the union.')

        new_alphabet = self.alphabet.union(other.alphabet)

        final_names = {}
        new_states = set()
        i = 0
        for cartersian_product in itertools.product(self.states, other.states):
            name = 'q' + str(i)
            new_states.add(name)
            final_names[cartersian_product] = name
            i += 1

        new_q0 = final_names[(self.q0, other.q0)]

        if is_union:
            first_group = {final_names[y] for y in itertools.product(
                self.final_states, other.states)}
            second_group = {final_names[z] for z in itertools.product(
                self.states, other.final_states)}
            new_final_states = first_group.union(second_group)
        else:
            new_final_states = {final_names[y] for y in itertools.product(
                self.final_states, other.final_states)}

        new_transitions = {}
        for key, value in final_names.items():
            for char in new_alphabet:
                # possible do the next lines because of dfa's check at begin
                first_target = self.transitions.get(Utils.TRANSITION(
                    key[0], char))
                if first_target is not None:
                    first_target = next(iter(first_target))

                second_target = other.transitions.get(Utils.TRANSITION(
                    key[1], char))
                if second_target is not None:
                    second_target = next(iter(second_target))

                real_target = final_names.get((first_target, second_target))

                new_transitions[Utils.TRANSITION(value, char)] = {real_target}

        return Automata(new_alphabet, new_states, new_q0, new_final_states,
                        new_transitions)

    def to_grammar(self):
        """Return a grammar equivalent to this automaton."""
        from .grammar import Grammar
        if not self.deterministic:
            dfa = self.to_dfa()
            return dfa.to_grammar()
        initial_symbol = self.q0.upper()
        productions = self._makeProductions()
        return Grammar(productions, initial_symbol)

    def _makeProductions(self):
        productions = list()
        for input in self.transitions:
            for output in self.transitions[input]:
                self._include_productions(productions, input, output)
        return productions

    def _include_productions(self, productions, input, output):
        if output in self.final_states:
            production = (input[0].upper(), input[1])
            productions.append(production)
        production = (input[0].upper(), input[1], output.upper())
        productions.append(production)

    @staticmethod
    def read_from_json(filename):
        """Return an automata from a json file

        The path in filename don't need contain the '.json' extension.
        """
        # str come as unicode from json
        with open(filename + '.json', 'r') as load_file:
            data = json.load(load_file)

        alphabet = set(data['alphabet'])
        states = set(data['states'])
        q0 = str(data['q0'])
        final_states = set(data['final_states'])

        transitions = {}
        for lst in data['transitions']:
            transition = Utils.TRANSITION(lst[0], lst[1])
            transitions[transition] = set(lst[2])

        return Automata(alphabet, states, q0, final_states, transitions)

    @staticmethod
    def validate(alphabet, states, q0, final_states, transitions):
        """Do automata validation about type, size and inner relationship

        To keep simple, don't has validation in transitions or complex
        validations in alphabet.
        """
        if not isinstance(alphabet, set) or \
           not isinstance(states, set) or \
           not isinstance(q0, str) or \
           not isinstance(final_states, set) or \
           not isinstance(transitions, dict):
            return False

        if not alphabet or not states or not final_states or not transitions:
            return False

        if not final_states.issubset(states) or \
                not states.issuperset(final_states) or \
                q0 not in states:
            return False

        if alphabet.intersection(states):
            return False

        return True
