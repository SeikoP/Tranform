import flet as ft
from ui.sidebar import create_sidebar
from ui.data_preview import create_data_preview_tab, refresh_data_tab
from ui.erd_tab import create_erd_tab, refresh_erd_tab
from ui.status_bar import create_status_bar
from utils.file_utils import on_file_selected, on_export_selected

def main(page: ft.Page):
    page.title = "Công cụ Chuẩn hóa Dữ liệu 3NF"
    page.window_width = 1600
    page.window_height = 900
    page.window_resizable = True
    page.theme_mode = "light"
    page.bgcolor = "#F5F5F5"
    page.padding = 0

    file_picker = ft.FilePicker(on_result=lambda e: on_file_selected(e, page, refresh_data_tab))
    export_picker = ft.FilePicker(on_result=lambda e: on_export_selected(e, page))
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