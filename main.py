#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from src.automata import Automata
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSlot, QVariant

class Operator(QObject):

    def __init__(self, context, parent=None):
        super(Operator, self).__init__(parent)
        self.win = parent
        self.ctx = context
        self.automatas = []
        self.grammars = []
        self.results = {
            'automata': None,
            'grammar': None,
            'regex': None
        }

    @pyqtSlot(QVariant)
    def load_automata(self, filename):
        automata = Automata.read_from_json(filename[0].toString().replace('.json', '').replace('file://', ''))
        if automata and len(self.automatas) < 2:
            self.automatas.append(automata)
        else:
            # TODO: Show some dialog to the user
            print('Reached the max number automatas')

    @pyqtSlot(QVariant)
    def nfa_to_dfa(self):
        if len(self.automatas) != 1:
            # TODO: Show some dialog to the user
            print('Only one automata is allowed for this operation')
            return

        result = self.automatas[0].to_dfa()
        self.results['automata'] = result

    @pyqtSlot(QVariant)
    def dfa_to_grammar(self):
        if len(self.automatas) != 1:
            # TODO: Show some dialog to the user
            print('Only one automata is allowed for this operation')
            return

        result = self.automatas[0].to_grammar()
        self.results['grammar'] = result

    @pyqtSlot(QVariant)
    def dfa_union(self):
        if len(self.automatas) != 2:
            # TODO: Show some dialog to the user
            print('You need two automatas to perform this operation')
            return

        result = self.automatas[0].union(self.automatas[1])
        self.results['automata'] = result

    @pyqtSlot(QVariant)
    def dfa_intersection(self):
        if len(self.automatas) != 2:
            # TODO: Show some dialog to the user
            print('You need two automatas to perform this operation')
            return

        result = self.automatas[0].intersection(self.automatas[1])
        self.results['automata'] = result

    @pyqtSlot(QVariant)
    def dfa_minimize(self):
        if len(self.automatas) != 1:
            # TODO: Show some dialog to the user
            print('Only one automata is allowed for this operation')
            return

        result = self.automatas[0].minimize()
        self.results['automata'] = result

if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()
    engine.load('ui/main.qml')
    win = engine.rootObjects()[0]
    operator = Operator(ctx, win)
    ctx.setContextProperty('operator', operator)
    win.show()
    sys.exit(app.exec_())
