import QtQuick
import QtQuick.Controls

Button {
    id: control
    
    width: 36
    height: 36
    
    contentItem: Text {
        text: Theme.isDarkMode ? "☀️" : "🌙"
        font.pixelSize: 18
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }
    
    background: Rectangle {
        color: control.hovered ? Theme.backgroundHover : "transparent"
        radius: Theme.radiusMedium
        border.color: Theme.borderColor
        border.width: 1
        
        Behavior on color {
            ColorAnimation { duration: Theme.animationDuration }
        }
    }
    
    onClicked: Theme.toggleTheme()
}
