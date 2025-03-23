import os
import pandas as pd
from etl import normalize_to_3nf
from utils import resource_path
import flet as ft
import json

def normalization(df: pd.DataFrame, page: ft.Page, format_dropdown, data_path: str = None):
    if df is None or df.empty:
        page.dialog = ft.AlertDialog(title=ft.Text("⚠ Dữ liệu đầu vào trống hoặc không hợp lệ!"))
        page.dialog.open = True
        page.update()
        return

    if data_path is None:
        data_path = resource_path("data")
    
    erd_path = os.path.join(data_path, 'erd.json')
    if not os.path.exists(erd_path):
        page.dialog = ft.AlertDialog(title=ft.Text("⚠ Bạn chưa lưu cấu trúc ERD!"))
        page.dialog.open = True
        page.update()
        return
    try:
        with open(erd_path, 'r', encoding='utf-8') as file:
            erd = json.load(file)
    except json.JSONDecodeError:
        page.dialog = ft.AlertDialog(title=ft.Text("⚠ File erd.json không hợp lệ!"))
        page.dialog.open = True
        page.update()
        return
    except IOError as e:
        page.dialog = ft.AlertDialog(title=ft.Text(f"⚠ Lỗi đọc file erd.json: {str(e)}"))
        page.dialog.open = True
        page.update()
        return

    file_picker = page.overlay[0]  # Sử dụng file_picker từ main.py
    file_picker.on_result = lambda e: save_files(e, df, erd, page, format_dropdown)
    file_picker.get_directory_path(dialog_title="Chọn thư mục để lưu file")
    page.update()

def create_script_sql(erd):
    if not erd or not isinstance(erd, dict):
        raise ValueError("Cấu trúc ERD không hợp lệ!")

    def infer_data_type(column_name):
        if "date" in column_name.lower():
            return "DATE"
        elif "is_" in column_name.lower():
            return "BOOLEAN"
        elif any(x in column_name.lower() for x in ["count", "days", "adults", "children", "babies", "changes", "spaces", "requests", "cancellations"]):
            return "INT"
        elif "adr" in column_name.lower():
            return "DECIMAL(10, 2)"
        else:
            return "VARCHAR(100)"

    sql_script = "-- Create the database\nCREATE DATABASE [Name_Database];\nUSE [Name_Database];\n\n"
    dim_tables = {k: v for k, v in erd.items() if k.startswith("Dim_")}
    for table_name, columns in dim_tables.items():
        sql_script += f"-- Dimension Table\nCREATE TABLE {table_name} (\n"
        for col in columns:
            col_name = col["name"]
            data_type = infer_data_type(col_name)
            primary_key = " PRIMARY KEY" if col["is_primary"] else ""
            sql_script += f"    {col_name} {data_type}{primary_key},\n"
        sql_script = sql_script.rstrip(",\n") + "\n);\n\n"

    fact_table = erd.get("Fact_Data")
    if fact_table:
        sql_script += "-- Fact Table\nCREATE TABLE Fact_Data (\n"
        for col in fact_table:
            col_name = col["name"].replace("-", "_")
            data_type = infer_data_type(col_name)
            sql_script += f"    {col_name} {data_type},\n"
        
        for dim_table, columns in dim_tables.items():
            for col in columns:
                col_name = col["name"]
                data_type = infer_data_type(col_name)
                sql_script += f"    {col_name} {data_type},\n"
        
        sql_script += "    -- Foreign key constraints\n"
        for dim_table, columns in dim_tables.items():
            for col in columns:
                col_name = col["name"]
                sql_script += f"    FOREIGN KEY ({col_name}) REFERENCES {dim_table}({col_name}),\n"
        
        sql_script = sql_script.rstrip(",\n") + "\n);\n"

    data_path = resource_path("data")
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    sql_file_path = os.path.join(data_path, 'create_data.sql')
    with open(sql_file_path, 'w', encoding='utf-8') as f:
        f.write(sql_script)

    return sql_file_path  # Trả về đường dẫn để thông báo

def save_files(event, df: pd.DataFrame, erd: dict, page: ft.Page, format_dropdown):
    if event.path is None:
        page.dialog = ft.AlertDialog(title=ft.Text("⚠ Bạn chưa chọn thư mục!"))
        page.dialog.open = True
        page.update()
        return

    save_path = event.path
    if format_dropdown.value not in ['csv', 'xlsx']:
        page.dialog = ft.AlertDialog(title=ft.Text("⚠ Định dạng file không hợp lệ!"))
        page.dialog.open = True
        page.update()
        return

    try:
        normalized_tables = normalize_to_3nf(df, erd)
    except Exception as ex:
        page.dialog = ft.AlertDialog(title=ft.Text(f"⚠ Lỗi khi chuẩn hóa dữ liệu: {str(ex)}"))
        page.dialog.open = True
        page.update()
        return

    output_excel_path = os.path.join(save_path, "normalized_data.xlsx") if format_dropdown.value == 'xlsx' else None

    def proceed_with_overwrite(page):
        try:
            if format_dropdown.value == 'xlsx':
                with pd.ExcelWriter(output_excel_path, mode='w') as writer:
                    for table_name, table_df in normalized_tables.items():
                        table_df.to_excel(writer, sheet_name=table_name, index=False)
            else:
                for table_name, table_df in normalized_tables.items():
                    table_df.to_csv(os.path.join(save_path, f"{table_name}.csv"), index=False, encoding='utf-8')
            page.dialog = ft.AlertDialog(title=ft.Text("✅ Đã lưu file thành công!"))
            page.dialog.open = True
            page.update()
        except Exception as ex:
            page.dialog = ft.AlertDialog(title=ft.Text(f"⚠ Lỗi khi lưu file: {str(ex)}"))
            page.dialog.open = True
            page.update()

    def proceed_with_append(page):
        try:
            if format_dropdown.value == 'xlsx':
                with pd.ExcelWriter(output_excel_path, mode='a', if_sheet_exists='new') as writer:
                    for table_name, table_df in normalized_tables.items():
                        table_df.to_excel(writer, sheet_name=table_name, index=False)
            else:
                for table_name, table_df in normalized_tables.items():
                    table_df.to_csv(os.path.join(save_path, f"{table_name}.csv"), index=False, encoding='utf-8')
            page.dialog = ft.AlertDialog(title=ft.Text("✅ Đã lưu file thành công!"))
            page.dialog.open = True
            page.update()
        except Exception as ex:
            page.dialog = ft.AlertDialog(title=ft.Text(f"⚠ Lỗi khi lưu file: {str(ex)}"))
            page.dialog.open = True
            page.update()

    if format_dropdown.value == 'xlsx' and os.path.exists(output_excel_path):
        page.dialog = ft.AlertDialog(
            title=ft.Text("File đã tồn tại!"),
            content=ft.Text("Bạn muốn ghi đè hay thêm sheet?"),
            actions=[
                ft.ElevatedButton("Ghi đè", on_click=lambda _: proceed_with_overwrite(page)),
                ft.ElevatedButton("Thêm sheet", on_click=lambda _: proceed_with_append(page))
            ]
        )
        page.dialog.open = True
        page.update()
    else:
        proceed_with_overwrite(page)