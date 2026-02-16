pragma Singleton
import QtQuick

QtObject {
    // Colors
    readonly property color primaryColor: "#1976D2"
    readonly property color primaryDark: "#1565C0"
    readonly property color accentColor: "#9C27B0"
    readonly property color accentDark: "#7B1FA2"
    readonly property color successColor: "#4CAF50"
    readonly property color warningColor: "#FF9800"
    
    readonly property color backgroundPrimary: "#FFFFFF"
    readonly property color backgroundSecondary: "#FAFAFA"
    readonly property color backgroundHover: "#F5F5F5"
    
    readonly property color textPrimary: "#212121"
    readonly property color textSecondary: "#757575"
    readonly property color textDisabled: "#9E9E9E"
    readonly property color textOnPrimary: "#FFFFFF"
    
    readonly property color borderColor: "#E0E0E0"
    readonly property color dividerColor: "#E0E0E0"
    
    readonly property color dimTableBg: "#E3F2FD"
    readonly property color factTableBg: "#E8F5E9"
    
    // Typography
    readonly property string fontFamily: "Segoe UI"
    
    readonly property int fontSizeXLarge: 14
    readonly property int fontSizeLarge: 12
    readonly property int fontSizeMedium: 11
    readonly property int fontSizeSmall: 10
    readonly property int fontSizeXSmall: 9
    readonly property int fontSizeTiny: 8
    readonly property int fontSizeMicro: 7
    
    // Spacing
    readonly property int spacingXLarge: 12
    readonly property int spacingLarge: 10
    readonly property int spacingMedium: 8
    readonly property int spacingSmall: 6
    readonly property int spacingXSmall: 4
    readonly property int spacingTiny: 2
    
    // Sizes
    readonly property int sidebarWidth: 120
    readonly property int erdSidebarWidth: 220
    readonly property int tabBarHeight: 36
    readonly property int statusBarHeight: 24
    readonly property int buttonHeightSmall: 24
    readonly property int buttonHeightMedium: 28
    readonly property int buttonHeightLarge: 32
    readonly property int inputHeight: 32
    
    readonly property int tableCardWidth: 240
    readonly property int tableCardHeaderHeight: 36
    readonly property int tableCardRowHeight: 24
    
    // Border Radius
    readonly property int radiusSmall: 2
    readonly property int radiusMedium: 4
    readonly property int radiusLarge: 8
    
    // Animations
    readonly property int animationDuration: 150
    readonly property int animationDurationFast: 100
    readonly property int animationDurationSlow: 200
}
