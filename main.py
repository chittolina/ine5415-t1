#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from src.automata import Automata
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty, QVariant

class Operator(QObject):
    automataLoaded = pyqtSignal()

    def __init__(self, context, parent=None):
        super(Operator, self).__init__(parent)
        self._ctx = context
        self._automatas = []
        self._grammars = []
        self._results = {
            'automata': None,
            'grammar': None,
            'regex': None
        }

    @pyqtProperty(str, notify=automataLoaded)
    def automatas(self):
        result_string = ''
        for automata in self._automatas:
            for i, input in enumerate(automata.alphabet):
                if i == 0:
                    result_string += '\t\t' + input
                else:
                    result_string += '\t' + input
            result_string += '\n'
            for state in automata.states:
                result_string += state + '\t'
                for input in automata.alphabet:
                    result_string += '\t' + str(list(automata.transition(state, input)))
                result_string += '\n'



        return result_string


    @automatas.setter
    def automatas(self, value):
        self._automatas = value
        self.automataLoaded.emit()

    @pyqtSlot(QVariant)
    def load_automata(self, filename):
        automata = Automata.read_from_json(filename[0].toString().replace('.json', '').replace('file://', ''))
        if automata and len(self._automatas) < 2:
            self._automatas.append(automata)
            self.automatas = self._automatas
        else:
            # TODO: Show some dialog to the user
            print('Reached the max number automatas')

    @pyqtSlot(QVariant)
    def nfa_to_dfa(self):
        if len(self._automatas) != 1:
            # TODO: Show some dialog to the user
            print('Only one automata is allowed for this operation')
            return

        result = self._automatas[0].to_dfa()
        self._results['automata'] = result

    @pyqtSlot(QVariant)
    def dfa_to_grammar(self):
        if len(self._automatas) != 1:
            # TODO: Show some dialog to the user
            print('Only one automata is allowed for this operation')
            return

        result = self._automatas[0].to_grammar()
        self._results['grammar'] = result

    @pyqtSlot(QVariant)
    def dfa_union(self):
        if len(self._automatas) != 2:
            # TODO: Show some dialog to the user
            print('You need two automatas to perform this operation')
            return

        result = self._automatas[0].union(self._automatas[1])
        self._results['automata'] = result

    @pyqtSlot(QVariant)
    def dfa_intersection(self):
        if len(self._automatas) != 2:
            # TODO: Show some dialog to the user
            print('You need two automatas to perform this operation')
            return

        result = self._automatas[0].intersection(self._automatas[1])
        self._results['automata'] = result

    @pyqtSlot(QVariant)
    def dfa_minimize(self):
        if len(self._automatas) != 1:
            # TODO: Show some dialog to the user
            print('Only one automata is allowed for this operation')
            return

        result = self._automatas[0].minimize()
        self._results['automata'] = result

if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()
    operator = Operator(ctx)
    ctx.setContextProperty('operator', operator)
    engine.load('ui/main.qml')
    win = engine.rootObjects()[0]
    win.show()
    sys.exit(app.exec_())
