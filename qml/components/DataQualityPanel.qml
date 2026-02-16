import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Effects
import ".."

Item {
    id: root
    
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: Theme.paddingLarge
        spacing: Theme.spacingLarge
        
        // Header - compact
        Text {
            text: "📊 Data Quality"
            font.pixelSize: Theme.fontSizeXLarge + 2
            font.weight: Font.Bold
            font.family: Theme.fontFamily
            color: Theme.textPrimary
        }
        
        // Summary Cards - compact
        RowLayout {
            Layout.fillWidth: true
            spacing: Theme.spacingMedium
            
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 60
                color: Theme.cardBackground
                radius: Theme.radiusMedium
                border.color: Theme.primaryColor
                border.width: Theme.borderWidthThin
                
                RowLayout {
                    anchors.fill: parent
                    anchors.margins: Theme.paddingMedium
                    spacing: Theme.spacingSmall
                    
                    Text {
                        text: "📊"
                        font.pixelSize: 20
                    }
                    
                    ColumnLayout {
                        spacing: 2
                        Layout.fillWidth: true
                        
                        Text {
                            text: "Rows"
                            font.pixelSize: Theme.fontSizeSmall
                            font.family: Theme.fontFamily
                            color: Theme.textSecondary
                        }
                        
                        Text {
                            text: bridge && bridge.dataQualityProfile && bridge.dataQualityProfile.profile ? 
                                  bridge.dataQualityProfile.profile.total_rows.toLocaleString() : "0"
                            font.pixelSize: Theme.fontSizeLarge + 4
                            font.weight: Font.Bold
                            font.family: Theme.fontFamily
                            color: Theme.textPrimary
                        }
                    }
                }
            }
            
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 60
                color: Theme.cardBackground
                radius: Theme.radiusMedium
                border.color: Theme.successColor
                border.width: Theme.borderWidthThin
                
                RowLayout {
                    anchors.fill: parent
                    anchors.margins: Theme.paddingMedium
                    spacing: Theme.spacingSmall
                    
                    Text {
                        text: "📋"
                        font.pixelSize: 20
                    }
                    
                    ColumnLayout {
                        spacing: 2
                        Layout.fillWidth: true
                        
                        Text {
                            text: "Columns"
                            font.pixelSize: Theme.fontSizeSmall
                            font.family: Theme.fontFamily
                            color: Theme.textSecondary
                        }
                        
                        Text {
                            text: bridge && bridge.dataQualityProfile && bridge.dataQualityProfile.profile ? 
                                  bridge.dataQualityProfile.profile.total_columns : "0"
                            font.pixelSize: Theme.fontSizeLarge + 4
                            font.weight: Font.Bold
                            font.family: Theme.fontFamily
                            color: Theme.textPrimary
                        }
                    }
                }
            }
            
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 60
                color: Theme.cardBackground
                radius: Theme.radiusMedium
                border.color: Theme.warningColor
                border.width: Theme.borderWidthThin
                
                RowLayout {
                    anchors.fill: parent
                    anchors.margins: Theme.paddingMedium
                    spacing: Theme.spacingSmall
                    
                    Text {
                        text: "⚠️"
                        font.pixelSize: 20
                    }
                    
                    ColumnLayout {
                        spacing: 2
                        Layout.fillWidth: true
                        
                        Text {
                            text: "Issues"
                            font.pixelSize: Theme.fontSizeSmall
                            font.family: Theme.fontFamily
                            color: Theme.textSecondary
                        }
                        
                        Text {
                            text: getTotalIssues()
                            font.pixelSize: Theme.fontSizeLarge + 4
                            font.weight: Font.Bold
                            font.family: Theme.fontFamily
                            color: Theme.warningColor
                        }
                    }
                }
            }
        }
        
        // Anomalies Section - compact
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: Theme.cardBackground
            radius: Theme.radiusMedium
            border.color: Theme.borderColor
            border.width: Theme.borderWidthThin
            
            ColumnLayout {
                anchors.fill: parent
                anchors.margins: Theme.paddingMedium
                spacing: Theme.spacingSmall
                
                Text {
                    text: "⚠️ Anomalies"
                    font.pixelSize: Theme.fontSizeLarge
                    font.weight: Font.Bold
                    font.family: Theme.fontFamily
                    color: Theme.textPrimary
                }
                
                ScrollView {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    clip: true
                    
                    ColumnLayout {
                        width: parent.parent.width - Theme.paddingMedium * 2
                        spacing: Theme.spacingXSmall
                        
                        Repeater {
                            model: getAnomaliesList()
                            
                            delegate: Rectangle {
                                Layout.fillWidth: true
                                height: 28
                                color: Theme.backgroundHover
                                radius: Theme.radiusSmall
                                
                                RowLayout {
                                    anchors.fill: parent
                                    anchors.leftMargin: Theme.paddingSmall
                                    anchors.rightMargin: Theme.paddingSmall
                                    spacing: Theme.spacingSmall
                                    
                                    Text {
                                        text: getIssueIcon(modelData.type)
                                        font.pixelSize: 12
                                    }
                                    
                                    Text {
                                        text: modelData.message
                                        font.pixelSize: Theme.fontSizeSmall
                                        font.family: Theme.fontFamily
                                        color: Theme.textSecondary
                                        Layout.fillWidth: true
                                        elide: Text.ElideRight
                                    }
                                }
                            }
                        }
                        
                        // Empty state
                        Item {
                            Layout.fillWidth: true
                            Layout.preferredHeight: 120
                            visible: getAnomaliesList().length === 0
                            
                            ColumnLayout {
                                anchors.centerIn: parent
                                spacing: Theme.spacingSmall
                                
                                Text {
                                    text: "✅"
                                    font.pixelSize: 32
                                    Layout.alignment: Qt.AlignHCenter
                                }
                                
                                Text {
                                    text: "No issues detected"
                                    font.pixelSize: Theme.fontSizeSmall
                                    font.family: Theme.fontFamily
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
    
    function getTotalIssues() {
        if (!bridge || !bridge.dataQualityProfile || !bridge.dataQualityProfile.anomalies) return "0"
        
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
        if (!bridge || !bridge.dataQualityProfile || !bridge.dataQualityProfile.anomalies) return []
        
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
