import flet as ft

import controller as ctrl
import view as vw

def main(page: ft.Page):
    """Inicializador de la aplicacion"""
    
    view = vw.View(page)
    controller = ctrl.Controller(view)
    
    view.controller = controller
    view.Start_App()
    
if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER, port=8000)