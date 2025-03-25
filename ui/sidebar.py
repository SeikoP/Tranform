import flet as ft

def create_sidebar(page: ft.Page, file_picker, export_picker, update_status):
    def change_theme(e):
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        theme_icon.icon = ft.icons.DARK_MODE if page.theme_mode == "light" else ft.icons.LIGHT_MODE
        page.update()

    theme_icon = ft.IconButton(
        icon=ft.icons.DARK_MODE if page.theme_mode == "light" else ft.icons.LIGHT_MODE,
        on_click=change_theme,
        tooltip="Chuyển đổi theme"
    )

    def on_export_click(e):
        if not page.session.get("file_path"):
            update_status("❌ Vui lòng tải file CSV trước!", "red")
        else:
            show_export_dialog(page, export_picker, update_status)

    sidebar = ft.Container(
        width=250,
        bgcolor="#1F2937",
        padding=10,
        content=ft.Column([
            ft.Row([ft.Text("Công cụ 3NF", size=20, weight="bold", color="white"), theme_icon], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(color="#374151"),
            ft.ElevatedButton(
                "📂 Mở CSV", bgcolor="#3B82F6", color="white", width=200, height=45,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), elevation=2),
                on_click=lambda _: file_picker.pick_files(
                    allow_multiple=False,
                    allowed_extensions=["csv"],
                    dialog_title="Chọn file CSV"
                )
            ),
            ft.ElevatedButton(
                "💾 Xuất Dữ liệu", bgcolor="#10B981", color="white", width=200, height=45,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), elevation=2),
                on_click=on_export_click
            )
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
        icon=ft.icons.CLOSE,
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
        bgcolor=ft.colors.TRANSPARENT,
        modal=True
    )
    
    page.dialog = export_dialog
    export_dialog.open = True
    page.update()