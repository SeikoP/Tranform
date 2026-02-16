import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id: root

    RowLayout {
        anchors.fill: parent
        spacing: 0

        // Left Settings Panel
        Rectangle {
            Layout.fillHeight: true
            Layout.preferredWidth: 320
            color: "#F1F5F9"
            border.color: "#E2E8F0"

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 25
                spacing: 15

                Text {
                    text: "Thiết kế Mô hình"
                    font.pixelSize: 20
                    font.weight: Font.Bold
                    color: "#0F172A"
                }

                Text {
                    text: "Đầu xác định các bảng và mối quan hệ để chuẩn hóa dữ liệu."
                    font.pixelSize: 13
                    color: "#64748B"
                    Layout.fillWidth: true
                    wrapMode: Text.WordWrap
                }

                Rectangle {
                    Layout.fillWidth: true
                    height: 1
                    color: "#E2E8F0"
                }

                TextField {
                    id: tableNameInput
                    placeholderText: "VD: Dim_Customer"
                    Layout.fillWidth: true
                    background: Rectangle {
                        radius: 8
                        color: "white"
                        border.color: tableNameInput.activeFocus ? "#3B82F6" : "#E2E8F0"
                    }
                }

                Button {
                    text: "➕ Tạo Bảng"
                    Layout.fillWidth: true
                    onClicked: {
                        bridge.add_table(tableNameInput.text)
                        tableNameInput.text = ""
                    }
                    background: Rectangle {
                        color: parent.hovered ? "#2563EB" : "#3B82F6"
                        radius: 8
                    }
                    contentItem: Text {
                        text: parent.text
                        color: "white"
                        font.pixelSize: 14
                        horizontalAlignment: Text.AlignHCenter
                    }
                }

                Item { Layout.preferredHeight: 10 }

                Text {
                    text: "TỰ ĐỘNG HÓA"
                    font.pixelSize: 11
                    font.weight: Font.Bold
                    color: "#94A3B8"
                }

                Button {
                    text: "✨ Đề xuất ERD (AI)"
                    Layout.fillWidth: true
                    onClicked: bridge.suggest_erd()
                    background: Rectangle {
                        color: parent.hovered ? "#7C3AED" : "#9333EA"
                        radius: 8
                    }
                    contentItem: Text {
                        text: parent.text
                        color: "white"
                        font.pixelSize: 14
                        horizontalAlignment: Text.AlignHCenter
                    }
                }

                Item { Layout.fillHeight: true }
            }
        }

        // Right Canvas Area
        ScrollView {
            Layout.fillHeight: true
            Layout.fillWidth: true
            clip: true

            Flow {
                id: erdFlow
                width: parent.width
                padding: 30
                spacing: 20

                Repeater {
                    model: bridge ? Object.keys(bridge.tables) : []
                    delegate: TableCard {
                        tableName: modelData
                        columns: bridge ? bridge.tables[modelData] : []
                    }
                }
            }
        }
    }
}
