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
        duration: Theme.animationDuration * 4
        easing.type: Easing.OutQuad
    }
    
    RowLayout {
        anchors.fill: parent
        spacing: 0
        
        // Left Panel - Pipeline Management (Compact)
        Rectangle {
            Layout.fillHeight: true
            Layout.preferredWidth: 220
            color: Theme.backgroundSecondary
            border.color: Theme.borderColor
            border.width: 1
            
            Behavior on color {
                ColorAnimation { duration: Theme.animationDuration }
            }
            
            ColumnLayout {
                anchors.fill: parent
                anchors.margins: Theme.spacingXLarge
                spacing: Theme.spacingMedium
                
                SectionHeader {
                    title: "ETL Pipeline"
                    accentColor: Theme.successColor
                }
                
                Text {
                    text: "Extract → Transform → Load"
                    font.pixelSize: Theme.fontSizeSmall
                    font.family: Theme.fontFamily
                    color: Theme.textSecondary
                    Layout.fillWidth: true
                }
                
                Rectangle {
                    Layout.fillWidth: true
                    height: 1
                    color: Theme.dividerColor
                }
                
                // Pipeline Selection
                Text {
                    text: "Pipeline:"
                    font.pixelSize: Theme.fontSizeMedium
                    font.weight: Font.Medium
                    font.family: Theme.fontFamily
                    color: Theme.textPrimary
                }
                
                ComboBox {
                    id: pipelineSelector
                    Layout.fillWidth: true
                    Layout.preferredHeight: Theme.inputHeight
                    model: bridge ? bridge.pipelineNames : []
                    font.pixelSize: Theme.fontSizeMedium
                    font.family: Theme.fontFamily
                    
                    onCurrentTextChanged: {
                        if (currentText) {
                            bridge.load_pipeline(currentText)
                        }
                    }
                    
                    background: Rectangle {
                        color: Theme.backgroundPrimary
                        radius: Theme.radiusMedium
                        border.color: parent.activeFocus ? Theme.successColor : Theme.borderColor
                        border.width: 1
                    }
                    
                    contentItem: Text {
                        text: parent.displayText || "Chọn pipeline..."
                        color: Theme.textPrimary
                        font: parent.font
                        verticalAlignment: Text.AlignVCenter
                        leftPadding: Theme.spacingMedium
                    }
                }
                
                // Create New Pipeline
                RowLayout {
                    Layout.fillWidth: true
                    spacing: Theme.spacingSmall
                    
                    StyledTextField {
                        id: newPipelineField
                        Layout.fillWidth: true
                        Layout.preferredHeight: Theme.inputHeight
                        placeholderText: "Tên pipeline..."
                    }
                    
                    Button {
                        text: "+"
                        width: Theme.inputHeight
                        height: Theme.inputHeight
                        font.pixelSize: 16
                        font.weight: Font.Bold
                        font.family: Theme.fontFamily
                        
                        onClicked: {
                            if (newPipelineField.text) {
                                bridge.create_pipeline(newPipelineField.text)
                                newPipelineField.text = ""
                            }
                        }
                        
                        background: Rectangle {
                            color: parent.hovered ? "#388E3C" : Theme.successColor
                            radius: Theme.radiusMedium
                        }
                        
                        contentItem: Text {
                            text: parent.text
                            color: Theme.textOnPrimary
                            font: parent.font
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                    }
                }
                
                Rectangle {
                    Layout.fillWidth: true
                    height: 1
                    color: Theme.dividerColor
                }
                
                // Action Buttons
                Text {
                    text: "THAO TÁC"
                    font.pixelSize: Theme.fontSizeSmall
                    font.weight: Font.Bold
                    font.family: Theme.fontFamily
                    color: Theme.primaryColor
                    font.letterSpacing: 1
                }
                
                PrimaryButton {
                    text: "Phân tích"
                    Layout.fillWidth: true
                    Layout.preferredHeight: Theme.inputHeight
                    buttonColor: Theme.accentColor
                    buttonHoverColor: Theme.accentDark
                    onClicked: bridge.analyze_data_quality()
                }
                
                PrimaryButton {
                    text: "Thực thi"
                    Layout.fillWidth: true
                    Layout.preferredHeight: Theme.inputHeight
                    buttonColor: Theme.successColor
                    buttonHoverColor: "#388E3C"
                    onClicked: bridge.execute_pipeline()
                }
                
                Button {
                    text: "Reset"
                    Layout.fillWidth: true
                    Layout.preferredHeight: Theme.buttonHeightMedium
                    font.pixelSize: Theme.fontSizeMedium
                    font.family: Theme.fontFamily
                    
                    onClicked: bridge.reset_transformations()
                    
                    background: Rectangle {
                        color: parent.hovered ? Theme.backgroundHover : Theme.backgroundSecondary
                        radius: Theme.radiusMedium
                        border.color: Theme.borderColor
                        border.width: 1
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        color: Theme.textSecondary
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
            
            // Tab Bar - Compact
            TabBar {
                id: etlTabs
                Layout.fillWidth: true
                Layout.preferredHeight: Theme.tabBarHeight
                
                background: Rectangle {
                    color: Theme.backgroundSecondary
                }
                
                TabButton {
                    text: "Transform Rules"
                    font.pixelSize: Theme.fontSizeMedium
                    font.weight: Font.DemiBold
                    font.family: Theme.fontFamily
                    
                    contentItem: Text {
                        text: parent.text
                        font: parent.font
                        color: parent.checked ? Theme.successColor : Theme.textSecondary
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    background: Rectangle {
                        color: "transparent"
                        
                        Rectangle {
                            anchors.bottom: parent.bottom
                            width: parent.width
                            height: 2
                            color: Theme.successColor
                            visible: parent.parent.checked
                        }
                    }
                }
                
                TabButton {
                    text: "Data Quality"
                    font.pixelSize: Theme.fontSizeMedium
                    font.weight: Font.DemiBold
                    font.family: Theme.fontFamily
                    
                    contentItem: Text {
                        text: parent.text
                        font: parent.font
                        color: parent.checked ? Theme.successColor : Theme.textSecondary
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    background: Rectangle {
                        color: "transparent"
                        
                        Rectangle {
                            anchors.bottom: parent.bottom
                            width: parent.width
                            height: 2
                            color: Theme.successColor
                            visible: parent.parent.checked
                        }
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
