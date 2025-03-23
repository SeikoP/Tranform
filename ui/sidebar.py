import flet as ft

def create_sidebar(page: ft.Page, file_picker, export_picker, update_status):
    def toggle_theme(e):
        if page.theme_mode == "light":
            page.theme_mode = "dark"
            theme_btn.text = "☀️ Chế độ Sáng"
            theme_btn.bgcolor = "#4B5563"
        else:
            page.theme_mode = "light"
            theme_btn.text = "🌙 Chế độ Tối"
            theme_btn.bgcolor = "#3B82F6"
        page.update()

    app_logo = ft.Row([
        ft.Icon(name=ft.icons.AUTO_AWESOME_MOTION, size=30, color=ft.colors.WHITE),
        ft.Text("Công cụ 3NF", size=24, weight="bold", color="white")
    ], alignment=ft.MainAxisAlignment.START)
    
    open_csv_btn = ft.ElevatedButton(
        "📂 Mở CSV", bgcolor="#3B82F6", color="white", width=200, height=50,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=lambda _: file_picker.pick_files(allowed_extensions=["csv"], allow_multiple=False)
    )
    
    theme_btn = ft.ElevatedButton(
        "🌙 Chế độ Tối", bgcolor="#3B82F6", color="white", width=200, height=50,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=toggle_theme
    )
    
    export_btn = ft.ElevatedButton(
        "⬇️ Xuất Dữ liệu", bgcolor="#10B981", color="white", width=200, height=50,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=lambda _: export_picker.get_directory_path(dialog_title="Chọn thư mục để lưu dữ liệu chuẩn hóa")
    )
    
    about_btn = ft.TextButton(
        "ℹ️ Giới thiệu", style=ft.ButtonStyle(color=ft.colors.WHITE70),
        on_click=lambda _: update_status("Công cụ 3NF v1.0.0", "blue")
    )
    
    return ft.Container(
        width=250, height=page.height, bgcolor="#1F2937", padding=20,
        content=ft.Column([
            app_logo, ft.Divider(color=ft.colors.WHITE24, height=30),
            open_csv_btn, theme_btn, export_btn, ft.Container(height=20),
            ft.Divider(color=ft.colors.WHITE24),
            ft.Text("Phiên bản 1.0.0", color=ft.colors.WHITE54, size=12), about_btn
        ], spacing=15, alignment=ft.MainAxisAlignment.START)
    )