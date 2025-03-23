import flet as ft

def show_dialog(page, message):
    dlg = ft.AlertDialog(title=ft.Text(message))
    page.dialog = dlg
    dlg.open = True
    page.update()

def add_table(table_name_input, tables, page, update_status, refresh_callback):
    table_name = table_name_input.value.strip()
    if table_name and table_name not in tables:
        tables[table_name] = []
        table_name_input.value = ""
        update_status(f"✅ Đã thêm bảng: {table_name}", "green")
        refresh_callback(page)
    else:
        update_status("❌ Tên bảng không hợp lệ hoặc đã tồn tại", "red")

def delete_table(table_name, tables, page, update_status, refresh_callback):
    if table_name in tables:
        del tables[table_name]
        update_status(f"✅ Đã xóa bảng: {table_name}", "green")
        refresh_callback()
    else:
        update_status("❌ Không tìm thấy bảng", "red")