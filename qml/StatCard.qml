import QtQuick
import QtQuick.Layouts

Rectangle {
    property string title: ""
    property var value: 0
    property string icon: ""
    property color statColor: "blue"

    color: "white"
    radius: 12
    border.color: "#E2E8F0"

    RowLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 15

        Text {
            text: icon
            font.pixelSize: 24
            color: statColor
            Layout.alignment: Qt.AlignVCenter
        }

        ColumnLayout {
            spacing: 2
            Text {
                text: title
                color: "#64748B"
                font.pixelSize: 13
                font.weight: Font.Medium
            }
            Text {
                text: value.toLocaleString()
                color: "#1E293B"
                font.pixelSize: 24
                font.weight: Font.Bold
            }
        }
    }
}
