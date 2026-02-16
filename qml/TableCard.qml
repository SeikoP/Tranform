import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Effects

Rectangle {
    id: root
    property string tableName: ""
    property list<var> columns: []

    width: 260
    height: Math.max(140, 55 + columns.length * 30 + 90)
    radius: 4
    color: "white"
    border.color: dragArea.drag.active ? "#3B82F6" : "#E0E0E0"
    border.width: dragArea.drag.active ? 2 : 1
    
    // Drag and drop properties
    x: 0
    y: 0
    z: dragArea.drag.active ? 100 : 0
    
    // Hover and drag animations
    scale: dragArea.drag.active ? 1.05 : (cardMouseArea.containsMouse ? 1.01 : 1.0)
    opacity: dragArea.drag.active ? 0.8 : 1.0
    
    Behavior on scale {
        NumberAnimation { duration: 150; easing.type: Easing.OutQuad }
    }
    
    Behavior on opacity {
        NumberAnimation { duration: 150 }
    }
    
    Behavior on border.color {
        ColorAnimation { duration: 200 }
    }
    
    // Shadow effect when dragging
    layer.enabled: dragArea.drag.active
    layer.effect: MultiEffect {
        shadowEnabled: true
        shadowColor: "#3B82F6"
        shadowOpacity: 0.5
        shadowBlur: 30
    }
    
    MouseArea {
        id: cardMouseArea
        anchors.fill: parent
        hoverEnabled: true
        propagateComposedEvents: true
        
        // Allow clicks to pass through to children
        onPressed: function(mouse) {
            mouse.accepted = false
        }
    }
    
    // Drag area for the header only
    MouseArea {
        id: dragArea
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        height: 42
        cursorShape: Qt.OpenHandCursor
        
        drag.target: root
        drag.axis: Drag.XAndYAxis
        drag.minimumX: 0
        drag.minimumY: 0
        
        onPressed: {
            cursorShape = Qt.ClosedHandCursor
        }
        
        onReleased: {
            cursorShape = Qt.OpenHandCursor
        }
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        // Header - compact
        Rectangle {
            Layout.fillWidth: true
            height: 42
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
                anchors.leftMargin: 12
                anchors.rightMargin: 12
                spacing: 8
                
                Rectangle {
                    width: 24
                    height: 24
                    radius: 3
                    color: tableName.toLowerCase().startsWith("fact") ? "#4CAF50" : "#2196F3"
                    opacity: 0.2
                    
                    Text {
                        anchors.centerIn: parent
                        text: tableName.toLowerCase().startsWith("fact") ? "F" : "D"
                        font.pixelSize: 12
                        font.weight: Font.Bold
                        font.family: "Microsoft YaHei UI"
                        color: tableName.toLowerCase().startsWith("fact") ? "#4CAF50" : "#2196F3"
                    }
                }
                
                Text {
                    text: tableName
                    font.pixelSize: 13
                    font.weight: Font.DemiBold
                    font.family: "Microsoft YaHei UI"
                    color: "#333333"
                    Layout.fillWidth: true
                    elide: Text.ElideRight
                }
                
                Rectangle {
                    width: 36
                    height: 18
                    radius: 3
                    color: tableName.toLowerCase().startsWith("fact") ? "#4CAF50" : "#2196F3"
                    opacity: 0.15
                    
                    Text {
                        anchors.centerIn: parent
                        text: tableName.toLowerCase().startsWith("fact") ? "Fact" : "Dim"
                        font.pixelSize: 9
                        font.weight: Font.Bold
                        font.family: "Microsoft YaHei UI"
                        color: tableName.toLowerCase().startsWith("fact") ? "#4CAF50" : "#2196F3"
                    }
                }
            }
        }

        // Body - Columns List - compact
        ColumnLayout {
            Layout.fillWidth: true
            Layout.margins: 12
            spacing: 5

            Repeater {
                model: columns
                delegate: Rectangle {
                    Layout.fillWidth: true
                    height: 28
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
                        anchors.leftMargin: 8
                        anchors.rightMargin: 8
                        spacing: 6
                        
                        Rectangle {
                            width: 18
                            height: 18
                            radius: 2
                            color: modelData.is_primary ? "#FF9800" : (modelData.ref_table ? "#2196F3" : "#BDBDBD")
                            opacity: 0.2
                            
                            Text {
                                anchors.centerIn: parent
                                text: modelData.is_primary ? "PK" : (modelData.ref_table ? "FK" : "")
                                font.pixelSize: 7
                                font.weight: Font.Bold
                                font.family: "Microsoft YaHei UI"
                                color: modelData.is_primary ? "#FF9800" : (modelData.ref_table ? "#2196F3" : "#BDBDBD")
                            }
                        }
                        
                        Text {
                            text: modelData.name
                            font.pixelSize: 11
                            font.weight: modelData.is_primary ? Font.DemiBold : Font.Normal
                            font.family: "Microsoft YaHei UI"
                            color: "#333333"
                            Layout.fillWidth: true
                            elide: Text.ElideRight
                        }
                        
                        Text {
                            text: modelData.ref_table ? "→ " + modelData.ref_table : ""
                            font.pixelSize: 9
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
                Layout.topMargin: 6
            }

            // Add Field area - compact
            RowLayout {
                spacing: 5
                Layout.topMargin: 6
                
                ComboBox {
                    id: fieldSelector
                    model: bridge ? bridge.columnNames : []
                    Layout.fillWidth: true
                    font.pixelSize: 10
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
                        leftPadding: 6
                        elide: Text.ElideRight
                    }
                }
                
                CheckBox {
                    id: pkCheck
                    text: "PK"
                    font.pixelSize: 9
                    font.weight: Font.Bold
                    font.family: "Microsoft YaHei UI"
                    
                    contentItem: Text {
                        text: pkCheck.text
                        font: pkCheck.font
                        color: pkCheck.checked ? "#FF9800" : "#999999"
                        leftPadding: pkCheck.indicator.width + 3
                        verticalAlignment: Text.AlignVCenter
                    }
                }
                
                Button {
                    text: "+"
                    width: 28
                    height: 28
                    font.pixelSize: 14
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
