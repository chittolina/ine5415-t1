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

    def nfa_to_dfa(self):
        """Conversion of an NFA to a DFA

        Use the technique known as 'the subset construction'.
        """
        # TODO: lembrar de testar aqui
        # TODO: conferir com anotações
        # TODO: pensar sobre como retornar isso, provavelmente uma nova inst.

        new_states = {self._e_closure([self.q0]): False}
        new_transitions = {}

        for k, v in new_states.items():
            if not v:
                new_states[k] = True

                for char in self.alphabet:
                    new_state = self._e_closure(self._move(k, char))

                    if new_state not in new_states:
                        new_states[new_state] = False

                    new_transitions[Utils.TRANSITION(k, char)] = new_state

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

    def _move(self, state, char_input):
        # TODO: testar isso separadamente
        # TODO: comentar
        pass

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
