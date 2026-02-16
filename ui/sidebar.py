import flet as ft

def create_sidebar(page: ft.Page, file_picker, export_picker, update_status):
    def change_theme(e):
        page.theme_mode = ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        theme_icon.icon = ft.icons.DARK_MODE_OUTLINED if page.theme_mode == ft.ThemeMode.LIGHT else ft.icons.LIGHT_MODE_OUTLINED
        page.update()

    theme_icon = ft.IconButton(
        icon=ft.Icons.DARK_MODE_OUTLINED,
        on_click=change_theme,
        tooltip="Chuyển đổi Giao diện",
        icon_color=ft.Colors.BLUE_200,
    )

    def on_export_click(e):
        if not page.session.get("file_path"):
            update_status("❌ Vui lòng tải file CSV trước!", "red")
        else:
            show_export_dialog(page, export_picker, update_status)

    sidebar = ft.Container(
        width=280,
        bgcolor="#0F172A", # Deep Slate/Navy
        padding=ft.padding.all(20),
        content=ft.Column([
            # Logo/Header Section
            ft.Row([
                ft.Icon(ft.Icons.AUTO_AWESOME_MOTION, color=ft.Colors.BLUE_400, size=30),
                ft.Text("Tranform 3NF", size=22, weight=ft.FontWeight.BOLD, color="white"),
            ], alignment=ft.MainAxisAlignment.START, spacing=10),
            
            ft.Container(height=20),
            
            # Action Buttons
            ft.Text("THAO TÁC", size=12, weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_GREY_400, letter_spacing=1.2),
            ft.Divider(color=ft.Colors.BLUE_GREY_800, height=1),
            
            ft.ElevatedButton(
                "📂 Mở File CSV", 
                icon=ft.Icons.UPLOAD_FILE_ROUNDED,
                bgcolor=ft.Colors.BLUE_600, 
                color="white", 
                width=240, 
                height=50,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=12),
                    elevation={"hovered": 5, "": 2},
                ),
                on_click=lambda _: file_picker.pick_files(
                    allow_multiple=False,
                    allowed_extensions=["csv"],
                    dialog_title="Chọn file CSV"
                )
            ),
            
            ft.ElevatedButton(
                "💾 Xuất Kết Quả", 
                icon=ft.Icons.REPLY_ALL_ROUNDED,
                bgcolor=ft.Colors.TEAL_600, 
                color="white", 
                width=240, 
                height=50,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=12),
                    elevation={"hovered": 5, "": 2},
                ),
                on_click=on_export_click
            ),
            
            ft.Spacer(),
            
            # Bottom section
            ft.Divider(color=ft.Colors.BLUE_GREY_800),
            ft.Row([
                ft.Text("Giao diện", color=ft.Colors.BLUE_GREY_200),
                theme_icon
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Text("v2.0.0 - Premium Edition", size=10, color=ft.Colors.BLUE_GREY_600, italic=True)
            
        ], spacing=15, alignment=ft.MainAxisAlignment.START)
    )
    return sidebar


def show_export_dialog(page, export_picker, update_status):
    df = page.session.get("file_path")
    if not df:
        update_status("⚠ Vui lòng tải file CSV trước!", "red")
        return
    
    format_dropdown = ft.Dropdown(
        label="Chọn định dạng xuất",
        options=[ft.dropdown.Option("csv"), ft.dropdown.Option("xlsx"), ft.dropdown.Option("database")],
        value="csv", width=225, border_radius=10, bgcolor="#F9FAFB",
        focused_border_color="#3B82F6"
    )
    
    create_db_button = ft.ElevatedButton(
        "Create DB Scripts", bgcolor="#10B981", color="white",
        width=120, height=40,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), elevation=2),
        on_click=lambda _: (
            page.session.set("export_format", format_dropdown.value),
            export_picker.get_directory_path(dialog_title="Chọn thư mục để lưu script SQL")
        )
    )
    
    normalize_btn = ft.ElevatedButton(
        "Transform", bgcolor="#3B82F6", color="white", width=120, height=40,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), elevation=2),
        on_click=lambda _: (
            page.session.set("export_format", format_dropdown.value),
            export_picker.get_directory_path(dialog_title="Chọn thư mục để lưu dữ liệu chuẩn hóa")
        )
    )
    
    close_btn = ft.IconButton(
        icon=ft.Icons.CLOSE,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), elevation=2),
        on_click=lambda _: (setattr(page.dialog, "open", False), page.update())
    )
    
    def update_dialog_content(e):
        buttons_row = export_dialog.content.content.controls[-1]
        buttons_row.controls.clear()
        if format_dropdown.value == "database":
            buttons_row.controls.extend([format_dropdown, create_db_button, normalize_btn])
        else:
            buttons_row.controls.extend([format_dropdown, normalize_btn])
        page.update()

    format_dropdown.on_change = update_dialog_content
    
    export_dialog = ft.AlertDialog(
        title=ft.Text("Xuất Dữ liệu", size=18, weight="bold", color="#1F2937"),
        content=ft.Container(
            width=page.window_width * 0.3,
            height=page.window_height * 0.3,
            content=ft.Column([
                ft.Row([close_btn], alignment=ft.MainAxisAlignment.END, vertical_alignment=ft.CrossAxisAlignment.START),
                ft.Container(height=10),
                ft.Column([ft.Text("Chọn định dạng và xuất dữ liệu", size=14, color="#6B7280"),
                           ft.Row([format_dropdown, normalize_btn], alignment=ft.MainAxisAlignment.CENTER, spacing=20)])
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=10),
            bgcolor="#FFFFFF", border_radius=10, padding=20
        ),
        bgcolor=ft.Colors.TRANSPARENT,
        modal=True
    )
    
    page.dialog = export_dialog
    export_dialog.open = True
    page.update()