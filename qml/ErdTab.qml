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

        // Left Settings Panel - Compact
        Rectangle {
            Layout.fillHeight: true
            Layout.preferredWidth: 260
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
                anchors.margins: 15
                spacing: 10

                RowLayout {
                    spacing: 8
                    
                    Rectangle {
                        width: 3
                        height: 20
                        radius: 2
                        gradient: Gradient {
                            GradientStop { position: 0.0; color: "#3B82F6" }
                            GradientStop { position: 1.0; color: "#8B5CF6" }
                        }
                    }
                    
                    Text {
                        text: "Thiết kế ERD"
                        font.pixelSize: 16
                        font.weight: Font.Bold
                        font.family: "Segoe UI"
                        color: "white"
                    }
                }

                Text {
                    text: "Xác định bảng và mối quan hệ"
                    font.pixelSize: 11
                    font.family: "Segoe UI"
                    color: "#94A3B8"
                    Layout.fillWidth: true
                    wrapMode: Text.WordWrap
                    lineHeight: 1.3
                }

                Rectangle {
                    Layout.fillWidth: true
                    height: 1
                    color: "#334155"
                }

                TextField {
                    id: tableNameInput
                    placeholderText: "Tên bảng..."
                    Layout.fillWidth: true
                    Layout.preferredHeight: 38
                    font.pixelSize: 12
                    color: "white"
                    
                    background: Rectangle {
                        radius: 8
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
                    text: "Tạo Bảng"
                    Layout.fillWidth: true
                    Layout.preferredHeight: 38
                    font.pixelSize: 12
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
                        radius: 8
                        scale: createTableBtn.pressed ? 0.95 : 1.0
                        
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

                Rectangle {
                    Layout.fillWidth: true
                    height: 1
                    color: "#334155"
                    Layout.topMargin: 5
                }

                Text {
                    text: "TỰ ĐỘNG"
                    font.pixelSize: 10
                    font.weight: Font.Bold
                    font.family: "Segoe UI"
                    color: "#60A5FA"
                    font.letterSpacing: 1.2
                }

                Button {
                    id: aiBtn
                    text: "Đề xuất ERD"
                    Layout.fillWidth: true
                    Layout.preferredHeight: 38
                    font.pixelSize: 12
                    font.weight: Font.DemiBold
                    
                    onClicked: bridge.suggest_erd()
                    
                    background: Rectangle {
                        gradient: Gradient {
                            GradientStop { position: 0.0; color: aiBtn.hovered ? "#7C3AED" : "#9333EA" }
                            GradientStop { position: 1.0; color: aiBtn.hovered ? "#6D28D9" : "#7C3AED" }
                        }
                        radius: 8
                        scale: aiBtn.pressed ? 0.95 : 1.0
                        
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
            
            // Info text overlay - compact
            Rectangle {
                anchors.top: parent.top
                anchors.right: parent.right
                anchors.margins: 15
                width: 160
                height: 50
                radius: 6
                color: "#1E293B"
                opacity: 0.9
                visible: tableRepeater.count > 0
                
                ColumnLayout {
                    anchors.centerIn: parent
                    spacing: 2
                    
                    Text {
                        text: "💡 Mẹo"
                        font.pixelSize: 11
                        font.weight: Font.Bold
                        font.family: "Microsoft YaHei UI"
                        color: "#60A5FA"
                        Layout.alignment: Qt.AlignHCenter
                    }
                    
                    Text {
                        text: "Kéo thả để sắp xếp"
                        font.pixelSize: 10
                        font.family: "Microsoft YaHei UI"
                        color: "#94A3B8"
                        Layout.alignment: Qt.AlignHCenter
                    }
                }
            }
            
            // Grid background
            Canvas {
                id: gridCanvas
                anchors.fill: parent
                
                onPaint: {
                    var ctx = getContext("2d")
                    ctx.clearRect(0, 0, width, height)
                    
                    // Draw grid
                    ctx.strokeStyle = "#E0E0E0"
                    ctx.lineWidth = 0.5
                    
                    var gridSize = 20
                    
                    // Vertical lines
                    for (var x = 0; x < width; x += gridSize) {
                        ctx.beginPath()
                        ctx.moveTo(x, 0)
                        ctx.lineTo(x, height)
                        ctx.stroke()
                    }
                    
                    // Horizontal lines
                    for (var y = 0; y < height; y += gridSize) {
                        ctx.beginPath()
                        ctx.moveTo(0, y)
                        ctx.lineTo(width, y)
                        ctx.stroke()
                    }
                }
                
                Component.onCompleted: requestPaint()
            }
            
            ScrollView {
                anchors.fill: parent
                clip: true
                contentWidth: 2000
                contentHeight: 2000
                
                ScrollBar.horizontal.policy: ScrollBar.AsNeeded
                ScrollBar.vertical.policy: ScrollBar.AsNeeded

                Item {
                    id: erdCanvas
                    width: 2000
                    height: 2000

                    Repeater {
                        id: tableRepeater
                        model: bridge ? Object.keys(bridge.tables) : []
                        delegate: TableCard {
                            tableName: modelData
                            columns: bridge ? bridge.tables[modelData] : []
                            
                            // Initial position with some spacing
                            Component.onCompleted: {
                                var col = index % 3
                                var row = Math.floor(index / 3)
                                x = 50 + col * 320
                                y = 50 + row * 300
                            }
                        }
                    }
                }
            }
        }
    }
}
