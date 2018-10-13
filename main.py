"""INE 5421 - Linguagem Formais e Compiladores - Trabalho 01

Universidade Federal de Santa Catarina

Departamento de Informática e Estatística (INE)

Alunos:

- Filipe Oliveira de Borba
- Gabriel Leal Chittolina Amaral
- Lucas João Martins
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from src.automata import Automata
from src.grammar import Grammar
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty, QVariant

class Operator(QObject):
    automataLoaded = pyqtSignal()
    grammarLoaded = pyqtSignal()
    automataGeneratedFromAutomata = pyqtSignal()
    automataGeneratedFromGrammar = pyqtSignal()
    grammarGeneratedFromAutomata = pyqtSignal()

    def __init__(self, context, parent=None):
        super(Operator, self).__init__(parent)
        self._ctx = context
        self._automatas = []
        self._grammars = []
        self._grammarFromAutomata = None
        self._automataFromAutomata = None
        self._automataFromGrammar = None
        self._automataFromRegex = None

    @pyqtProperty(str, notify=automataLoaded)
    def automatas(self):
        result_string = ''

        for automata in self._automatas:
            for i, input in enumerate(list(automata.alphabet) + ['&']):
                if i == 0:
                    result_string += '\t\t\t' + input
                else:
                    result_string += '\t' + input
            result_string += '\n'
            for state in automata.states:
                if state in automata.final_states:
                    result_string += '* ' + state + '\t'
                elif state == automata.q0:
                    result_string += '-> ' + state + '\t'
                else:
                    result_string += state + '\t'
                for input in list(automata.alphabet) + ['&']:
                    if automata.transition(state, input):
                        result_string += '\t' + str(list(automata.transition(state, input)))
                    else:
                        result_string += '\t' + '[]'
                result_string += '\n'



        return result_string

    @automatas.setter
    def automatas(self, value):
        self._automatas = value
        self.automataLoaded.emit()

    @pyqtProperty(str, notify=automataGeneratedFromAutomata)
    def automataFromAutomata(self):
        result_string = ''
        a = self._automataFromAutomata
        if not a:
            return result_string

        for i, input in enumerate(list(a.alphabet) + ['&']):
            if i == 0:
                result_string += '\t\t\t' + input
            else:
                result_string += '\t' + input
        result_string += '\n'
        for state in a.states:
            if state in a.final_states:
                result_string += '* ' + state + '\t'
            elif state == a.q0:
                result_string += '-> ' + state + '\t'
            else:
                result_string += state + '\t'
            for input in list(a.alphabet) + ['&']:
                if a.transition(state, input):
                    result_string += '\t' + str(list(a.transition(state, input)))
                else:
                    result_string += '\t' + str(list([]))
            result_string += '\n'



        return result_string

    @pyqtProperty(str, notify=automataGeneratedFromGrammar)
    def automataFromGrammar(self):
        result_string = ''
        a = self._automataFromGrammar
        if not a:
            return
        for i, input in enumerate(list(a.alphabet) + ['&']):
            if i == 0:
                result_string += '\t\t\t' + input
            else:
                result_string += '\t' + input
        result_string += '\n'
        for state in a.states:
            if state in a.final_states:
                result_string += '* ' + state + '\t'
            elif state == a.q0:
                result_string += '-> ' + state + '\t'
            else:
                result_string += state + '\t'
            for input in list(a.alphabet) + ['&']:
                if a.transition(state, input):
                    result_string += '\t' + str(list(a.transition(state, input)))
                else:
                    result_string += '\t' + str(list([]))
            result_string += '\n'

        return result_string

    @automataFromGrammar.setter
    def automataFromGrammar(self, value):
        self._automataFromGrammar = value
        self.automataGeneratedFromGrammar.emit()

    @automataFromAutomata.setter
    def automataFromAutomata(self, value):
        self._automatasFromAutomata = value
        self.automataGeneratedFromAutomata.emit()

    @pyqtProperty(str, notify=grammarLoaded)
    def grammars(self):
        result_string = ''
        if len(self._grammars) < 1:
            return

        for production in self._grammars[0]._productions:
            result_string += production[0] + '  ->  ' + production[1]
            if len(production) > 2:
                result_string += '  |  ' + production[2]
            result_string += '\n'
        return result_string

    @grammars.setter
    def grammars(self, value):
        self._grammars = value
        self.grammarLoaded.emit()

    @pyqtProperty(str, notify=grammarGeneratedFromAutomata)
    def grammarFromAutomata(self):
        result_string = ''
        if not self._grammarFromAutomata:
            return result_string

        for production in self._grammarFromAutomata._productions:
            result_string += production[0] + '  ->  ' + production[1]
            if len(production) > 2:
                result_string += '  |  ' + production[2]
            result_string += '\n'
        return result_string

    @grammarFromAutomata.setter
    def grammarFromAutomata(self, value):
        self._grammarFromAutomata = value
        self.grammarGeneratedFromAutomata.emit()

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
    def clear_automatas(self):
        self._automatas = []
        self._automataFromAutomata = None
        self._grammarFromAutomata = None
        self.automatas = self._automatas
        self.automataFromAutomata = self._automataFromAutomata
        self.grammarFromAutomata = self._grammarFromAutomata

    @pyqtSlot(QVariant)
    def clear_grammars(self):
        self._grammars = []
        self._automataFromGrammar = None
        self.grammars = self._grammars
        self.automataFromGrammar = self._automataFromGrammar

    @pyqtSlot(QVariant)
    def nfa_to_dfa(self):
        if len(self._automatas) != 1:
            # TODO: Show some dialog to the user
            print('Only one automata is allowed for this operation')
            return

        result = self._automatas[0].to_dfa()
        self._automataFromAutomata = result
        self.automataFromAutomata = self._automataFromAutomata

    @pyqtSlot(QVariant)
    def dfa_to_grammar(self):
        if len(self._automatas) != 1:
            # TODO: Show some dialog to the user
            print('Only one automata is allowed for this operation')
            return

        result = self._automatas[0].to_grammar()
        self._grammarFromAutomata = result
        self.grammarFromAutomata = self._grammarFromAutomata

    @pyqtSlot(QVariant)
    def dfa_union(self):
        if len(self._automatas) != 2:
            # TODO: Show some dialog to the user
            print('You need two automatas to perform this operation')
            return

        result = self._automatas[0].union(self._automatas[1])
        self._automataFromAutomata = result
        self.automataFromAutomata = self._automataFromAutomata

    @pyqtSlot(QVariant)
    def dfa_intersection(self):
        if len(self._automatas) != 2:
            # TODO: Show some dialog to the user
            print('You need two automatas to perform this operation')
            return

        result = self._automatas[0].intersection(self._automatas[1])
        self._automataFromAutomata = result
        self.automataFromAutomata = self._automataFromAutomata

    @pyqtSlot(QVariant)
    def dfa_minimize(self):
        if len(self._automatas) != 1:
            # TODO: Show some dialog to the user
            print('Only one automata is allowed for this operation')
            return

        result = self._automatas[0].minimize()
        self._automataFromAutomata = result
        self.automataFromAutomata = self._automataFromAutomata

    @pyqtSlot(QVariant)
    def load_grammar(self, filename):
        grammar = Grammar.read_from_json(filename[0].toString().replace('.json', '').replace('file://', ''))
        if grammar and len(self._grammars) < 1:
            self._grammars.append(grammar)
            self.grammars = self._grammars
        else:
            # TODO: Show some dialog to the user
            print('Reached the max number of grammars')

    @pyqtSlot(QVariant)
    def grammar_to_dfa(self):
        if len(self._grammars) != 1:
            # TODO: Show some dialog to the user
            print('You need exactly one grammar to perform this operation')
            return

        result = self._grammars[0].to_automaton()
        self._automataFromGrammar = result
        self.automataFromGrammar = self._automataFromGrammar

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
