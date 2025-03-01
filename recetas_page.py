import flet as ft

class Resetas:
    def __init__(self, page: ft.Page, controller):
        """Paguina de Inicio"""
        self.page = page
        self.controller = controller
        
    def build_page(self):
        """Constructor de la pagina de inicio"""
        Page = ft.View( 
            route="/",
            appbar=self.controller.Start_App_Bar("resetas", True),
            controls=[
                ft.Container(content=ft.Column(
                    controls=[
                        ft.Text("Pagina Resetas")
                    ]
                ))
            ]
        )
        
        return Page
    
    def get_page(self):
        """Mostrar la pagina de inicio"""
        return self.build_page()