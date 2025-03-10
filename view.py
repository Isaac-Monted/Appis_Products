import flet as ft

from home_page import Home
from appbarr import AppBarr, AppBarr_Son
from contactos_page import Contactos
from recetas_page import Resetas
from categorias_page import Categorias
from assets import Imagenes

class View:
    def __init__(self, page: ft.Page):
        """Interfaz grafica de la aplicacion"""
        self.page = page
        self.controller = None
        
        # Crear el FilePicker una sola vez
        self.file_picker = ft.FilePicker()
        # Agregarlo al overlay de la página
        self.page.overlay.append(self.file_picker)
        self.page.update()
        
        #self.page.horizontal_alignment = ft.CrossAxisAlignment.START
        
    def Start_App(self):
        """Inicializador de la aplicacion"""
        if self.controller is None:
            raise ValueError("No se a podido cargar el controlador correctamente")
        
        #Instancias
        self.Main = Home(self.page, self.controller)
        self.Contactos_Page = Contactos(self.page, self.controller)
        self.Resetas_Page = Resetas(self.page, self.controller)
        self.Categorias_Page = Categorias(self.page, self.controller)
        
        self.AppBarr = AppBarr(self.page, self.controller)
        self.AppBarr_Son = AppBarr_Son(self.page, self.controller)
        self.FilePiker = FilePiker(self.page, self.controller, self.file_picker)
        self.loadAppView = LoadAppView(self.page, self.controller)
        self.loadPhotoView = LoadPhotoView(self.page, self.controller)
        self.Assets = Imagenes()
        
        self.navigate_to("/")
        
        self.Start_View_Photo(self.Assets.Get_Image("Panela"))
        
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
    
    def Start_file_picker(self, control, types, Id):
        """Iniciar el selector de archivos"""
        self.FilePiker.setup_for_control(control, Id)
        
        match types:
            case "Abrir":
                print("Entro a abrir")
                self.FilePiker.pick_files()
                print("Abrió abrir")
            case "Guardar":
                self.FilePiker.save_file()
            case "Multiple":
                self.FilePiker.pick_files(allow_multiple=True)
            case _:
                self.FilePiker.pick_files()
        
    def Start_alert_dialog(self, type=None, title=None, message=None, description=None, actions=None, functions=None, error= None):
        self.alertDialog = MessageBox(self.page, type, title, message, description, actions, functions, error)
        self.alertDialog.star_message(self.alertDialog.buid_message())
        
    def Start_snackbar(self, message: str, color: ft.Colors, duration: int):
        snackbar = SnackBar(self.page, message, color, duration)
        snackbar.show_snackbar(snackbar.build_snackbar())
        
    def Start_View_Photo(self, Img):
        if Img == None:
            Img = self.Assets.Get_Image("Vacio")
        self.loadPhotoView.show_load_img_view(self.loadPhotoView.buld_img_view(Img))

class FilePiker:
    def __init__(self, page, controller, file_picker):
        self.page = page
        self.controller = controller
        self.file_picker = file_picker
    
    def setup_for_control(self, control, Id):
        self.file_picker.on_result = lambda e: self.on_file_selected(e, control, Id)
    
    def on_file_selected(self, e, control, Id):
        if e.files:
            root = e.files[0].path
            print(f"Archivo seleccionado: {root}")
            self.controller.Save_selected_file_picker(control, root, Id)
        else:
            print("No se seleccionó ningún archivo.")
    
    def pick_files(self, allow_multiple=False):
        self.file_picker.pick_files(allow_multiple=allow_multiple, allowed_extensions=["png", "jpg"])
    
    def save_file(self):
        self.file_picker.save_file()
    
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
                # Verificar que self.message no sea None
                if self.message is None:
                    raise ValueError("Message cannot be None for options type.")

                # Verificar que actions y functions no sean None y tengan la misma longitud
                if self.actions is None or self.functions is None:
                    raise ValueError("Actions and functions must be provided for options type.")
                if len(self.actions) != len(self.functions):
                    raise ValueError("Actions and functions must have the same length.")

                # Crear el cuadro de diálogo
                mensaje = ft.AlertDialog(
                    title=ft.Text(self.title),  # Título del cuadro de diálogo
                    content=ft.Container(
                        content=ft.Column([ft.Text(self.message)]),
                        width=300,  # Ajustamos el ancho del contenedor
                        height=100,  # Ajustamos la altura del contenedor
                    ),
                    actions=[],  # Inicialmente sin botones, los agregamos después
                )

                # Depuración: Verificar los valores de las variables
                print(f"Título del cuadro de diálogo: {self.title}")
                print(f"Mensaje del cuadro de diálogo: {self.message}")
                print(f"Actions: {self.actions}")
                print(f"Functions: {self.functions}")

                # Crear las acciones de los botones dinámicamente
                actions = [
                    ft.TextButton(
                        option, 
                        on_click=lambda e, func=func, mensaje=mensaje: (func() if func else None, self.page.close(mensaje))
                    )
                    for option, func in zip(self.actions, self.functions)
                ]

                # Verificar que actions no esté vacío
                if not actions:
                    raise ValueError("Actions list cannot be empty for options type.")

                # Actualizar los botones en el cuadro de diálogo
                mensaje.actions = actions

                # Verificar que 'mensaje' esté correctamente creado
                if mensaje is None:
                    raise RuntimeError("Failed to create the dialog box.")

                # Retornar el cuadro de diálogo
                return mensaje
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

class LoadPhotoView:
    def __init__(self, page, controller, ):
        self.page = page
        self.controller = controller
        
    def buld_img_view(self, Img):
        load = ft.AlertDialog(
            modal=False,
            content=ft.Column(
                height=400,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Text("Imagen Guardada", size=20, weight= ft.FontWeight.BOLD),
                    #ft.Image(src=f"data:image/png;base64,{Img}", width=350, height=350),
                    ft.Image(src_base64=Img, width=350, height=350),
                ]
            )
        )
        return load
        
    def show_load_img_view(self, viewer):
        self.page.open(viewer)
    
    def hide_load_img_view(self, viewer):
        self.page.close(viewer)
