import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Effects
import ".."

Item {
    id: root
    
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 30
        spacing: 20
        
        // Header
        RowLayout {
            Layout.fillWidth: true
            spacing: 15
            
            Text {
                text: "📋 Transformation Rules"
                font.pixelSize: 20
                font.weight: Font.Bold
                color: Theme.darkMode ? "white" : Theme.textPrimary
            }
            
            Item { Layout.fillWidth: true }
            
            Button {
                text: "+ Thêm Rule"
                font.pixelSize: 13
                font.weight: Font.DemiBold
                
                onClicked: addRuleDialog.open()
                
                background: Rectangle {
                    gradient: Gradient {
                        GradientStop { position: 0.0; color: parent.hovered ? Theme.primaryDark : Theme.primaryColor }
                        GradientStop { position: 1.0; color: parent.hovered ? Theme.primaryDark : Theme.primaryLight }
                    }
                    radius: 10
                }
                
                contentItem: Text {
                    text: parent.text
                    color: "white"
                    font: parent.font
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
            }
        }
        
        // Rules List
        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            
            ColumnLayout {
                width: parent.width
                spacing: 15
                
                Repeater {
                    model: bridge ? bridge.transformRules : []
                    
                    delegate: Rectangle {
                        Layout.fillWidth: true
                        height: 80
                        color: Theme.darkMode ? "#1E293B" : Theme.surfaceColor
                        opacity: 0.9
                        radius: 12
                        border.color: Theme.borderColor
                        border.width: 1
                        
                        RowLayout {
                            anchors.fill: parent
                            anchors.margins: 20
                            spacing: 15
                            
                            Rectangle {
                                width: 50
                                height: 50
                                radius: 10
                                color: getRuleColor(modelData.type)
                                opacity: 0.2
                                
                                Text {
                                    anchors.centerIn: parent
                                    text: getRuleIcon(modelData.type)
                                    font.pixelSize: 24
                                }
                            }
                            
                            ColumnLayout {
                                Layout.fillWidth: true
                                spacing: 5
                                
                                Text {
                                    text: modelData.name
                                    font.pixelSize: 15
                                    font.weight: Font.Bold
                                    color: Theme.darkMode ? "white" : Theme.textPrimary
                                }
                                
                                Text {
                                    text: getRuleDescription(modelData.type)
                                    font.pixelSize: 12
                                    color: Theme.textSecondary
                                }
                            }
                            
                            Switch {
                                checked: modelData.enabled
                                // TODO: Add toggle handler
                            }
                            
                            Button {
                                text: "🗑️"
                                width: 40
                                height: 40
                                font.pixelSize: 16
                                
                                onClicked: bridge.remove_transform_rule(modelData.name)
                                
                                background: Rectangle {
                                    color: parent.hovered ? Theme.errorColor : Theme.errorColor
                                    radius: 8
                                    opacity: parent.hovered ? 1.0 : 0.8
                                }
                                
                                contentItem: Text {
                                    text: parent.text
                                    color: "white"
                                    font: parent.font
                                    horizontalAlignment: Text.AlignHCenter
                                    verticalAlignment: Text.AlignVCenter
                                }
                            }
                        }
                    }
                }
                
                // Empty state
                Item {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 200
                    visible: bridge && bridge.transformRules.length === 0
                    
                    ColumnLayout {
                        anchors.centerIn: parent
                        spacing: 15
                        
                        Text {
                            text: "📋"
                            font.pixelSize: 48
                            Layout.alignment: Qt.AlignHCenter
                        }
                        
                        Text {
                            text: "Chưa có transformation rules"
                            font.pixelSize: 16
                            color: "#64748B"
                            Layout.alignment: Qt.AlignHCenter
                        }
                        
                        Text {
                            text: "Click '+ Thêm Rule' để bắt đầu"
                            font.pixelSize: 13
                            color: "#475569"
                            Layout.alignment: Qt.AlignHCenter
                        }
                    }
                }
            }
        }
    }
    
    // Add Rule Dialog
    Dialog {
        id: addRuleDialog
        title: "Thêm Transformation Rule"
        width: 500
        height: 400
        modal: true
        anchors.centerIn: parent
        
        background: Rectangle {
            color: Theme.darkMode ? "#1E293B" : Theme.surfaceColor
            radius: 16
            border.color: Theme.primaryColor
            border.width: 2
        }
        
        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 20
            spacing: 15
            
            Text {
                text: "Loại transformation:"
                font.pixelSize: 13
                color: "#E2E8F0"
            }
            
            ComboBox {
                id: ruleTypeCombo
                Layout.fillWidth: true
                model: [
                    "remove_duplicates",
                    "fill_missing",
                    "drop_missing",
                    "convert_type",
                    "trim_strings",
                    "normalize_text",
                    "filter_rows"
                ]
                
                background: Rectangle {
                    color: "#0F172A"
                    radius: 8
                    border.color: parent.activeFocus ? "#3B82F6" : "#334155"
                }
                
                contentItem: Text {
                    text: parent.displayText
                    color: "#E2E8F0"
                    font.pixelSize: 13
                    verticalAlignment: Text.AlignVCenter
                    leftPadding: 10
                }
            }
            
            Text {
                text: "Tên rule:"
                font.pixelSize: 13
                color: "#E2E8F0"
            }
            
            TextField {
                id: ruleNameField
                Layout.fillWidth: true
                placeholderText: "VD: remove_duplicates_1"
                font.pixelSize: 13
                color: "white"
                
                background: Rectangle {
                    color: "#0F172A"
                    radius: 8
                    border.color: parent.activeFocus ? "#3B82F6" : "#334155"
                }
            }
            
            Item { Layout.fillHeight: true }
            
            RowLayout {
                Layout.fillWidth: true
                spacing: 10
                
                Button {
                    text: "Hủy"
                    Layout.preferredWidth: 100
                    onClicked: addRuleDialog.close()
                    
                    background: Rectangle {
                        color: parent.hovered ? "#475569" : "#334155"
                        radius: 8
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        color: "#E2E8F0"
                        font.pixelSize: 13
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                }
                
                Item { Layout.fillWidth: true }
                
                Button {
                    text: "Thêm"
                    Layout.preferredWidth: 100
                    
                    onClicked: {
                        if (ruleNameField.text) {
                            var config = JSON.stringify({})
                            bridge.add_transform_rule(ruleNameField.text, ruleTypeCombo.currentText, config)
                            ruleNameField.text = ""
                            addRuleDialog.close()
                        }
                    }
                    
                    background: Rectangle {
                        gradient: Gradient {
                            GradientStop { position: 0.0; color: parent.hovered ? "#2563EB" : "#3B82F6" }
                            GradientStop { position: 1.0; color: parent.hovered ? "#1E40AF" : "#2563EB" }
                        }
                        radius: 8
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        color: "white"
                        font.pixelSize: 13
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                }
            }
        }
    }
    
    function getRuleIcon(type) {
        switch(type) {
            case "remove_duplicates": return "🔄"
            case "fill_missing": return "📝"
            case "drop_missing": return "🗑️"
            case "convert_type": return "🔧"
            case "trim_strings": return "✂️"
            case "normalize_text": return "📄"
            case "filter_rows": return "🔍"
            default: return "⚙️"
        }
    }
    
    function getRuleColor(type) {
        switch(type) {
            case "remove_duplicates": return "#3B82F6"
            case "fill_missing": return "#10B981"
            case "drop_missing": return "#EF4444"
            case "convert_type": return "#F59E0B"
            case "trim_strings": return "#8B5CF6"
            case "normalize_text": return "#06B6D4"
            case "filter_rows": return "#EC4899"
            default: return "#64748B"
        }
    }
    
    function getRuleDescription(type) {
        switch(type) {
            case "remove_duplicates": return "Loại bỏ các dòng trùng lặp"
            case "fill_missing": return "Điền giá trị thiếu"
            case "drop_missing": return "Xóa dòng có giá trị thiếu"
            case "convert_type": return "Chuyển đổi kiểu dữ liệu"
            case "trim_strings": return "Loại bỏ khoảng trắng"
            case "normalize_text": return "Chuẩn hóa text"
            case "filter_rows": return "Lọc dòng theo điều kiện"
            default: return "Transformation rule"
        }
    }
}
