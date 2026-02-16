import QtQuick
import QtQuick.Layouts
import QtQuick.Effects

Rectangle {
    id: root
    property string title: ""
    property var value: 0
    property string icon: ""
    property color statColor: "blue"

    color: "white"
    radius: 4
    border.color: "#E0E0E0"
    border.width: 1
    
    // Hover effect
    scale: mouseArea.containsMouse ? 1.02 : 1.0
    Behavior on scale {
        NumberAnimation { duration: 150; easing.type: Easing.OutQuad }
    }
    
    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
    }

    RowLayout {
        anchors.fill: parent
        anchors.margins: 15
        spacing: 12

        Rectangle {
            width: 40
            height: 40
            radius: 4
            color: statColor
            opacity: 0.15
            
            Text {
                anchors.centerIn: parent
                text: icon
                font.pixelSize: 11
                font.weight: Font.Bold
                font.family: "Microsoft YaHei UI"
                color: statColor
            }
        }

        ColumnLayout {
            spacing: 2
            Layout.fillWidth: true
            
            Text {
                text: title
                color: "#999999"
                font.pixelSize: 11
                font.family: "Microsoft YaHei UI"
            }
            Text {
                text: value.toLocaleString()
                color: "#333333"
                font.pixelSize: 20
                font.weight: Font.Bold
                font.family: "Microsoft YaHei UI"
            }
        }
    }
}
