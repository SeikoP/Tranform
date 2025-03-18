import pandas as pd
import json
import flet as ft
import os
import csv

def analyze_dependencies(df: pd.DataFrame):
    """Phân tích dữ liệu để đề xuất bảng Dim và Fact"""
    suggestions = {'Dim': [], 'Fact': []}
    for col in df.columns:
        unique_count = df[col].nunique()
        total_count = len(df)
        # Nếu cột có ít giá trị duy nhất, đề xuất làm bảng Dim
        if unique_count < total_count * 0.3:  # Ngưỡng 30% để coi là thực thể độc lập
            suggestions['Dim'].append(col)
        else:
            suggestions['Fact'].append(col)
    return suggestions

def normalize_to_3nf(df: pd.DataFrame, erd: dict):
    normalized_tables = {}
    
    # Xử lý bảng Dim
    for table_name, columns in erd.items():
        if table_name.lower().startswith('dim_'):
            selected_columns = [col['name'] for col in columns if col['name'] in df.columns]
            if not selected_columns:
                continue
            
            table_df = df[selected_columns].copy().dropna(subset=selected_columns)
            primary_key_col = next((col['name'] for col in columns if col.get('is_primary', False)), None)
            
            if primary_key_col and primary_key_col in table_df.columns:
                table_df = table_df.drop_duplicates(subset=[primary_key_col]).reset_index(drop=True)
                if f'{primary_key_col}_id' not in table_df.columns:
                    table_df.insert(0, f'{primary_key_col}_id', table_df.index + 1)
            
            normalized_tables[table_name] = table_df
    
    # Xử lý bảng Fact
    for table_name, columns in erd.items():
        if table_name.lower().startswith('fact_'):
            fact_columns = [col['name'] for col in columns if col['name'] in df.columns]
            if not fact_columns:
                continue
            
            fact_df = df[fact_columns].copy().dropna(subset=fact_columns)
            primary_key_col = next((col['name'] for col in columns if col.get('is_primary', False)), None)
            
            for col in columns:
                col_name = col['name']
                ref_table = col.get('ref_table')
                ref_column = col.get('ref_column')
                
                if ref_table and ref_table in normalized_tables:
                    dim_df = normalized_tables[ref_table]
                    dim_pk_col = next((c['name'] for c in erd[ref_table] if c.get('is_primary', False)), None)
                    
                    if ref_column and col_name in fact_df.columns and dim_pk_col:
                        if ref_column != dim_pk_col:
                            mapping = dict(zip(dim_df[ref_column], dim_df[f'{dim_pk_col}_id']))
                            fact_df[col_name] = fact_df[col_name].map(mapping).fillna(fact_df[col_name])
                        
                        fact_df = fact_df.merge(
                            dim_df[[f'{dim_pk_col}_id', ref_column if ref_column else dim_pk_col]],
                            how='left',
                            left_on=col_name,
                            right_on=ref_column if ref_column else dim_pk_col
                        )
                        fact_df = fact_df.drop(columns=[col_name, ref_column if ref_column else dim_pk_col], errors='ignore')
                        fact_df = fact_df.rename(columns={f'{dim_pk_col}_id': f'{col_name}_id'})
            
            normalized_tables[table_name] = fact_df
    
    return normalized_tables

def normalization(df: pd.DataFrame, page: ft.Page, format_dropdown, data_path: str = r'D:\TranformData\Tranform_Data\data'):
    if df is None or df.empty:
        page.dialog = ft.AlertDialog(title=ft.Text("⚠ Dữ liệu đầu vào trống hoặc không hợp lệ!"))
        page.dialog.open = True
        page.update()
        return

    erd_path = os.path.join(data_path, 'erd.json')
    if not os.path.exists(erd_path):
        page.dialog = ft.AlertDialog(title=ft.Text("⚠ Bạn chưa lưu cấu trúc ERD!"))
        page.dialog.open = True
        page.update()
        return

    try:
        with open(erd_path, 'r', encoding='utf-8') as file:
            erd = json.load(file)
        
        # Kiểm tra tính hợp lệ của ERD
        for table_name, columns in erd.items():
            if table_name.lower().startswith('dim_') and not any(col.get('is_primary', False) for col in columns):
                page.dialog = ft.AlertDialog(title=ft.Text(f"⚠ Bảng {table_name} phải có khóa chính!"))
                page.dialog.open = True
                page.update()
                return
    except Exception as e:
        page.dialog = ft.AlertDialog(title=ft.Text(f"⚠ Không thể tải file erd.json: {str(e)}"))
        page.dialog.open = True
        page.update()
        return

    file_picker = ft.FilePicker(on_result=lambda e: save_files(e, df, erd, page, format_dropdown))
    page.overlay.append(file_picker)
    page.update()
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

    normalized_tables = normalize_to_3nf(df, erd)
    excel_writer = None
    output_excel_path = os.path.join(save_path, "normalized_data.xlsx") if format_dropdown.value == 'xlsx' else None

    if format_dropdown.value == 'xlsx' and os.path.exists(output_excel_path):
        os.remove(output_excel_path)

    result_message = "✅ Đã chuẩn hóa thành công:\n"
    for table_name, table_df in normalized_tables.items():
        try:
            if format_dropdown.value == 'csv':
                table_df.to_csv(os.path.join(save_path, f"{table_name}.csv"), index=False, encoding='utf-8', quoting=csv.QUOTE_NONE, escapechar='\\')
            elif format_dropdown.value == 'xlsx':
                if excel_writer is None:
                    excel_writer = pd.ExcelWriter(output_excel_path, engine='openpyxl')
                table_df.to_excel(excel_writer, sheet_name=table_name, index=False, quoting=csv.QUOTE_NONE, escapechar='\\')
            result_message += f"- {table_name}: {len(table_df)} bản ghi\n"
        except Exception as e:
            page.dialog = ft.AlertDialog(title=ft.Text(f"❌ Lỗi khi lưu file {table_name}: {str(e)}"))
            page.dialog.open = True
            page.update()
            return

    if excel_writer:
        excel_writer.close()

    page.dialog = ft.AlertDialog(title=ft.Text(result_message))
    page.dialog.open = True
    page.update()