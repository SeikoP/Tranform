import os
import sys
import json
import flet as ft
import pandas as pd

def resource_path(relative_path):
    """Lấy đường dẫn tương đối đến tài nguyên, hoạt động cả khi đóng gói và không đóng gói"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)

def analyze_dependencies(df: pd.DataFrame):
    """Phân tích dữ liệu để đề xuất bảng Dim và Fact"""
    if df is None or df.empty:
        return {'Dim': [], 'Fact': []}
    suggestions = {'Dim': [], 'Fact': []}
    for col in df.columns:
        unique_count = df[col].nunique()
        total_count = len(df)
        if unique_count < total_count * 0.3:  # Ngưỡng 30% để coi là thực thể độc lập
            suggestions['Dim'].append(col)
        else:
            suggestions['Fact'].append(col)
    return suggestions

def get_data(page):
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

def save_edit(table_name, dialog, page, tables):
    controls_dict = page.session.get(f"edit_controls_{table_name}")
    if not controls_dict:
        page.dialog = ft.AlertDialog(title=ft.Text("⚠ Lỗi: Không tìm thấy dữ liệu chỉnh sửa!"))
        page.dialog.open = True
        page.update()
        return
    
    new_columns = []
    for col_name, controls in controls_dict.items():
        is_primary = controls['pk_check'].value
        ref_table = controls['fk_dropdown'].value if table_name.lower().startswith('fact_') else None
        ref_column = controls['ref_col_dropdown'].value if table_name.lower().startswith('fact_') else None
        new_columns.append({
            'name': col_name,
            'is_primary': is_primary,
            'ref_table': ref_table,
            'ref_column': ref_column
        })
    tables[table_name] = new_columns
    page.session.set("tables", tables)
    close_dialog(dialog, page)

def close_dialog(dialog, page):
    dialog.open = False
    page.update()

def add_field_to_table(table_name, field_name, tables, page, is_primary=False, ref_table=None, ref_column=None):
    if table_name in tables and field_name:
        if not any(col['name'] == field_name for col in tables[table_name]):
            tables[table_name].append({
                'name': field_name,
                'is_primary': is_primary,
                'ref_table': ref_table if table_name.lower().startswith('fact_') else None,
                'ref_column': ref_column if table_name.lower().startswith('fact_') else None
            })
            page.session.set("tables", tables)

def save_tables(page, tables):
    data_path = resource_path("data")
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

def add_table(table_name_input, tables, page):
    table_name = table_name_input.value.strip()
    if table_name and table_name not in tables and (table_name.lower().startswith('dim_') or table_name.lower().startswith('fact_')):
        tables[table_name] = []
        page.session.set("tables", tables)
        page.update_right_panel()  # Cập nhật giao diện ngay sau khi thêm bảng
        table_name_input.value = ""  # Reset giá trị nhập
    else:
        page.dialog = ft.AlertDialog(title=ft.Text("⚠ Tên bảng không hợp lệ hoặc đã tồn tại! (Phải bắt đầu bằng Dim_ hoặc Fact_)"))
        page.dialog.open = True
        page.update()

def add_field(table_name_input, column_dropdown, tables, page, pk_checkbox):
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
        pk_checkbox.value = False
        column_dropdown.value = None  # Reset dropdown
    else:
        page.dialog = ft.AlertDialog(title=ft.Text("⚠ Trường này đã tồn tại trong bảng!"))
        page.dialog.open = True
        page.update()

def delete_table(table_name, tables, page):
    if table_name in tables:
        for t, cols in tables.items():
            if any(col['ref_table'] == table_name for col in cols):
                page.dialog = ft.AlertDialog(title=ft.Text(f"⚠ Không thể xóa '{table_name}' vì đang được tham chiếu bởi '{t}'!"))
                page.dialog.open = True
                page.update()
                return
        del tables[table_name]
        page.session.set("tables", tables)
        page.dialog = ft.AlertDialog(title=ft.Text(f"✅ Đã xóa bảng '{table_name}'!"))
        page.dialog.open = True
        page.update_right_panel()  # Cập nhật giao diện sau khi xóa
        page.update()

def edit_table(tables, table_name, df, page):
    if table_name not in tables or df is None:
        page.dialog = ft.AlertDialog(title=ft.Text("⚠ Không thể chỉnh sửa: Bảng hoặc dữ liệu không hợp lệ!"))
        page.dialog.open = True
        page.update()
        return
    
    edit_dialog = ft.AlertDialog(
        title=ft.Text(f"Chỉnh sửa bảng {table_name}"),
        content=ft.Column([], scroll="auto", width=800),
        actions=[
            ft.ElevatedButton("Lưu", on_click=lambda e: save_edit(table_name, edit_dialog, page, tables)),
            ft.ElevatedButton("Hủy", on_click=lambda e: close_dialog(edit_dialog, page))
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