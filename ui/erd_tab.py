import flet as ft
from utils.ui_utils import add_table, delete_table

def create_erd_tab(page: ft.Page, update_status):
    table_name_input = ft.TextField(label="Tên bảng mới", hint_text="VD: Dim_Customer hoặc Fact_Sales", prefix_icon=ft.icons.TABLE_CHART, border=ft.InputBorder.OUTLINE, width=400)
    column_input = ft.TextField(label="Tên cột", hint_text="VD: id, name", border=ft.InputBorder.OUTLINE, width=300)
    add_table_btn = ft.ElevatedButton("Thêm bảng", bgcolor="#3B82F6", color="white", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)), on_click=lambda e: add_table(table_name_input, page.session.get("tables"), page, update_status, lambda: refresh_erd_tab(page, erd_tab_container, table_name_input, column_input, add_table_btn, update_status)))
    
    erd_tab_container = ft.Container(
        padding=20, bgcolor="white", border_radius=10,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=15, color=ft.colors.with_opacity(0.1, "black"), offset=ft.Offset(0, 2))
    )
    
    refresh_erd_tab(page, erd_tab_container, table_name_input, column_input, add_table_btn, update_status)
    return erd_tab_container

def refresh_erd_tab(page: ft.Page, container, table_name_input, column_input, add_table_btn, update_status):
    tables = page.session.get("tables")
    if not tables:
        container.content = ft.Column([
            ft.Container(
                padding=20,
                content=ft.Column([
                    ft.Icon(ft.icons.TABLE_ROWS, size=64, color="#9CA3AF"),
                    ft.Text("Chưa có bảng nào được định nghĩa. Thêm bảng để bắt đầu.", size=18, color="#6B7280")
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )
        ], alignment=ft.MainAxisAlignment.CENTER)
    else:
        table_displays = []
        for table_name, columns in tables.items():
            def add_column(e, t_name=table_name):
                col_name = column_input.value.strip()
                if col_name and col_name not in tables[t_name]:
                    tables[t_name].append(col_name)
                    column_input.value = ""
                    update_status(f"✅ Đã thêm cột '{col_name}' vào bảng '{t_name}'", "green")
                    refresh_erd_tab(page, container, table_name_input, column_input, add_table_btn, update_status)
                else:
                    update_status("❌ Tên cột không hợp lệ hoặc đã tồn tại", "red")

            def delete_column(col_name, t_name=table_name):
                if col_name in tables[t_name]:
                    tables[t_name].remove(col_name)
                    update_status(f"✅ Đã xóa cột '{col_name}' khỏi bảng '{t_name}'", "green")
                    refresh_erd_tab(page, container, table_name_input, column_input, add_table_btn, update_status)

            column_list = ft.Column([
                ft.Row([
                    ft.Text(f"- {col}", size=14, color="#374151"),
                    ft.IconButton(icon=ft.icons.DELETE, icon_color="#EF4444", tooltip="Xóa cột", on_click=lambda e, c=col: delete_column(c))
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                for col in columns
            ]) if columns else ft.Text("Chưa có cột nào được định nghĩa", size=14, italic=True, color="#6B7280")

            table_card = ft.Container(
                padding=15, bgcolor="#F9FAFB", border_radius=8, border=ft.border.all(1, "#E5E7EB"),
                content=ft.Column([
                    ft.Row([
                        ft.Text(table_name, size=16, weight="bold", color="#1F2937"),
                        ft.IconButton(icon=ft.icons.DELETE, icon_color="#EF4444", tooltip="Xóa bảng", on_click=lambda e, name=table_name: delete_table(name, page.session.get("tables"), page, update_status, lambda: refresh_erd_tab(page, container, table_name_input, column_input, add_table_btn, update_status)))
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Divider(),
                    column_list,
                    ft.Row([
                        column_input,
                        ft.ElevatedButton("Thêm cột", bgcolor="#10B981", color="white", on_click=add_column)
                    ], spacing=10)
                ])
            )
            table_displays.append(table_card)
        
        container.content = ft.Column([
            ft.Row([table_name_input, add_table_btn], spacing=10),
            ft.Container(height=20),
            ft.Text("Các bảng đã định nghĩa:", size=18, weight="bold", color="#1F2937"),
            ft.Column(table_displays, spacing=10, scroll=ft.ScrollMode.AUTO)
        ], scroll=ft.ScrollMode.AUTO)
    page.update()