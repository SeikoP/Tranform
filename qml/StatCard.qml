import QtQuick
import QtQuick.Layouts
import "."

Rectangle {
    id: root
    property string title: ""
    property var value: 0
    property string icon: ""
    property color statColor: Theme.primaryColor

    color: Theme.backgroundPrimary
    radius: Theme.radiusMedium
    border.color: Theme.borderColor
    border.width: Theme.borderWidthThin
    
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
        anchors.margins: Theme.paddingMedium
        spacing: Theme.spacingSmall

        Rectangle {
            width: 28
            height: 28
            radius: Theme.radiusSmall
            color: statColor
            opacity: 0.15
            
            Text {
                anchors.centerIn: parent
                text: icon
                font.pixelSize: Theme.fontSizeXSmall
                font.weight: Font.Bold
                font.family: Theme.fontFamily
                color: statColor
            }
        }

        ColumnLayout {
            spacing: 1
            Layout.fillWidth: true
            
            Text {
                text: title
                color: Theme.textSecondary
                font.pixelSize: Theme.fontSizeXSmall
                font.family: Theme.fontFamily
            }
            Text {
                text: value.toLocaleString()
                color: Theme.textPrimary
                font.pixelSize: Theme.fontSizeLarge + 2
                font.weight: Font.Bold
                font.family: Theme.fontFamily
            }
        }
    }
}
