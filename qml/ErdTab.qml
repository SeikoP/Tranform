import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Effects
import "components"

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
        duration: Theme.animationDuration * 4
        easing.type: Easing.OutQuad
    }

    RowLayout {
        anchors.fill: parent
        spacing: 0

        // Left Settings Panel
        Rectangle {
            Layout.fillHeight: true
            Layout.preferredWidth: Theme.erdSidebarWidth
            color: Theme.backgroundSecondary
            border.color: Theme.borderColor
            border.width: 1

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: Theme.spacingXLarge
                spacing: Theme.spacingMedium

                SectionHeader {
                    title: "Thiết kế ERD"
                    accentColor: Theme.primaryColor
                }

                Text {
                    text: "Xác định bảng và mối quan hệ"
                    font.pixelSize: Theme.fontSizeMedium
                    font.family: Theme.fontFamily
                    color: Theme.textSecondary
                    Layout.fillWidth: true
                    wrapMode: Text.WordWrap
                }

                Rectangle {
                    Layout.fillWidth: true
                    height: 1
                    color: Theme.dividerColor
                }

                StyledTextField {
                    id: tableNameInput
                    placeholderText: "Tên bảng..."
                    Layout.fillWidth: true
                    Layout.preferredHeight: Theme.inputHeight
                }

                PrimaryButton {
                    id: createTableBtn
                    text: "Tạo Bảng"
                    Layout.fillWidth: true
                    Layout.preferredHeight: Theme.inputHeight
                    font.weight: Font.DemiBold
                    
                    onClicked: {
                        bridge.add_table(tableNameInput.text)
                        tableNameInput.text = ""
                    }
                }

                Rectangle {
                    Layout.fillWidth: true
                    height: 1
                    color: Theme.dividerColor
                    Layout.topMargin: Theme.spacingXSmall
                }

                Text {
                    text: "TỰ ĐỘNG"
                    font.pixelSize: Theme.fontSizeSmall
                    font.weight: Font.Bold
                    font.family: Theme.fontFamily
                    color: Theme.primaryColor
                    font.letterSpacing: 1
                }

                PrimaryButton {
                    id: aiBtn
                    text: "Đề xuất ERD"
                    Layout.fillWidth: true
                    Layout.preferredHeight: Theme.inputHeight
                    font.weight: Font.DemiBold
                    buttonColor: Theme.accentColor
                    buttonHoverColor: Theme.accentDark
                    
                    onClicked: bridge.suggest_erd()
                }

                Item { Layout.fillHeight: true }
            }
        }

        // Right Canvas Area
        Rectangle {
            Layout.fillHeight: true
            Layout.fillWidth: true
            color: "transparent"
            
            // Info tooltip
            InfoTooltip {
                anchors.top: parent.top
                anchors.right: parent.right
                anchors.margins: Theme.spacingXLarge
                title: "💡 Mẹo"
                message: "Kéo thả để sắp xếp"
                visible: tableRepeater.count > 0
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
