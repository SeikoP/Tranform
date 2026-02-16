import QtQuick
import QtQuick.Shapes

Shape {
    id: root
    
    property point startPoint: Qt.point(0, 0)
    property point endPoint: Qt.point(100, 100)
    property color lineColor: "#2196F3"
    property real lineWidth: 2
    
    ShapePath {
        strokeColor: root.lineColor
        strokeWidth: root.lineWidth
        fillColor: "transparent"
        
        startX: root.startPoint.x
        startY: root.startPoint.y
        
        PathCubic {
            x: root.endPoint.x
            y: root.endPoint.y
            
            control1X: root.startPoint.x + (root.endPoint.x - root.startPoint.x) / 2
            control1Y: root.startPoint.y
            
            control2X: root.startPoint.x + (root.endPoint.x - root.startPoint.x) / 2
            control2Y: root.endPoint.y
        }
    }
    
    // Arrow head at end point
    Shape {
        x: root.endPoint.x
        y: root.endPoint.y
        
        ShapePath {
            strokeColor: root.lineColor
            fillColor: root.lineColor
            strokeWidth: 1
            
            startX: -8
            startY: -5
            
            PathLine { x: 0; y: 0 }
            PathLine { x: -8; y: 5 }
            PathLine { x: -8; y: -5 }
        }
    }
}
