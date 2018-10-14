import QtQuick 2.4
import QtQuick.Controls 2.2
import QtQuick.Controls 1.4
import QtQuick.Dialogs 1.0

ApplicationWindow {
    title: 'Test'
    width: 1000
    height: 1000

    Page {
      width: 1000
      height: 1000

      header: Label {
        text: 'Trabalho 1 - INE5421'
      }

      SplitView {
        anchors.fill: parent
        orientation: Qt.Vertical

        Rectangle {
          width: 1000
          height: 330
          color: 'white'
          Text {
              text: 'Automata'
          }
          Button {
            anchors { top: parent.top; topMargin: 20; left: parent.left; leftMargin: 20 }
            text: 'NFA to DFA'
            onClicked: operator.nfa_to_dfa('')
          }
          Button {
            anchors { top: parent.top; topMargin: 20; left: parent.left; leftMargin: 150 }
            text: 'DFA to GR'
            onClicked: operator.dfa_to_grammar('')
          }
          Button {
            anchors { top: parent.top; topMargin: 20; left: parent.left; leftMargin: 300 }
            text: 'DFA Union'
            onClicked: operator.dfa_union('')
          }
          Button {
            anchors { top: parent.top; topMargin: 20; left: parent.left; leftMargin: 450 }
            text: 'DFA Intersection'
            onClicked: operator.dfa_intersection('')
          }
          Button {
            anchors { top: parent.top; topMargin: 20; left: parent.left; leftMargin: 600 }
            text: 'DFA Minimize'
            onClicked: operator.dfa_minimize('')
          }
          Button {
            anchors { top: parent.top; topMargin: 100; left: parent.left; leftMargin: 20 }
            text: 'Import automata'
            onClicked: automataFileDialog.open()
          }
          Button {
            anchors { top: parent.top; topMargin: 100; left: parent.left; leftMargin: 200 }
            text: 'Clear'
            onClicked: operator.clear_automatas('')
          }
          Text {
            anchors { top: parent.top; topMargin: 150; left: parent.left; leftMargin: 20 }
            text: operator.automatas
          }
          Text {
            anchors { top: parent.top; topMargin: 150; right: parent.right; rightMargin: 20 }
            text: operator.automataFromAutomata
          }
          Text {
            anchors { top: parent.top; topMargin: 150; right: parent.right; rightMargin: 20 }
            text: operator.grammarFromAutomata
          }
        }
        Rectangle {
          width: 1000
          height: 330
          color: 'white'
          Text {
              text: 'Grammar'
          }
          Button {
            anchors { top: parent.top; topMargin: 100; left: parent.left; leftMargin: 20 }
            text: 'Import grammar'
            onClicked: grammarFileDialog.open()
          }
          Button {
            anchors { top: parent.top; topMargin: 100; left: parent.left; leftMargin: 200 }
            text: 'Clear'
            onClicked: operator.clear_grammars('')
          }
          Button {
            anchors { top: parent.top; topMargin: 20; left: parent.left; leftMargin: 20 }
            text: 'GR to DFA'
            onClicked: operator.grammar_to_dfa('')
          }
          Text {
            anchors { top: parent.top; topMargin: 150; left: parent.left; leftMargin: 20 }
            text: operator.grammars
          }
          Text {
            anchors { top: parent.top; topMargin: 150; right: parent.right; rightMargin: 20 }
            text: operator.automataFromGrammar
          }
        }
        Rectangle {
          width: 1000
          height: 330
          color: 'white'
          Text {
              text: 'Regular expression'
          }
        }
      }
    }

    FileDialog {
      id: automataFileDialog
      title: "Please choose a file"
      folder: shortcuts.home
      onAccepted: {
          operator.load_automata(automataFileDialog.fileUrls)
      }
    }
    FileDialog {
      id: grammarFileDialog
      title: "Please choose a file"
      folder: shortcuts.home
      onAccepted: {
          operator.load_grammar(grammarFileDialog.fileUrls)
      }
    }
}
