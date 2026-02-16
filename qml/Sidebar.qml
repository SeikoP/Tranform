import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import QtQuick.Effects
import "components"

Rectangle {
    id: root
    color: Theme.backgroundPrimary
    
    Behavior on color {
        ColorAnimation { duration: Theme.animationDuration }
    }
    
    Rectangle {
        anchors.right: parent.right
        width: 1
        height: parent.height
        color: Theme.borderColor
    }
    
    ImportDialog {
        id: importDialog
    }
    
    ExportDialog {
        id: exportDialog
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: Theme.spacingMedium
        spacing: Theme.spacingSmall

        // Logo
        Text {
            text: "Transform 3NF"
            color: Theme.textPrimary
            font.pixelSize: Theme.fontSizeLarge
            font.weight: Font.Bold
            font.family: Theme.fontFamily
            Layout.alignment: Qt.AlignHCenter
        }

        Rectangle {
            Layout.fillWidth: true
            height: 1
            color: Theme.dividerColor
        }

        PrimaryButton {
            text: "Import"
            Layout.fillWidth: true
            Layout.preferredHeight: Theme.buttonHeightMedium
            onClicked: importDialog.open()
        }

        PrimaryButton {
            text: "Export"
            Layout.fillWidth: true
            Layout.preferredHeight: Theme.buttonHeightMedium
            buttonColor: Theme.successColor
            buttonHoverColor: "#388E3C"
            onClicked: exportDialog.open()
        }

        Item { Layout.fillHeight: true }
        
        // Theme toggle
        ThemeToggle {
            Layout.alignment: Qt.AlignHCenter
        }
        
        Rectangle {
            Layout.fillWidth: true
            height: 1
            color: Theme.dividerColor
        }

        Text {
            text: "v3.0"
            color: Theme.textDisabled
            font.pixelSize: Theme.fontSizeXSmall
            font.family: Theme.fontFamily
            Layout.alignment: Qt.AlignHCenter
        }
    }
}
