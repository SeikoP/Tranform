import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Effects

Rectangle {
    id: root
    property string tableName: ""
    property list<var> columns: []

    width: 280
    height: Math.max(150, 60 + columns.length * 32 + 100)
    radius: 4
    color: "white"
    border.color: "#E0E0E0"
    border.width: 1
    
    // Hover animation
    scale: cardMouseArea.containsMouse ? 1.01 : 1.0
    Behavior on scale {
        NumberAnimation { duration: 150; easing.type: Easing.OutQuad }
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
            height: 48
            radius: 4
            color: tableName.toLowerCase().startsWith("fact") ? "#E8F5E9" : "#E3F2FD"
            
            // Only top corners rounded
            Rectangle {
                anchors.bottom: parent.bottom
                width: parent.width
                height: 4
                color: parent.color
            }

            RowLayout {
                anchors.fill: parent
                anchors.leftMargin: 15
                anchors.rightMargin: 15
                spacing: 10
                
                Rectangle {
                    width: 28
                    height: 28
                    radius: 4
                    color: tableName.toLowerCase().startsWith("fact") ? "#4CAF50" : "#2196F3"
                    opacity: 0.2
                    
                    Text {
                        anchors.centerIn: parent
                        text: tableName.toLowerCase().startsWith("fact") ? "F" : "D"
                        font.pixelSize: 14
                        font.weight: Font.Bold
                        font.family: "Microsoft YaHei UI"
                        color: tableName.toLowerCase().startsWith("fact") ? "#4CAF50" : "#2196F3"
                    }
                }
                
                Text {
                    text: tableName
                    font.pixelSize: 14
                    font.weight: Font.DemiBold
                    font.family: "Microsoft YaHei UI"
                    color: "#333333"
                    Layout.fillWidth: true
                }
                
                Rectangle {
                    width: 40
                    height: 20
                    radius: 3
                    color: tableName.toLowerCase().startsWith("fact") ? "#4CAF50" : "#2196F3"
                    opacity: 0.15
                    
                    Text {
                        anchors.centerIn: parent
                        text: tableName.toLowerCase().startsWith("fact") ? "Fact" : "Dim"
                        font.pixelSize: 10
                        font.weight: Font.Bold
                        font.family: "Microsoft YaHei UI"
                        color: tableName.toLowerCase().startsWith("fact") ? "#4CAF50" : "#2196F3"
                    }
                }
            }
        }

        // Body - Columns List
        ColumnLayout {
            Layout.fillWidth: true
            Layout.margins: 15
            spacing: 6

            Repeater {
                model: columns
                delegate: Rectangle {
                    Layout.fillWidth: true
                    height: 32
                    radius: 3
                    color: columnMouseArea.containsMouse ? "#F5F5F5" : "transparent"
                    border.color: modelData.is_primary ? "#FF9800" : "#E0E0E0"
                    border.width: modelData.is_primary ? 1 : 0
                    
                    Behavior on color {
                        ColorAnimation { duration: 100 }
                    }
                    
                    MouseArea {
                        id: columnMouseArea
                        anchors.fill: parent
                        hoverEnabled: true
                    }
                    
                    RowLayout {
                        anchors.fill: parent
                        anchors.leftMargin: 10
                        anchors.rightMargin: 10
                        spacing: 8
                        
                        Rectangle {
                            width: 20
                            height: 20
                            radius: 3
                            color: modelData.is_primary ? "#FF9800" : (modelData.ref_table ? "#2196F3" : "#BDBDBD")
                            opacity: 0.2
                            
                            Text {
                                anchors.centerIn: parent
                                text: modelData.is_primary ? "PK" : (modelData.ref_table ? "FK" : "")
                                font.pixelSize: 8
                                font.weight: Font.Bold
                                font.family: "Microsoft YaHei UI"
                                color: modelData.is_primary ? "#FF9800" : (modelData.ref_table ? "#2196F3" : "#BDBDBD")
                            }
                        }
                        
                        Text {
                            text: modelData.name
                            font.pixelSize: 12
                            font.weight: modelData.is_primary ? Font.DemiBold : Font.Normal
                            font.family: "Microsoft YaHei UI"
                            color: "#333333"
                            Layout.fillWidth: true
                        }
                        
                        Text {
                            text: modelData.ref_table ? "→ " + modelData.ref_table : ""
                            font.pixelSize: 10
                            font.family: "Microsoft YaHei UI"
                            color: "#999999"
                            visible: modelData.ref_table !== null
                        }
                    }
                }
            }

            Rectangle {
                Layout.fillWidth: true
                height: 1
                color: "#E0E0E0"
                Layout.topMargin: 8
            }

            // Add Field area
            RowLayout {
                spacing: 6
                Layout.topMargin: 8
                
                ComboBox {
                    id: fieldSelector
                    model: bridge ? bridge.columnNames : []
                    Layout.fillWidth: true
                    font.pixelSize: 11
                    font.family: "Microsoft YaHei UI"
                    
                    background: Rectangle {
                        color: "white"
                        radius: 3
                        border.color: fieldSelector.activeFocus ? "#2196F3" : "#E0E0E0"
                        border.width: 1
                    }
                    
                    contentItem: Text {
                        text: fieldSelector.displayText
                        color: "#333333"
                        font: fieldSelector.font
                        verticalAlignment: Text.AlignVCenter
                        leftPadding: 8
                    }
                }
                
                CheckBox {
                    id: pkCheck
                    text: "PK"
                    font.pixelSize: 10
                    font.weight: Font.Bold
                    font.family: "Microsoft YaHei UI"
                    
                    contentItem: Text {
                        text: pkCheck.text
                        font: pkCheck.font
                        color: pkCheck.checked ? "#FF9800" : "#999999"
                        leftPadding: pkCheck.indicator.width + 4
                        verticalAlignment: Text.AlignVCenter
                    }
                }
                
                Button {
                    text: "+"
                    width: 32
                    height: 32
                    font.pixelSize: 16
                    font.weight: Font.Bold
                    font.family: "Microsoft YaHei UI"
                    
                    onClicked: {
                        bridge.add_field(tableName, fieldSelector.currentText, pkCheck.checked, "")
                    }
                    
                    background: Rectangle {
                        color: parent.hovered ? "#1976D2" : "#2196F3"
                        radius: 3
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
