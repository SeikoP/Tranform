import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import QtQuick.Effects

Rectangle {
    id: root
    color: "transparent"
    
    // Glassmorphism background
    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            GradientStop { position: 0.0; color: "#1E293B" }
            GradientStop { position: 1.0; color: "#0F172A" }
        }
        opacity: 0.95
        border.color: "#334155"
        border.width: 1
        
        layer.enabled: true
        layer.effect: MultiEffect {
            shadowEnabled: true
            shadowColor: "#000000"
            shadowOpacity: 0.5
            shadowBlur: 30
        }
    }
    
    ImportDialog {
        id: importDialog
    }
    
    ExportDialog {
        id: exportDialog
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 15

        // Logo with gradient
        RowLayout {
            spacing: 12
            
            Rectangle {
                width: 48
                height: 48
                radius: 12
                
                gradient: Gradient {
                    GradientStop { position: 0.0; color: "#3B82F6" }
                    GradientStop { position: 1.0; color: "#8B5CF6" }
                }
                
                layer.enabled: true
                layer.effect: MultiEffect {
                    shadowEnabled: true
                    shadowColor: "#3B82F6"
                    shadowOpacity: 0.5
                    shadowBlur: 15
                }
                
                Text {
                    anchors.centerIn: parent
                    text: "T"
                    color: "white"
                    font.pixelSize: 24
                    font.weight: Font.Bold
                }
                
                SequentialAnimation on scale {
                    loops: Animation.Infinite
                    NumberAnimation { to: 1.05; duration: 2000; easing.type: Easing.InOutQuad }
                    NumberAnimation { to: 1.0; duration: 2000; easing.type: Easing.InOutQuad }
                }
            }
            
            ColumnLayout {
                spacing: 0
                Text {
                    text: "Transform 3NF"
                    color: "white"
                    font.pixelSize: 20
                    font.weight: Font.Bold
                }
                Text {
                    text: "Premium Edition"
                    color: "#60A5FA"
                    font.pixelSize: 11
                    font.weight: Font.Medium
                }
            }
        }

        Item { Layout.preferredHeight: 30 }

        Rectangle {
            Layout.fillWidth: true
            height: 1
            gradient: Gradient {
                orientation: Gradient.Horizontal
                GradientStop { position: 0.0; color: "transparent" }
                GradientStop { position: 0.5; color: "#334155" }
                GradientStop { position: 1.0; color: "transparent" }
            }
        }
        
        Text {
            text: "⚡ THAO TÁC"
            color: "#60A5FA"
            font.pixelSize: 12
            font.weight: Font.Bold
            font.letterSpacing: 1.5
        }

        Button {
            id: openBtn
            text: "📥 Import Dữ liệu"
            Layout.fillWidth: true
            Layout.preferredHeight: 50
            font.pixelSize: 15
            font.weight: Font.DemiBold
            onClicked: importDialog.open()
            
            contentItem: Text {
                text: parent.text
                color: "white"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font: parent.font
            }
            
            background: Rectangle {
                gradient: Gradient {
                    GradientStop { position: 0.0; color: openBtn.hovered ? "#2563EB" : "#3B82F6" }
                    GradientStop { position: 1.0; color: openBtn.hovered ? "#1E40AF" : "#2563EB" }
                }
                radius: 12
                
                layer.enabled: openBtn.hovered
                layer.effect: MultiEffect {
                    shadowEnabled: true
                    shadowColor: "#3B82F6"
                    shadowOpacity: 0.6
                    shadowBlur: 20
                }
                
                Behavior on scale {
                    NumberAnimation { duration: 150 }
                }
                
                scale: openBtn.pressed ? 0.95 : 1.0
            }
        }

        Button {
            id: exportBtn
            text: "📤 Export Kết Quả"
            Layout.fillWidth: true
            Layout.preferredHeight: 50
            font.pixelSize: 15
            font.weight: Font.DemiBold
            onClicked: exportDialog.open()
            
            contentItem: Text {
                text: parent.text
                color: "white"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font: parent.font
            }
            
            background: Rectangle {
                gradient: Gradient {
                    GradientStop { position: 0.0; color: exportBtn.hovered ? "#059669" : "#10B981" }
                    GradientStop { position: 1.0; color: exportBtn.hovered ? "#047857" : "#059669" }
                }
                radius: 12
                
                layer.enabled: exportBtn.hovered
                layer.effect: MultiEffect {
                    shadowEnabled: true
                    shadowColor: "#10B981"
                    shadowOpacity: 0.6
                    shadowBlur: 20
                }
                
                Behavior on scale {
                    NumberAnimation { duration: 150 }
                }
                
                scale: exportBtn.pressed ? 0.95 : 1.0
            }
        }

        Item { Layout.fillHeight: true }

        // Bottom section
        Rectangle {
            Layout.fillWidth: true
            height: 1
            gradient: Gradient {
                orientation: Gradient.Horizontal
                GradientStop { position: 0.0; color: "transparent" }
                GradientStop { position: 0.5; color: "#334155" }
                GradientStop { position: 1.0; color: "transparent" }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: 8
            
            Rectangle {
                width: 6
                height: 6
                radius: 3
                color: "#10B981"
                
                SequentialAnimation on opacity {
                    loops: Animation.Infinite
                    NumberAnimation { to: 0.3; duration: 1000 }
                    NumberAnimation { to: 1.0; duration: 1000 }
                }
            }
            
            Text {
                text: "v3.0 Premium"
                color: "#60A5FA"
                font.pixelSize: 11
                font.weight: Font.Medium
            }
        }
    }
}
