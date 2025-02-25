import flet as ft

class AppBarr:
    def __init__(self, page: ft.Page, controller):
        """Barra de la aplicacion"""
        self.page = page
        self.controller = controller
        
    def build_appBarr(self, Titulo:str):
        """Constructor de la barra de la aplicacion"""
        appBar = ft.AppBar(
            bgcolor=ft.Colors.PRIMARY,
            adaptive=True,
            title=ft.Text(value=Titulo, color=ft.Colors.SURFACE, height=ft.FontWeight.BOLD, size=25),
        )
        
        return appBar
    
    def get_appBarr(self, Titulo: str):
        """Mostrar la barra de la aplicacion"""
        return self.build_appBarr(Titulo)
    
class AppBarr_Son(AppBarr):
    def __init__(self, page, controller):
        super().__init__(page, controller)
        
    def build_appBarr(self, Titulo:str):
        """Constructor de la barra de la aplicacion"""
        appBar = ft.AppBar(
            bgcolor=ft.Colors.PRIMARY,
            title=ft.Text(value=Titulo, color=ft.Colors.SURFACE),
            leading=ft.IconButton(ft.Icons.ARROW_BACK, icon_color=ft.Colors.SURFACE, on_click=lambda e: self.controller.go_back()),  # Flecha de retroceso
        )
        
        return appBar
        
