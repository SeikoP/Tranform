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
        update_status = page.session.get("status_bar_update") or (lambda t, c: None)
        update_status("❌ Bảng không tồn tại hoặc không hợp lệ", "red")
        return
    
    if column_name and column_name not in [col['name'] for col in tables[table_name]]:
        tables[table_name].append({
            'name': column_name, 
            'is_primary': is_primary, 
            'ref_table': ref_table, 
            'ref_column': ref_column or "ID" if ref_table else None
        })
        page.session.set("tables", tables)
        
        status_bar_container = page.session.get("status_bar")
        if status_bar_container:
            # Re-using the update logic from main
            status_text = status_bar_container.content.controls[1]
            status_text.value = f"✅ Đã thêm trường '{column_name}' vào bảng '{table_name}'"
            status_bar_container.bgcolor = ft.Colors.GREEN_50
            status_text.color = ft.Colors.GREEN_700
            
        erd_layout = page.session.get("erd_layout")
        if erd_layout:
            refresh_erd_tab(page, erd_layout, lambda t, c: None) # Status update handled above
        page.update()
    else:
        # Generic update status if available
        pass

def refresh_erd_tab(page: ft.Page, erd_layout, update_status):
    tables = page.session.get("tables") or {}
    erd_layout.controls.clear()
    df = get_data(page)
    
    for table, cols in tables.items():
        # Determine table type and color
        is_fact = table.lower().startswith('fact_')
        header_color = ft.Colors.TEAL_600 if is_fact else ft.Colors.BLUE_600
        header_bg = ft.Colors.TEAL_50 if is_fact else ft.Colors.BLUE_50
        
        column_items = []
        for col in cols:
            icn = ft.Icons.KEY_ROUNDED if col['is_primary'] else (ft.Icons.LINK_ROUNDED if col.get('ref_table') else ft.Icons.LABEL_OUTLINED)
            icn_color = ft.Colors.AMBER_600 if col['is_primary'] else (ft.Colors.INDIGO_400 if col.get('ref_table') else ft.Colors.BLUE_GREY_400)
            
            column_items.append(
                ft.Row([
                    ft.Icon(icn, size=16, color=icn_color),
                    ft.Text(col['name'], size=14, weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_GREY_800),
                    ft.Text("(PK)" if col['is_primary'] else "", size=11, color=ft.Colors.AMBER_700, weight=ft.FontWeight.BOLD),
                    ft.Text(f"→ {col['ref_table']}" if col.get('ref_table') else "", size=11, color=ft.Colors.INDIGO_400, italic=True),
                ], spacing=8)
            )

        column_display = ft.Column(column_items, spacing=8)
        
        # Field addition controls
        table_field_dropdown = ft.Dropdown(
            expand=True, border_radius=8, bgcolor=ft.Colors.WHITE, border_color=ft.Colors.BLUE_GREY_100,
            options=[ft.dropdown.Option(col) for col in df.columns] if df is not None else [],
            label="Chọn cột", text_size=13, height=45
        )
        pk_checkbox = ft.Checkbox(label="PK", value=False, active_color=ft.Colors.AMBER_600)
        
        additional_controls = [pk_checkbox]
        if is_fact:
            fk_dropdown = ft.Dropdown(
                width=140, border_radius=8, bgcolor=ft.Colors.WHITE, border_color=ft.Colors.BLUE_GREY_100,
                options=[ft.dropdown.Option(t) for t in tables.keys() if t.lower().startswith('dim_')],
                label="FK to", text_size=12, height=45
            )
            additional_controls.append(fk_dropdown)

        add_btn = ft.IconButton(
            icon=ft.Icons.ADD_CIRCLE_ROUNDED,
            icon_color=ft.Colors.GREEN_600,
            on_click=lambda _, t=table, fd=table_field_dropdown, pk=pk_checkbox, fk=fk_dropdown if is_fact else None: (
                add_field(t, fd.value, page.session.get("tables"), page, pk.value, fk.value if is_fact else None) if fd.value else None
            )
        )

        table_card = ft.Container(
            content=ft.Column([
                # Header
                ft.Container(
                    content=ft.Row([
                        ft.Row([
                            ft.Icon(ft.Icons.TABLE_CHART_ROUNDED, color=header_color, size=20),
                            ft.Text(table, size=16, weight=ft.FontWeight.BOLD, color=header_color),
                        ], spacing=10),
                        ft.IconButton(ft.Icons.DELETE_OUTLINE_ROUNDED, icon_color=ft.Colors.RED_400, icon_size=18,
                                    on_click=lambda _, t=table: delete_table(t, page.session.get("tables"), page, update_status, lambda: refresh_erd_tab(page, erd_layout, update_status)))
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=12,
                    bgcolor=header_bg,
                    border_radius=ft.border_radius.only(top_left=12, top_right=12)
                ),
                # Body
                ft.Container(
                    content=ft.Column([
                        column_display if cols else ft.Text("Chưa có cột nào", size=13, italic=True, color=ft.Colors.BLUE_GREY_300),
                        ft.Divider(height=20, color=ft.Colors.BLUE_GREY_50),
                        ft.Row([table_field_dropdown] + additional_controls + [add_btn], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    ], spacing=10),
                    padding=15
                )
            ], spacing=0),
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            border=ft.border.all(1, ft.Colors.BLUE_GREY_100),
            shadow=ft.BoxShadow(blur_radius=10, spread_radius=1, color=ft.Colors.with_opacity(0.05, "black")),
        )
        
        erd_layout.controls.append(table_card)
    
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
            bgcolor=ft.Colors.TRANSPARENT,
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