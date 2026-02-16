import QtQuick
import QtQuick.Layouts

Rectangle {
    id: root
    
    property string title: ""
    property string message: ""
    
    width: 140
    height: 40
    radius: Theme.radiusMedium
    color: Theme.backgroundSecondary
    border.color: Theme.borderColor
    border.width: 1
    
    ColumnLayout {
        anchors.centerIn: parent
        spacing: Theme.spacingTiny
        
        Text {
            text: root.title
            font.pixelSize: Theme.fontSizeSmall
            font.weight: Font.Bold
            font.family: Theme.fontFamily
            color: Theme.primaryColor
            Layout.alignment: Qt.AlignHCenter
        }
        
        Text {
            text: root.message
            font.pixelSize: Theme.fontSizeXSmall
            font.family: Theme.fontFamily
            color: Theme.textSecondary
            Layout.alignment: Qt.AlignHCenter
        }
    }
}
