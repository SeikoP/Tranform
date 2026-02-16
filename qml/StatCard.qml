import QtQuick
import QtQuick.Layouts

Rectangle {
    id: root
    property string title: ""
    property var value: 0
    property string icon: ""
    property color statColor: Theme.primaryColor

    color: Theme.backgroundPrimary
    radius: Theme.radiusMedium
    border.color: Theme.borderColor
    border.width: 1
    
    Behavior on color {
        ColorAnimation { duration: Theme.animationDuration }
    }
    
    scale: mouseArea.containsMouse ? 1.02 : 1.0
    Behavior on scale {
        NumberAnimation { duration: Theme.animationDuration }
    }
    
    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
    }

    RowLayout {
        anchors.fill: parent
        anchors.margins: 12
        spacing: 10

        Rectangle {
            width: 36
            height: 36
            radius: Theme.radiusMedium
            color: statColor
            opacity: 0.15
            
            Text {
                anchors.centerIn: parent
                text: icon
                font.pixelSize: Theme.fontSizeSmall
                font.weight: Font.Bold
                font.family: Theme.fontFamily
                color: statColor
            }
        }

        ColumnLayout {
            spacing: 2
            Layout.fillWidth: true
            
            Text {
                text: title
                color: Theme.textSecondary
                font.pixelSize: Theme.fontSizeSmall
                font.family: Theme.fontFamily
            }
            Text {
                text: value.toLocaleString()
                color: Theme.textPrimary
                font.pixelSize: 18
                font.weight: Font.Bold
                font.family: Theme.fontFamily
            }
        }
    }
}
