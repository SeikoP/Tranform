import flet as ft

def create_status_bar(page: ft.Page):
    status_text = ft.Text("✅ Sẵn sàng", size=14, color="green")
    status_bar = ft.Container(
        content=status_text, padding=ft.padding.only(left=20, right=20, top=10, bottom=10),
        bgcolor="white", alignment=ft.alignment.center_left, border=ft.border.only(top=ft.BorderSide(1, "#E5E7EB"))
    )
    
    def update_status(text, color="black"):
        status_text.value = text
        status_text.color = color
        page.update()
    
    page.session.set("status_bar", status_bar)
    return status_bar, update_status