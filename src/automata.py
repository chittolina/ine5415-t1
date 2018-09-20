# -*- coding: utf-8 -*-
import json

class Automata:

    def __init__(self, alphabet, states, q0, final_states, transitions):
        if self._validate(alphabet, states, q0, final_states, transitions):
            self.alphabet = alphabet # type is a set of string
            self.states = states # type is a set of string
            self.q0 = q0 # type is a string
            self.final_states = final_states # type is a set of string
            self.transitions = transitions # type is a dict(namedtuple(state, alphabet): state)
        else:
            raise ValueError('Invalid input to create an automata.')


    def _validate(self, alphabet, states, q0, final_states, transitions):
        """Do validation about type, size and inner relationship.

        To keep simple, dont has validation in transitions or complex validations in alphabet.
        """
        if not type(alphabet) is set or \
           not type(states) is set or \
           not type(q0) is str or \
           not type(final_states) is set or \
           not type(transitions) is dict:
            return False
        elif not alphabet or not states or not final_states or not transitions:
            return False
        elif not final_states.issubset(states) or \
             not states.issuperset(final_states) or \
             not q0 in states:
            return False
        elif alphabet.intersection(states):
            return False

        return True

    # TODO: check local and parameter
    def read_from_json(self):
        pass

    def create_json(self):
        tmp = {self.q0: self.q0}
        with open('test.json', 'w') as write_file:
            json.dump(tmp, write_file)