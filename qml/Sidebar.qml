import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import QtQuick.Effects

Rectangle {
    id: root
    color: "#FAFAFA"
    
    Rectangle {
        anchors.right: parent.right
        width: 1
        height: parent.height
        color: "#E0E0E0"
    }
    
    ImportDialog {
        id: importDialog
    }
    
    ExportDialog {
        id: exportDialog
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 15
        spacing: 12

        // Logo
        Text {
            text: "Transform 3NF"
            color: "#333333"
            font.pixelSize: 16
            font.weight: Font.Bold
            font.family: "Microsoft YaHei UI"
            Layout.alignment: Qt.AlignHCenter
        }

        Rectangle {
            Layout.fillWidth: true
            height: 1
            color: "#E0E0E0"
        }

        Button {
            id: openBtn
            text: "Import"
            Layout.fillWidth: true
            Layout.preferredHeight: 36
            font.pixelSize: 12
            font.family: "Microsoft YaHei UI"
            onClicked: importDialog.open()
            
            contentItem: Text {
                text: parent.text
                color: "white"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font: parent.font
            }
            
            background: Rectangle {
                color: parent.hovered ? "#1565C0" : "#1976D2"
                radius: 4
            }
        }

        Button {
            id: exportBtn
            text: "Export"
            Layout.fillWidth: true
            Layout.preferredHeight: 36
            font.pixelSize: 12
            font.family: "Microsoft YaHei UI"
            onClicked: exportDialog.open()
            
            contentItem: Text {
                text: parent.text
                color: "white"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font: parent.font
            }
            
            background: Rectangle {
                color: parent.hovered ? "#388E3C" : "#4CAF50"
                radius: 4
            }
        }

        Item { Layout.fillHeight: true }

        Text {
            text: "v3.0"
            color: "#999999"
            font.pixelSize: 10
            font.family: "Microsoft YaHei UI"
            Layout.alignment: Qt.AlignHCenter
        }
    }
}
