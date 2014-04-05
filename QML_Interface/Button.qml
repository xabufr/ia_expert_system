import QtQuick 1.1

Rectangle {
    id: button
    width: 100
    height: 62
    color: "#ec0000"
    radius: 20
    smooth: true
    property color mouseOverColor: "#ff0000"
    property string text: "Button !"
    property bool clickAllowed: true

    signal clicked

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
        onClicked: {
            if(clickAllowed)
                button.clicked()
        }
    }
    Text {
        id: textElement
        text: button.text
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
    }
    states: [
        State {
            name: "mouseOver"
            when: mouseArea.containsMouse == true
            PropertyChanges {
                target: button
                color: mouseOverColor
            }
        }
    ]
    transitions: Transition {
        from: ""
        to: "mouseOver"
        reversible: true
        PropertyAnimation {
            target: button
            properties: "color"
            duration: 250
        }
    }
}
