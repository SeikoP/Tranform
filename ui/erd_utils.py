import flet as ft
import json
import os
import sys
from utils.file_utils import get_data
from utils.data_analysis import AdvancedNormalizer

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)

def add_field(table_name, column_name, tables, page, is_primary=False, ref_table=None, ref_column=None):
    if not table_name or table_name not in tables:
        page.session.get("status_bar").content.value = "❌ Bảng không tồn tại hoặc không hợp lệ"
        page.session.get("status_bar").content.color = "red"
        return
    if column_name and column_name not in [col['name'] for col in tables[table_name]]:
        tables[table_name].append({'name': column_name, 'is_primary': is_primary, 'ref_table': ref_table, 'ref_column': ref_column})
        page.session.set("tables", tables)
        page.session.get("status_bar").content.value = f"✅ Đã thêm trường '{column_name}' vào bảng '{table_name}'"
        page.session.get("status_bar").content.color = "green"
        refresh_erd_tab(page, page.controls[0].controls[1].controls[0].tabs[1].content.controls[1].content.controls[1], page.session.get("status_bar").content.update)
    else:
        page.session.get("status_bar").content.value = "❌ Trường không hợp lệ hoặc đã tồn tại"
        page.session.get("status_bar").content.color = "red"

def refresh_erd_tab(page: ft.Page, erd_layout, update_status):
    tables = page.session.get("tables") or {}
    erd_layout.controls.clear()
    df = get_data(page)
    for table, cols in tables.items():
        column_display = ft.Column([
            ft.Text(
                f"🔹 {col['name']}" + 
                (" (PK)" if col['is_primary'] else "") +
                (f" (FK -> {col['ref_table']}.{col.get('ref_column', 'ID')})" if col.get('ref_table') else ""),
                size=16, color="#374151"
            ) for col in cols
        ])
        
        table_field_dropdown = ft.Dropdown(
            width=200, border_radius=8, bgcolor="#F9FAFB", border_color="#D1D5DB",
            options=[ft.dropdown.Option(col) for col in df.columns] if df is not None else [],
            label="Thêm trường"
        )
        pk_checkbox_table = ft.Checkbox(label="Primary Key", value=False, active_color="#3B82F6")
        
        additional_controls = [pk_checkbox_table]
        if table.lower().startswith('fact_'):
            fk_dropdown = ft.Dropdown(
                width=200, border_radius=8, bgcolor="#F9FAFB", border_color="#D1D5DB",
                options=[ft.dropdown.Option(t) for t in tables.keys() if t.lower().startswith('dim_')],
                label="Foreign Key"
            )
            ref_column_dropdown = ft.Dropdown(
                width=200, border_radius=8, bgcolor="#F9FAFB", border_color="#D1D5DB",
                options=[ft.dropdown.Option(col) for col in df.columns] if df is not None else [],
                label="Cột tham chiếu"
            )
            additional_controls.extend([fk_dropdown, ref_column_dropdown])
            add_button = ft.ElevatedButton(
                "➕ Thêm", bgcolor="#10B981", color="white", width=100,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), elevation=2),
                on_click=lambda _, t=table, fd=table_field_dropdown, pk=pk_checkbox_table, fk=fk_dropdown, rc=ref_column_dropdown: (
                    add_field(t, fd.value, page.session.get("tables"), page, pk.value, fk.value, rc.value) if fd.value else None
                )
            )
        else:
            add_button = ft.ElevatedButton(
                "➕ Thêm", bgcolor="#10B981", color="white", width=100,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), elevation=2),
                on_click=lambda _, t=table, fd=table_field_dropdown, pk=pk_checkbox_table: (
                    add_field(t, fd.value, page.session.get("tables"), page, pk.value) if fd.value else None
                )
            )
        
        erd_layout.controls.append(
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([ft.Text(f"📌 {table}", size=18, weight="bold", color="#3B82F6"),
                                ft.IconButton(ft.icons.DELETE, icon_color="#EF4444", tooltip="Xóa bảng",
                                              on_click=lambda _, t=table: delete_table(t, page.session.get("tables"), page, update_status, lambda: refresh_erd_tab(page, erd_layout, update_status)))]),
                        ft.Divider(color="#E5E7EB"),
                        column_display if cols else ft.Text("Chưa có cột", italic=True, color="#6B7280"),
                        ft.Row([table_field_dropdown] + additional_controls, spacing=10),
                        ft.Row([add_button], alignment=ft.MainAxisAlignment.END)
                    ], spacing=10),
                    padding=15, bgcolor="#FFFFFF", border_radius=10, border=ft.border.all(1, "#E5E7EB")
                ),
                elevation=5
            )
        )
    page.update()

def delete_table(table_name, tables, page, update_status, refresh_callback):
    if table_name in tables:
        del tables[table_name]
        update_status(f"✅ Đã xóa bảng: {table_name}", "green")
        refresh_callback()
    else:
        update_status("❌ Không tìm thấy bảng", "red")

def suggest_erd(page, update_status, erd_layout):
    try:
        df = get_data(page)
        if df is None or df.empty:
            update_status("❌ Vui lòng tải file CSV hợp lệ trước!", "red")
            return
        
        update_status("⏳ Đang phân tích và đề xuất ERD...", "blue")
        normalizer = AdvancedNormalizer(df)
        normalized_tables = normalizer.normalize_to_3nf()
        
        if not normalized_tables:
            update_status("❌ Không thể tạo bảng từ dữ liệu!", "red")
            return
        
        tables = {}
        for name, table in normalized_tables.items():
            columns = [{"name": col, "is_primary": i == 0, "ref_table": None, "ref_column": None} 
                      for i, col in enumerate(table.columns)]
            tables[name] = columns
        
        preview_dialog = ft.AlertDialog(
            title=ft.Text("Xem trước ERD", size=18, weight="bold", color="#1F2937"),
            content=ft.Container(
                width=page.window_width * 0.5,
                height=page.window_height * 0.5,
                content=ft.Column([
                    ft.Text("Cấu trúc ERD đề xuất:", size=14, color="#6B7280"),
                    ft.ListView(
                        controls=[
                            ft.Column([
                                ft.Text(f"📌 {table_name}", size=16, weight="bold", color="#3B82F6"),
                                ft.Column([
                                    ft.Text(f"🔹 {col['name']}" + (" (PK)" if col['is_primary'] else ""), size=14, color="#374151")
                                    for col in cols
                                ])
                            ])
                            for table_name, cols in tables.items()
                        ],
                        expand=True, spacing=10
                    ),
                    ft.Row([
                        ft.ElevatedButton(
                            "Áp dụng", bgcolor="#3B82F6", color="white", width=120, height=40,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), elevation=2),
                            on_click=lambda _: (
                                page.session.set("tables", tables),
                                refresh_erd_tab(page, erd_layout, update_status),
                                update_status("✅ Đã áp dụng ERD!", "green"),
                                setattr(page.dialog, "open", False),
                                page.update()
                            )
                        ),
                        ft.ElevatedButton(
                            "Hủy", bgcolor="#EF4444", color="white", width=120, height=40,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), elevation=2),
                            on_click=lambda _: (
                                setattr(page.dialog, "open", False),
                                page.update()
                            )
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
                ], spacing=10),
                bgcolor="#FFFFFF", border_radius=10, padding=20
            ),
            bgcolor=ft.colors.TRANSPARENT,
            modal=True
        )
        
        page.dialog = preview_dialog
        preview_dialog.open = True
        page.update()
        
    except Exception as ex:
        normalizer = AdvancedNormalizer(df) if df is not None else None
        error_details = normalizer.error_log if normalizer else []
        error_msg = f"❌ Lỗi khi đề xuất ERD: {str(ex)}\nChi tiết: {', '.join(error_details) if error_details else 'Không có chi tiết'}"
        update_status(error_msg, "red")
        page.update()

def save_tables(page, update_status):
    data_path = resource_path("data")
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    file_path = os.path.join(data_path, "erd.json")
    tables = page.session.get("tables")
    if not tables:
        page.dialog = ft.AlertDialog(title=ft.Text("⚠ Chưa có bảng nào để lưu!"))
        page.dialog.open = True
        page.update()
        return
    if os.path.exists(file_path):
        confirm_dialog = ft.AlertDialog(
            title=ft.Text("⚠ File đã tồn tại!"),
            content=ft.Text("File erd.json đã tồn tại. Bạn có muốn ghi đè không?"),
            actions=[
                ft.ElevatedButton("Có", on_click=lambda _: (
                    save_to_file(file_path, page, update_status),
                    setattr(page.dialog, "open", False),
                    page.update()
                )),
                ft.ElevatedButton("Không", on_click=lambda _: (
                    setattr(page.dialog, "open", False),
                    page.update()
                ))
            ]
        )
        page.dialog = confirm_dialog
        confirm_dialog.open = True
        page.update()
    else:
        save_to_file(file_path, page, update_status)

def save_to_file(file_path, page, update_status):
    try:
        tables = page.session.get("tables")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(tables, f, indent=4)
        page.dialog = ft.AlertDialog(title=ft.Text(f"✅ Đã lưu cấu trúc tại: {file_path}"))
        page.dialog.open = True
        update_status(f"✅ Đã lưu cấu trúc tại: {file_path}", "green")
    except Exception as ex:
        page.dialog = ft.AlertDialog(title=ft.Text(f"❌ Lỗi khi lưu cấu trúc: {str(ex)}"))
        page.dialog.open = True
        update_status(f"❌ Lỗi khi lưu: {str(ex)}", "red")

def load_tables(page, update_status, erd_layout):
    data_path = resource_path("data")
    file_path = os.path.join(data_path, "erd.json")
    if not os.path.exists(file_path):
        page.dialog = ft.AlertDialog(title=ft.Text("⚠ File erd.json không tồn tại!"))
        page.dialog.open = True
        page.update()
        return
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tables = json.load(f)
        page.session.set("tables", tables)
        refresh_erd_tab(page, erd_layout, update_status)
        page.dialog = ft.AlertDialog(title=ft.Text(f"✅ Đã tải cấu trúc từ: {file_path}"))
        page.dialog.open = True
        update_status(f"✅ Đã tải cấu trúc từ: {file_path}", "green")
    except Exception as ex:
        page.dialog = ft.AlertDialog(title=ft.Text(f"❌ Lỗi khi tải cấu trúc: {str(ex)}"))
        page.dialog.open = True
        update_status(f"❌ Lỗi khi tải: {str(ex)}", "red")