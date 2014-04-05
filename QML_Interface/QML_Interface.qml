import QtQuick 1.1

Rectangle {
    id: rectangle1
    width: 451
    height: 300
    z: -1

    property alias dialogText: dialogElement.text
    property bool finished: false

    signal answerYes
    signal answerNo
    signal restartProcess


    Image {
        id: image1
        x: 0
        y: 0
        z: 0
        anchors.rightMargin: 0
        anchors.bottomMargin: 0
        anchors.leftMargin: 0
        anchors.topMargin: 0
        fillMode: Image.PreserveAspectCrop
        anchors.fill: parent
        source: "madame.jpg"
    }

    Button {
        id: btnRestart
        x: 0
        y: 286
        width: 71
        height: 14
        color: "#40ffffff"
        text: qsTr("Restart")
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 0
        mouseOverColor: "#ffffff"
        onClicked: {
            restartProcess()
        }
    }

    Column {
        id: column1
        anchors.fill: parent
        spacing: 5

        DialogElement {
            id: dialogElement
            width: 245 * parent.width / 451
            height: 51 * parent.height / 300
            gradient: Gradient {
                GradientStop {
                    position: 0.02
                    color: "#f5ef98"
                }

                GradientStop {
                    position: 1
                    color: "#80ffffff"
                }
            }

            z: 2
        }

        Row {
            id: row1
            width: 110
            height: 31
            spacing: 10
            z: 1

            Button {
                id: btnYes
                width: 50
                height: 31
                color: "#80ffffff"
                text: qsTr("Yes")
                mouseOverColor: "#ffffff"
                onClicked: {
                    answerYes()
                }
            }

            Button {
                id: btnNo
                width: 50
                height: 31
                color: "#80ffffff"
                text: qsTr("No")
                mouseOverColor: "#ffffffff"
                onClicked: {
                    answerNo()
                }
            }
        }
    }

    Button {
        id: btnClose
        x: 380
        y: 286
        width: 71
        height: 14
        color: "#40ffffff"
        text: qsTr("Close")
        anchors.right: parent.right
        anchors.rightMargin: 0
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 0
        mouseOverColor: "#ffffff"
        onClicked: {
            Qt.quit()
        }
    }

    states: [
        State {
            name: "finished"
            when: finished
            PropertyChanges {
            }

            PropertyChanges {
                target: row1
                visible: false
            }
        }
    ]
}

