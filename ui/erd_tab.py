import flet as ft
from utils.file_utils import get_data
from ui.erd_utils import add_field, refresh_erd_tab, suggest_erd, save_tables, load_tables

def create_erd_tab(page: ft.Page, update_status):
    df = get_data(page)
    
    # Left Toolbar Panel
    table_name_input = ft.TextField(
        label="Tên Bảng Mới", 
        hint_text="VD: Dim_Customer",
        border_radius=12,
        prefix_icon=ft.Icons.ADD_BOX_OUTLINED,
        bgcolor=ft.Colors.WHITE,
        border_color=ft.Colors.BLUE_GREY_100,
        focused_border_color=ft.Colors.BLUE_600,
        text_size=14,
    )
    
    # Action Buttons Group
    action_buttons = ft.Column([
        ft.ElevatedButton(
            "Tạo Bảng", 
            icon=ft.Icons.ADD_TASK_ROUNDED,
            bgcolor=ft.Colors.BLUE_600, 
            color="white", 
            width=300, 
            height=45,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            on_click=lambda _: add_table(table_name_input, page.session.get("tables"), page, update_status, lambda: refresh_erd_tab(page, erd_layout, update_status))
        ),
        ft.Container(height=10),
        ft.Text("TỰ ĐỘNG HÓA", size=11, color=ft.Colors.BLUE_GREY_400, weight=ft.FontWeight.BOLD),
        ft.ElevatedButton(
            "Đề xuất ERD (AI)", 
            icon=ft.Icons.AUTO_AWESOME_ROUNDED,
            bgcolor=ft.Colors.PURPLE_600, 
            color="white", 
            width=300, 
            height=45,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            on_click=lambda _: suggest_erd(page, update_status, erd_layout)
        ),
        ft.Container(height=10),
        ft.Text("QUẢN LÝ CẤU TRÚC", size=11, color=ft.Colors.BLUE_GREY_400, weight=ft.FontWeight.BOLD),
        ft.Row([
            ft.TextButton(
                "Lưu", icon=ft.Icons.SAVE_ROUNDED, 
                on_click=lambda _: save_tables(page, update_status)
            ),
            ft.TextButton(
                "Tải", icon=ft.Icons.FOLDER_OPEN_ROUNDED,
                on_click=lambda _: load_tables(page, update_status, erd_layout)
            ),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
    ], spacing=10)

    left_panel = ft.Container(
        width=320, 
        bgcolor=ft.Colors.BLUE_GREY_50, 
        padding=25,
        border_radius=ft.border_radius.only(top_left=15, bottom_left=15),
        content=ft.Column([
            ft.Text("Thiết kế Mô hình", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
            ft.Text("Đầu xác định các bảng và mối quan hệ để chuẩn hóa dữ liệu.", size=13, color=ft.Colors.BLUE_GREY_600),
            ft.Divider(height=40, color=ft.Colors.BLUE_GREY_200),
            table_name_input,
            ft.Container(height=10),
            action_buttons,
        ], spacing=10)
    )
    
    # Center Canvas Panel (Scrollable list of tables)
    erd_layout = ft.ListView(
        expand=True, 
        spacing=20, 
        padding=30,
    )
    
    # Export Settings in a sub-header or side-area? Let's put them in a small top-bar of the center panel
    format_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("csv", "Dữ liệu CSV"),
            ft.dropdown.Option("xlsx", "Báo cáo Excel"),
            ft.dropdown.Option("database", "Script SQL"),
        ],
        value="csv", 
        width=180, 
        height=45,
        border_radius=10,
        text_size=13,
        bgcolor=ft.Colors.WHITE,
    )

    create_db_btn = ft.ElevatedButton(
        "Tạo SQL Script", 
        icon=ft.Icons.CODE_ROUNDED,
        bgcolor=ft.Colors.TEAL_600, 
        color="white", 
        height=45,
        visible=False,
        on_click=lambda _: create_db_script(page)
    )
    
    def on_format_change(e):
        create_db_btn.visible = (format_dropdown.value == "database")
        page.update()
    format_dropdown.on_change = on_format_change

    center_header = ft.Row([
        ft.Text("Cơ cấu Bảng (3NF)", size=18, weight=ft.FontWeight.W_600),
        ft.Row([
            format_dropdown,
            create_db_btn,
            ft.ElevatedButton(
                "Transform", 
                icon=ft.Icons.PLAY_ARROW_ROUNDED,
                bgcolor=ft.Colors.BLUE_600, 
                color="white", 
                height=45,
                on_click=lambda _: normalize_and_export(page, format_dropdown)
            ),
        ], spacing=15)
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    center_panel = ft.Container(
        expand=True, 
        bgcolor=ft.Colors.WHITE, 
        padding=25,
        border_radius=ft.border_radius.only(top_right=15, bottom_right=15),
        border=ft.border.all(1, ft.Colors.BLUE_GREY_100),
        content=ft.Column([
            center_header,
            ft.Divider(height=30, color=ft.Colors.BLUE_GREY_100),
            erd_layout,
        ], spacing=0)
    )
    
    def normalize_and_export(page, format_dropdown):
        if len(page.overlay) < 3: # 0: progress, 1: file, 2: export
            update_status("❌ Không tìm thấy bộ chọn xuất!", "red")
            return
        export_picker = page.overlay[2]
        page.session.set("export_format", format_dropdown.value)
        export_picker.get_directory_path(dialog_title="Chọn thư mục để lưu dữ liệu chuẩn hóa")

    def create_db_script(page):
        df = get_data(page)
        if df is None:
            show_dialog(page, "⚠ Vui lòng tải file CSV trước!")
            return
        tables = page.session.get("tables")
        if not tables:
            show_dialog(page, "⚠ Chưa có bảng nào để tạo script!")
            return
        try:
            from utils.sql_generator import create_script_sql
            sql_path = create_script_sql(tables, df)
            show_dialog(page, f"✅ Đã tạo script SQL tại: {sql_path}")
        except Exception as ex:
            show_dialog(page, f"❌ Lỗi khi tạo script SQL: {str(ex)}")

    erd_container = ft.Row([left_panel, center_panel], expand=True, spacing=0)
    
    # Store reference to layout for refresh
    page.session.set("erd_layout", erd_layout)
    
    refresh_erd_tab(page, erd_layout, update_status)
    return erd_container


def show_dialog(page, message):
    dlg = ft.AlertDialog(title=ft.Text(message))
    page.dialog = dlg
    dlg.open = True
    page.update()

def add_table(table_name_input, tables, page, update_status, refresh_callback):
    table_name = table_name_input.value.strip()
    if table_name and table_name not in tables:
        tables[table_name] = []
        table_name_input.value = ""
        update_status(f"✅ Đã thêm bảng: {table_name}", "green")
        refresh_callback()
    else:
        update_status("❌ Tên bảng không hợp lệ hoặc đã tồn tại", "red")