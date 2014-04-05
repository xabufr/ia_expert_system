import QtQuick 1.1

Rectangle {
    id: thinkDialog
    width: 100
    height: 62
    radius: 20
    border.width: 1
    border.color: "#000000"

    property alias text: textElement.text

    Text {
        id: textElement
        x: 38
        y: 28
        width: 84
        height: 47
        text: "content"
        smooth: true
        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignHCenter
        wrapMode: Text.WordWrap
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        font.pixelSize: 12
    }


    DialogBubbleElement {
        id: bubble_1
        x: 93
        y: 63
        anchors.right: parent.right
        anchors.rightMargin: -12
        anchors.bottom: parent.bottom
        anchors.bottomMargin: -20
    }

    DialogBubbleElement {
        id: bubble_2
        x: 105
        y: 78
        anchors.right: parent.right
        anchors.rightMargin: -24
        anchors.bottom: parent.bottom
        anchors.bottomMargin: -35
        opacity: 0.75
        scale: 0.75
    }

    DialogBubbleElement {
        id: bubble_3
        x: 114
        y: 91
        anchors.right: parent.right
        anchors.rightMargin: -33
        anchors.bottom: parent.bottom
        anchors.bottomMargin: -48
        opacity: 0.5
        scale: 0.5
    }

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
                target: thinkDialog
                color: "#e0e08d"
            }

        }
    ]

    transitions: Transition {
        from: ""
        to: "mouseOver"
        reversible: true
        PropertyAnimation {
            target: thinkDialog
            properties: "color"
            duration: 250
        }

    }

}
