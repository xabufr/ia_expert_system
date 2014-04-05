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


    MouseArea {
        id: mouseArea
        anchors.fill: parent
        property variant clickPos: "1,1"
        property variant resize: false
        z: 1

        onPressed: {
            clickPos = Qt.point(mouse.x, mouse.y)
            if(clickPos.x >= mainWindow.size.width - 10 ||
                    clickPos.y >= mainWindow.size.height - 10 ) {
                resize = {
                    x: clickPos.x >= mainWindow.size.width - 10,
                    y: clickPos.y >= mainWindow.size.height - 10
                }
            }
            else
                resize = false
        }

        onPositionChanged: {
            var delta = Qt.size(mouse.x - clickPos.x, mouse.y - clickPos.y)
            if(resize !== false) {
                var newSize = Qt.size(mainWindow.size.width, mainWindow.size.height)
                if(resize.x === true) {
                    newSize.width += delta.width
                }
                if(resize.y === true) {
                    newSize.height += delta.height
                }
                mainWindow.size = newSize
                parent.height = mainWindow.size.height
                parent.width = mainWindow.size.width
                clickPos = Qt.point(mouse.x, mouse.y)
            }
            else
                mainWindow.pos = Qt.point(mainWindow.pos.x + delta.width, mainWindow.pos.y + delta.height)
        }
    }

    Image {
        id: image1
        x: 0
        y: 0
        z: 1
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
        z: 2
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 0
        mouseOverColor: "#ffffff"
        onClicked: {
            restartProcess()
        }
    }

    Column {
        id: column1
        z: 2
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
        z: 2
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
                target: btnYes
                clickAllowed: false
            }
            PropertyChanges {
                target: btnNo
                clickAllowed: false
            }

            PropertyChanges {
                target: row1
                opacity: 0
                visible: false
            }
        }
    ]

    transitions: Transition {
        from: ""
        to: "finished"
        reversible: true
        SequentialAnimation {
            PropertyAnimation {
                target: row1
                properties: "opacity"
                duration: 500
            }
            PropertyAnimation {
                target: row1
                properties: "visible"
            }
        }
    }
}

