import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import QtQuick.Effects

Dialog {
    id: importDialog
    title: "📥 Import Dữ liệu"
    width: 600
    height: 500
    modal: true
    anchors.centerIn: parent
    
    background: Rectangle {
        color: "#1E293B"
        radius: 16
        border.color: "#3B82F6"
        border.width: 2
        
        layer.enabled: true
        layer.effect: MultiEffect {
            shadowEnabled: true
            shadowColor: "#3B82F6"
            shadowOpacity: 0.4
            shadowBlur: 30
        }
    }
    
    FileDialog {
        id: fileDialog
        onAccepted: {
            var path = selectedFile.toString()
            if (sourceTypeCombo.currentIndex === 0) {
                bridge.load_csv(path)
            } else if (sourceTypeCombo.currentIndex === 1) {
                bridge.load_excel(path)
            } else if (sourceTypeCombo.currentIndex === 2) {
                bridge.load_json(path)
            } else if (sourceTypeCombo.currentIndex === 3) {
                bridge.load_sqlite(path, tableNameField.text)
            }
            importDialog.close()
        }
    }
    
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 25
        spacing: 20
        
        // Header
        RowLayout {
            spacing: 15
            
            Rectangle {
                width: 50
                height: 50
                radius: 12
                gradient: Gradient {
                    GradientStop { position: 0.0; color: "#3B82F6" }
                    GradientStop { position: 1.0; color: "#8B5CF6" }
                }
                
                Text {
                    anchors.centerIn: parent
                    text: "IN"
                    font.pixelSize: 16
                    font.weight: Font.Bold
                    font.family: "Segoe UI"
                    color: "white"
                }
            }
            
            ColumnLayout {
                spacing: 2
                Text {
                    text: "Import Dữ liệu"
                    font.pixelSize: 22
                    font.weight: Font.Bold
                    font.family: "Segoe UI"
                    color: "white"
                }
                Text {
                    text: "Chọn nguồn dữ liệu để import"
                    font.pixelSize: 13
                    font.family: "Segoe UI"
                    color: "#94A3B8"
                }
            }
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
        
        // Source Type Selection
        ColumnLayout {
            spacing: 10
            
            Text {
                text: "Loại nguồn dữ liệu:"
                font.pixelSize: 14
                font.weight: Font.Medium
                color: "#E2E8F0"
            }
            
            ComboBox {
                id: sourceTypeCombo
                Layout.fillWidth: true
                Layout.preferredHeight: 50
                model: ["CSV File", "Excel File", "JSON File", "SQLite Database", "MySQL", "PostgreSQL"]
                font.pixelSize: 14
                
                background: Rectangle {
                    color: "#0F172A"
                    radius: 12
                    border.color: sourceTypeCombo.activeFocus ? "#3B82F6" : "#334155"
                    border.width: 2
                }
                
                contentItem: Text {
                    text: sourceTypeCombo.displayText
                    color: "#E2E8F0"
                    font: sourceTypeCombo.font
                    verticalAlignment: Text.AlignVCenter
                    leftPadding: 15
                }
            }
        }
        
        // Dynamic content based on selection
        StackLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            currentIndex: sourceTypeCombo.currentIndex
            
            // CSV, Excel, JSON - File selection
            Item {
                ColumnLayout {
                    anchors.fill: parent
                    spacing: 15
                    
                    Text {
                        text: "Chọn file CSV để import"
                        font.pixelSize: 13
                        color: "#94A3B8"
                    }
                    
                    Button {
                        text: "Chọn File CSV"
                        Layout.fillWidth: true
                        Layout.preferredHeight: 50
                        onClicked: {
                            fileDialog.nameFilters = ["CSV files (*.csv)"]
                            fileDialog.open()
                        }
                        
                        background: Rectangle {
                            gradient: Gradient {
                                GradientStop { position: 0.0; color: parent.hovered ? "#2563EB" : "#3B82F6" }
                                GradientStop { position: 1.0; color: parent.hovered ? "#1E40AF" : "#2563EB" }
                            }
                            radius: 12
                        }
                        
                        contentItem: Text {
                            text: parent.text
                            color: "white"
                            font.pixelSize: 15
                            font.weight: Font.DemiBold
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                    }
                }
            }
            
            Item {
                ColumnLayout {
                    anchors.fill: parent
                    spacing: 15
                    
                    Text {
                        text: "Chọn file Excel để import"
                        font.pixelSize: 13
                        color: "#94A3B8"
                    }
                    
                    Button {
                        text: "Chọn File Excel"
                        Layout.fillWidth: true
                        Layout.preferredHeight: 50
                        onClicked: {
                            fileDialog.nameFilters = ["Excel files (*.xlsx *.xls)"]
                            fileDialog.open()
                        }
                        
                        background: Rectangle {
                            gradient: Gradient {
                                GradientStop { position: 0.0; color: parent.hovered ? "#059669" : "#10B981" }
                                GradientStop { position: 1.0; color: parent.hovered ? "#047857" : "#059669" }
                            }
                            radius: 12
                        }
                        
                        contentItem: Text {
                            text: parent.text
                            color: "white"
                            font.pixelSize: 15
                            font.weight: Font.DemiBold
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                    }
                }
            }
            
            Item {
                ColumnLayout {
                    anchors.fill: parent
                    spacing: 15
                    
                    Text {
                        text: "Chọn file JSON để import"
                        font.pixelSize: 13
                        color: "#94A3B8"
                    }
                    
                    Button {
                        text: "Chọn File JSON"
                        Layout.fillWidth: true
                        Layout.preferredHeight: 50
                        onClicked: {
                            fileDialog.nameFilters = ["JSON files (*.json)"]
                            fileDialog.open()
                        }
                        
                        background: Rectangle {
                            gradient: Gradient {
                                GradientStop { position: 0.0; color: parent.hovered ? "#7C3AED" : "#9333EA" }
                                GradientStop { position: 1.0; color: parent.hovered ? "#6D28D9" : "#7C3AED" }
                            }
                            radius: 12
                        }
                        
                        contentItem: Text {
                            text: parent.text
                            color: "white"
                            font.pixelSize: 15
                            font.weight: Font.DemiBold
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                    }
                }
            }
            
            // SQLite
            Item {
                ColumnLayout {
                    anchors.fill: parent
                    spacing: 15
                    
                    Text {
                        text: "Tên bảng trong database:"
                        font.pixelSize: 13
                        color: "#94A3B8"
                    }
                    
                    TextField {
                        id: tableNameField
                        Layout.fillWidth: true
                        Layout.preferredHeight: 50
                        placeholderText: "VD: customers"
                        font.pixelSize: 14
                        color: "white"
                        
                        background: Rectangle {
                            color: "#0F172A"
                            radius: 12
                            border.color: parent.activeFocus ? "#3B82F6" : "#334155"
                            border.width: 2
                        }
                    }
                    
                    Button {
                        text: "Chọn SQLite Database"
                        Layout.fillWidth: true
                        Layout.preferredHeight: 50
                        onClicked: {
                            fileDialog.nameFilters = ["SQLite files (*.db *.sqlite)"]
                            fileDialog.open()
                        }
                        
                        background: Rectangle {
                            gradient: Gradient {
                                GradientStop { position: 0.0; color: parent.hovered ? "#B45309" : "#F59E0B" }
                                GradientStop { position: 1.0; color: parent.hovered ? "#92400E" : "#D97706" }
                            }
                            radius: 12
                        }
                        
                        contentItem: Text {
                            text: parent.text
                            color: "white"
                            font.pixelSize: 15
                            font.weight: Font.DemiBold
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                    }
                }
            }
            
            // MySQL
            Item {
                ScrollView {
                    anchors.fill: parent
                    
                    ColumnLayout {
                        width: parent.width
                        spacing: 12
                        
                        TextField {
                            id: mysqlHost
                            Layout.fillWidth: true
                            placeholderText: "Host (VD: localhost)"
                            font.pixelSize: 13
                            color: "white"
                            background: Rectangle {
                                color: "#0F172A"
                                radius: 8
                                border.color: parent.activeFocus ? "#3B82F6" : "#334155"
                            }
                        }
                        
                        TextField {
                            id: mysqlUser
                            Layout.fillWidth: true
                            placeholderText: "Username"
                            font.pixelSize: 13
                            color: "white"
                            background: Rectangle {
                                color: "#0F172A"
                                radius: 8
                                border.color: parent.activeFocus ? "#3B82F6" : "#334155"
                            }
                        }
                        
                        TextField {
                            id: mysqlPassword
                            Layout.fillWidth: true
                            placeholderText: "Password"
                            echoMode: TextInput.Password
                            font.pixelSize: 13
                            color: "white"
                            background: Rectangle {
                                color: "#0F172A"
                                radius: 8
                                border.color: parent.activeFocus ? "#3B82F6" : "#334155"
                            }
                        }
                        
                        TextField {
                            id: mysqlDatabase
                            Layout.fillWidth: true
                            placeholderText: "Database name"
                            font.pixelSize: 13
                            color: "white"
                            background: Rectangle {
                                color: "#0F172A"
                                radius: 8
                                border.color: parent.activeFocus ? "#3B82F6" : "#334155"
                            }
                        }
                        
                        TextField {
                            id: mysqlTable
                            Layout.fillWidth: true
                            placeholderText: "Table name"
                            font.pixelSize: 13
                            color: "white"
                            background: Rectangle {
                                color: "#0F172A"
                                radius: 8
                                border.color: parent.activeFocus ? "#3B82F6" : "#334155"
                            }
                        }
                        
                        Button {
                            text: "Kết nối MySQL"
                            Layout.fillWidth: true
                            Layout.preferredHeight: 45
                            onClicked: {
                                bridge.load_mysql(mysqlHost.text, mysqlUser.text, 
                                                mysqlPassword.text, mysqlDatabase.text, mysqlTable.text)
                                importDialog.close()
                            }
                            
                            background: Rectangle {
                                color: parent.hovered ? "#0369A1" : "#0284C7"
                                radius: 10
                            }
                            
                            contentItem: Text {
                                text: parent.text
                                color: "white"
                                font.pixelSize: 14
                                font.weight: Font.DemiBold
                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter
                            }
                        }
                    }
                }
            }
            
            // PostgreSQL
            Item {
                ScrollView {
                    anchors.fill: parent
                    
                    ColumnLayout {
                        width: parent.width
                        spacing: 12
                        
                        TextField {
                            id: pgHost
                            Layout.fillWidth: true
                            placeholderText: "Host (VD: localhost)"
                            font.pixelSize: 13
                            color: "white"
                            background: Rectangle {
                                color: "#0F172A"
                                radius: 8
                                border.color: parent.activeFocus ? "#3B82F6" : "#334155"
                            }
                        }
                        
                        TextField {
                            id: pgUser
                            Layout.fillWidth: true
                            placeholderText: "Username"
                            font.pixelSize: 13
                            color: "white"
                            background: Rectangle {
                                color: "#0F172A"
                                radius: 8
                                border.color: parent.activeFocus ? "#3B82F6" : "#334155"
                            }
                        }
                        
                        TextField {
                            id: pgPassword
                            Layout.fillWidth: true
                            placeholderText: "Password"
                            echoMode: TextInput.Password
                            font.pixelSize: 13
                            color: "white"
                            background: Rectangle {
                                color: "#0F172A"
                                radius: 8
                                border.color: parent.activeFocus ? "#3B82F6" : "#334155"
                            }
                        }
                        
                        TextField {
                            id: pgDatabase
                            Layout.fillWidth: true
                            placeholderText: "Database name"
                            font.pixelSize: 13
                            color: "white"
                            background: Rectangle {
                                color: "#0F172A"
                                radius: 8
                                border.color: parent.activeFocus ? "#3B82F6" : "#334155"
                            }
                        }
                        
                        TextField {
                            id: pgTable
                            Layout.fillWidth: true
                            placeholderText: "Table name"
                            font.pixelSize: 13
                            color: "white"
                            background: Rectangle {
                                color: "#0F172A"
                                radius: 8
                                border.color: parent.activeFocus ? "#3B82F6" : "#334155"
                            }
                        }
                        
                        Button {
                            text: "Kết nối PostgreSQL"
                            Layout.fillWidth: true
                            Layout.preferredHeight: 45
                            onClicked: {
                                bridge.load_postgresql(pgHost.text, pgUser.text, 
                                                      pgPassword.text, pgDatabase.text, pgTable.text)
                                importDialog.close()
                            }
                            
                            background: Rectangle {
                                color: parent.hovered ? "#1E40AF" : "#2563EB"
                                radius: 10
                            }
                            
                            contentItem: Text {
                                text: parent.text
                                color: "white"
                                font.pixelSize: 14
                                font.weight: Font.DemiBold
                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter
                            }
                        }
                    }
                }
            }
        }
        
        Item { Layout.fillHeight: true }
        
        // Close button
        Button {
            text: "Đóng"
            Layout.alignment: Qt.AlignRight
            Layout.preferredWidth: 100
            onClicked: importDialog.close()
            
            background: Rectangle {
                color: parent.hovered ? "#475569" : "#334155"
                radius: 8
            }
            
            contentItem: Text {
                text: parent.text
                color: "#E2E8F0"
                font.pixelSize: 13
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
        }
    }
}
