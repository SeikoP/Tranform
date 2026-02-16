import sys
import os
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import Qt
from bridge import DataBridge

def main():
    # Set environment variables for better scaling on high DPI
    os.environ["QT_QUICK_CONTROLS_STYLE"] = "Basic"
    
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # Create and register the bridge
    bridge = DataBridge()
    engine.rootContext().setContextProperty("bridge", bridge)

    # Load main QML
    qml_file = os.path.join(os.path.dirname(__file__), "qml", "Main.qml")
    
    # Connect warnings to print
    engine.warnings.connect(print)

    engine.load(qml_file)

    if not engine.rootObjects():
        print("Root objects not found. Check QML syntax.")
        sys.exit(-1)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
