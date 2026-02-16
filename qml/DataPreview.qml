import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Effects

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
                statColor: "#2196F3"
                Layout.fillWidth: true
                Layout.preferredHeight: 80
            }
            StatCard {
                title: "Số cột"
                value: bridge ? bridge.stats.columns : 0
                icon: "COL"
                statColor: "#9C27B0"
                Layout.fillWidth: true
                Layout.preferredHeight: 80
            }
            StatCard {
                title: "Dim Candidates"
                value: bridge ? bridge.stats.dim : 0
                icon: "DIM"
                statColor: "#FF9800"
                Layout.fillWidth: true
                Layout.preferredHeight: 80
            }
            StatCard {
                title: "Fact Candidates"
                value: bridge ? bridge.stats.fact : 0
                icon: "FCT"
                statColor: "#009688"
                Layout.fillWidth: true
                Layout.preferredHeight: 80
            }
        }

        // Data Preview Title
        Text {
            text: "Xem trước dữ liệu (15 dòng đầu)"
            font.pixelSize: 14
            font.weight: Font.DemiBold
            font.family: "Microsoft YaHei UI"
            color: "#333333"
        }

        // Data Table Container
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "white"
            radius: 4
            border.color: "#E0E0E0"
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
                                color: "#FAFAFA"
                                border.color: "#E0E0E0"
                                border.width: 1
                                
                                Text {
                                    anchors.centerIn: parent
                                    anchors.margins: 8
                                    text: modelData
                                    font.pixelSize: 12
                                    font.weight: Font.DemiBold
                                    font.family: "Microsoft YaHei UI"
                                    color: "#333333"
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
                            
                            Repeater {
                                model: bridge ? bridge.columnNames : []
                                delegate: Rectangle {
                                    width: 150
                                    height: 36
                                    color: rowMouseArea.containsMouse ? "#F5F5F5" : "white"
                                    border.color: "#E0E0E0"
                                    border.width: 1
                                    
                                    Behavior on color {
                                        ColorAnimation { duration: 100 }
                                    }
                                    
                                    Text {
                                        anchors.centerIn: parent
                                        anchors.margins: 8
                                        text: modelData ? parent.parent.modelData[modelData] : ""
                                        color: "#666666"
                                        font.pixelSize: 11
                                        font.family: "Microsoft YaHei UI"
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
