import QtQuick
import QtQuick.Layouts
import ".."

RowLayout {
    id: root
    
    property string title: ""
    property color accentColor: Theme.primaryColor
    property bool useGradient: false
    
    spacing: Theme.spacingSmall
    
    Rectangle {
        width: 3
        height: 18
        radius: 1.5
        
        gradient: root.useGradient ? gradientObj : null
        color: root.useGradient ? "transparent" : root.accentColor
        
        Gradient {
            id: gradientObj
            GradientStop { position: 0.0; color: Theme.primaryColor }
            GradientStop { position: 1.0; color: Theme.primaryDark }
        }
    }
    
    Text {
        text: root.title
        font.pixelSize: Theme.fontSizeXLarge
        font.weight: Font.Bold
        font.family: Theme.fontFamily
        color: Theme.textPrimary
    }
}
