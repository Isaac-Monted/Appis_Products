import flet as ft
import model as md

class Controller:
    def __init__(self, view):
        """Controlador de la aplicacion"""
        self.view = view
        self.model = md.Model()
        
    def navigate_to(self, view_name: str):
        """Navegacion de la aplicacion"""
        self.view.navigate_to(view_name)
        
    def go_back(self):
        """Regresar a la vista anterior"""
        self.view.go_back()
        
    def Start_App_Bar(self, Titulo: str, SubPagina:bool):
        """Mostrar la barra de la aplicacion"""
        appbar = self.view.Start_App_Bar(Titulo, SubPagina)
        return appbar