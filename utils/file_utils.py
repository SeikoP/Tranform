import os
import pandas as pd
from utils.ui_utils import show_dialog
from utils.data_analysis import normalize_to_3nf

def get_data(page):
    file_path = page.session.get("file_path")
    if file_path and os.path.exists(file_path):
        return pd.read_csv(file_path)
    return None

def on_file_selected(e, page, refresh_callback):
    if e.files:
        file_path = e.files[0].path
        if os.path.getsize(file_path) > 100 * 1024 * 1024:
            show_dialog(page, "⚠️ Tệp quá lớn (>100MB)!")
            return
        page.session.set("file_path", file_path)
        page.session.get("status_bar").content.value = f"📄 Đã chọn: {os.path.basename(file_path)}"
        page.session.get("status_bar").content.color = "blue"
        refresh_callback(page)
    else:
        show_dialog(page, "⚠️ Chưa chọn tệp!")

def on_export_selected(e, page):
    if e.path:
        df = get_data(page)
        if df is not None:
            tables = page.session.get("tables")
            try:
                normalized_tables = normalize_to_3nf(df, tables)
                for table_name, table_df in normalized_tables.items():
                    table_df.to_csv(os.path.join(e.path, f"{table_name}.csv"), index=False, encoding='utf-8')
                show_dialog(page, "✅ Đã xuất dữ liệu chuẩn hóa thành công!")
                page.session.get("status_bar").content.value = "✅ Xuất thành công!"
                page.session.get("status_bar").content.color = "green"
            except Exception as ex:
                show_dialog(page, f"⚠️ Lỗi chuẩn hóa: {str(ex)}")
                page.session.get("status_bar").content.value = f"❌ Xuất thất bại: {str(ex)}"
                page.session.get("status_bar").content.color = "red"
    else:
        show_dialog(page, "⚠️ Chưa chọn thư mục!")