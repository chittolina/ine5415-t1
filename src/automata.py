# -*- coding: utf-8 -*-
import json
from collections import namedtuple
from .utils_automata import Utils


class Automata:

    def __init__(self, alphabet, states, q0, final_states, transitions):
        if self._validate(alphabet, states, q0, final_states, transitions):
            self.alphabet = alphabet  # type is a set of string
            self.states = states  # type is a set of string
            self.q0 = q0  # type is a string
            self.final_states = final_states  # type is a set of string
            # transitions is a dict(namedtuple(state, alphabet): set(state))
            self.transitions = transitions
        else:
            raise ValueError('Invalid input to create an automata.')

        self.deterministic = self._is_deterministic()

    def _validate(self, alphabet, states, q0, final_states, transitions):
        """Do validation about type, size and inner relationship.

        To keep simple, dont has validation in transitions or complex
        validations in alphabet.
        """
        if not type(alphabet) is set or \
           not type(states) is set or \
           not type(q0) is str or \
           not type(final_states) is set or \
           not type(transitions) is dict:
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

    def save_json(self, filename):
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

        for k, v in self.transitions.items():
            if k[1] == Utils.EPSILON or len(v) != 1:
                return False

        return True

    def to_dfa(self):
        """Conversion of an NFA to a DFA

        Use the technique known as 'the subset construction'.
        """
        # TODO: when code the view, see the better way to work with this
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
        # TODO: maybe _move and _e_closure could be just one method
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
        """
        # TODO: testes

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
            old_source = group.pop()
            for char in self.alphabet:
                old_target = self.transitions[Utils.TRANSITION(old_source,
                                                               char)]

                new_source = None
                new_target = None
                for name, value in final_names.items():
                    if old_source in value:
                        new_source = name

                    if old_target in value:
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
                    set_of_target = self.transitions[Utils.TRANSITION(state,
                                                                      char)]
                    state = set_of_target.pop()
                    tmp.add(state)

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
        # TODO: testar separado (?)

        if not self.deterministic:
            raise Warning('Its necessary be a DFA to merge nondistinguishable'
                          ' states.')

        nonaccepting_states = new_states - new_final_states
        partition = {new_final_states, nonaccepting_states}
        work_set = {new_final_states}

        # TODO: debugar para ver mudancas enquanto itera
        while work_set:
            group = work_set.pop()
            for char in self.alphabet:
                # create a set of states for which a transition on char leads
                # to a state in group
                sources = set()
                for k, v in self.transitions.items():
                    if k[1] == char and v in group:
                        sources.add(k[0])

                # TODO: debugar para ver mudancas enquanto itera
                for item in partition:
                    intersection_result = sources.intersection(item)
                    relative_complement_result = item - sources
                    if intersection_result and relative_complement_result:
                        partition.remove(item)
                        partition.add(intersection_result)
                        partition.add(relative_complement_result)

                        if item in work_set:
                            work_set.remove(item)
                            work_set.add(intersection_result)
                            work_set.add(relative_complement_result)
                        else:
                            if len(intersection_result) <= \
                               len(relative_complement_result):
                                work_set.add(intersection_result)
                            else:
                                work_set.add(relative_complement_result)

        return partition

    @staticmethod
    def read_from_json(filename):
        # str come as unicode from json
        with open(filename + '.json', 'r') as load_file:
            data = json.load(load_file)

        alphabet = set(data['alphabet'])
        states = set(data['states'])
        q0 = str(data['q0'])
        final_states = set(data['final_states'])

        transitions = {}
        for l in data['transitions']:
            t = Utils.TRANSITION(l[0], l[1])
            transitions[t] = set(l[2])

        return Automata(alphabet, states, q0, final_states, transitions)
