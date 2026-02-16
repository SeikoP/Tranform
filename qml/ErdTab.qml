import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Effects
import "components"
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
        duration: Theme.animationDuration * 4
        easing.type: Easing.OutQuad
    }

    RowLayout {
        anchors.fill: parent
        spacing: 0

        // Left Settings Panel - More compact
        Rectangle {
            Layout.fillHeight: true
            Layout.preferredWidth: Theme.erdSidebarWidth
            color: Theme.backgroundSecondary
            border.color: Theme.borderColor
            border.width: Theme.borderWidthThin

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: Theme.paddingMedium
                spacing: Theme.spacingSmall

                SectionHeader {
                    title: "ERD Design"
                    accentColor: Theme.primaryColor
                }

                Text {
                    text: "Define tables & relationships"
                    font.pixelSize: Theme.fontSizeXSmall
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
                    placeholderText: "Table name..."
                    Layout.fillWidth: true
                    Layout.preferredHeight: Theme.inputHeight
                }

                PrimaryButton {
                    id: createTableBtn
                    text: "Create Table"
                    Layout.fillWidth: true
                    Layout.preferredHeight: Theme.buttonHeightMedium
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
                    text: "AUTO GENERATE"
                    font.pixelSize: Theme.fontSizeXSmall
                    font.weight: Font.Bold
                    font.family: Theme.fontFamily
                    color: Theme.primaryColor
                    font.letterSpacing: 0.5
                }

                PrimaryButton {
                    id: aiBtn
                    text: "Suggest ERD"
                    Layout.fillWidth: true
                    Layout.preferredHeight: Theme.buttonHeightMedium
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
                    
                    // Relationship lines layer (behind tables)
                    Item {
                        id: relationshipsLayer
                        anchors.fill: parent
                        z: 0
                        
                        Repeater {
                            id: relationshipRepeater
                            model: getRelationships()
                            
                            delegate: ConnectionLine {
                                startPoint: modelData.start
                                endPoint: modelData.end
                                lineColor: Theme.primaryColor
                                lineWidth: 2
                                relationshipType: modelData.type
                            }
                        }
                    }

                    // Tables layer (on top)
                    Repeater {
                        id: tableRepeater
                        model: bridge ? Object.keys(bridge.tables) : []
                        delegate: TableCard {
                            id: tableCard
                            tableName: modelData
                            columns: bridge ? bridge.tables[modelData] : []
                            z: 1
                            
                            // Initial position with some spacing
                            Component.onCompleted: {
                                var col = index % 3
                                var row = Math.floor(index / 3)
                                x = 50 + col * 320
                                y = 50 + row * 300
                            }
                            
                            // Update relationships when table moves
                            onXChanged: updateRelationships()
                            onYChanged: updateRelationships()
                        }
                    }
                }
            }
        }
    }
    
    // Helper functions
    function getRelationships() {
        if (!bridge || !bridge.tables) return []
        
        var relationships = []
        var tables = bridge.tables
        var tableNames = Object.keys(tables)
        
        // Find all foreign key relationships
        for (var i = 0; i < tableNames.length; i++) {
            var tableName = tableNames[i]
            var columns = tables[tableName]
            
            for (var j = 0; j < columns.length; j++) {
                var col = columns[j]
                if (col.ref_table && tableNames.indexOf(col.ref_table) !== -1) {
                    // Find table positions
                    var sourceTable = findTableCard(tableName)
                    var targetTable = findTableCard(col.ref_table)
                    
                    if (sourceTable && targetTable) {
                        relationships.push({
                            start: Qt.point(
                                sourceTable.x + sourceTable.width / 2,
                                sourceTable.y + sourceTable.height / 2
                            ),
                            end: Qt.point(
                                targetTable.x + targetTable.width / 2,
                                targetTable.y + targetTable.height / 2
                            ),
                            type: "one-to-many"
                        })
                    }
                }
            }
        }
        
        return relationships
    }
    
    function findTableCard(tableName) {
        for (var i = 0; i < tableRepeater.count; i++) {
            var item = tableRepeater.itemAt(i)
            if (item && item.tableName === tableName) {
                return item
            }
        }
        return null
    }
    
    function updateRelationships() {
        relationshipRepeater.model = getRelationships()
    }
    
    Connections {
        target: bridge
        function onErdChanged() {
            updateRelationships()
        }
    }
}
