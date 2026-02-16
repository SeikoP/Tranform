import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id: root

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
        Text {
            text: "Xem trước Dữ liệu (15 dòng đầu):"
            font.pixelSize: 18
            font.weight: Font.DemiBold
            color: "#1E293B"
        }

        // Data Table Container
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "white"
            radius: 12
            border.color: "#E2E8F0"
            clip: true

            ScrollView {
                anchors.fill: parent
                ScrollBar.horizontal.policy: ScrollBar.AlwaysOn
                
                ColumnLayout {
                    id: tableContent
                    spacing: 0
                    width: Math.max(parent.width, (bridge ? bridge.columnNames.length : 0) * 150)

                    // Table Header
                    Row {
                        Layout.fillWidth: true
                        height: 50
                        
                        Repeater {
                            model: bridge ? bridge.columnNames : []
                            delegate: Rectangle {
                                width: 150; height: 50
                                color: "#F8FAFC"
                                border.color: "#E2E8F0"
                                Text {
                                    anchors.centerIn: parent
                                    text: modelData
                                    font.bold: true
                                    color: "#475569"
                                    elide: Text.ElideRight
                                }
                            }
                        }
                    }

                    // Table Rows
                    Repeater {
                        model: bridge ? bridge.previewData : []
                        delegate: Row {
                            height: 40
                            Repeater {
                                model: bridge ? bridge.columnNames : []
                                delegate: Rectangle {
                                    width: 150; height: 40
                                    border.color: "#F1F5F9"
                                    Text {
                                        anchors.centerIn: parent
                                        text: modelData ? parent.parent.modelData[modelData] : ""
                                        color: "#64748B"
                                        font.pixelSize: 12
                                        elide: Text.ElideRight
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
