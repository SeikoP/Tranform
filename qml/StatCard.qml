import QtQuick
import QtQuick.Layouts
import QtQuick.Effects

Rectangle {
    id: root
    property string title: ""
    property var value: 0
    property string icon: ""
    property color statColor: "blue"

    color: "#1E293B"
    opacity: 0.9
    radius: 16
    border.color: Qt.lighter(statColor, 1.3)
    border.width: 1
    
    layer.enabled: true
    layer.effect: MultiEffect {
        shadowEnabled: true
        shadowColor: statColor
        shadowOpacity: 0.3
        shadowBlur: 15
    }
    
    // Gradient overlay
    Rectangle {
        anchors.fill: parent
        radius: parent.radius
        opacity: 0.1
        gradient: Gradient {
            GradientStop { position: 0.0; color: statColor }
            GradientStop { position: 1.0; color: "transparent" }
        }
    }
    
    // Hover effect
    scale: mouseArea.containsMouse ? 1.03 : 1.0
    Behavior on scale {
        NumberAnimation { duration: 200; easing.type: Easing.OutQuad }
    }
    
    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
    }

    RowLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 15

        Rectangle {
            width: 50
            height: 50
            radius: 12
            color: statColor
            opacity: 0.2
            
            Text {
                anchors.centerIn: parent
                text: icon
                font.pixelSize: 28
                
                SequentialAnimation on scale {
                    loops: Animation.Infinite
                    NumberAnimation { to: 1.1; duration: 1500; easing.type: Easing.InOutQuad }
                    NumberAnimation { to: 1.0; duration: 1500; easing.type: Easing.InOutQuad }
                }
            }
        }

        ColumnLayout {
            spacing: 4
            Layout.fillWidth: true
            
            Text {
                text: title
                color: "#94A3B8"
                font.pixelSize: 13
                font.weight: Font.Medium
                font.letterSpacing: 0.5
            }
            Text {
                text: value.toLocaleString()
                color: "white"
                font.pixelSize: 28
                font.weight: Font.Bold
            }
        }
    }
}
