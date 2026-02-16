import QtQuick

Item {
    id: root
    
    signal importRequested()
    signal exportRequested()
    signal suggestErdRequested()
    signal toggleThemeRequested()
    signal saveRequested()
    signal undoRequested()
    signal redoRequested()
    
    focus: true
    
    Keys.onPressed: function(event) {
        // Ctrl+I: Import
        if (event.key === Qt.Key_I && event.modifiers & Qt.ControlModifier) {
            importRequested()
            event.accepted = true
        }
        // Ctrl+E: Export
        else if (event.key === Qt.Key_E && event.modifiers & Qt.ControlModifier) {
            exportRequested()
            event.accepted = true
        }
        // Ctrl+G: Generate/Suggest ERD
        else if (event.key === Qt.Key_G && event.modifiers & Qt.ControlModifier) {
            suggestErdRequested()
            event.accepted = true
        }
        // Ctrl+T: Toggle Theme
        else if (event.key === Qt.Key_T && event.modifiers & Qt.ControlModifier) {
            toggleThemeRequested()
            event.accepted = true
        }
        // Ctrl+S: Save
        else if (event.key === Qt.Key_S && event.modifiers & Qt.ControlModifier) {
            saveRequested()
            event.accepted = true
        }
        // Ctrl+Z: Undo
        else if (event.key === Qt.Key_Z && event.modifiers & Qt.ControlModifier) {
            undoRequested()
            event.accepted = true
        }
        // Ctrl+Y: Redo
        else if (event.key === Qt.Key_Y && event.modifiers & Qt.ControlModifier) {
            redoRequested()
            event.accepted = true
        }
    }
}
