import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Effects
import "."

Item {
    id: root
    
    // Entrance animation
    opacity: 0
    Component.onCompleted: {
        fadeIn.start()
    }
    
    NumberAnimation on opacity {
        id: fadeIn
        to: 1.0
        duration: 600
        easing.type: Easing.OutQuad
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 15

        // Stats Cards
        RowLayout {
            Layout.fillWidth: true
            spacing: 15

            StatCard {
                title: "Số bản ghi"
                value: bridge ? bridge.stats.records : 0
                icon: "REC"
                statColor: Theme.primaryColor
                Layout.fillWidth: true
                Layout.preferredHeight: 80
            }
            StatCard {
                title: "Số cột"
                value: bridge ? bridge.stats.columns : 0
                icon: "COL"
                statColor: Theme.primaryLight
                Layout.fillWidth: true
                Layout.preferredHeight: 80
            }
            StatCard {
                title: "Dim Candidates"
                value: bridge ? bridge.stats.dim : 0
                icon: "DIM"
                statColor: Theme.warningColor
                Layout.fillWidth: true
                Layout.preferredHeight: 80
            }
            StatCard {
                title: "Fact Candidates"
                value: bridge ? bridge.stats.fact : 0
                icon: "FCT"
                statColor: Theme.successColor
                Layout.fillWidth: true
                Layout.preferredHeight: 80
            }
        }

        // Data Preview Title
        Text {
            text: "Xem trước dữ liệu (15 dòng đầu)"
            font.pixelSize: 14
            font.weight: Font.DemiBold
            font.family: Theme.fontFamily
            color: Theme.textPrimary
        }

        // Data Table Container
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: Theme.surfaceColor
            radius: 4
            border.color: Theme.borderColor
            border.width: 1
            clip: true

            ScrollView {
                anchors.fill: parent
                ScrollBar.horizontal.policy: ScrollBar.AlwaysOn
                
                ColumnLayout {
                    id: tableContent
                    spacing: 0
                    width: Math.max(parent.width, (bridge ? bridge.columnNames.length : 0) * 180)

                    // Table Header
                    Row {
                        Layout.fillWidth: true
                        height: 40
                        
                        Repeater {
                            model: bridge ? bridge.columnNames : []
                            delegate: Rectangle {
                                width: 150
                                height: 40
                                color: Theme.backgroundHover
                                border.color: Theme.borderColor
                                border.width: 1
                                
                                Text {
                                    anchors.centerIn: parent
                                    anchors.margins: 8
                                    text: modelData
                                    font.pixelSize: 12
                                    font.weight: Font.DemiBold
                                    font.family: Theme.fontFamily
                                    color: Theme.textPrimary
                                    elide: Text.ElideRight
                                    width: parent.width - 16
                                    horizontalAlignment: Text.AlignHCenter
                                }
                            }
                        }
                    }

                    // Table Rows
                    Repeater {
                        model: bridge ? bridge.previewData : []
                        delegate: Row {
                            height: 36
                            property var rowData: modelData
                            
                            Repeater {
                                model: bridge ? bridge.columnNames : []
                                delegate: Rectangle {
                                    width: 150
                                    height: 36
                                    color: rowMouseArea.containsMouse ? Theme.backgroundHover : Theme.surfaceColor
                                    border.color: Theme.borderColor
                                    border.width: 1
                                    
                                    Behavior on color {
                                        ColorAnimation { duration: 100 }
                                    }
                                    
                                    Text {
                                        anchors.centerIn: parent
                                        anchors.margins: 8
                                        text: parent.parent.rowData[modelData] !== undefined ? parent.parent.rowData[modelData] : ""
                                        color: Theme.textSecondary
                                        font.pixelSize: 11
                                        font.family: Theme.fontFamily
                                        elide: Text.ElideRight
                                        width: parent.width - 16
                                        horizontalAlignment: Text.AlignHCenter
                                    }
                                }
                            }
                            
                            MouseArea {
                                id: rowMouseArea
                                anchors.fill: parent
                                hoverEnabled: true
                            }
                        }
                    }
                }
            }
        }
    }
}
