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

    FileDialog {
        id: csvDialog
        title: "Chọn file CSV"
        nameFilters: ["CSV files (*.csv)"]
        onAccepted: {
            bridge.load_csv(selectedFile)
        }
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 15

        // Logo
        RowLayout {
            spacing: 10
            Rectangle {
                width: 30; height: 30
                radius: 6
                color: "#3B82F6"
                Text {
                    anchors.centerIn: parent
                    text: "T"
                    color: "white"
                    font.bold: true
                }
            }
            Text {
                text: "Tranform 3NF"
                color: "white"
                font.pixelSize: 20
                font.weight: Font.Bold
            }
        }

        Item { Layout.preferredHeight: 30 }

        Text {
            text: "THAO TÁC"
            color: "#64748B"
            font.pixelSize: 11
            font.weight: Font.DemiBold
            font.letterSpacing: 1.2
        }

        Button {
            text: "📂 Mở File CSV"
            Layout.fillWidth: true
            font.pixelSize: 14
            onClicked: csvDialog.open()
            
            contentItem: Text {
                text: parent.text
                color: "white"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font: parent.font
            }
            background: Rectangle {
                color: parent.hovered ? "#2563EB" : "#3B82F6"
                radius: 8
            }
        }

        Button {
            text: "💾 Xuất Kết Quả"
            Layout.fillWidth: true
            font.pixelSize: 14
            
            contentItem: Text {
                text: parent.text
                color: "white"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font: parent.font
            }
            background: Rectangle {
                color: parent.hovered ? "#059669" : "#10B981"
                radius: 8
            }
        }

        Item { Layout.fillHeight: true }

        // Bottom section
        Rectangle {
            Layout.fillWidth: true
            height: 1
            color: "#334155"
        }

        Text {
            text: "v2.0.0 Premium"
            color: "#64748B"
            font.pixelSize: 10
            font.italic: true
        }
    }
}
