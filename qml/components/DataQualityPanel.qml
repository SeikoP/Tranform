import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Effects
import ".."

Item {
    id: root
    
    ScrollView {
        anchors.fill: parent
        anchors.margins: Theme.paddingXXXLarge
        clip: true
        
        ColumnLayout {
            width: parent.width
            spacing: Theme.spacingXXLarge
            
            // Header
            Text {
                text: "📊 Data Quality Analysis"
                font.pixelSize: 20
                font.weight: Font.Bold
                color: Theme.darkMode ? "white" : Theme.textPrimary
            }
            
            // Summary Cards
            RowLayout {
                Layout.fillWidth: true
                spacing: Theme.spacingXLarge
                
                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 100
                    color: Theme.dialogBackground
                    opacity: 0.9
                    radius: Theme.radiusXLarge
                    border.color: Theme.primaryColor
                    border.width: Theme.borderWidthThin
                    
                    RowLayout {
                        anchors.fill: parent
                        anchors.margins: Theme.paddingXLarge
                        spacing: Theme.paddingLarge
                        
                        Text {
                            text: "📊"
                            font.pixelSize: 32
                        }
                        
                        ColumnLayout {
                            spacing: 5
                            
                            Text {
                                text: "Total Rows"
                                font.pixelSize: 12
                                color: Theme.textSecondary
                            }
                            
                            Text {
                                text: bridge && bridge.dataQualityProfile.profile ? 
                                      bridge.dataQualityProfile.profile.total_rows.toLocaleString() : "0"
                                font.pixelSize: 24
                                font.weight: Font.Bold
                                color: Theme.darkMode ? "white" : Theme.textPrimary
                            }
                        }
                    }
                }
                
                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 100
                    color: Theme.dialogBackground
                    opacity: 0.9
                    radius: Theme.radiusXLarge
                    border.color: Theme.successColor
                    border.width: Theme.borderWidthThin
                    
                    RowLayout {
                        anchors.fill: parent
                        anchors.margins: Theme.paddingXLarge
                        spacing: Theme.paddingLarge
                        
                        Text {
                            text: "📋"
                            font.pixelSize: 32
                        }
                        
                        ColumnLayout {
                            spacing: 5
                            
                            Text {
                                text: "Total Columns"
                                font.pixelSize: 12
                                color: Theme.textSecondary
                            }
                            
                            Text {
                                text: bridge && bridge.dataQualityProfile.profile ? 
                                      bridge.dataQualityProfile.profile.total_columns : "0"
                                font.pixelSize: 24
                                font.weight: Font.Bold
                                color: Theme.darkMode ? "white" : Theme.textPrimary
                            }
                        }
                    }
                }
                
                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 100
                    color: Theme.dialogBackground
                    opacity: 0.9
                    radius: Theme.radiusXLarge
                    border.color: Theme.warningColor
                    border.width: Theme.borderWidthThin
                    
                    RowLayout {
                        anchors.fill: parent
                        anchors.margins: Theme.paddingXLarge
                        spacing: Theme.paddingLarge
                        
                        Text {
                            text: "⚠️"
                            font.pixelSize: 32
                        }
                        
                        ColumnLayout {
                            spacing: 5
                            
                            Text {
                                text: "Issues Found"
                                font.pixelSize: 12
                                color: Theme.textSecondary
                            }
                            
                            Text {
                                text: getTotalIssues()
                                font.pixelSize: 24
                                font.weight: Font.Bold
                                color: Theme.warningColor
                            }
                        }
                    }
                }
            }
            
            // Anomalies Section
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 300
                color: Theme.dialogBackground
                opacity: 0.9
                radius: Theme.radiusXLarge
                border.color: Theme.borderColor
                border.width: Theme.borderWidthThin
                
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: Theme.paddingXLarge
                    spacing: Theme.paddingLarge
                    
                    Text {
                        text: "⚠️ Detected Anomalies"
                        font.pixelSize: 16
                        font.weight: Font.Bold
                        color: Theme.darkMode ? "white" : Theme.textPrimary
                    }
                    
                    ScrollView {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        clip: true
                        
                        ColumnLayout {
                            width: parent.width
                            spacing: Theme.paddingMedium
                            
                            Repeater {
                                model: getAnomaliesList()
                                
                                delegate: Rectangle {
                                    Layout.fillWidth: true
                                    height: 40
                                    color: Theme.dialogInputBackground
                                    radius: Theme.radiusLarge
                                    
                                    RowLayout {
                                        anchors.fill: parent
                                        anchors.leftMargin: Theme.paddingLarge
                                        anchors.rightMargin: Theme.paddingLarge
                                        spacing: Theme.paddingMedium
                                        
                                        Text {
                                            text: getIssueIcon(modelData.type)
                                            font.pixelSize: 16
                                        }
                                        
                                        Text {
                                            text: modelData.message
                                            font.pixelSize: 13
                                            color: Theme.textSecondary
                                            Layout.fillWidth: true
                                        }
                                    }
                                }
                            }
                            
                            // Empty state
                            Item {
                                Layout.fillWidth: true
                                Layout.preferredHeight: 150
                                visible: getAnomaliesList().length === 0
                                
                                ColumnLayout {
                                    anchors.centerIn: parent
                                    spacing: Theme.paddingMedium
                                    
                                    Text {
                                        text: "✅"
                                        font.pixelSize: 48
                                        Layout.alignment: Qt.AlignHCenter
                                    }
                                    
                                    Text {
                                        text: "Không phát hiện vấn đề"
                                        font.pixelSize: 14
                                        color: Theme.successColor
                                        Layout.alignment: Qt.AlignHCenter
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    
    function getTotalIssues() {
        if (!bridge || !bridge.dataQualityProfile.anomalies) return "0"
        
        var anomalies = bridge.dataQualityProfile.anomalies
        var total = 0
        
        for (var key in anomalies) {
            if (anomalies[key] && Array.isArray(anomalies[key])) {
                total += anomalies[key].length
            }
        }
        
        return total.toString()
    }
    
    function getAnomaliesList() {
        if (!bridge || !bridge.dataQualityProfile.anomalies) return []
        
        var anomalies = bridge.dataQualityProfile.anomalies
        var list = []
        
        for (var type in anomalies) {
            if (anomalies[type] && Array.isArray(anomalies[type])) {
                for (var i = 0; i < anomalies[type].length; i++) {
                    list.push({
                        type: type,
                        message: anomalies[type][i]
                    })
                }
            }
        }
        
        return list
    }
    
    function getIssueIcon(type) {
        switch(type) {
            case "high_missing": return "❌"
            case "low_variance": return "📊"
            case "potential_duplicates": return "🔄"
            case "outliers": return "📈"
            case "inconsistent_types": return "⚠️"
            default: return "ℹ️"
        }
    }
}
