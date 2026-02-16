import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Window
import QtQuick.Effects

ApplicationWindow {
    visible: true
    width: 1100
    height: 700
    minimumWidth: 900
    minimumHeight: 600
    title: "Transform 3NF"
    color: "#FFFFFF"
    
    // Clean flat background
    Rectangle {
        anchors.fill: parent
        color: "#FFFFFF"
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
                color: "#FAFAFA"
                
                Rectangle {
                    anchors.bottom: parent.bottom
                    width: parent.width
                    height: 1
                    color: "#E0E0E0"
                }
                
                TabBar {
                    id: mainTabs
                    anchors.fill: parent
                    anchors.leftMargin: 8
                    background: Rectangle { color: "transparent" }
                    
                    TabButton { 
                        text: "Dữ liệu"
                        font.pixelSize: 12
                        font.family: "Segoe UI"
                        
                        contentItem: Text {
                            text: parent.text
                            font: parent.font
                            color: parent.checked ? "#1976D2" : "#757575"
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                        
                        background: Rectangle {
                            color: "transparent"
                            
                            Rectangle {
                                anchors.bottom: parent.bottom
                                width: parent.width
                                height: 2
                                color: "#1976D2"
                                visible: parent.parent.checked
                            }
                        }
                    }
                    
                    TabButton { 
                        text: "ETL"
                        font.pixelSize: 12
                        font.family: "Segoe UI"
                        
                        contentItem: Text {
                            text: parent.text
                            font: parent.font
                            color: parent.checked ? "#1976D2" : "#757575"
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                        
                        background: Rectangle {
                            color: "transparent"
                            
                            Rectangle {
                                anchors.bottom: parent.bottom
                                width: parent.width
                                height: 2
                                color: "#1976D2"
                                visible: parent.parent.checked
                            }
                        }
                    }
                    
                    TabButton { 
                        text: "Mô hình ERD"
                        font.pixelSize: 12
                        font.family: "Segoe UI"
                        
                        contentItem: Text {
                            text: parent.text
                            font: parent.font
                            color: parent.checked ? "#1976D2" : "#757575"
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                        
                        background: Rectangle {
                            color: "transparent"
                            
                            Rectangle {
                                anchors.bottom: parent.bottom
                                width: parent.width
                                height: 2
                                color: "#1976D2"
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
                color: "#FAFAFA"
                
                Rectangle {
                    anchors.top: parent.top
                    width: parent.width
                    height: 1
                    color: "#E0E0E0"
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
                        font.family: "Segoe UI"
                        color: "#4CAF50"
                    }
                    
                    Item { Layout.fillWidth: true }
                    
                    Text {
                        text: "v3.0"
                        font.pixelSize: 10
                        font.family: "Segoe UI"
                        color: "#9E9E9E"
                    }
                }
                
                Connections {
                    target: bridge
                    function onStatusChanged(message, color) {
                        statusText.text = message
                        if (color === "red") statusText.color = "#F44336"
                        else if (color === "green") statusText.color = "#4CAF50"
                        else statusText.color = "#2196F3"
                    }
                }
            }
        }
    }
}
