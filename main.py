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

    @pyqtSlot(QVariant)
    def load_automata(self, filename):
        automata = Automata.read_from_json(filename[0].toString().replace('.json', '').replace('file://', ''))
        if automata and len(self.automatas) < 2:
            self.automatas.append(automata)
        else:
            # TODO: Show some dialog to the user
            print('Reached the max number automatas')



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
