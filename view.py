import flet as ft

from home_page import Home
from appbarr import AppBarr, AppBarr_Son
from contactos_page import Contactos
from recetas_page import Resetas
from categorias_page import Categorias

class View:
    def __init__(self, page: ft.Page):
        """Interfaz grafica de la aplicacion"""
        self.page = page
        self.controller = None
        
        #self.page.horizontal_alignment = ft.CrossAxisAlignment.START
        
    def Start_App(self):
        """Inicializador de la aplicacion"""
        if self.controller is None:
            raise ValueError("No se a podido cargar el controlador correctamente")
        
        #Instancias
        self.Main = Home(self.page, self.controller)
        self.Contactos_Page = Contactos(self.page, self.controller)
        self.Resetas_Page = Resetas(self.page, self.controller)
        self.Categorias_Page = Contactos(self.page, self.controller)
        
        self.AppBarr = AppBarr(self.page, self.controller)
        self.AppBarr_Son = AppBarr_Son(self.page, self.controller)
        self.FilePiker = FilePiker(self.page, self.controller)
        self.loadAppView = LoadAppView(self.page, self.controller)
        
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
            case "/resetas":
                self.page.views.append(self.Resetas_Page.get_page())
            case "/categorias":
                self.page.views.append(self.Categorias_Page.get_page())
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
    
    def Start_file_picker(self, control, types):
        dialog = self.FilePiker.get_content(control)
        self.page.add(dialog)
        print(f"Paso con :{control} | {types}")
        match types:
            case "Abrir":
                print("Entro a abrir")
                dialog.pick_files()
                "Abrio abrir"
            case "Guardar":
                dialog.save_file()
            case "Multiple":
                dialog.pick_files(allow_multiple=True)
            case _:
                dialog.pick_files()
        
    def Start_alert_dialog(self, type=None, title=None, message=None, description=None, actions=None, functions=None, error= None):
        self.alertDialog = MessageBox(self.page, type, title, message, description, actions, functions, error)
        self.alertDialog.star_message(self.alertDialog.buid_message())
        
    def Start_snackbar(self, message: str, color: ft.Colors, duration: int):
        snackbar = SnackBar(self.page, message, color, duration)
        snackbar.show_snackbar(snackbar.build_snackbar())
                
class FilePiker:
    def __init__(self, page, controller):
        self.page = page
        self.controller = controller
    
    def init_content(self, Control):
        file_picker = ft.FilePicker(
            on_result=lambda e: self.on_file_selected(e, Control),
            
            #allowed_extensions=extencions,
            #dialog_title=title,
        )
        
        return file_picker
    
    def on_file_selected(self, e, control):
        if e.files:
            root = e.files[0].path
            print(f"Archivo seleccionado: {root}")
            self.controller.Save_selected_file_picker(control, root)
        else:
            print("No se seleccionó ningún archivo.")
    
    def get_content(self, control):
        return self.init_content(control)
    
class MessageBox:
    def __init__(self,page, type: str, title: str, message: str, description: str=None, actions: list=None, functions: list=None, error: str=None):
        self.page = page
        self.type = type
        self.title = title
        self.message = message
        self.description = description
        self.actions = actions
        self.functions = functions
        self.error = error
    
    def buid_message(self):
        match self.type:
            case "normal":
                mensaje = ft.AlertDialog(
                    title=ft.Text(self.title),  # Título del cuadro de diálogo
                    content=ft.Container(
                        content=ft.Column([ft.Text(self.message)]),
                        width=300,  # Ajustamos el ancho del contenedor
                        height=100,  # Ajustamos la altura del contenedor
                    ),
                actions=[ft.TextButton("Aceptar", on_click=lambda e: self.page.close(mensaje))],  # Botón para cerrar
                )
                return mensaje
            case "informative":
                mensaje = ft.AlertDialog(
                    icon=ft.Icon(ft.Icons.INFO, color="White"),
                    title=ft.Text(self.title, color="White"),  # Título del cuadro de diálogo
                    bgcolor= ft.Colors.BLUE_800, #Color del cuadro de dialogo
                    content=ft.Container(
                        content=ft.Column([ft.Text(self.message, color="White")]),
                        width=300,  # Ajustamos el ancho del contenedor
                        height=100,  # Ajustamos la altura del contenedor
                    ),
                actions=[ft.TextButton("Aceptar", on_click=lambda e: self.page.close(mensaje), style=ft.ButtonStyle(color="White"))],  # Botón para cerrar
                )
                return mensaje
            case "warning":
                txtColor = ft.Colors.BLACK
                mensaje = ft.AlertDialog(
                    icon=ft.Icon(ft.Icons.WARNING, color= txtColor),
                    title=ft.Text(self.title, color= txtColor),  # Título del cuadro de diálogo
                    bgcolor= ft.Colors.YELLOW_800, #Color del cuadro de dialogo
                    content=ft.Container(
                        content=ft.Column([ft.Text(self.message, style=ft.TextStyle(color=txtColor))]),
                        width=300,  # Ajustamos el ancho del contenedor
                        height=100,  # Ajustamos la altura del contenedor
                    ),
                actions=[ft.TextButton("Aceptar", on_click=lambda e: self.page.close(mensaje), style=ft.ButtonStyle(color=txtColor))],  # Botón para cerrar
                )
                return mensaje
            case "danger":
                mensaje = ft.AlertDialog(
                    icon=ft.Icon(ft.Icons.DANGEROUS, color="White"),
                    title=ft.Text(self.title, color="White"),  # Título del cuadro de diálogo
                    bgcolor= ft.Colors.RED_800, #Color del cuadro de dialogo
                    content=ft.Container(
                        content=ft.Column([ft.Text(self.message, color="White")]),
                        width=300,  # Ajustamos el ancho del contenedor
                        height=100,  # Ajustamos la altura del contenedor
                    ),
                actions=[ft.TextButton("Aceptar", on_click=lambda e: self.page.close(mensaje), style=ft.ButtonStyle(color="White"))],  # Botón para cerrar
                )
                return mensaje
            case "options":
                actions = [ft.TextButton(option, on_click=lambda e, func=func: func()) for option, func in zip(self.actions, self.functions)]
                mensaje = ft.AlertDialog(
                    title=ft.Text(self.title),  # Título del cuadro de diálogo
                    content=ft.Container(
                        content=ft.Column([ft.Text(self.message)]),
                        width=300,  # Ajustamos el ancho del contenedor
                        height=100,  # Ajustamos la altura del contenedor
                    ),
                actions=actions,  # Botón para cerrar
                )
            case "descriptive":
                mensaje = ft.AlertDialog(
                    title=ft.Text(self.title),  # Título del cuadro de diálogo
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(self.message, size=15),
                            ft.Text(self.description, size=12)
                        ]),
                        width=300,  # Ajustamos el ancho del contenedor
                        height=100,  # Ajustamos la altura del contenedor
                    ),
                actions=[ft.TextButton("Aceptar", on_click=lambda e: self.page.close(mensaje))],  # Botón para cerrar
                )
                return mensaje
            case "error":
                mensaje = ft.AlertDialog(
                    icon=ft.Icon(ft.Icons.DANGEROUS, color="White"),
                    title=ft.Text(self.title, color="White"),  # Título del cuadro de diálogo
                    bgcolor= ft.Colors.RED_800, #Color del cuadro de dialogo
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(self.message, size=15, color="White"),
                            ft.Text(self.description, color="White"),
                            ft.Text(self.error, size=12, color="White")
                        ]),
                        width=300,  # Ajustamos el ancho del contenedor
                        height=100,  # Ajustamos la altura del contenedor
                    ),
                actions=[ft.TextButton("Aceptar", on_click=lambda e: self.page.close(mensaje), style=ft.ButtonStyle(color="White"))],  # Botón para cerrar
                )
                return mensaje
            case _:
                mensaje = ft.AlertDialog(
                    icon=ft.Icon(ft.Icons.DANGEROUS, color="White"),
                    title=ft.Text("Error al llamar la funcion MessageBox", color="White"),  # Título del cuadro de diálogo
                    bgcolor= ft.Colors.RED_800, #Color del cuadro de dialogo
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Error de sintaxis", size=15, color="White"),
                            ft.Text("Hubo un error al moento de declarar la funcion en el codigo", color="White"),
                            ft.Text("Por favor revise que se haya escrito correctamente la funcion en el llamamiento de la funcion", size=12, color="White")
                        ]),
                        width=300,  # Ajustamos el ancho del contenedor
                        height=100,  # Ajustamos la altura del contenedor
                    ),
                actions=[ft.TextButton("Aceptar", on_click=lambda e: self.page.close(mensaje), style=ft.ButtonStyle(color="White"))],  # Botón para cerrar
                )
                return mensaje
    
    
    def star_message(self, message):
        self.page.open(message)
        self.page.update()

class SnackBar:
    def __init__(self, page, message: str, color: ft.Colors, duration: int):
        self.page = page
        self.message = message
        self.color = color
        self.duration = duration
        
    def build_snackbar(self):
        snackbar = ft.SnackBar(
            content=ft.Text(value=self.message, color=ft.Colors.INVERSE_SURFACE),
            duration=self.duration,
            bgcolor=self.color,
        )
        
        return snackbar

    def show_snackbar(self, snackbar):
        self.page.open(snackbar)
        self.page.update()
        
class LoadAppView:
    def __init__(self, page, controller):
        self.page = page
        self.controller = controller
        
        self.load = ft.AlertDialog(
            bgcolor=ft.Colors.TRANSPARENT,
            modal=True,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.ProgressRing(width=100,height=100)
                ]
            )
        )
        
    def show_load_app_view(self):
        self.page.open(self.load)
    
    def hide_load_app_view(self):
        self.page.close(self.load)
  
