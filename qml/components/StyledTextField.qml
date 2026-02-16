import QtQuick
import QtQuick.Controls
import ".."

TextField {
    id: control
    
    font.pixelSize: Theme.fontSizeMedium
    font.family: Theme.fontFamily
    color: Theme.textPrimary
    
    background: Rectangle {
        radius: Theme.radiusMedium
        color: Theme.backgroundPrimary
        border.color: control.activeFocus ? Theme.primaryColor : Theme.borderColor
        border.width: 1
        
        Behavior on border.color {
            ColorAnimation { duration: Theme.animationDuration }
        }
    }
}
