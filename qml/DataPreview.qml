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

    // New layout: Stats on left, Table on right
    RowLayout {
        anchors.fill: parent
        anchors.margins: Theme.paddingLarge
        spacing: Theme.spacingLarge

        // Left column - Stats and Info
        ColumnLayout {
            Layout.preferredWidth: 200
            Layout.fillHeight: true
            spacing: Theme.spacingMedium

            // Header
            Text {
                text: "📊 Statistics"
                font.pixelSize: Theme.fontSizeLarge
                font.weight: Font.Bold
                font.family: Theme.fontFamily
                color: Theme.textPrimary
            }

            // Stats Cards - vertical
            StatCard {
                title: "Records"
                value: bridge ? bridge.stats.records : 0
                icon: "REC"
                statColor: Theme.primaryColor
                Layout.fillWidth: true
                Layout.preferredHeight: 60
            }
            
            StatCard {
                title: "Columns"
                value: bridge ? bridge.stats.columns : 0
                icon: "COL"
                statColor: Theme.primaryLight
                Layout.fillWidth: true
                Layout.preferredHeight: 60
            }
            
            StatCard {
                title: "Dim Tables"
                value: bridge ? bridge.stats.dim : 0
                icon: "DIM"
                statColor: Theme.warningColor
                Layout.fillWidth: true
                Layout.preferredHeight: 60
            }
            
            StatCard {
                title: "Fact Tables"
                value: bridge ? bridge.stats.fact : 0
                icon: "FCT"
                statColor: Theme.successColor
                Layout.fillWidth: true
                Layout.preferredHeight: 60
            }

            Item { Layout.fillHeight: true }
        }

        // Right column - Data Table
        ColumnLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: Theme.spacingSmall

            // Table Header
            RowLayout {
                Layout.fillWidth: true
                spacing: Theme.spacingMedium

                Text {
                    text: "📋 Data Preview"
                    font.pixelSize: Theme.fontSizeLarge
                    font.weight: Font.Bold
                    font.family: Theme.fontFamily
                    color: Theme.textPrimary
                }

                Item { Layout.fillWidth: true }

                Text {
                    text: "Showing first 15 rows"
                    font.pixelSize: Theme.fontSizeSmall
                    font.family: Theme.fontFamily
                    color: Theme.textSecondary
                }
            }

            // Data Table Container
            Rectangle {
                Layout.fillWidth: true
                Layout.fillHeight: true
                color: Theme.cardBackground
                radius: Theme.radiusSmall
                border.color: Theme.borderColor
                border.width: Theme.borderWidthThin
                clip: true

                ScrollView {
                    anchors.fill: parent
                    ScrollBar.horizontal.policy: ScrollBar.AlwaysOn
                    ScrollBar.vertical.policy: ScrollBar.AlwaysOn
                    
                    ColumnLayout {
                        id: tableContent
                        spacing: 0
                        width: Math.max(parent.width, (bridge ? bridge.columnNames.length : 0) * 120)

                        // Table Header
                        Row {
                            Layout.fillWidth: true
                            height: 28
                            
                            Repeater {
                                model: bridge ? bridge.columnNames : []
                                delegate: Rectangle {
                                    width: 120
                                    height: 28
                                    color: Theme.backgroundHover
                                    border.color: Theme.borderColor
                                    border.width: Theme.borderWidthThin
                                    
                                    Text {
                                        anchors.centerIn: parent
                                        anchors.margins: Theme.paddingSmall
                                        text: modelData
                                        font.pixelSize: Theme.fontSizeSmall
                                        font.weight: Font.DemiBold
                                        font.family: Theme.fontFamily
                                        color: Theme.textPrimary
                                        elide: Text.ElideRight
                                        width: parent.width - Theme.paddingSmall * 2
                                        horizontalAlignment: Text.AlignHCenter
                                    }
                                }
                            }
                        }

                        // Table Rows
                        Repeater {
                            model: bridge ? bridge.previewData : []
                            delegate: Row {
                                height: 24
                                property var rowData: modelData
                                
                                Repeater {
                                    model: bridge ? bridge.columnNames : []
                                    delegate: Rectangle {
                                        width: 120
                                        height: 24
                                        color: rowMouseArea.containsMouse ? Theme.backgroundHover : Theme.cardBackground
                                        border.color: Theme.borderColor
                                        border.width: Theme.borderWidthThin
                                        
                                        Behavior on color {
                                            ColorAnimation { duration: Theme.animationDurationFast }
                                        }
                                        
                                        Text {
                                            anchors.centerIn: parent
                                            anchors.margins: Theme.paddingSmall
                                            text: parent.parent.rowData[modelData] !== undefined ? parent.parent.rowData[modelData] : ""
                                            color: Theme.textSecondary
                                            font.pixelSize: Theme.fontSizeSmall
                                            font.family: Theme.fontFamily
                                            elide: Text.ElideRight
                                            width: parent.width - Theme.paddingSmall * 2
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
}
