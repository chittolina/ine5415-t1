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

    def to_dfa(self):
        """Conversion of an NFA to a DFA

        Use the technique known as 'the subset construction'.
        """
        # TODO: conferir com anotações

        # start determinization process
        new_q0 = frozenset(self._e_closure([self.q0]))
        new_states_with_marks = [(new_q0, False)]
        new_transitions = {}

        for i in new_states_with_marks:
            if not i[1]:
                new_states_with_marks.remove(i)
                new_states_with_marks.append((i[0], True))

                for char in self.alphabet:
                    new_state = \
                        frozenset(self._e_closure(self._move(i[0], char)))

                    if (new_state, True) not in new_states_with_marks and \
                       (new_state, False) not in new_states_with_marks:
                        new_states_with_marks.append((new_state, False))

                    new_transitions[Utils.TRANSITION(i[0], char)] = new_state

        new_states = {i[0] for i in new_states_with_marks}
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
            normal_target = final_names[target]
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
