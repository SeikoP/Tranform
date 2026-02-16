import QtQuick
import QtQuick.Controls
import ".."

Item {
    id: root
    
    property bool running: false
    property string message: "Đang tải..."
    property int size: 48
    
    width: size
    height: size + 30
    
    visible: running
    
    Rectangle {
        anchors.fill: parent
        color: Theme.backgroundPrimary
        opacity: 0.95
        radius: Theme.radiusMedium
        border.color: Theme.borderColor
        border.width: 1
    }
    
    BusyIndicator {
        id: spinner
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 5
        width: root.size
        height: root.size
        running: root.running
        
        contentItem: Item {
            implicitWidth: root.size
            implicitHeight: root.size
            
            Rectangle {
                id: circle
                width: root.size
                height: root.size
                radius: root.size / 2
                color: "transparent"
                border.color: Theme.primaryColor
                border.width: 3
                
                Rectangle {
                    width: 8
                    height: 8
                    radius: 4
                    color: Theme.primaryColor
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.top: parent.top
                    anchors.topMargin: 3
                    
                    // Glow effect
                    layer.enabled: true
                    layer.effect: MultiEffect {
                        shadowEnabled: true
                        shadowColor: Theme.primaryColor
                        shadowOpacity: 0.8
                        shadowBlur: 10
                    }
                }
                
                RotationAnimation on rotation {
                    running: root.running
                    loops: Animation.Infinite
                    from: 0
                    to: 360
                    duration: 1000
                    easing.type: Easing.Linear
                }
            }
        }
    }
    
    Text {
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 5
        text: root.message
        font.pixelSize: Theme.fontSizeSmall
        font.family: Theme.fontFamily
        color: Theme.textSecondary
    }
}
