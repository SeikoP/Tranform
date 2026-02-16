import QtQuick
import QtQuick.Controls

Button {
    id: control
    
    property color buttonColor: Theme.primaryColor
    property color buttonHoverColor: Theme.primaryDark
    property string variant: "primary" // "primary", "accent", "success", "outlined"
    
    font.pixelSize: Theme.fontSizeMedium
    font.family: Theme.fontFamily
    
    // Set colors based on variant
    Component.onCompleted: {
        if (variant === "accent") {
            buttonColor = Theme.accentColor
            buttonHoverColor = Theme.accentDark
        } else if (variant === "success") {
            buttonColor = Theme.successColor
            buttonHoverColor = "#00A344"
        } else if (variant === "outlined") {
            buttonColor = "transparent"
            buttonHoverColor = Theme.backgroundHover
        }
    }
    
    contentItem: Text {
        text: control.text
        color: variant === "outlined" ? Theme.primaryColor : Theme.textOnPrimary
        font: control.font
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }
    
    background: Rectangle {
        color: control.hovered ? control.buttonHoverColor : control.buttonColor
        radius: Theme.radiusMedium
        border.color: variant === "outlined" ? Theme.primaryColor : "transparent"
        border.width: variant === "outlined" ? 2 : 0
        
        Behavior on color {
            ColorAnimation { duration: Theme.animationDuration }
        }
        
        Behavior on border.color {
            ColorAnimation { duration: Theme.animationDuration }
        }
    }
}
