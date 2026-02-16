import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Window
import QtQuick.Effects

ApplicationWindow {
    visible: true
    width: 1400
    height: 900
    title: "Transform 3NF - Premium Edition"
    color: "#0A0E1A"
    
    // Animated gradient background
    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            GradientStop { position: 0.0; color: "#0A0E1A" }
            GradientStop { position: 0.5; color: "#0F172A" }
            GradientStop { position: 1.0; color: "#1E293B" }
        }
        
        // Animated orbs
        Repeater {
            model: 3
            Rectangle {
                width: 300 + index * 100
                height: width
                radius: width / 2
                opacity: 0.03
                gradient: Gradient {
                    GradientStop { position: 0.0; color: "#3B82F6" }
                    GradientStop { position: 1.0; color: "#8B5CF6" }
                }
                x: parent.width * (0.2 + index * 0.3)
                y: parent.height * (0.3 + index * 0.2)
                
                SequentialAnimation on y {
                    loops: Animation.Infinite
                    NumberAnimation { 
                        to: parent.height * (0.3 + index * 0.2) + 50
                        duration: 3000 + index * 1000
                        easing.type: Easing.InOutQuad
                    }
                    NumberAnimation { 
                        to: parent.height * (0.3 + index * 0.2)
                        duration: 3000 + index * 1000
                        easing.type: Easing.InOutQuad
                    }
                }
            }
        }
    }

    RowLayout {
        anchors.fill: parent
        spacing: 0

        // Sidebar component
        Sidebar {
            id: sidebar
            Layout.fillHeight: true
            Layout.preferredWidth: 260
        }

        // Main Content Area
        ColumnLayout {
            Layout.fillHeight: true
            Layout.fillWidth: true
            spacing: 0

            // Header / Navigation Tabs area
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 70
                color: "transparent"
                
                Rectangle {
                    anchors.fill: parent
                    anchors.margins: 15
                    anchors.bottomMargin: 0
                    color: "#1E293B"
                    opacity: 0.6
                    radius: 16
                    border.color: "#334155"
                    border.width: 1
                    
                    layer.enabled: true
                    layer.effect: MultiEffect {
                        shadowEnabled: true
                        shadowColor: "#000000"
                        shadowOpacity: 0.3
                        shadowBlur: 20
                    }
                }
                
                TabBar {
                    id: mainTabs
                    anchors.fill: parent
                    anchors.margins: 15
                    anchors.bottomMargin: 0
                    background: Rectangle { color: "transparent" }
                    
                    TabButton { 
                        text: "📊 Dữ liệu Gốc"
                        font.pixelSize: 15
                        font.weight: Font.DemiBold
                        
                        contentItem: Text {
                            text: parent.text
                            font: parent.font
                            color: parent.checked ? "#60A5FA" : "#94A3B8"
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                            
                            Behavior on color {
                                ColorAnimation { duration: 200 }
                            }
                        }
                        
                        background: Rectangle {
                            color: parent.checked ? "#1E40AF" : "transparent"
                            radius: 12
                            opacity: parent.checked ? 0.3 : (parent.hovered ? 0.1 : 0)
                            
                            Behavior on opacity {
                                NumberAnimation { duration: 200 }
                            }
                        }
                    }
                    
                    TabButton { 
                        text: "🎯 Mô hình ERD (3NF)"
                        font.pixelSize: 15
                        font.weight: Font.DemiBold
                        
                        contentItem: Text {
                            text: parent.text
                            font: parent.font
                            color: parent.checked ? "#60A5FA" : "#94A3B8"
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                            
                            Behavior on color {
                                ColorAnimation { duration: 200 }
                            }
                        }
                        
                        background: Rectangle {
                            color: parent.checked ? "#1E40AF" : "transparent"
                            radius: 12
                            opacity: parent.checked ? 0.3 : (parent.hovered ? 0.1 : 0)
                            
                            Behavior on opacity {
                                NumberAnimation { duration: 200 }
                            }
                        }
                    }
                }
            }

            StackLayout {
                id: contentStack
                currentIndex: mainTabs.currentIndex
                Layout.fillWidth: true
                Layout.fillHeight: true

                DataPreview {
                    // Component for data preview
                }

                ErdTab {
                    // Component for ERD
                }
            }

            // Status Bar
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 45
                color: "#0F172A"
                opacity: 0.8
                
                Rectangle {
                    anchors.top: parent.top
                    width: parent.width
                    height: 1
                    gradient: Gradient {
                        orientation: Gradient.Horizontal
                        GradientStop { position: 0.0; color: "transparent" }
                        GradientStop { position: 0.5; color: "#334155" }
                        GradientStop { position: 1.0; color: "transparent" }
                    }
                }
                
                RowLayout {
                    anchors.fill: parent
                    anchors.leftMargin: 20
                    anchors.rightMargin: 20
                    spacing: 15
                    
                    Rectangle {
                        width: 8
                        height: 8
                        radius: 4
                        color: statusText.color
                        
                        SequentialAnimation on opacity {
                            loops: Animation.Infinite
                            NumberAnimation { to: 0.3; duration: 800 }
                            NumberAnimation { to: 1.0; duration: 800 }
                        }
                    }
                    
                    Text {
                        id: statusText
                        text: "⚡ Sẵn sàng"
                        font.pixelSize: 13
                        font.weight: Font.Medium
                        color: "#10B981"
                        
                        Behavior on color {
                            ColorAnimation { duration: 300 }
                        }
                    }
                    
                    Item { Layout.fillWidth: true }
                    
                    Text {
                        text: "✨ Premium Edition v3.0"
                        font.pixelSize: 11
                        color: "#60A5FA"
                        font.weight: Font.Medium
                    }
                }
                
                Connections {
                    target: bridge
                    function onStatusChanged(message, color) {
                        statusText.text = "⚡ " + message
                        if (color === "red") statusText.color = "#EF4444"
                        else if (color === "green") statusText.color = "#10B981"
                        else statusText.color = "#60A5FA"
                    }
                }
            }
        }
    }
}
