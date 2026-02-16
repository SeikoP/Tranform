import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: root
    property string tableName: ""
    property list<var> columns: []

    width: 280
    height: Math.max(150, 60 + columns.length * 30 + 100)
    radius: 12
    color: "white"
    border.color: "#E2E8F0"
    
    layer.enabled: true
    // shadow effect could be added here

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        // Header
        Rectangle {
            Layout.fillWidth: true
            height: 45
            color: tableName.toLowerCase().startsWith("fact") ? "#F0FDFA" : "#EFF6FF"
            radius: 12
            // Only top corners rounded
            Rectangle {
                anchors.bottom: parent.bottom
                width: parent.width; height: 12
                color: parent.color
            }

            RowLayout {
                anchors.fill: parent
                anchors.leftMargin: 15
                anchors.rightMargin: 15
                
                Text {
                    text: tableName
                    font.pixelSize: 15
                    font.weight: Font.Bold
                    color: tableName.toLowerCase().startsWith("fact") ? "#0D9488" : "#2563EB"
                }
                
                Item { Layout.fillWidth: true }
                
                Text {
                    text: tableName.toLowerCase().startsWith("fact") ? "Fact" : "Dim"
                    font.pixelSize: 11
                    color: "#94A3B8"
                }
            }
        }

        // Body - Columns List
        ColumnLayout {
            Layout.fillWidth: true
            Layout.margins: 15
            spacing: 8

            Repeater {
                model: columns
                delegate: RowLayout {
                    spacing: 10
                    Text {
                        text: modelData.is_primary ? "🔑" : (modelData.ref_table ? "🔗" : "🔹")
                        font.pixelSize: 12
                    }
                    Text {
                        text: modelData.name
                        font.pixelSize: 13
                        color: "#334155"
                        Layout.fillWidth: true
                    }
                    Text {
                        text: modelData.ref_table ? "→ " + modelData.ref_table : ""
                        font.pixelSize: 11
                        color: "#94A3B8"
                        visible: modelData.ref_table !== null
                    }
                }
            }

            Rectangle {
                Layout.fillWidth: true
                height: 1
                color: "#F1F5F9"
                Layout.topMargin: 10
            }

            // Add Field area
            RowLayout {
                spacing: 5
                Layout.topMargin: 10
                
                ComboBox {
                    id: fieldSelector
                    model: bridge ? bridge.columnNames : []
                    Layout.fillWidth: true
                    flat: true
                    font.pixelSize: 12
                }
                
                CheckBox {
                    id: pkCheck
                    text: "PK"
                    font.pixelSize: 10
                }
                
                Button {
                    text: "+"
                    width: 30
                    onClicked: {
                        bridge.add_field(tableName, fieldSelector.currentText, pkCheck.checked, "")
                    }
                }
            }
        }

        Item { Layout.fillHeight: true }
    }
}
