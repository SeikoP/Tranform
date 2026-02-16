import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Effects
import "components"

Item {
    id: root
    
    opacity: 0
    Component.onCompleted: fadeIn.start()
    
    NumberAnimation on opacity {
        id: fadeIn
        to: 1.0
        duration: 600
        easing.type: Easing.OutQuad
    }
    
    RowLayout {
        anchors.fill: parent
        spacing: 0
        
        // Left Panel - Pipeline Management
        Rectangle {
            Layout.fillHeight: true
            Layout.preferredWidth: 360
            color: "#1E293B"
            opacity: 0.95
            border.color: "#334155"
            border.width: 1
            
            layer.enabled: true
            layer.effect: MultiEffect {
                shadowEnabled: true
                shadowColor: "#000000"
                shadowOpacity: 0.4
                shadowBlur: 20
            }
            
            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 25
                spacing: 15
                
                // Header
                RowLayout {
                    spacing: 10
                    
                    Rectangle {
                        width: 4
                        height: 28
                        radius: 2
                        gradient: Gradient {
                            GradientStop { position: 0.0; color: "#10B981" }
                            GradientStop { position: 1.0; color: "#059669" }
                        }
                    }
                    
                    Text {
                        text: "ETL Pipeline"
                        font.pixelSize: 22
                        font.weight: Font.Bold
                        font.family: "Segoe UI"
                        color: "white"
                    }
                }
                
                Text {
                    text: "Extract → Transform → Load"
                    font.pixelSize: 13
                    color: "#94A3B8"
                    Layout.fillWidth: true
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
                
                // Pipeline Selection
                Text {
                    text: "Pipeline hiện tại:"
                    font.pixelSize: 13
                    font.weight: Font.Medium
                    color: "#E2E8F0"
                }
                
                ComboBox {
                    id: pipelineSelector
                    Layout.fillWidth: true
                    Layout.preferredHeight: 45
                    model: bridge ? bridge.pipelineNames : []
                    font.pixelSize: 13
                    
                    onCurrentTextChanged: {
                        if (currentText) {
                            bridge.load_pipeline(currentText)
                        }
                    }
                    
                    background: Rectangle {
                        color: "#0F172A"
                        radius: 10
                        border.color: parent.activeFocus ? "#10B981" : "#334155"
                        border.width: 2
                    }
                    
                    contentItem: Text {
                        text: parent.displayText || "Chọn pipeline..."
                        color: "#E2E8F0"
                        font: parent.font
                        verticalAlignment: Text.AlignVCenter
                        leftPadding: 12
                    }
                }
                
                // Create New Pipeline
                RowLayout {
                    Layout.fillWidth: true
                    spacing: 10
                    
                    TextField {
                        id: newPipelineField
                        Layout.fillWidth: true
                        Layout.preferredHeight: 45
                        placeholderText: "Tên pipeline mới..."
                        font.pixelSize: 13
                        color: "white"
                        
                        background: Rectangle {
                            color: "#0F172A"
                            radius: 10
                            border.color: parent.activeFocus ? "#10B981" : "#334155"
                            border.width: 1
                        }
                    }
                    
                    Button {
                        text: "+"
                        Layout.preferredWidth: 45
                        Layout.preferredHeight: 45
                        font.pixelSize: 18
                        font.weight: Font.Bold
                        
                        onClicked: {
                            if (newPipelineField.text) {
                                bridge.create_pipeline(newPipelineField.text)
                                newPipelineField.text = ""
                            }
                        }
                        
                        background: Rectangle {
                            gradient: Gradient {
                                GradientStop { position: 0.0; color: parent.hovered ? "#059669" : "#10B981" }
                                GradientStop { position: 1.0; color: parent.hovered ? "#047857" : "#059669" }
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
                
                Rectangle {
                    Layout.fillWidth: true
                    height: 1
                    color: "#334155"
                }
                
                // Action Buttons
                Text {
                    text: "THAO TÁC"
                    font.pixelSize: 11
                    font.weight: Font.Bold
                    font.family: "Segoe UI"
                    color: "#60A5FA"
                    font.letterSpacing: 1.5
                }
                
                Button {
                    text: "Phân tích Chất lượng"
                    Layout.fillWidth: true
                    Layout.preferredHeight: 45
                    font.pixelSize: 13
                    font.weight: Font.DemiBold
                    
                    onClicked: bridge.analyze_data_quality()
                    
                    background: Rectangle {
                        gradient: Gradient {
                            GradientStop { position: 0.0; color: parent.hovered ? "#7C3AED" : "#9333EA" }
                            GradientStop { position: 1.0; color: parent.hovered ? "#6D28D9" : "#7C3AED" }
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
                
                Button {
                    text: "Thực thi Pipeline"
                    Layout.fillWidth: true
                    Layout.preferredHeight: 45
                    font.pixelSize: 13
                    font.weight: Font.DemiBold
                    
                    onClicked: bridge.execute_pipeline()
                    
                    background: Rectangle {
                        gradient: Gradient {
                            GradientStop { position: 0.0; color: parent.hovered ? "#059669" : "#10B981" }
                            GradientStop { position: 1.0; color: parent.hovered ? "#047857" : "#059669" }
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
                
                Button {
                    text: "Reset Dữ liệu"
                    Layout.fillWidth: true
                    Layout.preferredHeight: 40
                    font.pixelSize: 12
                    
                    onClicked: bridge.reset_transformations()
                    
                    background: Rectangle {
                        color: parent.hovered ? "#475569" : "#334155"
                        radius: 10
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        color: "#E2E8F0"
                        font: parent.font
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                }
                
                Item { Layout.fillHeight: true }
            }
        }
        
        // Right Panel - Rules & Quality
        ColumnLayout {
            Layout.fillHeight: true
            Layout.fillWidth: true
            spacing: 0
            
            // Tab Bar
            TabBar {
                id: etlTabs
                Layout.fillWidth: true
                Layout.preferredHeight: 60
                
                background: Rectangle {
                    color: "#0F172A"
                    opacity: 0.6
                }
                
                TabButton {
                    text: "Transform Rules"
                    font.pixelSize: 14
                    font.weight: Font.DemiBold
                    
                    contentItem: Text {
                        text: parent.text
                        font: parent.font
                        color: parent.checked ? "#10B981" : "#94A3B8"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    background: Rectangle {
                        color: parent.checked ? "#10B981" : "transparent"
                        opacity: parent.checked ? 0.2 : 0
                        radius: 10
                    }
                }
                
                TabButton {
                    text: "Data Quality"
                    font.pixelSize: 14
                    font.weight: Font.DemiBold
                    
                    contentItem: Text {
                        text: parent.text
                        font: parent.font
                        color: parent.checked ? "#10B981" : "#94A3B8"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    background: Rectangle {
                        color: parent.checked ? "#10B981" : "transparent"
                        opacity: parent.checked ? 0.2 : 0
                        radius: 10
                    }
                }
            }
            
            StackLayout {
                Layout.fillWidth: true
                Layout.fillHeight: true
                currentIndex: etlTabs.currentIndex
                
                // Transform Rules Tab
                TransformRulesPanel {
                    id: rulesPanel
                }
                
                // Data Quality Tab
                DataQualityPanel {
                    id: qualityPanel
                }
            }
        }
    }
}
