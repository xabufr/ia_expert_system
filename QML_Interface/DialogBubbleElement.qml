import QtQuick 1.1

Rectangle {
    id: bubble
    width: 20
    height: 20
    radius: 20
    smooth: true
    border.color: "#000000"

    MouseArea {
        id: mouseArea
        hoverEnabled: true
        anchors.fill: parent
    }
    states: [
        State {
            name: "mouseOver"
            when: mouseArea.containsMouse
            PropertyChanges {
                target: bubble
                scale: 1.1 * bubble.scale
            }
        }
    ]
    transitions: Transition {
        from: ""
        to: "mouseOver"
        reversible: true
        PropertyAnimation {
            target: bubble
            properties: "scale"
            duration: 150
        }
    }
}
