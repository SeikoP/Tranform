import pandas as pd
import json
import flet as ft
import csv
import os


def normalization(df: pd.DataFrame, page: ft.Page, format_dropdown, data_path: str = r'D:\TranformData\Tranform_Data\data'):
    try:
        with open(os.path.join(data_path, 'erd.json')) as file:
            erd = json.load(file)
    except FileNotFoundError:
        page.dialog = ft.AlertDialog(title=ft.Text("⚠ Bạn chưa lưu cấu trúc!"))
        page.dialog.open = True
        page.update()
        return
    except Exception as e:
        page.dialog = ft.AlertDialog(title=ft.Text(f"⚠ Không thể load file erd.json: {str(e)}"))
        page.dialog.open = True
        page.update()
        return

    file_picker = ft.FilePicker(on_result=lambda e: save_files(e, df, erd, page, format_dropdown))
    page.overlay.append(file_picker)
    page.update()

    # Mở hộp thoại chọn thư mục
    file_picker.get_directory_path(dialog_title="Chọn thư mục để lưu file")


def save_files(event, df: pd.DataFrame, erd: dict, page: ft.Page, format_dropdown):
    if event.path is None:
        page.dialog = ft.AlertDialog(title=ft.Text("⚠ Bạn chưa chọn thư mục!"))
        page.dialog.open = True
        page.update()
        return

    save_path = event.path

    if format_dropdown.value not in ['csv', 'xlsx']:
        page.dialog = ft.AlertDialog(title=ft.Text("⚠ Vui lòng chọn định dạng file hợp lệ (csv hoặc xlsx)!"))
        page.dialog.open = True
        page.update()
        return
        
    for table_name, columns in erd.items():
        print(f"Processing table: {table_name}")
        selected_columns = [col['name'] for col in columns if col['name'] in df.columns]
        
        output_path_csv = os.path.join(save_path, f"{table_name}.csv")
        output_path_xlsx = os.path.join(save_path, "data.xlsx")

        if selected_columns:
            table_df = df[selected_columns].copy()

            # Xử lý cột kiểu object
            for col in table_df.columns:
                if table_df[col].dtype == 'object':
                    table_df[col] = table_df[col].str.strip().str.replace('"', '')

            # Lưu file theo định dạng
            if format_dropdown.value == 'csv':
                table_df.to_csv(output_path_csv, index=False)  # Sử dụng output_path_csv đã định nghĩa
                page.dialog = ft.AlertDialog(title=ft.Text("✅ Đã lưu tất cả file thành công!"))
                page.dialog.open = True
                page.update()

            elif format_dropdown.value == 'xlsx':
                # Sử dụng ExcelWriter để ghi nhiều sheet vào cùng file
                with pd.ExcelWriter(output_path_xlsx, mode='a' if os.path.exists(output_path_xlsx) else 'w', engine='openpyxl') as writer:
                    table_df.to_excel(writer, sheet_name=table_name, index=False)
                page.dialog = ft.AlertDialog(title=ft.Text("✅ Đã lưu tất cả file thành công!"))
                page.dialog.open = True
                page.update()

            else:
                page.dialog = ft.AlertDialog(title=ft.Text("❌ Định dạng không hợp lệ!"))
                page.dialog.open = True
                page.update()
        
            