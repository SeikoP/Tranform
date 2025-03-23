import os
import flet as ft
import pandas as pd
from etl import normalize_to_3nf
from utils import *
from normalization import normalization, create_script_sql

def main(page: ft.Page):
    page.title = "Chuyển đổi dữ liệu sang 3NF"
    page.window_icon = resource_path("assets/normalization.ico")
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
            page_menu()
        else:
            page.dialog = ft.AlertDialog(title=ft.Text("⚠ Bạn chưa chọn file!"))
            page.dialog.open = True
            page.update()

    def page_menu():
        page.controls.clear()
        df = get_data(page)
        
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
        
        table_content = ft.Text("⚠ Không có dữ liệu! Vui lòng chọn file CSV.", size=40, text_align=ft.TextAlign.CENTER)
        stats = None
        if df is not None:
            unique_counts = page.session.get("unique_counts")
            if unique_counts is None:
                unique_counts = {col: df[col].nunique() for col in df.columns}
                page.session.set("unique_counts", unique_counts)
            table_data = [
                ft.DataRow(cells=[ft.DataCell(ft.Text(str(df.iloc[i, j]))) for j in range(min(10, len(df.columns)))])
                for i in range(min(10, len(df)))
            ]
            table_content = ft.DataTable(
                columns=[ft.DataColumn(ft.Text(f"{col} ({unique_counts[col]} unique)")) for col in df.columns[:10]],
                rows=table_data,
                expand=True,
                data_row_max_height=50,
                vertical_lines=ft.BorderSide(1, "grey"),
                horizontal_lines=ft.BorderSide(1, "grey")
            )
            stats = ft.Text(f"Tổng số bản ghi: {len(df)}", size=14, italic=True)
        
        right_panel = ft.Container(
            width=1580,
            content=ft.Column([table_content, stats] if stats else [table_content], scroll="auto"),
            bgcolor="white",
            padding=10,
            border=ft.border.all(1, "black"),
        )
        page.add(ft.Row([left_panel, right_panel], expand=True))
        page.update()

    def page_erd():
        page.controls.clear()
        df = get_data(page)
        
        if df is None:
            page.go('/menu')
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
            options=[ft.dropdown.Option("csv"), ft.dropdown.Option("xlsx"), ft.dropdown.Option("database")],
            value="csv",
            on_change=lambda e: update_right_panel()
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

        # Lưu instance của nút ở phạm vi page_erd
        create_db_button = ft.ElevatedButton(
            text='Create database scripts',
            on_click=lambda _: create_script_sql(tables),
            width=200,
            height=50
        )

        def update_right_panel():
            column_content = right_panel.content
            # Xóa nút cũ nếu có
            for control in column_content.controls[:]:  # Sao chép danh sách để tránh lỗi khi xóa
                if isinstance(control, ft.ElevatedButton) and control.text == 'Create database scripts':
                    column_content.controls.remove(control)
            # Thêm nút nếu là 'database'
            if format_dropdown.value == 'database':
                column_content.controls.append(create_db_button)
            right_panel.update()
            update_erd()  # Cập nhật ERD cùng lúc

        page.update_right_panel = update_right_panel

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
                            add_field_to_table(t, fd.value, tables, page, pk.value, fk.value, rc.value) if fd.value else None
                        )
                    )
                else:
                    add_button = ft.ElevatedButton(
                        "➕ Thêm",
                        on_click=lambda _, t=table, fd=table_field_dropdown, pk=pk_checkbox_table: (
                            add_field_to_table(t, fd.value, tables, page, pk.value) if fd.value else None
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
                                        ft.ElevatedButton("✏️ Chỉnh sửa", on_click=lambda _, t=table: edit_table(tables, t, df, page)),
                                        ft.ElevatedButton(
                                            "🗑️ Xóa",
                                            on_click=lambda _, t=table: delete_table(t, tables, page),
                                            bgcolor=ft.colors.RED_400,
                                            color="white"
                                        ),
                                    ], alignment=ft.MainAxisAlignment.END, spacing=10),
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
                ft.Row([table_name_input, ft.ElevatedButton("➕ Thêm bảng", on_click=lambda _: add_table(table_name_input, tables, page))]),
                ft.Column([
                    column_dropdown,
                    ft.Row([pk_checkbox]),
                    ft.ElevatedButton("➕ Thêm trường", on_click=lambda _: add_field(table_name_input, column_dropdown, tables, page, pk_checkbox))
                ], spacing=10),
                ft.ElevatedButton("🤖 Đề xuất ERD", on_click=lambda _: suggest_erd()),
                ft.ElevatedButton("💾 Lưu cấu trúc", on_click=lambda _: save_tables(page, tables), width=200),
                ft.ElevatedButton("🔙 Quay lại", on_click=lambda _: page.go("/menu"), width=200)
            ], spacing=15, alignment=ft.MainAxisAlignment.START),
            padding=10,
            bgcolor="white",
            border=ft.border.all(1, "black")
        )

        page.add(ft.Row([left_panel, right_panel], expand=True))
        update_erd()
        update_right_panel()

    def route_change(route):
        if page.route == "/menu":
            page_menu()
        elif page.route == "/erd":
            page_erd()
        page.update()

    page.on_route_change = route_change
    page.go("/menu")

if __name__ == "__main__":
    ft.app(target=main)