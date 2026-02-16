import QtQuick
import QtQuick.Shapes
import ".."

Shape {
    id: root
    
    property point startPoint: Qt.point(0, 0)
    property point endPoint: Qt.point(100, 100)
    property color lineColor: Theme.primaryColor
    property real lineWidth: 2
    property string relationshipType: "one-to-many" // "one-to-one", "one-to-many", "many-to-many"
    
    ShapePath {
        strokeColor: root.lineColor
        strokeWidth: root.lineWidth
        fillColor: "transparent"
        
        startX: root.startPoint.x
        startY: root.startPoint.y
        
        // Curved line for better visibility
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
    Canvas {
        id: arrowCanvas
        x: root.endPoint.x - 10
        y: root.endPoint.y - 10
        width: 20
        height: 20
        
        onPaint: {
            var ctx = getContext("2d")
            ctx.clearRect(0, 0, width, height)
            
            // Calculate arrow angle
            var dx = root.endPoint.x - root.startPoint.x
            var dy = root.endPoint.y - root.startPoint.y
            var angle = Math.atan2(dy, dx)
            
            ctx.save()
            ctx.translate(10, 10)
            ctx.rotate(angle)
            
            // Draw arrow
            ctx.fillStyle = root.lineColor
            ctx.beginPath()
            ctx.moveTo(8, 0)
            ctx.lineTo(0, -5)
            ctx.lineTo(0, 5)
            ctx.closePath()
            ctx.fill()
            
            // Draw relationship indicator
            if (root.relationshipType === "many-to-many") {
                ctx.beginPath()
                ctx.moveTo(-8, -5)
                ctx.lineTo(-8, 5)
                ctx.stroke()
            }
            
            ctx.restore()
        }
        
        Connections {
            target: root
            function onEndPointChanged() { arrowCanvas.requestPaint() }
            function onStartPointChanged() { arrowCanvas.requestPaint() }
        }
    }
    
    // Start point indicator (for FK)
    Rectangle {
        x: root.startPoint.x - 3
        y: root.startPoint.y - 3
        width: 6
        height: 6
        radius: 3
        color: root.lineColor
        border.color: Theme.backgroundPrimary
        border.width: 1
    }
}
