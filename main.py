import flet as ft
from ui.sidebar import create_sidebar
from ui.data_preview import create_data_preview_tab, refresh_data_tab
from ui.erd_tab import create_erd_tab
from utils.file_utils import on_file_selected, on_export_selected

def create_status_bar(page: ft.Page):
    status_text = ft.Text("✅ Sẵn sàng", size=14, color="green")
    status_bar = ft.Container(
        content=status_text, padding=ft.padding.only(left=20, right=20, top=10, bottom=10),
        bgcolor="#18c9e7", alignment=ft.alignment.center_left
    )
    
    def update_status(text, color="black"):
        status_text.value = text
        status_text.color = color
        page.update()
    
    page.session.set("status_bar", status_bar)
    return status_bar, update_status

def main(page: ft.Page):
    page.title = "Công cụ Chuẩn hóa Dữ liệu 3NF"
    page.window_width = 1600
    page.window_height = 900
    page.window_resizable = True
    page.theme_mode = "light"
    page.bgcolor = "#F5F5F5"  # Màu nền chính của ứng dụng
    page.padding = 0

    progress_bar = ft.ProgressBar(width=400, visible=False)
    page.overlay.append(progress_bar)

    file_picker = ft.FilePicker(on_result=lambda e: on_file_selected(e, page, refresh_data_tab, progress_bar))
    export_picker = ft.FilePicker(on_result=lambda e: on_export_selected(e, page, page.session.get("export_format") or "csv"))
    page.overlay.extend([file_picker, export_picker])

    page.session.set("tables", {})
    status_bar, update_status = create_status_bar(page)
    sidebar = create_sidebar(page, file_picker, export_picker, update_status)
    data_tab_container = create_data_preview_tab(page)
    erd_tab_container = create_erd_tab(page, update_status)
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(text="Xem trước Dữ liệu", content=data_tab_container),
            ft.Tab(text="Thiết kế ERD", content=erd_tab_container),
        ],
        expand=1
    )

    page.add(
        ft.Row([
            sidebar,
            ft.Column([tabs, status_bar], expand=True)
        ], expand=True)
    )

if __name__ == "__main__":
    ft.app(target=main)