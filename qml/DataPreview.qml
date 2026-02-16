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
        anchors.margins: 30
        spacing: 25

        // Stats Cards
        RowLayout {
            Layout.fillWidth: true
            spacing: 20

            StatCard {
                title: "Số bản ghi"
                value: bridge ? bridge.stats.records : 0
                icon: "📊"
                statColor: "#2563EB"
                Layout.fillWidth: true
                Layout.preferredHeight: 100
            }
            StatCard {
                title: "Số cột"
                value: bridge ? bridge.stats.columns : 0
                icon: "📋"
                statColor: "#9333EA"
                Layout.fillWidth: true
                Layout.preferredHeight: 100
            }
            StatCard {
                title: "Dim Candidates"
                value: bridge ? bridge.stats.dim : 0
                icon: "🔍"
                statColor: "#EA580C"
                Layout.fillWidth: true
                Layout.preferredHeight: 100
            }
            StatCard {
                title: "Fact Candidates"
                value: bridge ? bridge.stats.fact : 0
                icon: "📍"
                statColor: "#0D9488"
                Layout.fillWidth: true
                Layout.preferredHeight: 100
            }
        }

        // Data Preview Title
        RowLayout {
            Layout.fillWidth: true
            spacing: 10
            
            Rectangle {
                width: 4
                height: 24
                radius: 2
                gradient: Gradient {
                    GradientStop { position: 0.0; color: "#3B82F6" }
                    GradientStop { position: 1.0; color: "#8B5CF6" }
                }
            }
            
            Text {
                text: "📋 Xem trước Dữ liệu (15 dòng đầu)"
                font.pixelSize: 20
                font.weight: Font.Bold
                color: "white"
            }
        }

        // Data Table Container
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "#1E293B"
            opacity: 0.9
            radius: 16
            border.color: "#334155"
            border.width: 1
            clip: true
            
            layer.enabled: true
            layer.effect: MultiEffect {
                shadowEnabled: true
                shadowColor: "#000000"
                shadowOpacity: 0.4
                shadowBlur: 20
            }

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
                        height: 55
                        
                        Repeater {
                            model: bridge ? bridge.columnNames : []
                            delegate: Rectangle {
                                width: 180
                                height: 55
                                gradient: Gradient {
                                    GradientStop { position: 0.0; color: "#334155" }
                                    GradientStop { position: 1.0; color: "#1E293B" }
                                }
                                border.color: "#475569"
                                
                                Text {
                                    anchors.centerIn: parent
                                    anchors.margins: 10
                                    text: modelData
                                    font.pixelSize: 13
                                    font.weight: Font.Bold
                                    color: "#60A5FA"
                                    elide: Text.ElideRight
                                    width: parent.width - 20
                                    horizontalAlignment: Text.AlignHCenter
                                }
                            }
                        }
                    }

                    // Table Rows
                    Repeater {
                        model: bridge ? bridge.previewData : []
                        delegate: Row {
                            height: 45
                            
                            Repeater {
                                model: bridge ? bridge.columnNames : []
                                delegate: Rectangle {
                                    width: 180
                                    height: 45
                                    color: index % 2 === 0 ? "#0F172A" : "#1E293B"
                                    border.color: "#334155"
                                    opacity: rowMouseArea.containsMouse ? 1.0 : 0.8
                                    
                                    Behavior on opacity {
                                        NumberAnimation { duration: 150 }
                                    }
                                    
                                    Text {
                                        anchors.centerIn: parent
                                        anchors.margins: 10
                                        text: modelData ? parent.parent.modelData[modelData] : ""
                                        color: "#CBD5E1"
                                        font.pixelSize: 13
                                        elide: Text.ElideRight
                                        width: parent.width - 20
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
