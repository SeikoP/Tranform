import QtQuick
import QtQuick.Controls

Button {
    id: control
    
    property color buttonColor: Theme.primaryColor
    property color buttonHoverColor: Theme.primaryDark
    
    font.pixelSize: Theme.fontSizeMedium
    font.family: Theme.fontFamily
    
    contentItem: Text {
        text: control.text
        color: Theme.textOnPrimary
        font: control.font
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }
    
    background: Rectangle {
        color: control.hovered ? control.buttonHoverColor : control.buttonColor
        radius: Theme.radiusMedium
        
        Behavior on color {
            ColorAnimation { duration: Theme.animationDuration }
        }
    }
}
