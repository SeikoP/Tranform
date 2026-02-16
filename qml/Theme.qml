pragma Singleton
import QtQuick

QtObject {
    id: theme
    
    // Theme mode
    property bool isDarkMode: false
    
    function toggleTheme() {
        isDarkMode = !isDarkMode
    }
    
    // Primary Colors - Teal/Cyan palette
    readonly property color primaryColor: "#00BCD4"        // Cyan 500
    readonly property color primaryLight: "#4DD0E1"        // Cyan 300
    readonly property color primaryDark: "#0097A7"         // Cyan 700
    readonly property color primaryVeryDark: "#006064"     // Cyan 900
    
    // Accent Colors - Deep Orange for contrast
    readonly property color accentColor: "#FF6F00"         // Orange 900
    readonly property color accentLight: "#FF9800"         // Orange 500
    readonly property color accentDark: "#E65100"          // Orange 900 dark
    
    // Semantic Colors
    readonly property color successColor: "#00C853"        // Green A700
    readonly property color warningColor: "#FFB300"        // Amber 600
    readonly property color errorColor: "#D32F2F"          // Red 700
    readonly property color infoColor: "#0288D1"           // Light Blue 700
    
    // Background Colors - Dynamic based on theme
    property color backgroundPrimary: isDarkMode ? "#1A1A1A" : "#FFFFFF"
    property color backgroundSecondary: isDarkMode ? "#2D2D2D" : "#F5F5F5"
    property color backgroundTertiary: isDarkMode ? "#3D3D3D" : "#FAFAFA"
    property color backgroundHover: isDarkMode ? "#404040" : "#E0F7FA"  // Cyan 50
    
    // Text Colors - Dynamic based on theme
    property color textPrimary: isDarkMode ? "#FFFFFF" : "#212121"
    property color textSecondary: isDarkMode ? "#B0B0B0" : "#616161"
    property color textDisabled: isDarkMode ? "#707070" : "#9E9E9E"
    readonly property color textOnPrimary: "#FFFFFF"
    readonly property color textOnAccent: "#FFFFFF"
    
    // Border & Divider Colors
    property color borderColor: isDarkMode ? "#404040" : "#E0E0E0"
    property color dividerColor: isDarkMode ? "#404040" : "#EEEEEE"
    property color borderFocus: primaryColor
    
    // Table Colors - Cyan/Teal theme
    property color dimTableBg: isDarkMode ? "#004D40" : "#E0F2F1"      // Teal 50/900
    property color factTableBg: isDarkMode ? "#1B5E20" : "#E8F5E9"     // Green 50/900
    
    // Card & Surface Colors
    property color cardBackground: isDarkMode ? "#2D2D2D" : "#FFFFFF"
    property color cardBorder: isDarkMode ? "#404040" : "#E0E0E0"
    property color cardShadow: isDarkMode ? "#000000" : "#00000020"
    
    // Typography
    readonly property string fontFamily: "Segoe UI"
    
    readonly property int fontSizeXLarge: 13
    readonly property int fontSizeLarge: 11
    readonly property int fontSizeMedium: 10
    readonly property int fontSizeSmall: 9
    readonly property int fontSizeXSmall: 8
    readonly property int fontSizeTiny: 7
    readonly property int fontSizeMicro: 6
    
    // Spacing
    readonly property int spacingXXLarge: 16
    readonly property int spacingXLarge: 10
    readonly property int spacingLarge: 8
    readonly property int spacingMedium: 6
    readonly property int spacingSmall: 4
    readonly property int spacingXSmall: 3
    readonly property int spacingTiny: 2
    
    // Padding/Margins
    readonly property int paddingXXXLarge: 20
    readonly property int paddingXXLarge: 16
    readonly property int paddingXLarge: 12
    readonly property int paddingLarge: 10
    readonly property int paddingMedium: 8
    readonly property int paddingSmall: 6
    
    // Sizes
    readonly property int sidebarWidth: 100
    readonly property int erdSidebarWidth: 180
    readonly property int tabBarHeight: 32
    readonly property int statusBarHeight: 20
    readonly property int buttonHeightSmall: 22
    readonly property int buttonHeightMedium: 26
    readonly property int buttonHeightLarge: 30
    readonly property int inputHeight: 28
    
    readonly property int tableCardWidth: 200
    readonly property int tableCardHeaderHeight: 30
    readonly property int tableCardRowHeight: 20
    
    // Border Radius
    readonly property int radiusXXLarge: 12
    readonly property int radiusXLarge: 10
    readonly property int radiusLarge: 6
    readonly property int radiusMedium: 4
    readonly property int radiusSmall: 2
    
    // Border Width
    readonly property int borderWidthThin: 1
    readonly property int borderWidthMedium: 2
    
    // Icon Sizes
    readonly property int iconSizeXLarge: 48
    readonly property int iconSizeLarge: 32
    readonly property int iconSizeMedium: 20
    readonly property int iconSizeSmall: 16
    
    // Dialog specific colors (for dark themed dialogs)
    readonly property color dialogBackground: "#1E293B"
    readonly property color dialogInputBackground: "#0F172A"
    readonly property color dialogTextPrimary: "#E2E8F0"
    readonly property color dialogTextSecondary: "#94A3B8"
    readonly property color dialogBorder: "#334155"
    readonly property color dialogDivider: "#475569"
    
    // Delete/Error button colors
    readonly property color deleteButtonColor: "#EF5350"
    readonly property color deleteButtonHover: "#E53935"
    
    // Success dark variant
    readonly property color successDark: "#00A344"
    
    // Animations
    readonly property int animationDuration: 150
    readonly property int animationDurationFast: 100
    readonly property int animationDurationSlow: 200
}
