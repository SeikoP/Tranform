import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Effects

Item {
    id: root
    
    ScrollView {
        anchors.fill: parent
        anchors.margins: 30
        clip: true
        
        ColumnLayout {
            width: parent.width
            spacing: 25
            
            // Header
            Text {
                text: "📊 Data Quality Analysis"
                font.pixelSize: 20
                font.weight: Font.Bold
                color: "white"
            }
            
            // Summary Cards
            RowLayout {
                Layout.fillWidth: true
                spacing: 20
                
                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 100
                    color: "#1E293B"
                    opacity: 0.9
                    radius: 12
                    border.color: "#3B82F6"
                    border.width: 1
                    
                    RowLayout {
                        anchors.fill: parent
                        anchors.margins: 20
                        spacing: 15
                        
                        Text {
                            text: "📊"
                            font.pixelSize: 32
                        }
                        
                        ColumnLayout {
                            spacing: 5
                            
                            Text {
                                text: "Total Rows"
                                font.pixelSize: 12
                                color: "#94A3B8"
                            }
                            
                            Text {
                                text: bridge && bridge.dataQualityProfile.profile ? 
                                      bridge.dataQualityProfile.profile.total_rows.toLocaleString() : "0"
                                font.pixelSize: 24
                                font.weight: Font.Bold
                                color: "white"
                            }
                        }
                    }
                }
                
                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 100
                    color: "#1E293B"
                    opacity: 0.9
                    radius: 12
                    border.color: "#10B981"
                    border.width: 1
                    
                    RowLayout {
                        anchors.fill: parent
                        anchors.margins: 20
                        spacing: 15
                        
                        Text {
                            text: "📋"
                            font.pixelSize: 32
                        }
                        
                        ColumnLayout {
                            spacing: 5
                            
                            Text {
                                text: "Total Columns"
                                font.pixelSize: 12
                                color: "#94A3B8"
                            }
                            
                            Text {
                                text: bridge && bridge.dataQualityProfile.profile ? 
                                      bridge.dataQualityProfile.profile.total_columns : "0"
                                font.pixelSize: 24
                                font.weight: Font.Bold
                                color: "white"
                            }
                        }
                    }
                }
                
                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 100
                    color: "#1E293B"
                    opacity: 0.9
                    radius: 12
                    border.color: "#F59E0B"
                    border.width: 1
                    
                    RowLayout {
                        anchors.fill: parent
                        anchors.margins: 20
                        spacing: 15
                        
                        Text {
                            text: "⚠️"
                            font.pixelSize: 32
                        }
                        
                        ColumnLayout {
                            spacing: 5
                            
                            Text {
                                text: "Issues Found"
                                font.pixelSize: 12
                                color: "#94A3B8"
                            }
                            
                            Text {
                                text: getTotalIssues()
                                font.pixelSize: 24
                                font.weight: Font.Bold
                                color: "#F59E0B"
                            }
                        }
                    }
                }
            }
            
            // Anomalies Section
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 300
                color: "#1E293B"
                opacity: 0.9
                radius: 12
                border.color: "#334155"
                border.width: 1
                
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 20
                    spacing: 15
                    
                    Text {
                        text: "⚠️ Detected Anomalies"
                        font.pixelSize: 16
                        font.weight: Font.Bold
                        color: "white"
                    }
                    
                    ScrollView {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        clip: true
                        
                        ColumnLayout {
                            width: parent.width
                            spacing: 10
                            
                            Repeater {
                                model: getAnomaliesList()
                                
                                delegate: Rectangle {
                                    Layout.fillWidth: true
                                    height: 40
                                    color: "#0F172A"
                                    radius: 8
                                    
                                    RowLayout {
                                        anchors.fill: parent
                                        anchors.leftMargin: 15
                                        anchors.rightMargin: 15
                                        spacing: 10
                                        
                                        Text {
                                            text: getIssueIcon(modelData.type)
                                            font.pixelSize: 16
                                        }
                                        
                                        Text {
                                            text: modelData.message
                                            font.pixelSize: 13
                                            color: "#CBD5E1"
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
                                    spacing: 10
                                    
                                    Text {
                                        text: "✅"
                                        font.pixelSize: 48
                                        Layout.alignment: Qt.AlignHCenter
                                    }
                                    
                                    Text {
                                        text: "Không phát hiện vấn đề"
                                        font.pixelSize: 14
                                        color: "#10B981"
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
