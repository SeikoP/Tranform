import flet as ft
from utils.file_utils import get_data
from ui.erd_utils import add_field, refresh_erd_tab, suggest_erd, save_tables, load_tables

def create_erd_tab(page: ft.Page, update_status):
    df = get_data(page)
    
    # Left Panel
    table_name_input = ft.TextField(
        label="Nhập tên bảng", hint_text="VD: Dim_Customer, Fact_Sales",
        width=300, border_radius=10, bgcolor="#F9FAFB", border_color="#D1D5DB",
        focused_border_color="#3B82F6", prefix_icon=ft.icons.TABLE_CHART
    )
    column_dropdown = ft.Dropdown(
        label="Chọn trường",
        options=[ft.dropdown.Option(col) for col in df.columns] if df is not None else [],
        width=300, border_radius=10, bgcolor="#F9FAFB", border_color="#D1D5DB",
        focused_border_color="#3B82F6"
    )
    pk_checkbox = ft.Checkbox(label="Primary Key", value=False, active_color="#3B82F6")
    
    left_panel = ft.Container(
        width=350, bgcolor="#FFFFFF", border_radius=10, padding=20,
        shadow=ft.BoxShadow(blur_radius=10, spread_radius=1, color=ft.colors.with_opacity(0.1, "black")),
        content=ft.Column([
            ft.Row([ft.Icon(ft.icons.SETTINGS, color="#3B82F6"), ft.Text("Thiết lập bảng", size=20, weight="bold", color="#1F2937")], spacing=5),
            ft.Divider(color="#E5E7EB"),
            ft.Row([table_name_input], alignment=ft.MainAxisAlignment.CENTER),
            ft.ElevatedButton(
                "➕ Thêm bảng", bgcolor="#3B82F6", color="white", width=300, height=45,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), elevation=2),
                on_click=lambda _: add_table(table_name_input, page.session.get("tables"), page, update_status, lambda: refresh_erd_tab(page, erd_layout, update_status))
            ),
            ft.Container(height=10),
            # ft.Column([column_dropdown, ft.Row([pk_checkbox], alignment=ft.MainAxisAlignment.START),
            #     ft.ElevatedButton(
            #         "➕ Thêm trường", bgcolor="#10B981", color="white", width=300, height=45,
            #         style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), elevation=2),
            #         on_click=lambda _: add_field(table_name_input.value.strip(), column_dropdown.value, page.session.get("tables"), page, pk_checkbox.value) if table_name_input.value.strip() and column_dropdown.value else None
            #     )], spacing=10),
            # ft.Container(height=20),
            ft.ElevatedButton(
                "🤖 Đề xuất ERD", bgcolor="#8B5CF6", color="white", width=300, height=45,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), elevation=2),
                on_click=lambda _: suggest_erd(page, update_status, erd_layout)
            ),
            ft.ElevatedButton(
                "💾 Lưu cấu trúc", bgcolor="#F59E0B", color="white", width=300, height=45,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), elevation=2),
                on_click=lambda _: save_tables(page, update_status)
            ),
            ft.ElevatedButton(
                "📂 Tải cấu trúc", bgcolor="#4CAF50", color="white", width=300, height=45,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), elevation=2),
                on_click=lambda _: load_tables(page, update_status, erd_layout)
            ),
        ], spacing=15, alignment=ft.MainAxisAlignment.START)
    )
    
    # Right Panel
    erd_layout = ft.ListView(expand=True, spacing=15, padding=20)
    
    format_dropdown = ft.Dropdown(
        label="Chọn định dạng xuất",
        options=[ft.dropdown.Option("csv"), ft.dropdown.Option("xlsx"), ft.dropdown.Option("database")],
        value="csv", width=200, border_radius=10, bgcolor="#F9FAFB", border_color="#D1D5DB",
        focused_border_color="#3B82F6"
    )
    normalize_btn = ft.ElevatedButton(
        "Transform", bgcolor="#3B82F6", color="white", width=200, height=45,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), elevation=2),
        on_click=lambda _: normalize_and_export(page, format_dropdown)
    )
    create_db_btn = ft.ElevatedButton(
        "Create DB Scripts", bgcolor="#10B981", color="white", width=200, height=45,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), elevation=2),
        visible=False,
        on_click=lambda _: create_db_script(page)
    )
    
    def update_right_panel(e):
        create_db_btn.visible = (format_dropdown.value == "database")
        page.update()

    format_dropdown.on_change = update_right_panel
    
    right_panel = ft.Container(
        expand=True, bgcolor="#F3F4F6", border_radius=10, padding=20,
        shadow=ft.BoxShadow(blur_radius=10, spread_radius=1, color=ft.colors.with_opacity(0.1, "black")),
        content=ft.Column([
            ft.Text("Danh sách bảng", size=20, weight="bold", color="#1F2937"),
            erd_layout,
        ], spacing=15)
    )
    
    def normalize_and_export(page, format_dropdown):
        if len(page.overlay) < 2:
            update_status("❌ Không tìm thấy export picker!", "red")
            return
        export_picker = page.overlay[1]
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

    erd_container = ft.Row([left_panel, right_panel], expand=True)
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