import flet as ft

from home_page import Home
from appbarr import AppBarr, AppBarr_Son
from contactos_page import Contactos

class View:
    def __init__(self, page: ft.Page):
        """Interfaz grafica de la aplicacion"""
        self.page = page
        self.controller = None
        
    def Start_App(self):
        """Inicializador de la aplicacion"""
        if self.controller is None:
            raise ValueError("No se a podido cargar el controlador correctamente")
        
        self.Main = Home(self.page, self.controller)
        self.Contactos_Page = Contactos(self.page, self.controller)
        self.AppBarr = AppBarr(self.page, self.controller)
        self.AppBarr_Son = AppBarr_Son(self.page, self.controller)
        
        self.navigate_to("/")
        
    def go_back(self):
        """Regresar a la vista anterior"""
        if len(self.page.views) > 1:
            self.page.views.pop()
            top_view = self.page.views[-1]
            self.page.update()
        
    def navigate_to(self, view_name: str):
        """Navegacion de la aplicacion"""
        match view_name:
            case "/":
                self.page.views.clear()
                self.page.views.append(self.Main.get_page())
            case "/contactos":
                self.page.views.append(self.Contactos_Page.get_page())
            case _:
                self.page.views.append(self.Main.get_page())
            
        self.page.update()
        
    def Start_App_Bar(self, Titulo: str, SubPagina:bool):
        """Mostrar la barra de la aplicacion"""
        match SubPagina:
            case True:
                appbarr = self.AppBarr_Son.get_appBarr(Titulo)
            case False:
                appbarr = self.AppBarr.get_appBarr(Titulo)
            case _:
                appbarr = self.AppBarr.get_appBarr(Titulo)
                
        return appbarr
                
        
        
        
        
