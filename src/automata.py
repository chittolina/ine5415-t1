# -*- coding: utf-8 -*-

class Automata:

    def __init__(self, alphabet, states, q0, final_states, transitions):
        if self._validate(alphabet, states, q0, final_states, transitions):
            self.alphabet = alphabet # type is a set of string
            self.states = states # type is a set of string
            self.qo = q0 # type is a string
            self.final_states = final_states # type is a set of string
            self.transitions = transitions # type is a dict(namedtuple(state, alphabet): state)
        else:
            raise ValueError('Invalid input to create an automata.')

    def _validate(self, alphabet, states, q0, final_states, transitions):
        if not type(alphabet) is set or \
            not type(states) is set or \
            not type(q0) is str or \
            not type(final_states) is set or \
            not type(transitions) is dict:
           return False
        # TODO: size
        # TODO: meaning
            # q0 and final states in states
            # intersection alphabet and states == empty
            # doubt: alphabet
            # doubt: transitions

        return True

    # TODO: check local and parameter
    def read_from_json(self):
        pass

    def create_json(self):
        pass
