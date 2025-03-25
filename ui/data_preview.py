import os
import flet as ft
from utils.data_analysis import analyze_dependencies
from utils.file_utils import get_data

def create_data_preview_tab(page: ft.Page):
    data_summary = ft.Container(
        padding=ft.padding.all(15), bgcolor="#F0F9FF", border_radius=8,
        border=ft.border.all(1, "#93C5FD"),
        content=ft.Row([ft.Icon(ft.icons.INSIGHTS, color="#2563EB", size=24), ft.Text("Chưa tải dữ liệu", size=14, color="#1E40AF")])
    )
    
    data_table_container = ft.Container(
        padding=20, bgcolor="white", border_radius=10,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=15, color=ft.colors.with_opacity(0.1, "black"), offset=ft.Offset(0, 2)),
        content=ft.Column([data_summary, ft.Divider(), ft.Text("Vui lòng tải tệp CSV để xem dữ liệu", size=16, color="#6B7280", italic=True)])
    )

    return data_table_container

def refresh_data_tab(page: ft.Page):
    try:
        if not page.controls or len(page.controls) < 1 or len(page.controls[0].controls) < 2:
            return
        
        container = page.controls[0].controls[1].controls[0].tabs[0].content
        file_path = page.session.get("file_path")
        
        if not file_path:
            container.content = ft.Column([
                ft.Container(
                    padding=20,
                    content=ft.Column([
                        ft.Icon(ft.icons.CLOUD_UPLOAD, size=64, color="#9CA3AF"),
                        ft.Text("Vui lòng chọn tệp CSV để bắt đầu", size=18, color="#6B7280")
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                )
            ], alignment=ft.MainAxisAlignment.CENTER)
        else:
            df = get_data(page)
            if df is None or df.empty:
                container.content = ft.Column([
                    ft.Text("Không thể tải dữ liệu từ file CSV", size=16, color="#EF4444")
                ])
                page.update()
                return
            
            record_count = len(df)
            column_count = len(df.columns)
            suggestions = analyze_dependencies(df)
            dim_cols = len(suggestions['Dim'])
            fact_cols = len(suggestions['Fact'])
            
            summary_content = ft.Column([
                ft.Row([
                    ft.Column([ft.Text("Số bản ghi", size=12, color="#6B7280"), ft.Text(f"{record_count:,}", size=18, weight="bold", color="#1E40AF")], spacing=5),
                    ft.VerticalDivider(width=30, thickness=1, color="#D1D5DB"),
                    ft.Column([ft.Text("Số cột", size=12, color="#6B7280"), ft.Text(f"{column_count}", size=18, weight="bold", color="#1E40AF")], spacing=5),
                    ft.VerticalDivider(width=30, thickness=1, color="#D1D5DB"),
                    ft.Column([ft.Text("Dim Candidates", size=12, color="#6B7280"), ft.Text(f"{dim_cols}", size=18, weight="bold", color="#047857")], spacing=5),
                    ft.VerticalDivider(width=30, thickness=1, color="#D1D5DB"),
                    ft.Column([ft.Text("Fact Candidates", size=12, color="#6B7280"), ft.Text(f"{fact_cols}", size=18, weight="bold", color="#B91C1C")], spacing=5)
                ], alignment=ft.MainAxisAlignment.START)
            ])
            
            unique_counts = {col: df[col].nunique() for col in df.columns}
            data_columns = [ft.DataColumn(ft.Container(content=ft.Column([ft.Text(col, size=14, weight="bold", color="#374151"), ft.Text(f"{unique_counts[col]} giá trị duy nhất", size=12, color="#6B7280")], spacing=2))) for col in df.columns]
            data_rows = [ft.DataRow(cells=[ft.DataCell(ft.Text(str(df.iloc[i, j]), size=14)) for j in range(len(df.columns))]) for i in range(min(10, len(df)))]
            
            suggestion_row = ft.Container(
                padding=ft.padding.all(10), bgcolor="#F3F4F6", border_radius=5,
                content=ft.Column([
                    ft.Text("Gợi ý Loại Cột:", size=14, weight="bold"),
                    ft.Text(f"Dim col: {', '.join(suggestions['Dim'][:5]) + ('...' if len(suggestions['Dim']) > 5 else '')}", size=14, color="#047857"),
                    ft.Text(f"Fact col: {', '.join(suggestions['Fact'][:5]) + ('...' if len(suggestions['Fact']) > 5 else '')}", size=14, color="#B91C1C")
                ])
            )
            
            container.content = ft.Column([
                ft.Row([ft.Icon(ft.icons.INSERT_DRIVE_FILE, color="#3B82F6", size=24), ft.Text(f"{os.path.basename(file_path)}", size=18, weight="bold", color="#1F2937")], spacing=10),
                ft.Container(height=10), summary_content, ft.Container(height=15), suggestion_row, ft.Container(height=20),
                ft.Text("Xem trước Dữ liệu (10 Hàng đầu tiên):", size=16, weight="bold", color="#374151"), ft.Container(height=10),
                ft.Container(content=ft.DataTable(columns=data_columns, rows=data_rows, border=ft.border.all(1, "#E5E7EB"), border_radius=5, vertical_lines=ft.border.BorderSide(1, "#E5E7EB"), horizontal_lines=ft.border.BorderSide(1, "#E5E7EB"), heading_row_height=60, data_row_max_height=50), padding=ft.padding.all(5), border_radius=5)
            ], scroll=ft.ScrollMode.AUTO)
        page.update()
    except Exception as ex:
        container.content = ft.Text(f"Lỗi khi cập nhật tab: {str(ex)}", color="#EF4444")
        page.update()