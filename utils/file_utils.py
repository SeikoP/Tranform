import os
import pandas as pd
import json
import sys
import flet as ft
from utils.data_analysis import AdvancedNormalizer
from utils.sql_generator import create_script_sql

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)

def get_data(page):
    file_path = page.session.get("file_path")
    if file_path and os.path.exists(file_path):
        return pd.read_csv(file_path)
    return None

def on_file_selected(e, page, refresh_callback, progress_bar):
    if e.files:
        file_path = e.files[0].path
        if os.path.getsize(file_path) > 100 * 1024 * 1024:
            page.dialog = ft.AlertDialog(title=ft.Text("⚠️ Tệp quá lớn (>100MB)!"))
            page.dialog.open = True
            page.update()
            return
        progress_bar.visible = True
        page.update()
        page.session.set("file_path", file_path)
        page.session.get("status_bar").content.value = f"📄 Đã chọn: {os.path.basename(file_path)}"
        page.session.get("status_bar").content.color = "blue"
        progress_bar.visible = False
        refresh_callback(page)
    else:
        page.dialog = ft.AlertDialog(title=ft.Text("⚠️ Chưa chọn tệp!"))
        page.dialog.open = True
        page.update()

def on_export_selected(e, page, format_type="csv"):
    if not e.path:
        page.dialog = ft.AlertDialog(title=ft.Text("⚠ Vui lòng chọn thư mục!"))
        page.dialog.open = True
        page.update()
        return
    df = get_data(page)
    if df is None:
        page.dialog = ft.AlertDialog(title=ft.Text("⚠ Chưa tải file CSV!"))
        page.dialog.open = True
        page.update()
        return
    
    data_path = resource_path("data")
    erd_path = os.path.join(data_path, "erd.json")
    if not os.path.exists(erd_path):
        page.dialog = ft.AlertDialog(title=ft.Text("⚠ Bạn chưa lưu cấu trúc ERD!"))
        page.dialog.open = True
        page.update()
        return
    
    try:
        with open(erd_path, 'r', encoding='utf-8') as file:
            tables = json.load(file)
        
        normalizer = AdvancedNormalizer(df)
        normalized_tables = normalizer.normalize_to_3nf()
        output_path = e.path
        for table_name, table_df in normalized_tables.items():
            if format_type == "csv":
                table_df.to_csv(os.path.join(output_path, f"{table_name}.csv"), index=False, encoding='utf-8')
            elif format_type == "xlsx":
                table_df.to_excel(os.path.join(output_path, f"{table_name}.xlsx"), index=False)
            elif format_type == "database":
                sql_path = create_script_sql(tables, df)
                page.dialog = ft.AlertDialog(title=ft.Text(f"✅ Đã tạo script SQL tại: {sql_path}"))
                page.dialog.open = True
                page.update()
                return
        page.dialog = ft.AlertDialog(title=ft.Text(f"✅ Đã xuất dữ liệu chuẩn hóa thành {format_type} tại: {output_path}"))
        page.dialog.open = True
        page.session.get("status_bar").content.value = f"✅ Xuất thành công tại: {output_path}"
        page.session.get("status_bar").content.color = "green"
    except Exception as ex:
        page.dialog = ft.AlertDialog(title=ft.Text(f"⚠️ Lỗi xuất dữ liệu: {str(ex)}"))
        page.dialog.open = True
        page.session.get("status_bar").content.value = f"❌ Xuất thất bại: {str(ex)}"
        page.session.get("status_bar").content.color = "red"