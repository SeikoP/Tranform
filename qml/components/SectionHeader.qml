import QtQuick
import QtQuick.Layouts

RowLayout {
    id: root
    
    property string title: ""
    property color accentColor: Theme.primaryColor
    
    spacing: Theme.spacingSmall
    
    Rectangle {
        width: 3
        height: 18
        radius: 1.5
        color: root.accentColor
    }
    
    Text {
        text: root.title
        font.pixelSize: Theme.fontSizeXLarge
        font.weight: Font.Bold
        font.family: Theme.fontFamily
        color: Theme.textPrimary
    }
}
