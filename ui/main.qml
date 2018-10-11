import QtQuick 2.4
import QtQuick.Controls 2.2
import QtQuick.Controls 1.4
import QtQuick.Dialogs 1.0

ApplicationWindow {
    title: 'Test'
    width: 800
    height: 900

    Page {
      width: 800
      height: 900

      header: Label {
        text: 'Trabalho 1 - INE5421'
      }

      SplitView {
        anchors.fill: parent
        orientation: Qt.Vertical

        Rectangle {
          width: 200
          height: 300
          color: 'white'
          Text {
              text: 'Automata'
          }
          Button {
            anchors { top: parent.top; topMargin: 20; left: parent.left; leftMargin: 20 }
            text: 'NFA to DFA'
          }
          Button {
            anchors { top: parent.top; topMargin: 20; left: parent.left; leftMargin: 150 }
            text: 'DFA to GR'
          }
          Button {
            anchors { top: parent.top; topMargin: 20; left: parent.left; leftMargin: 300 }
            text: 'DFA Union'
          }
          Button {
            anchors { top: parent.top; topMargin: 20; left: parent.left; leftMargin: 450 }
            text: 'DFA Intersection'
          }
          Button {
            anchors { top: parent.top; topMargin: 20; left: parent.left; leftMargin: 600 }
            text: 'DFA Minimize'
          }
          Button {
            anchors { top: parent.top; topMargin: 100; left: parent.left; leftMargin: 20 }
            text: 'Import automata'
            onClicked: automataFileDialog.open()
          }
        }
        Rectangle {
          width: 200
          height: 300
          color: 'white'
          Text {
              text: 'Grammar'
          }
        }
        Rectangle {
          width: 200
          height: 300
          color: 'white'
          Text {
              text: 'Regular expression'
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
    }
}
