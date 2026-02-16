import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import QtQuick.Effects

Dialog {
    id: exportDialog
    title: "📤 Export Dữ liệu"
    width: 600
    height: 550
    modal: true
    anchors.centerIn: parent
    
    background: Rectangle {
        color: "#1E293B"
        radius: 16
        border.color: "#10B981"
        border.width: 2
        
        layer.enabled: true
        layer.effect: MultiEffect {
            shadowEnabled: true
            shadowColor: "#10B981"
            shadowOpacity: 0.4
            shadowBlur: 30
        }
    }
    
    FolderDialog {
        id: folderDialog
        onAccepted: {
            var folder = selectedFolder.toString()
            var filename = filenameField.text || "export"
            
            if (exportTypeCombo.currentIndex === 0) {
                bridge.export_csv(folder, filename)
            } else if (exportTypeCombo.currentIndex === 1) {
                bridge.export_excel(folder, filename)
            } else if (exportTypeCombo.currentIndex === 2) {
                bridge.export_json(folder, filename)
            } else if (exportTypeCombo.currentIndex === 3) {
                bridge.export_sql_script(folder, filename)
            } else if (exportTypeCombo.currentIndex === 4) {
                bridge.export_sqlite(folder, filename)
            }
            
            exportDialog.close()
        }
    }
    
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 25
        spacing: 20
        
        // Header
        RowLayout {
            spacing: 15
            
            Rectangle {
                width: 50
                height: 50
                radius: 12
                gradient: Gradient {
                    GradientStop { position: 0.0; color: "#10B981" }
                    GradientStop { position: 1.0; color: "#059669" }
                }
                
                Text {
                    anchors.centerIn: parent
                    text: "📤"
                    font.pixelSize: 24
                }
            }
            
            ColumnLayout {
                spacing: 2
                Text {
                    text: "Export Dữ liệu"
                    font.pixelSize: 22
                    font.weight: Font.Bold
                    color: "white"
                }
                Text {
                    text: "Xuất dữ liệu đã chuẩn hóa"
                    font.pixelSize: 13
                    color: "#94A3B8"
                }
            }
        }
        
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
        
        // Export Type Selection
        ColumnLayout {
            spacing: 10
            
            Text {
                text: "Định dạng xuất:"
                font.pixelSize: 14
                font.weight: Font.Medium
                color: "#E2E8F0"
            }
            
            ComboBox {
                id: exportTypeCombo
                Layout.fillWidth: true
                Layout.preferredHeight: 50
                model: [
                    "📄 CSV Files (nhiều file)",
                    "📊 Excel File (nhiều sheet)",
                    "📋 JSON Files (nhiều file)",
                    "📜 SQL Script",
                    "🗄️ SQLite Database"
                ]
                font.pixelSize: 14
                
                background: Rectangle {
                    color: "#0F172A"
                    radius: 12
                    border.color: exportTypeCombo.activeFocus ? "#10B981" : "#334155"
                    border.width: 2
                }
                
                contentItem: Text {
                    text: exportTypeCombo.displayText
                    color: "#E2E8F0"
                    font: exportTypeCombo.font
                    verticalAlignment: Text.AlignVCenter
                    leftPadding: 15
                }
            }
        }
        
        // Filename input
        ColumnLayout {
            spacing: 10
            
            Text {
                text: "Tên file/database:"
                font.pixelSize: 14
                font.weight: Font.Medium
                color: "#E2E8F0"
            }
            
            TextField {
                id: filenameField
                Layout.fillWidth: true
                Layout.preferredHeight: 50
                placeholderText: "VD: normalized_data"
                text: "normalized_data"
                font.pixelSize: 14
                color: "white"
                
                background: Rectangle {
                    color: "#0F172A"
                    radius: 12
                    border.color: parent.activeFocus ? "#10B981" : "#334155"
                    border.width: 2
                }
            }
        }
        
        // Export info
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 120
            color: "#0F172A"
            opacity: 0.6
            radius: 12
            border.color: "#334155"
            
            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 20
                spacing: 10
                
                RowLayout {
                    spacing: 10
                    Text {
                        text: "ℹ️"
                        font.pixelSize: 20
                    }
                    Text {
                        text: "Thông tin xuất"
                        font.pixelSize: 15
                        font.weight: Font.Bold
                        color: "#60A5FA"
                    }
                }
                
                Text {
                    text: getExportInfo()
                    font.pixelSize: 13
                    color: "#CBD5E1"
                    Layout.fillWidth: true
                    wrapMode: Text.WordWrap
                    lineHeight: 1.3
                }
            }
        }
        
        Item { Layout.fillHeight: true }
        
        // Action buttons
        RowLayout {
            Layout.fillWidth: true
            spacing: 15
            
            Button {
                text: "Hủy"
                Layout.preferredWidth: 120
                Layout.preferredHeight: 50
                onClicked: exportDialog.close()
                
                background: Rectangle {
                    color: parent.hovered ? "#475569" : "#334155"
                    radius: 12
                }
                
                contentItem: Text {
                    text: parent.text
                    color: "#E2E8F0"
                    font.pixelSize: 14
                    font.weight: Font.Medium
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
            }
            
            Item { Layout.fillWidth: true }
            
            Button {
                text: "📤 Xuất Dữ liệu"
                Layout.preferredWidth: 180
                Layout.preferredHeight: 50
                onClicked: folderDialog.open()
                
                background: Rectangle {
                    gradient: Gradient {
                        GradientStop { position: 0.0; color: parent.hovered ? "#059669" : "#10B981" }
                        GradientStop { position: 1.0; color: parent.hovered ? "#047857" : "#059669" }
                    }
                    radius: 12
                    
                    layer.enabled: parent.hovered
                    layer.effect: MultiEffect {
                        shadowEnabled: true
                        shadowColor: "#10B981"
                        shadowOpacity: 0.6
                        shadowBlur: 20
                    }
                }
                
                contentItem: Text {
                    text: parent.text
                    color: "white"
                    font.pixelSize: 15
                    font.weight: Font.Bold
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
            }
        }
    }
    
    function getExportInfo() {
        switch(exportTypeCombo.currentIndex) {
            case 0:
                return "Mỗi bảng sẽ được xuất thành một file CSV riêng biệt. Phù hợp để import vào các hệ thống khác."
            case 1:
                return "Tất cả các bảng sẽ được xuất vào một file Excel với nhiều sheet. Dễ dàng xem và chỉnh sửa."
            case 2:
                return "Mỗi bảng sẽ được xuất thành một file JSON riêng. Phù hợp cho API và web applications."
            case 3:
                return "Tạo SQL script với CREATE TABLE và INSERT statements. Có thể chạy trên bất kỳ SQL database nào."
            case 4:
                return "Tạo SQLite database file với tất cả các bảng. Có thể query trực tiếp hoặc import vào hệ thống khác."
            default:
                return ""
        }
    }
}
