import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Effects

Rectangle {
    id: root
    property string tableName: ""
    property list<var> columns: []

    width: 320
    height: Math.max(180, 70 + columns.length * 35 + 120)
    radius: 16
    color: "#1E293B"
    opacity: 0.95
    border.color: tableName.toLowerCase().startsWith("fact") ? "#0D9488" : "#3B82F6"
    border.width: 2
    
    layer.enabled: true
    layer.effect: MultiEffect {
        shadowEnabled: true
        shadowColor: tableName.toLowerCase().startsWith("fact") ? "#0D9488" : "#3B82F6"
        shadowOpacity: 0.4
        shadowBlur: 20
    }
    
    // Hover animation
    scale: cardMouseArea.containsMouse ? 1.02 : 1.0
    Behavior on scale {
        NumberAnimation { duration: 200; easing.type: Easing.OutQuad }
    }
    
    MouseArea {
        id: cardMouseArea
        anchors.fill: parent
        hoverEnabled: true
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        // Header
        Rectangle {
            Layout.fillWidth: true
            height: 60
            radius: 16
            
            gradient: Gradient {
                GradientStop { 
                    position: 0.0
                    color: tableName.toLowerCase().startsWith("fact") ? "#0D9488" : "#3B82F6"
                }
                GradientStop { 
                    position: 1.0
                    color: tableName.toLowerCase().startsWith("fact") ? "#0F766E" : "#2563EB"
                }
            }
            
            // Only top corners rounded
            Rectangle {
                anchors.bottom: parent.bottom
                width: parent.width
                height: 16
                color: parent.gradient.stops[1].color
            }

            RowLayout {
                anchors.fill: parent
                anchors.leftMargin: 20
                anchors.rightMargin: 20
                spacing: 12
                
                Rectangle {
                    width: 32
                    height: 32
                    radius: 6
                    color: "white"
                    opacity: 0.2
                    
                    Text {
                        anchors.centerIn: parent
                        text: tableName.toLowerCase().startsWith("fact") ? "F" : "D"
                        font.pixelSize: 16
                        font.weight: Font.Bold
                        font.family: "Segoe UI"
                        color: "white"
                    }
                }
                
                Text {
                    text: tableName
                    font.pixelSize: 16
                    font.weight: Font.Bold
                    font.family: "Segoe UI"
                    color: "white"
                    Layout.fillWidth: true
                }
                
                Rectangle {
                    width: 50
                    height: 24
                    radius: 12
                    color: "white"
                    opacity: 0.2
                    
                    Text {
                        anchors.centerIn: parent
                        text: tableName.toLowerCase().startsWith("fact") ? "Fact" : "Dim"
                        font.pixelSize: 10
                        font.weight: Font.Bold
                        color: "white"
                    }
                }
            }
        }

        // Body - Columns List
        ColumnLayout {
            Layout.fillWidth: true
            Layout.margins: 20
            spacing: 10

            Repeater {
                model: columns
                delegate: Rectangle {
                    Layout.fillWidth: true
                    height: 40
                    radius: 8
                    color: "#0F172A"
                    opacity: columnMouseArea.containsMouse ? 1.0 : 0.6
                    border.color: modelData.is_primary ? "#F59E0B" : "#334155"
                    border.width: modelData.is_primary ? 2 : 1
                    
                    Behavior on opacity {
                        NumberAnimation { duration: 150 }
                    }
                    
                    MouseArea {
                        id: columnMouseArea
                        anchors.fill: parent
                        hoverEnabled: true
                    }
                    
                    RowLayout {
                        anchors.fill: parent
                        anchors.leftMargin: 12
                        anchors.rightMargin: 12
                        spacing: 10
                        
                        Rectangle {
                            width: 24
                            height: 24
                            radius: 4
                            color: modelData.is_primary ? "#F59E0B" : (modelData.ref_table ? "#3B82F6" : "#64748B")
                            opacity: 0.3
                            
                            Text {
                                anchors.centerIn: parent
                                text: modelData.is_primary ? "PK" : (modelData.ref_table ? "FK" : "")
                                font.pixelSize: 9
                                font.weight: Font.Bold
                                font.family: "Segoe UI"
                                color: "white"
                            }
                        }
                        
                        Text {
                            text: modelData.name
                            font.pixelSize: 14
                            font.weight: modelData.is_primary ? Font.Bold : Font.Normal
                            font.family: "Segoe UI"
                            color: modelData.is_primary ? "#FCD34D" : "#E2E8F0"
                            Layout.fillWidth: true
                        }
                        
                        Text {
                            text: modelData.ref_table ? "→ " + modelData.ref_table : ""
                            font.pixelSize: 11
                            color: "#60A5FA"
                            font.italic: true
                            visible: modelData.ref_table !== null
                        }
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
                Layout.topMargin: 10
            }

            // Add Field area
            RowLayout {
                spacing: 8
                Layout.topMargin: 10
                
                ComboBox {
                    id: fieldSelector
                    model: bridge ? bridge.columnNames : []
                    Layout.fillWidth: true
                    font.pixelSize: 13
                    
                    background: Rectangle {
                        color: "#0F172A"
                        radius: 8
                        border.color: fieldSelector.activeFocus ? "#3B82F6" : "#334155"
                        border.width: 1
                    }
                    
                    contentItem: Text {
                        text: fieldSelector.displayText
                        color: "#E2E8F0"
                        font: fieldSelector.font
                        verticalAlignment: Text.AlignVCenter
                        leftPadding: 10
                    }
                }
                
                CheckBox {
                    id: pkCheck
                    text: "PK"
                    font.pixelSize: 11
                    font.weight: Font.Bold
                    
                    contentItem: Text {
                        text: pkCheck.text
                        font: pkCheck.font
                        color: pkCheck.checked ? "#FCD34D" : "#94A3B8"
                        leftPadding: pkCheck.indicator.width + 5
                        verticalAlignment: Text.AlignVCenter
                    }
                }
                
                Button {
                    text: "+"
                    width: 40
                    height: 40
                    font.pixelSize: 20
                    font.weight: Font.Bold
                    
                    onClicked: {
                        bridge.add_field(tableName, fieldSelector.currentText, pkCheck.checked, "")
                    }
                    
                    background: Rectangle {
                        gradient: Gradient {
                            GradientStop { position: 0.0; color: parent.hovered ? "#2563EB" : "#3B82F6" }
                            GradientStop { position: 1.0; color: parent.hovered ? "#1E40AF" : "#2563EB" }
                        }
                        radius: 8
                        scale: parent.pressed ? 0.9 : 1.0
                        
                        Behavior on scale {
                            NumberAnimation { duration: 100 }
                        }
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

        Item { Layout.fillHeight: true }
    }
}
