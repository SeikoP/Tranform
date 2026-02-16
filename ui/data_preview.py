import os
import flet as ft
from utils.data_analysis import analyze_dependencies
from utils.file_utils import get_data

def create_stat_card(title: str, value: str, icon: str, color: str):
    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(icon, color=color, size=24),
                ft.Text(title, size=14, weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_GREY_400),
            ], spacing=10),
            ft.Text(value, size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
        ], spacing=5),
        padding=20,
        bgcolor="white",
        border_radius=15,
        border=ft.border.all(1, ft.Colors.BLUE_GREY_100),
        width=240,
        shadow=ft.BoxShadow(blur_radius=10, spread_radius=1, color=ft.Colors.with_opacity(0.05, "black")),
    )

def create_data_preview_tab(page: ft.Page):
    # Initial view when no file is loaded
    no_data_view = ft.Container(
        expand=True,
        content=ft.Column([
            ft.Icon(ft.Icons.CLOUD_UPLOAD_ROUNDED, size=100, color=ft.Colors.BLUE_GREY_200),
            ft.Text("Chưa có dữ liệu nào được tải", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_400),
            ft.Text("Vui lòng mở một tệp CSV từ thanh công cụ bên trái", size=16, color=ft.Colors.BLUE_GREY_400),
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=100
    )
    
    container = ft.Container(content=no_data_view, expand=True)
    return container

def refresh_data_tab(page: ft.Page):
    try:
        # Find the container - more robust search
        # We manually set it in page.session for easier access
        container = page.session.get("data_tab_container")
        if not container:
            # Fallback search if session not set
            try:
                container = page.controls[0].controls[1].content.controls[0].tabs[0].content.content
            except:
                return

        file_path = page.session.get("file_path")
        if not file_path:
            return # Should already be in no-data state
            
        df = get_data(page)
        if df is None or df.empty:
            container.content = ft.Container(
                content=ft.Text("❌ Không thể tải dữ liệu từ file CSV", size=16, color=ft.Colors.RED_400),
                alignment=ft.alignment.center
            )
            page.update()
            return
        
        record_count = len(df)
        column_count = len(df.columns)
        suggestions = analyze_dependencies(df)
        
        # Stats Row
        stats_row = ft.Row([
            create_stat_card("Số bản ghi", f"{record_count:,}", ft.Icons.STORAGE_ROUNDED, ft.Colors.BLUE_600),
            create_stat_card("Số cột", f"{column_count}", ft.Icons.TABLE_ROWS_ROUNDED, ft.Colors.PURPLE_600),
            create_stat_card("Dim Candidates", f"{len(suggestions['Dim'])}", ft.Icons.FACT_CHECK_ROUNDED, ft.Colors.ORANGE_600),
            create_stat_card("Fact Candidates", f"{len(suggestions['Fact'])}", ft.Icons.ANALYTICS_ROUNDED, ft.Colors.TEAL_600),
        ], spacing=20, alignment=ft.MainAxisAlignment.START)
        
        # Preview Table
        preview_data = df.head(15)
        unique_counts = {col: df[col].nunique() for col in df.columns}
        
        data_columns = [
            ft.DataColumn(
                ft.Container(
                    content=ft.Column([
                        ft.Text(col, size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_800),
                        ft.Text(f"{unique_counts[col]} unique", size=11, color=ft.Colors.BLUE_GREY_400)
                    ], spacing=2),
                    padding=ft.padding.symmetric(vertical=10)
                )
            ) for col in df.columns
        ]
        
        data_rows = [
            ft.DataRow(
                cells=[ft.DataCell(ft.Text(str(preview_data.iloc[i, j]), size=13, color=ft.Colors.BLUE_GREY_700)) 
                       for j in range(len(preview_data.columns))]
            ) for i in range(len(preview_data))
        ]
        
        container.content = ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.INSERT_DRIVE_FILE_ROUNDED, color=ft.Colors.BLUE_600, size=28),
                ft.Text(os.path.basename(file_path), size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
            ], spacing=10),
            
            ft.Container(height=10),
            stats_row,
            ft.Container(height=30),
            
            ft.Text("Xem trước Dữ liệu (15 dòng đầu tiên):", size=18, weight=ft.FontWeight.W_600, color=ft.Colors.BLUE_GREY_800),
            ft.Container(
                content=ft.Column([
                    ft.DataTable(
                        columns=data_columns,
                        rows=data_rows,
                        heading_row_color=ft.Colors.with_opacity(0.05, ft.Colors.BLUE_GREY_200),
                        border=ft.border.all(1, ft.Colors.BLUE_GREY_100),
                        border_radius=10,
                        vertical_lines=ft.border.BorderSide(1, ft.Colors.with_opacity(0.05, "black")),
                        heading_row_height=70,
                        data_row_min_height=45,
                        column_spacing=40,
                    )
                ], scroll=ft.ScrollMode.ALWAYS),
                bgcolor="white",
                padding=10,
                border_radius=10,
                border=ft.border.all(1, ft.Colors.BLUE_GREY_100),
                expand=True
            )
        ], spacing=10, expand=True)
        
        page.update()
    except Exception as ex:
        print(f"Error refreshing data tab: {ex}")
        import traceback
        traceback.print_exc()
