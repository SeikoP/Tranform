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

    RowLayout {
        anchors.fill: parent
        spacing: 0

        // Left Settings Panel
        Rectangle {
            Layout.fillHeight: true
            Layout.preferredWidth: 360
            color: "#1E293B"
            opacity: 0.95
            border.color: "#334155"
            border.width: 1
            
            layer.enabled: true
            layer.effect: MultiEffect {
                shadowEnabled: true
                shadowColor: "#000000"
                shadowOpacity: 0.4
                shadowBlur: 20
            }

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 25
                spacing: 15

                RowLayout {
                    spacing: 10
                    
                    Rectangle {
                        width: 4
                        height: 28
                        radius: 2
                        gradient: Gradient {
                            GradientStop { position: 0.0; color: "#3B82F6" }
                            GradientStop { position: 1.0; color: "#8B5CF6" }
                        }
                    }
                    
                    Text {
                        text: "Thiết kế Mô hình"
                        font.pixelSize: 22
                        font.weight: Font.Bold
                        font.family: "Segoe UI"
                        color: "white"
                    }
                }

                Text {
                    text: "Xác định các bảng và mối quan hệ để chuẩn hóa dữ liệu lên 3NF."
                    font.pixelSize: 14
                    font.family: "Segoe UI"
                    color: "#94A3B8"
                    Layout.fillWidth: true
                    wrapMode: Text.WordWrap
                    lineHeight: 1.4
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
                }

                TextField {
                    id: tableNameInput
                    placeholderText: "VD: Dim_Customer"
                    Layout.fillWidth: true
                    Layout.preferredHeight: 50
                    font.pixelSize: 14
                    color: "white"
                    
                    background: Rectangle {
                        radius: 12
                        color: "#0F172A"
                        border.color: tableNameInput.activeFocus ? "#3B82F6" : "#334155"
                        border.width: 2
                        
                        Behavior on border.color {
                            ColorAnimation { duration: 200 }
                        }
                    }
                }

                Button {
                    id: createTableBtn
                    text: "Tạo Bảng Mới"
                    Layout.fillWidth: true
                    Layout.preferredHeight: 50
                    font.pixelSize: 15
                    font.weight: Font.DemiBold
                    
                    onClicked: {
                        bridge.add_table(tableNameInput.text)
                        tableNameInput.text = ""
                    }
                    
                    background: Rectangle {
                        gradient: Gradient {
                            GradientStop { position: 0.0; color: createTableBtn.hovered ? "#2563EB" : "#3B82F6" }
                            GradientStop { position: 1.0; color: createTableBtn.hovered ? "#1E40AF" : "#2563EB" }
                        }
                        radius: 12
                        scale: createTableBtn.pressed ? 0.95 : 1.0
                        
                        layer.enabled: createTableBtn.hovered
                        layer.effect: MultiEffect {
                            shadowEnabled: true
                            shadowColor: "#3B82F6"
                            shadowOpacity: 0.6
                            shadowBlur: 20
                        }
                        
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

                Item { Layout.preferredHeight: 15 }

                Text {
                    text: "TỰ ĐỘNG HÓA"
                    font.pixelSize: 12
                    font.weight: Font.Bold
                    font.family: "Segoe UI"
                    color: "#60A5FA"
                    font.letterSpacing: 1.5
                }

                Button {
                    id: aiBtn
                    text: "Đề xuất ERD (AI)"
                    Layout.fillWidth: true
                    Layout.preferredHeight: 50
                    font.pixelSize: 15
                    font.weight: Font.DemiBold
                    
                    onClicked: bridge.suggest_erd()
                    
                    background: Rectangle {
                        gradient: Gradient {
                            GradientStop { position: 0.0; color: aiBtn.hovered ? "#7C3AED" : "#9333EA" }
                            GradientStop { position: 1.0; color: aiBtn.hovered ? "#6D28D9" : "#7C3AED" }
                        }
                        radius: 12
                        scale: aiBtn.pressed ? 0.95 : 1.0
                        
                        layer.enabled: aiBtn.hovered
                        layer.effect: MultiEffect {
                            shadowEnabled: true
                            shadowColor: "#9333EA"
                            shadowOpacity: 0.6
                            shadowBlur: 20
                        }
                        
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

                Item { Layout.fillHeight: true }
            }
        }

        // Right Canvas Area
        Rectangle {
            Layout.fillHeight: true
            Layout.fillWidth: true
            color: "transparent"
            
            ScrollView {
                anchors.fill: parent
                clip: true

                Flow {
                    id: erdFlow
                    width: parent.width
                    padding: 30
                    spacing: 25

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
}
