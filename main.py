import flet as ft
import pandas as pd
import json
from ETL import normalization, analyze_dependencies
import os
import sys

# Hàm để lấy đường dẫn động
def resource_path(relative_path):
    """Lấy đường dẫn tương đối đến tài nguyên, hoạt động cả khi đóng gói và không đóng gói"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        return os.path.join(os.path.dirname(__file__), relative_path)

def hi(page: ft.Page):
    page.title = "Chuyển đổi dữ liệu sang 3NF"
    page.window_icon = resource_path("assets/normalization.ico")  # Sửa đường dẫn icon
    page.window_resizable = True
    page.theme_mode = "light"
    page.window_width = 1800
    page.window_height = 1000

    file_picker = ft.FilePicker(on_result=lambda e: on_file_selected(e, page))
    page.overlay.append(file_picker)
    page.session.set("tables", {})

    def on_file_selected(e, page):
        if e.files:
            file_path = e.files[0].path
            page.session.set("file_path", file_path)
            update_layout()
        else:
            page.dialog = ft.AlertDialog(title=ft.Text("⚠ Bạn chưa chọn file!"))
            page.dialog.open = True
            page.update()

    def get_data():
        file_path = page.session.get("file_path")
        if not file_path or not file_path.lower().endswith('.csv'):
            return None
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
            if df.empty:
                raise ValueError("File CSV trống")
            return df
        except Exception as ex:
            page.dialog = ft.AlertDialog(title=ft.Text(f"⚠ Lỗi đọc file: {str(ex)}"))
            page.dialog.open = True
            page.update()
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
            ], spacing=10, alignment=ft.MainAxisAlignment.START),
            border=ft.border.all(1, "black"),
            padding=10
        )
        
        table_content = ft.Text("⚠ Không có dữ liệu! Vui lòng chọn file CSV.")
        if df is not None:
            table_data = [
                ft.DataRow(cells=[ft.DataCell(ft.Text(str(df.iloc[i, j]))) for j in range(len(df.columns))])
                for i in range(min(10, len(df)))
            ]
            table_content = ft.DataTable(
                columns=[ft.DataColumn(ft.Text(f"{col} ({df[col].nunique()} unique)")) for col in df.columns],
                rows=table_data,
                expand=True,
                data_row_max_height=50,
                vertical_lines=ft.BorderSide(1, "grey"),
                horizontal_lines=ft.BorderSide(1, "grey")
            )
            stats = ft.Text(f"Tổng số bản ghi: {len(df)}", size=14, italic=True)
        
        right_panel = ft.Container(
            width=1200, 
            content=ft.Column([table_content, stats] if df is not None else [table_content], scroll="auto"),
            bgcolor="white", 
            padding=10
        )
        page.add(ft.Row([left_panel, right_panel], expand=True))
        page.update()

    def show_erd():
        page.controls.clear()
        df = get_data()
        
        if df is None:
            page.go('/preview')
            return

        tables = page.session.get("tables") or {}
        
        table_name_input = ft.TextField(label="Nhập tên bảng (Dim_ hoặc Fact_)", width=300)
        column_dropdown = ft.Dropdown(
            label="Chọn trường",
            options=[ft.dropdown.Option(col) for col in df.columns],
            width=300
        )
        pk_checkbox = ft.Checkbox(label="Primary Key", value=False)

        erd_layout = ft.ListView(expand=True, spacing=10, padding=10)
        format_dropdown = ft.Dropdown(
            label="Chọn định dạng file",
            options=[ft.dropdown.Option("csv"), ft.dropdown.Option("xlsx")],
            value="csv"
        )

        def suggest_erd():
            suggestions = analyze_dependencies(df)
            nonlocal tables
            tables = {}
            for dim_col in suggestions['Dim']:
                tables[f"Dim_{dim_col}"] = [{'name': dim_col, 'is_primary': True, 'ref_table': None, 'ref_column': None}]
            tables['Fact_Data'] = [
                {'name': col, 'is_primary': col == df.columns[0], 'ref_table': f'Dim_{col}' if col in suggestions['Dim'] else None, 'ref_column': col if col in suggestions['Dim'] else None}
                for col in suggestions['Fact']
            ]
            page.session.set("tables", tables)
            update_erd()

        def add_table():
            table_name = table_name_input.value.strip()
            if table_name and table_name not in tables and (table_name.lower().startswith('dim_') or table_name.lower().startswith('fact_')):
                tables[table_name] = []
                page.session.set("tables", tables)
                update_erd()
            else:
                page.dialog = ft.AlertDialog(title=ft.Text("⚠ Tên bảng không hợp lệ hoặc đã tồn tại! (Phải bắt đầu bằng Dim_ hoặc Fact_)"))
                page.dialog.open = True
                page.update()

        def add_field():
            table_name = table_name_input.value.strip()
            selected_field = column_dropdown.value
            
            if table_name not in tables:
                page.dialog = ft.AlertDialog(title=ft.Text("⚠ Vui lòng chọn hoặc thêm bảng trước!"))
                page.dialog.open = True
                page.update()
                return
            
            if not selected_field:
                page.dialog = ft.AlertDialog(title=ft.Text("⚠ Vui lòng chọn trường!"))
                page.dialog.open = True
                page.update()
                return

            if not any(col['name'] == selected_field for col in tables[table_name]):
                tables[table_name].append({
                    'name': selected_field,
                    'is_primary': pk_checkbox.value,
                    'ref_table': None,
                    'ref_column': None
                })
                page.session.set("tables", tables)
                update_erd()
                pk_checkbox.value = False
            else:
                page.dialog = ft.AlertDialog(title=ft.Text("⚠ Trường này đã tồn tại trong bảng!"))
                page.dialog.open = True
                page.update()

        def delete_table(table_name):
            if table_name in tables:
                for t, cols in tables.items():
                    if any(col['ref_table'] == table_name for col in cols):
                        page.dialog = ft.AlertDialog(title=ft.Text(f"⚠ Không thể xóa '{table_name}' vì đang được tham chiếu bởi '{t}'!"))
                        page.dialog.open = True
                        page.update()
                        return
                del tables[table_name]
                page.session.set("tables", tables)
                update_erd()
                page.dialog = ft.AlertDialog(title=ft.Text(f"✅ Đã xóa bảng '{table_name}'!"))
                page.dialog.open = True
                page.update()

        def edit_table(table_name):
            if table_name not in tables:
                return
            
            edit_dialog = ft.AlertDialog(
                title=ft.Text(f"Chỉnh sửa bảng {table_name}"),
                content=ft.Column([], scroll="auto", width=800),
                actions=[
                    ft.ElevatedButton("Lưu", on_click=lambda e: save_edit(table_name, edit_dialog)),
                    ft.ElevatedButton("Hủy", on_click=lambda e: close_dialog(edit_dialog))
                ]
            )
            
            controls_dict = {}
            for col in tables[table_name]:
                col_name_field = ft.TextField(value=col['name'], width=150, disabled=True)
                pk_check = ft.Checkbox(label="Primary Key", value=col['is_primary'])
                fk_dropdown = ft.Dropdown(
                    width=200,
                    options=[ft.dropdown.Option(t) for t in tables.keys() if t.lower().startswith('dim_')],
                    value=col['ref_table'],
                    label="Foreign Key",
                    disabled=not table_name.lower().startswith('fact_')
                )
                ref_col_dropdown = ft.Dropdown(
                    width=200,
                    options=[ft.dropdown.Option(c) for c in df.columns],
                    value=col['ref_column'],
                    label="Cột tham chiếu",
                    disabled=not table_name.lower().startswith('fact_')
                )
                controls_dict[col['name']] = {
                    'name_field': col_name_field,
                    'pk_check': pk_check,
                    'fk_dropdown': fk_dropdown,
                    'ref_col_dropdown': ref_col_dropdown
                }
                edit_dialog.content.controls.append(
                    ft.Row([col_name_field, pk_check, fk_dropdown, ref_col_dropdown], spacing=10)
                )
            
            page.dialog = edit_dialog
            edit_dialog.open = True
            page.session.set(f"edit_controls_{table_name}", controls_dict)
            page.update()

        def save_edit(table_name, dialog):
            controls_dict = page.session.get(f"edit_controls_{table_name}")
            if not controls_dict:
                page.dialog = ft.AlertDialog(title=ft.Text("⚠ Lỗi: Không tìm thấy dữ liệu chỉnh sửa!"))
                page.dialog.open = True
                page.update()
                return
            
            new_columns = []
            for col_name, controls in controls_dict.items():
                is_primary = controls['pk_check'].value
                ref_table = controls['fk_dropdown'].value
                ref_column = controls['ref_col_dropdown'].value
                new_columns.append({
                    'name': col_name,
                    'is_primary': is_primary,
                    'ref_table': ref_table if table_name.lower().startswith('fact_') else None,
                    'ref_column': ref_column if table_name.lower().startswith('fact_') else None
                })
            
            tables[table_name] = new_columns
            page.session.set("tables", tables)
            dialog.open = False
            update_erd()
            page.update()

        def close_dialog(dialog):
            dialog.open = False
            page.update()

        def add_field_to_table(table_name, field_name, is_primary=False, ref_table=None, ref_column=None):
            if table_name in tables and field_name:
                if not any(col['name'] == field_name for col in tables[table_name]):
                    tables[table_name].append({
                        'name': field_name,
                        'is_primary': is_primary,
                        'ref_table': ref_table if table_name.lower().startswith('fact_') else None,
                        'ref_column': ref_column if table_name.lower().startswith('fact_') else None
                    })
                    page.session.set("tables", tables)
                    update_erd()

        def save_tables():
            data_path = resource_path("data")  # Sử dụng đường dẫn động
            if not os.path.exists(data_path):
                os.makedirs(data_path)
            try:
                with open(os.path.join(data_path, 'erd.json'), 'w', encoding='utf-8') as f:
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
                column_display = ft.Column([ft.Text(
                    f"🔹 {col['name']}" + 
                    (" (PK)" if col['is_primary'] else "") +
                    (f" (FK -> {col['ref_table']}.{col.get('ref_column', 'ID')})" if col.get('ref_table') else ""),
                    size=16, italic=True
                ) for col in cols])
                
                table_field_dropdown = ft.Dropdown(
                    width=200,
                    options=[ft.dropdown.Option(col) for col in df.columns],
                    label="Thêm trường"
                )
                pk_checkbox_table = ft.Checkbox(label="Primary Key", value=False)
                
                additional_controls = [pk_checkbox_table]
                if table.lower().startswith('fact_'):
                    fk_dropdown = ft.Dropdown(
                        width=200,
                        options=[ft.dropdown.Option(t) for t in tables.keys() if t.lower().startswith('dim_')],
                        label="Foreign Key (Tham chiếu bảng)"
                    )
                    ref_column_dropdown = ft.Dropdown(
                        width=200,
                        options=[ft.dropdown.Option(col) for col in df.columns],
                        label="Cột tham chiếu"
                    )
                    additional_controls.extend([fk_dropdown, ref_column_dropdown])
                    add_button = ft.ElevatedButton(
                        "➕ Thêm",
                        on_click=lambda _, t=table, fd=table_field_dropdown, pk=pk_checkbox_table, fk=fk_dropdown, rc=ref_column_dropdown: (
                            add_field_to_table(t, fd.value, pk.value, fk.value, rc.value) if fd.value else None
                        )
                    )
                else:
                    add_button = ft.ElevatedButton(
                        "➕ Thêm",
                        on_click=lambda _, t=table, fd=table_field_dropdown, pk=pk_checkbox_table: (
                            add_field_to_table(t, fd.value, pk.value) if fd.value else None
                        )
                    )
                
                erd_layout.controls.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.Row([
                                ft.Column([
                                    ft.Text(f"📌 {table}", size=18, weight="bold", color=ft.colors.BLUE),
                                    column_display if cols else ft.Text("Chưa có cột", italic=True)
                                ], spacing=5),
                                ft.Column([
                                    ft.Row([table_field_dropdown] + additional_controls, spacing=10),
                                    ft.Row([
                                        add_button,
                                        ft.ElevatedButton("✏️ Chỉnh sửa", on_click=lambda _, t=table: edit_table(t)),
                                        ft.ElevatedButton(
                                            "🗑️ Xóa",
                                            on_click=lambda _, t=table: delete_table(t),
                                            bgcolor=ft.colors.RED_400,
                                            color="white"
                                        )
                                    ], alignment=ft.MainAxisAlignment.END, spacing=10)
                                ], spacing=5)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            padding=10,
                            bgcolor=ft.colors.GREY_100,
                            border_radius=10
                        ),
                        elevation=2
                    )
                )
            page.update()

        left_panel = ft.Container(
            width=400,
            content=ft.Column([
                ft.Text("📌 Thiết lập bảng", size=18, weight="bold", color=ft.colors.BLUE),
                ft.Row([table_name_input, ft.ElevatedButton("➕ Thêm bảng", on_click=lambda _: add_table())]),
                ft.Column([
                    column_dropdown,
                    ft.Row([pk_checkbox]),
                    ft.ElevatedButton("➕ Thêm trường", on_click=lambda _: add_field())
                ], spacing=10),
                ft.ElevatedButton("🤖 Đề xuất ERD", on_click=lambda _: suggest_erd()),
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
                    format_dropdown,
                    ft.ElevatedButton(
                        text='Normalization',
                        on_click=lambda _: normalization(df=df, page=page, format_dropdown=format_dropdown)
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
            ]),
            bgcolor="white",
            padding=10,
            border=ft.border.all(1, "black")
        )
        page.add(ft.Row([left_panel, right_panel], expand=True))
        update_erd()

    def route_change(route):
        if page.route == "/preview":
            update_layout()
        elif page.route == "/erd":
            show_erd()

    page.on_route_change = route_change
    page.go("/preview")

if __name__ == "__main__":
    ft.app(target=hi)