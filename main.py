import flet as ft
import pandas as pd
import json
from ETL import normalization

def hi(page: ft.Page):
    
    page.title = "Chuyển đổi dữ liệu"
    page.winwindow_icon = r'D:\TranformData\Tranform_Data\assets\normalization.png'
    page.window_resizable = True
    page.theme_mode = "light"
    page.window_width = 1800
    page.window_height = 1000

    file_picker = ft.FilePicker(on_result=lambda e: on_file_selected(e, page))
    
    page.overlay.append(file_picker)
    page.session.set("tables", {})  # Initialize tables dictionary

    def on_file_selected(e, page):
        if e.files:
            file_path = e.files[0].path
            page.session.set("file_path", file_path)
            update_layout()

    def get_data():
        file_path = page.session.get("file_path")
        if file_path and file_path.lower().endswith('.csv'):
            try:
                df = pd.read_csv(file_path)
                if df.empty:
                    raise ValueError("File CSV trống")
                return df
            except Exception as ex:
                page.dialog = ft.AlertDialog(title=ft.Text(f"⚠ Lỗi đọc file: {str(ex)}"))
                page.dialog.open = True
                page.update()
                return None
        return None

    def update_layout():
        page.controls.clear()
        df = get_data()
        
        left_panel = ft.Container(
            width=200, bgcolor="white",
            content=ft.Column([
                ft.Text("📌 Menu", size=18, weight="bold", color=ft.colors.BLUE),
                ft.ElevatedButton("📂 Chọn file CSV", on_click=lambda _: file_picker.pick_files(allow_multiple=False)),
                ft.ElevatedButton("📊 Tạo sơ đồ ERD", on_click=lambda _: page.go("/erd")),
            ], spacing=10, alignment=ft.MainAxisAlignment.SPACE_EVENLY),
            border=ft.border.all(1, "black"),
            padding=10
        )
        
        table_content = ft.Text("⚠ Không có dữ liệu! Vui lòng chọn file CSV.")
        if df is not None:
            table_data = [
                ft.DataRow(cells=[ft.DataCell(ft.Text(str(df.iloc[i, j]))) for j in range(len(df.columns))])
                for i in range(min(len(df), 20))
            ]
            table_content = ft.DataTable(
                columns=[ft.DataColumn(ft.Text(col)) for col in df.columns],
                rows=table_data, expand=True
            )
        
        right_panel = ft.Container(width=1200, content=table_content, bgcolor="white", padding=10)
        page.add(ft.Row([left_panel, right_panel], expand=True))
        page.update()

    def show_erd():
        page.controls.clear()
        file_path = page.session.get("file_path")
        
        if not file_path:
            page.dialog = ft.AlertDialog(title=ft.Text("⚠ Bạn chưa chọn file!"))
            page.dialog.open = True
            page.update()
            page.go('/preview')
            return

        df = get_data()
        if df is None:
            page.dialog = ft.AlertDialog(title=ft.Text("⚠ Không thể đọc dữ liệu từ file!"))
            page.dialog.open = True
            page.update()
            return

        tables = page.session.get("tables") or {}
        
        # Input controls
        table_name_input = ft.TextField(label="Nhập tên bảng", width=300)
        column_dropdown = ft.Dropdown(
            label="Chọn trường",
            options=[ft.dropdown.Option(col) for col in df.columns],
            width=300
        )
        pk_checkbox = ft.Checkbox(label="Primary Key", value=False)
        fk_checkbox = ft.Checkbox(label="Foreign Key", value=False)
        
        # ERD display area
        erd_layout = ft.ListView(expand=True, spacing=10, padding=10)

        # Format dropdown
        format_dropdown = ft.Dropdown(
            label="Chọn định dạng file",
            options=[
                ft.dropdown.Option("csv"),
                ft.dropdown.Option("xlsx"),
            ],
            value="csv"  # Giá trị mặc định
        )

        def add_table():
            table_name = table_name_input.value.strip()
            if table_name and table_name not in tables:
                tables[table_name] = []
                page.session.set("tables", tables)
                update_erd()
            else:
                page.dialog = ft.AlertDialog(title=ft.Text("⚠ Tên bảng không hợp lệ hoặc đã tồn tại!"))
                page.dialog.open = True
                page.update()

        def add_field():
            table_name = table_name_input.value.strip()
            selected_field = column_dropdown.value
            if table_name in tables and selected_field:
                if not any(col['name'] == selected_field for col in tables[table_name]):
                    tables[table_name].append({
                        'name': selected_field,
                        'is_primary': pk_checkbox.value,
                        'is_foreign': fk_checkbox.value
                    })
                    page.session.set("tables", tables)
                    update_erd()
                    pk_checkbox.value = False
                    fk_checkbox.value = False
                else:
                    page.dialog = ft.AlertDialog(title=ft.Text("⚠ Trường này đã tồn tại trong bảng!"))
                    page.dialog.open = True
                    page.update()

        def delete_table(table_name):
            if table_name in tables:
                del tables[table_name]
                page.session.set("tables", tables)
                update_erd()
                page.dialog = ft.AlertDialog(title=ft.Text(f"✅ Đã xóa bảng '{table_name}'!"))
                page.dialog.open = True
                page.update()

        def add_field_to_table(table_name, field_name):
            if table_name in tables and field_name:
                if not any(col['name'] == field_name for col in tables[table_name]):
                    tables[table_name].append({
                        'name': field_name,
                        'is_primary': False,
                        'is_foreign': False
                    })
                    page.session.set("tables", tables)
                    update_erd()
                else:
                    page.dialog = ft.AlertDialog(title=ft.Text(f"⚠ Trường '{field_name}' đã tồn tại trong bảng '{table_name}'!"))
                    page.dialog.open = True
                    page.update()

        def save_tables():
            try:
                with open(r'D:\TranformData\Tranform_Data\data\erd.json', 'w') as f:
                    json.dump(tables, f, indent=4)
                page.dialog = ft.AlertDialog(title=ft.Text("✅ Đã lưu cấu trúc thành công!"))
                page.dialog.open = True
                page.update()
            except Exception as ex:
                page.dialog = ft.AlertDialog(title=ft.Text(f"⚠ Lỗi khi lưu: {str(ex)}"))
                page.dialog.open = True
                page.update()

        def update_erd():
            erd_layout.controls.clear()
            for table, cols in tables.items():
                column_display = ft.Column([
                    ft.Text(
                        f"🔹 {col['name']}" + 
                        (" (PK)" if col['is_primary'] else "") +
                        (" (FK)" if col['is_foreign'] else ""),
                        size=16,
                        italic=True
                    ) for col in cols
                ])
                table_field_dropdown = ft.Dropdown(
                    width=200,
                    options=[ft.dropdown.Option(col) for col in df.columns],
                    on_change=lambda e, t=table: add_field_to_table(t, e.control.value),
                )
                erd_layout.controls.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.Row([
                                ft.Column([
                                    ft.Text(f"📌 {table}", size=18, weight="bold", color=ft.colors.BLUE),
                                    column_display if cols else ft.Text("Chưa có cột", italic=True)
                                ], spacing=5),
                                ft.Row([
                                    table_field_dropdown,
                                    ft.ElevatedButton(
                                        "🗑️ Xóa",
                                        on_click=lambda _, t=table: delete_table(t),
                                        bgcolor=ft.colors.RED_400,
                                        color="white"
                                    )
                                ], alignment=ft.MainAxisAlignment.END, spacing=10)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            padding=10,
                            bgcolor=ft.colors.GREY_100,
                            border_radius=10
                        ),
                        elevation=2
                    )
                )
            page.update()

        # Layout arrangement
        left_panel = ft.Container(
            width=400,
            content=ft.Column([
                ft.Text("📌 Thiết lập bảng", size=18, weight="bold", color=ft.colors.BLUE),
                ft.Container(
                    content=ft.Row([table_name_input, ft.ElevatedButton("➕ Thêm bảng", on_click=lambda _: add_table())],
                                 alignment=ft.MainAxisAlignment.START),
                    padding=5
                ),
                ft.Container(
                    content=ft.Column([
                        column_dropdown,
                        ft.Row([pk_checkbox, fk_checkbox]),
                        ft.ElevatedButton("➕ Thêm trường", on_click=lambda _: add_field())
                    ], spacing=10),
                    padding=5
                ),
                ft.ElevatedButton("💾 Lưu cấu trúc", on_click=lambda _: save_tables(), width=200),
                ft.ElevatedButton("🔙 Quay lại", on_click=lambda _: page.go("/preview"), width=200)
            ], spacing=15, alignment=ft.MainAxisAlignment.START),
            padding=10,
            bgcolor="white",
            border=ft.border.all(1, "black")
        )
        right_panel = ft.Container(
            width=1300,
            content=ft.Column([
                erd_layout,
                ft.Row([
                    format_dropdown,  # Thêm format_dropdown vào đây
                    ft.ElevatedButton(
                        text='Normalization',
                        on_click=lambda _: normalization(df=get_data(), page=page, format_dropdown=format_dropdown)
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
            ]),
            bgcolor="white",
            padding=10,
            border=ft.border.all(1, "black")
        )
        page.add(ft.Row([left_panel, right_panel], expand=True))
        update_erd()
        page.update()

    def route_change(route):
        if page.route == "/preview":
            update_layout()
        elif page.route == "/erd":
            show_erd()

    page.on_route_change = route_change
    page.go("/preview")

ft.app(target=hi)