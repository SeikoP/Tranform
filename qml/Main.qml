import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Window
import QtQuick.Effects
import "."

ApplicationWindow {
    visible: true
    width: 1200
    height: 750
    minimumWidth: 1000
    minimumHeight: 650
    title: "Transform 3NF"
    color: Theme.backgroundColor
    
    // Clean flat background
    Rectangle {
        anchors.fill: parent
        color: Theme.backgroundColor
    }

    RowLayout {
        anchors.fill: parent
        spacing: 0

        // Sidebar component
        Sidebar {
            id: sidebar
            Layout.fillHeight: true
            Layout.preferredWidth: 120
        }

        // Main Content Area
        ColumnLayout {
            Layout.fillHeight: true
            Layout.fillWidth: true
            spacing: 0

            // Header / Navigation Tabs area - compact
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 36
                color: Theme.surfaceColor
                
                Rectangle {
                    anchors.bottom: parent.bottom
                    width: parent.width
                    height: 1
                    color: Theme.borderColor
                }
                
                TabBar {
                    id: mainTabs
                    anchors.fill: parent
                    anchors.leftMargin: 8
                    background: Rectangle { color: "transparent" }
                    
                    TabButton { 
                        text: "Dữ liệu"
                        font.pixelSize: 12
                        font.family: Theme.fontFamily
                        
                        contentItem: Text {
                            text: parent.text
                            font: parent.font
                            color: parent.checked ? Theme.primaryColor : Theme.textSecondary
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                        
                        background: Rectangle {
                            color: "transparent"
                            
                            Rectangle {
                                anchors.bottom: parent.bottom
                                width: parent.width
                                height: 2
                                color: Theme.primaryColor
                                visible: parent.parent.checked
                            }
                        }
                    }
                    
                    TabButton { 
                        text: "ETL"
                        font.pixelSize: 12
                        font.family: Theme.fontFamily
                        
                        contentItem: Text {
                            text: parent.text
                            font: parent.font
                            color: parent.checked ? Theme.primaryColor : Theme.textSecondary
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                        
                        background: Rectangle {
                            color: "transparent"
                            
                            Rectangle {
                                anchors.bottom: parent.bottom
                                width: parent.width
                                height: 2
                                color: Theme.primaryColor
                                visible: parent.parent.checked
                            }
                        }
                    }
                    
                    TabButton { 
                        text: "Mô hình ERD"
                        font.pixelSize: 12
                        font.family: Theme.fontFamily
                        
                        contentItem: Text {
                            text: parent.text
                            font: parent.font
                            color: parent.checked ? Theme.primaryColor : Theme.textSecondary
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                        
                        background: Rectangle {
                            color: "transparent"
                            
                            Rectangle {
                                anchors.bottom: parent.bottom
                                width: parent.width
                                height: 2
                                color: Theme.primaryColor
                                visible: parent.parent.checked
                            }
                        }
                    }
                }
            }

            StackLayout {
                id: contentStack
                currentIndex: mainTabs.currentIndex
                Layout.fillWidth: true
                Layout.fillHeight: true

                DataPreview {
                    // Component for data preview
                }
                
                ETLTab {
                    // Component for ETL Pipeline
                }

                ErdTab {
                    // Component for ERD
                }
            }

            // Status Bar - compact
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 24
                color: Theme.surfaceColor
                
                Rectangle {
                    anchors.top: parent.top
                    width: parent.width
                    height: 1
                    color: Theme.borderColor
                }
                
                RowLayout {
                    anchors.fill: parent
                    anchors.leftMargin: 12
                    anchors.rightMargin: 12
                    spacing: 8
                    
                    Rectangle {
                        width: 5
                        height: 5
                        radius: 2.5
                        color: statusText.color
                    }
                    
                    Text {
                        id: statusText
                        text: "Sẵn sàng"
                        font.pixelSize: 11
                        font.family: Theme.fontFamily
                        color: Theme.successColor
                    }
                    
                    Item { Layout.fillWidth: true }
                    
                    Text {
                        text: "v3.0"
                        font.pixelSize: 10
                        font.family: Theme.fontFamily
                        color: Theme.textSecondary
                    }
                }
                
                Connections {
                    target: bridge
                    function onStatusChanged(message, color) {
                        statusText.text = message
                        if (color === "red") statusText.color = Theme.errorColor
                        else if (color === "green") statusText.color = Theme.successColor
                        else statusText.color = Theme.primaryColor
                    }
                }
            }
        }
    }
}
