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
        self.Categorias_Page = Contactos(self.page, self.controller)
        
        self.AppBarr = AppBarr(self.page, self.controller)
        self.AppBarr_Son = AppBarr_Son(self.page, self.controller)
        self.FilePiker = FilePiker(self.page, self.controller, self.file_picker)
        self.loadAppView = LoadAppView(self.page, self.controller)
        self.loadPhotoView = LoadPhotoView(self.page, self.controller)
        
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
        print(Img)
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

class LoadPhotoView:
    def __init__(self, page, controller, ):
        self.page = page
        self.controller = controller
        
    def buld_img_view(self, Img):
        if Img is None:
            Img = "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAIAAAD8QzmZAAAAWElEQVRIDbXBAQEAAAABIP6PzgpVqmvNzMkAAAAAElFTkSuQmCC"
        else: 
            Img = "aVZCT1J3MEtHZ29BQUFBTlNVaEVVZ0FBQVRZQUFBQzhDQVlBQUFEeTRJS2pBQUFBR1hSRldIUlRiMlowZDJGeVpRQkJaRzlpWlNCSmJXRm5aVkpsWVdSNWNjbGxQQUFBTm50SlJFRlVlTnJzZlFtWUZOVzU5dW1lbFhXYUFReTdBeGdOS2dRbDNDUXVMSEg3azRoQVROQmZ2UUkvR3BSY0ZhSWtseVFLYUNKeEM2aHhJV29ZakJwRkRZTm9mRndpNDBiaUpjQ0lDMWNpTUN5Q1JwWVpobVhXN3YrOE5lYzBwNnRyT1ZWZDFiUHd2Yy9Uejh6MFZGZFZmM1hxcmZkYnpuY1lJeEFJQkFLQlFDQVFDQVFDZ1VBZ0VBZ0VBb0ZBSUJBSUJBS0JRQ0FRQ0FRQ2dVQWdFQWdFQW9GQUlCQUlCQUtCUUNBUUNBUUNnVUFnRUFnRUFvRkFJQkFJQkFLQlFDQVFDQVFDZ1VBZ0VBZ0VBb0ZBSUJBSUJBS0JRQ0FRQ0FRQ2dVQWdFQWdFQW9GQUlCQUlCQUtCUUNBUUNBUUNvVzBoUWlad1J5S1JHTTUveFBnTFA2djRxNUsvS2lLUlNCVlpoMEFndEJVaW04QmZDL2xyVmNJWnkvbHJDbG1NUUNDMFJpS0xnYUFFVWZuQmVxSHFDQVFDb2NVSmJReC9MVWtFaDVsa1ZRS2g1WEhNeGRpZ3p2aVBDZncxbDc5S1FqaEVhU1FTbVlwZlh1amNheFVOc1JRc3Zlamc1NlZrQmdJUlc3Q0VCa1YxQTJ0T0JJUUpnOXc0c1NWb2lLVmhLcEViSVd6a0VxSFpZK3Z1L2V5MXRWdlkvM3l5aTYzNjMxMXN5OGJQR090YnpNWVA2Y01XVGorUERlemR6ZTZqaU5kdFc5bWx0L0ZIejdyYVkzNmdIYzdKWllkeWplRzJoQk0rSTNJamtHTHpUMnBUK0krRlhnaHQzYVpkN01HVmE5bGpmL3VRc1IzN0hMZWRObVVVZS9UR2NiYi9YenYrRXJicmpiZFl2OXFETk5JNDl1Y1dTbklqNVVZZ1l2TkJhR09nREpobURBM0s3Q0ZPWm5lVnJYRWxzelNjM0pmdGUzUTY2OWFsUTlxLzZuWit4dDQ4ODF6V2M5ZE9HbWxFYmdRaU50K0VWaUlVMmdTZDdWOWZ1NVhOZmVvdHR2clZEek03c0FPNWJiLzdQclozemk5cHBGbVRHd3FjeDNKeXF5Q3JFSWpZckVrTmNiUzVPbTduSDE1Y3k2Yi82VzNHUHY0c3NPT1B2M2drSzVzM0tlMzllUFVCdG5Id1VGWmZ2WTlHRzVFYmdZak5rMHFEMnpuR2JkdG55ejltays1YzRkM2QxTVN5KzZleUg0MDVPZTM5TDYrNW51MThiSW5uL2ZYNndVVFdhZml3NU45N3lsYXk2blhyMnMzZzI1ZmJnUjNPelNGeUl3U09hQnNudFNuOHgzbzNVb1BMT2ZqcXhXelNkVXRDSXpYQUlFMExkQnAxbG1kQysvcVdqYXpucjM2ZWZDLzMrQUZzNEtzdnNLSHIvc0dLVGovZDl6bm1GeFduL2QxcDRDRGI3WFdPaGMvMytNNTNQSjlMdDZZNmxoK1BNNkd5VjczUXVSZk4zaUFjdTRwTmxIQkFBam5HMHBBVW1MWDROYmJpK1RWWk83ZlhTbWV3YzBjTVRIbXYvcDNWN0tPeEYyaDl2dCswcWF6bncvZFpxandReUtEbm4ySTVBL3F4ZjQwY3hRNXQzWklrbjBIdnZja1MxZFVwN3dPbnJIcUY1UTA5SmZuK0NmZitqbldaY1RXTDc5akpHcmR0VDVMbXdTZWVacHR2bVo5eUhqM3V1STAxZlBDUjhmbW03VHZaQjZkL0srVjhqcjl4Sm92OVpEcUxWMVZ6bDd2YTJBN2JmM0hiSFd6UEcyL29YY3RJbEgyWlY4anFvMUZTYm9SalY3R0pPWm5yM1VqdHQwKzl5d2I5YUdGV1NZMFZkV0NEKy9pdi9UV1VEeWVUbWdjZnNYUmRRVXhiTHI2TVJZcUtXTWtmSDBxK0QvZTBrUk1LU0VVbE5XRHYvUStudlAvcERUODFmb0xJUUxaNGJUenRUSGFvWWtQS2VZQmNRWWI0LzhlRGg3Rm9yQ2hsdnljdGZZeDF2ZnhTVnZuRHl3M0NrOXMxY2dMcy84b0tRM1ZxUFZrVGNkYXpvWmFVRytIWUpUYmhlbUthVW9uZE5xaERpMXl5aU0xWlVNYnYrQ05aSmJWbHY3N1VzbWkzYnNOSFdydm9QZk8vRE5MYXZlajN0dHVBb0E0L3RZemxuM1ZHaWdzSnhRUlNNYU9ScXlrM0lMSHgrVitXSi8vdU1MQWs3ZitmbnZQOUZEWFg4YkpKYlB0Vk0xSmlmdGp1azhuVERJWGE2dy8zcDdtOVJHNEVJclowVWxzbzNFOWJTZlN6UDd6T1JseThNTkJzcHl0Tzdzc1dMN2lVN1h0NWptWGl3UEN2VnJ5b3RhdUNZYWNZN3FSWmRhV1IyMXZ2V0JLUWRDM2RBSFdud2t4QVI3WldHai9oOWtyeVZNK3BHM2MvYTE5NnhUYVJBWlVJZ2k0K1o3UitUSVRJalhBc0VadG9LUVE1WWRzNUE3RTBKQWZ1dXYrVnJLbXoyZGRkd0xhOCtndVdlR1ltKy9HRkl5eHIySktianpsYmE3ZFFZVTNiM1l0NWE3ZHVhM1laVHh2bTYvU2g3Z3JQUG9NTnZuV3U4VHBwMVYvVFZDRmlmTGxEVDJGZlhmTldtbHVKOStzM2ZHQzdmNm4rMUl5dUYzTExUU1JVY292UmJVcG9WOFFta2dSd1BXM2phU2poUUN4dHl6OCt6UnFwVFpzNGtyMzd5V2ZzM0Z1V3NRbnpsaG54UEpDckhick91VWtyYXdnbEJkSndRNjZJZHgxYXY4SDMxNERiV2wzK05tdXN0blpWRWVQYmNjRjRsamhRdzNvLzg3amhmbVlEUnlJNXJER1N6R25OdXVqZzU5U2xtTkIraUUxSkV0aTZJMWZkczdLNWhDT2JzVFIrck1kS20yY3JnRXlSbkVBOGI5RDV0eHNrdDcvRytseStjdlBQWFhkZEwxeEV0OEI3NTlITkN2REEydFRrWWY2d29mckV4dDFXWkM2MzNiTW9MZHNwZ2Y4anNRRENSVEpCdXF4d2x6dGUrRjNYWTlScHVzWVNoNk41YkY5K2dmeVRwbHNSMmhleENWS3pUUktBUE9CNmdtQmFFMEJ5eFZjdHRpUTN1Smx1TldFNzUvM0crS25XcjZYdGg1Tkw1OHNuR1FrRTgyeUdhRkdYdE8wTEJ4N1BhdDllN2VsN3FFa0pIQU9aV0VONWptaCt4aUJyQzJWcDkzMmc3a0IrLzM1dWhWOVNtMCtrUm1oWHhLYVFtbVZzQlZsUGtFZldYRSt2K1Bnek52c1ByMXYrcStma0t4dy9xc2EyaHBROWx4YlVCK0VnSG9ZNDNOYnJaNmY4TDE1ZFk5U1JwWDFtMUZscDdpYnExdkJLOGJBNVNhSEdEUml3OE00VTBwSkpDcWtRZDl4enY2SGlCano2WU5yeDhEbVVyT3hmY0xmMk5ESVRxWlZ5VXB0SHR5WWhFN1NxQWwwZFVodngveDdPcnV2cEUwZ3NtRXMvVUJUNy9xQWhycDlGUEs3dm93K3dTTmN1ck82ZGZ4aUJlcmlaaGQrL3dGQnFJRFV6YVlCUU1ETUJwSGZneWFlYjFSbytjL1laaGpzcHQ1Y0Z3QWFoOEgzQkpVVUdFeXBRRnZFaW9ZQWkzb05QTGpPVUYzN2Y4L09iVTJyclFHaGZMZnV6UWFaeU81QmxCMzZPSURXNHVENUpiU3JkbG9SMlEyeHVwR1pNWEovemRGYlBhZEMzVG1BWGp4ek1panQzWU44NHFZL2hZaTVhdVVhckc4aUNPUlBZZjE5Mlp0cjdIL1U0WGx2SmdLdzZsQnh2WkJjbHNVRXBnYmgyUC9wNDJuNUFOc2Y5Y0R3ckVHb01NUzY0ZytwMjJHZGVMTjNFRFZWVktlVWJJRmRrYzZIMjl2emxCZHNTRkVPaFRSaG5lendpTmNJeFMyeEs5bk40UzVNYXVuUmNQdVpVMjVvMEFQVnlicVVsWjV4L0tudjNuc2xwN3lQVHFEdmR5QXk0b3YzbS9kSW9qZ1ZRUzdiLzhTZFRpbXZOMjd2VnhMVVVpTlFJN1pyWVdnV3BvUzd0eWxGc3p2ODkwN0VlTGNWdzMxdmdPS0VlYW0vekk5TURKVFl6d2NIdGd4c0pvTnBmVFJKQTRlMjY5ZlpXMlEyRVNJMFFObHBEOG1CSmk1R2FLTFRGcklFN2YzeXVOcWtCMDg0NTFmSC94dm9JVm9mVUxOWjFBbFFZcGk1aGJpYVNEWWlWQVlpbkljNEZsM0RqaEI4U3FSR09XYlRvWWk1Y3JjMWpOc1czWVpNYVhNNGxONDd6UkdZcWl0MCtsNFVFQjJKWlJrRGZSNiszb0lCWW5LNENKVklqdEh0aTQ2UW0xL1pNQS9xbmhVWnEvWXZaYTdkZG10WmFpS0FISkNqNjMzZ2Q2M3pGcFN6YXYxK3pTVmx6eHZmUXlwZlo5bHQrYlprOElGTFR2aTlpd29QQlM4M3lsUE5YUlNRU29aa1lyWlhZbEg1cWFVQkp4M2szaEtOQVBLbzBGRzB0RllNcmpZQXhwY3FOUUsyd2E5Zm5iR2RoNTR5L1MwRnhqSFVmUG96RmhwM0M4b3BTczV5SHVTdjZ4WnZ2c2dOaU1uc1F3UEcrZHQyMXJOL1ZVMWkwcUd0NlRJT1RITXBDaGx4K0Nmdnd1aHZadHVXMkUvOWJqTlFjU0FPQXNjbzVjVlMyd0huaElUK2VOVGRNTGJIWmJLN1l0cFQvdUplZlowVXJzbHRGTnMrbk5TdTI1UllHTXNvcFJzeGNHcndiVjlTQkxmN3Y4Y1prZFExZzRNeVhBMXhNd0UvRDZ2YzJPKzVrVUY5cllqdTBmWWMvbCsvMHI3UGpScDNCaXM4OGd4VjkrejhzeVVYRjEwQndIMjFrMng5K2pQMnI5TW1Nek5mbk82UFlxUS84amhYMDYrdTZMYzVyMk9PUHNFT2ovdy9icys3OU5OdU9xOWs5SzlFY2ZsRGpxcmd4eWtLNElVdEVxR08wT0Y2SnhtY3FCSEdVaGt3V09CZXNkVHVGZVZ2dkZ0dGozVnFNMFhraG5wdFh1MVdLKzZhME5SQmIxck9pWXRHVmhWYi93elNwd0djVWNGSmIrOGRyMk9rbjl2RkVhTW9GM21xbEtvMzJTQTZ3Sy9mZ0dNdVBVYTVwS3d5cXlXS1FsV1JnQmR5c1UvMDhWVVc3cUprK2psbkpqemZRWk11NTRzYTAzSjYvWm1WS2NLM0JaaTduTjBiWVlVd0F1MXZFejI5V1FPY1ZsTjF3SFNlMnRJTExhbFpVR2R4cFFHMVk0S1IyY2wrMjVkbFpicVJXS2NobXFvVWJZbmtUWWtGbE41eDVrclc2Y1NNMTJBaEpGZjRDb2E0WHBGS1NvU1dNNG1jeGVMV3ZGWCt0OTBscVFJbG9EQ3FUUkZzZFNJMko3N2hjZnNicnVBclJabE1DR3Z0aitBdGxUYXNDSWpWZ3BuQmpmZCtQRUJvQjJ3MmZYeCtVM2RxRVloTnVYZHFGUUxMZ3ZDa1BCazVxZG10OTZqenhSRnhocTVXYkVEbnJGbGQzMldydEE3T0tzWGlTMzhBMDEwVDFpU3BCNGhVYXFtSzVtNHVFelBWZi83blpxYUJaa3JqWEcxbEwxV2JKWnNCcGZoV0lsMVhVL0Nva3V6SGxZcmZKTGcrYUlLRHRuUVNOck1YWWhESFRCaURpYXVmZEhIQUd0SCt4RzZsVkNibnNaSFRMTlVweE0rdkVBRWVjMk12T3ZUSGJaWW80VmtrV0xrTk1xS0xUN0xKcjRud2NzemZHZ3dqWFRCUW9vNnZKMnVjdGxiSGZtM211UW9wMjUzZ0RjMmhwRlRDZzNBWjZ5VWlLQitOY0w0b1hQZjJlV2ZVeFc3bjJVN1o2NDY2akJlQjhQTStlTU5Lb3RiUlJ4aE4wWEhoaHQ4a2hrcXdaeTczYXJjMFJHN09KcXhtZE1JSmNFZzh4dFVXVG5VaXRRcEJhcGN0VDFuSkFUbi93VlMyMWFIUDhONE1nTkJETHEyczNzK2ZYYkdaYlB0dVhhai8rL2MvNDVtQTIvN0pSZGlVdDhydk5zL2plUzV5ZTRuZ0lUYjFucGVVQ09VK1hmNndUeDlRRjNMWVM4elVLd21iSVpxL2V1VCt0ZlR4aW9nNDJpOW5aekdiOFRHQXViZXhWbXk1ZXVZN05XYkhHdnFVOXY3Nll3b2R6dDRuYklzaGY1a0pvTFdVMzNQZFp6NEpueFJXMVV3RTZRWGl2c0Z1MFdIR05Kcm85UVVRc1pJeVZXdE9wcjdPYkFBK1hSbHpzSlY0R1djcVRYR01DdmdUV1lyREpCRmR4RzNRenFZdUZUcVJtWEN0a3JHMGVRcGpCWWFNbzBtN2tCWDkrbDkzMStGdUc4cDAyWlJSNzlNWnhqbTZNVVBzTHZTaTBNR3pHWDQ3cVEzZFpTSGwreHRLUXIzL29xUXJBcW1zTWF5NVRHV3ZqSlhsS1ZPRDZQUHZteDJ6cHFnODkyYzNsK25mTHRtckxsbUt6VEJqODZLNlZHYXN6ZFZEZ0puRWd0VklrQ0RSSWVLYlZRTUFGMTFKckhKZU1QZGxKdFk3eE1zRHVXUEZQMzBrVmtIQzN6aDJzYkJLVDdvdmJYTjBrb2Y5MlJjWmxPQVk1M3J3czVhbi8yUEkxZHNRMlJwUVFMUFFTUThPNWVyMHBkVzBtcmwyWlE2akZOUzZaNlZxM20zZFZXYTZFWnVGeFpOVnVVSlFqdVdLM3VmOXdIcVh0aXRqRUJTK3hrcmlaWkVIeFpFMjVFTno5czdsQkRQZFRrOVNHMjVFd1ZJYVd5OHpQdzJIZ3VaSWFCdjV2bm5ySHVPR0RxT2ZENnZRSjY4RTJuSC9mY2pkU1E3dnpJTlptdGUybDE5ZDJpYjd4SW80V2EwMDJzeUkya2ZXZHE2VlVRMTV3U0R5WTUrcmE3YUdWYTVQcU9VUzdsYkFzSXh1SzdRYkxKK1BEci9yZUlWdzlZMlVvL21RRnNhR1R4ajkvZDZYZDVuanFqOVhjdFdWY0JEZWw3b0JjL0ovK0pybUQ2SCsvY2szd0N6emJrM0dSRTZuaFJ2ekdUeDhQcEFRSEMrNU0rdFhUbGpmUGJQdG1Bc04xYnN4TTFJOFBtMW01bnN2ZEhsaEJLVjRObGFhVmZXMXB1N1Y1WWhNWGZrS1FhZzNUb21UOENySTM4Y0ZkYmgrWnFPUGZpOEM1NWMxa3VFK2FydkdQUnAvc1djbkFKUStyMVRuY2N4dk1kRklYYUw4ZXhQcXNqbkZKYnE5cng0M3d2RS9jbUZmYy9ZSnZ0eWtEbTVtSlpMa1RBZU04c1pKWmtOZldKdHN1Rno0SzFRM1d1VGVQQ1dKak5zRm9LQk5mNEc1ZTJieEpYajR4UzZmK1NDUTNMTThWaGNPNk56aDZ1dWwyQ3dsN2tMbGtxN3k3akVHVG1yQ1hXN3dvbXphRDhsOTh6ZmxPTnF0UVFoYXJuSWdrREpXR2Eyb3p2bUp1YnJCZE5qdExkcXRzYjhRMjJzckl2Z3pNbis2b1RmTUFKQXRjRysrTFFickV6ajNVam9udzgwT2pTaDBZSFhnRGltdllBWE5aOTQvejlnVE5oTlRRUGwyRmEyeU9QNlIwc3FqWnRCbDY2RzNaRFhmSzhnYXRGTWtXUjFJTGswVHdvUElLckhrNzU4RlhXdEp1VlMweGZ6UnNZa3R6UTVIcDg0Tmx2NzdVUysrMFVnL0pnbFYyQTlSTGx4RWR0V2FWRlF3TmZDQWpyb1VwWlRxcUtGT2xoalVodEVuTncwTXEyemFEd2p4dnhDQkxteWt4dFZpMnp4VnVuaGYxM1lyczFpSnRsa0tiS3lxeW9XbkFGQncvRjlWcERRS1Q1SjJvU1dxT2d4U0JjKzJiWEVPdFFYRVlOWHNCRFRTNEpYQUIzQVljYXJreUlqWFJaVmdIZUJpY2VlTlNaMUxyWDJ3MEpkQjVTSVZoTXloRk45allyRVNNbHhJN2RXL1lNQXdpNGRkZ2lYM0dQM1M3WVp6cHhNOGVzcDVEWGRJU3hCYW1Zck1rdGhYL3N6bklpNHJVdSt5TlUrNmhhNGFzM2JJME9oU0hsNER2Z2hrWDJONm9RUWJpY1dOT0hudXFrYUNBOHRVcEZ0NTM4SWdyR1ZtU21ta2RDRGVYWE9kNzZ2YkRDeklqYTdiWjZzeHNOc1kybmhaaXQrZlg3cDJxOVNBSXkyNkliUnBqcEEwaFRHSTczc3J3WGxQQzZLTm1jMUdoenFaNnJXaldXVHpHVTN5RUt3Q2JXUWJCQk9MNS9sRkNnZ0VtN2VEbFJqcWhqN01iaW5oUXl2bjVXTmdHc0N2blFHa08zTlRCZldKWmNZbWx6UmFNSDhtbWp6czlGSnNGUm1xbUFuUEw4YjlBcjl1ejI4d1FMM1pEZ2JtOFZsNnVoeGU3dFdWaVMxTkRhemQ5N20wUDNHMXhhQTRaQ3FsNUhhUnJiNXNVeW9DZk5uRWsrK1ZsWjZXUmdhZjlPdHZQd0pjMVIxSVUxY0xwNTNuS1ZLcHVyOVZOcWRuYzgraDM4NXRKRkRhYk1XNUUycHpWb0cybWtvbHh2ajdPRlRGanR6VnFkZTFuTkNWQVBOaW4zY2FmZXlxN2hZODFzOTA4UFdTNDNXeEtuU3JiRzdGbGpNVXp6cmY3VjZuWGRpaHVwT1pua0NMMlpEWHgyemVwOGNHQjc2eXFzMHoyaTdVZDNQREVUUmV4MTdqTFlSY3c5MzN0L0pCYUc3R1poQkdjOTBvbTZCRzRhTEpoNi8zYzViVWpObDM3aFdvM0R3K1paVCt6OWF4a0pobHVmSXhscVFWN21NU1dSaUQvL0dTWHB5ZUp3MlRrV1I1SkRlcHh1Uk9wZVhaL2JNb1YvQXcwalRvZ3ovc0Y2ZXE0TUxqQnZCQlFheUUxMk95M2w1L3RtRlFLeTJaeTMxN2pwdVlKLzdEUjlEKzluYm9mRDRzTitWcjBTQkNhMC9YeGFqZVhPZHFvakpocGNVOEcxdjAzMjhTV2xtMTBDMlNuR0d1aWJSYm1Ybzk5c1J6cmpueVJHbG9qV2JpZ2h1cnpNdEEwQjdIWGdZYWIza3VOV0V1U21tZWx6RzBHZGVDV0pRL2Jacm9ORVZUWDArcWNVZmFDMWwyci9uY1h1NW9yWnpVdTZHWTNUNHNlYVJDYXI0ZU04eHh0eTVDVXdFelJtbXBpV3lPMkNyTkNHdW1oWDljTSs2azJpenlRMmhqbVZuZmtJMUNOaEliWkJVMW1GelVIT2pLcGRrbUhqQVlhSDhBTzgyWmJGYWw1V3J5bkZka000MFk3U0srNG5sWUFpVDNxb1pRamFUZGROMWdrZzNSSTI3UGR2QmZOcDZrNXpQb0pvNEEzVEdLcnNycUl1Z1BOcG1saG1hNWFjMW8wSmhOU2creTJ1bm5Uc29zT3l1RDFXeWRweGJPTWFuc3YzU0RjbTJ6NkIrcS9IRnd2MlpqQUM3U2JqTHFRUTZZM3AxZWJvYW1tSDljektNelduZVlYcHQwNGRPc1JYWUFtR1cySzJIempqQ0cyeXM3Vlo5SHBjdUNYMUpBMXRCcW9pSFhvbEloNEdlaCsyZ1ZaS2NtZ01LaHJCN2JGNGYvcXpBTmQxZk5ZNlZ0YU50ZWRINXd0bTZGemNkRHFWUmVvS1F2YWJwNGZvT0pCRnRCWUM2VzllNWlyVktWTlB0Y056TnF0OE1TYzJ4L0hsTldReGpnOW1ZeXFiQi9aTEx0QzRibFB2YVUxME1Na05ReGtyemNTQnJReHliOEZjT3RUNzJqWkxFeFNReEdxSDV1NUZjQnFrRnFsSDV2aFlUQm8yc05hWThHTDNieVNHdXltRXhKUWdUbXJPSlpEeUtqTktMWnFPemZUemYwNGY4Umd5OEZnNVlZS2hUYUZhVFFsTkNZRUwvQ3hiS1hEaWxlSWQ3aTF6N0Z6WDYzMjVhdHkzT09VR3p6MUJ5RzJ4ZDBabmFDNTE1a1lPdC9UallTODJPeENmbjZlV3hoeG03M29vVk9NN3JYUmVNQmdBRTRWU2tXNzNibnUyTlVsTmQrVDlUT3htLzEwTnRpZ3ZLMFFHMDUwcnBXYnVkcGZkWFNsaWRDUVJoN1BOSmNRODkwSjFtVVpQN2loYnAvWFVXb3EyWGlGdyt5TU5KaWJQcnJkcUVGMTBFMEpBK0I3Qm1DelRLYXJaV0l6SjZEUTFRR3pSRHhKanQzaG5vakJEVncwNkpLYVg3dDVhYzJWVmpoc2Z6eDBBVm9VSlBsazFSVUZ4bzA0d2UvK1ltSnhWeXpwdFo4MVp6dW42TnhJa1VzV2hVSnF3SnBOenJWNXIvMXN2SjZMOFNPSFNjdW9xcmRyZnFoWktZL0JmQlYvUWsrNkxyMUNIYVJxdGIxdnV6bUZBUkRiZEhtdzZkcXMrTHNML05uTXZrWlMyMloyY0lrN1FhSEIyRm9Mdm9CUThSMTExZkl5WGJ2eDYrcGtOOXVtQng1YWM4RnV4bHJCSnJ1dHM3NWZZa0dUVDJqRUp0ekd0RmlDdzBJbmJwRFNmUUxUWE5Zc295NEhlZ3N1dXo1QmRXclVIR04rT0krWDU3REgvbWJ0YWsyemI2MmQ4dVRFWUxZS09pTWVaTTZhZ2VpOFB0R3hSSnZUdFVEWER5UHI1a1lRdWpaelN2NUltOWswWE1BVUlpMEM0RGJRQ2RTN1BTUzhBdnVBdmJ3UXF0RzkyYVcyRDBUcCtHQkJGdlhaV2JiSkVTenJxTk9hSzJJejF1eG02ckFRV2h1RnFkaVlsZDlzM0VRdXJXTTh6VkN3R2ZpNGtmMHVuSUU0UmNha2h2Mzh4MkRIbXgxdW5sT0tIZWVSZUdabTh4eGJtOEZZN0hDT1VuRVlUMDZMejV1RDNCaVUyTjVSUGRvQVRTRDMxeHl4dmhaY2Rlakd3SnhzSnBXQUUwR20yTXptTzV6WXA5alZabllQUk5qTWlCUGJ3S1oxajNZOENnOWoyTjlyekJDazQyWTNKNktVWXg3bllLY1FoN2pZelVsSXVDelA5MmJReEJOMnVjY0tLM2NSM1NxY2JtZ3NIdXMxNnlKdklxTWlQSU1PQjdyclkwb2cwV0czNm9MZERhVFRCRkFsSGFkVzZuZVZyVW5yeEtHeitwQzZmOWNBdkVzTm13RitIQkFZWm95QWJEZnQybWUvWnFaRFY0dVdzcGw1dlZPbi9SdExJdHFNTVR4TTBlWENhNkd5MjdIZHJvTmRKWUdPM2RSMWNJMTZUQnRnRlRCell3WXZkck5CRlF1aGppMzBCWk5GUEN5V0ZyeEVmTVRoSXVyV0FRVzI5SnJEdEJmVFJVaHpneU5uM1dKNWJIT0dDdDhieFpXTzdnMEtSdjk0VFZLeUc3WTY0eGJYYzhjVEcwOVV3LzF5SWlHK0xRTG5LcWs1dXAzQ0pYYzlCdzkyeHZlemE3R0RVZ0oxdFhPdFplc3l0Qm1tTXpuR3NVdzJnL3B4YzFIeGdIUnIvUVRTUWRtTHpxTEpjaXhGdnJmQTBtN0libTkrWkxwbnU2SFhtM1Q5ZGU1TGZHYlFrTDVzN05mNnVOdE5qOVRHNnF4TDBocUpEWEd4dEVtd091bHJ1eFhWRVROQ1RPY3V4SjJDNkJLcVY2RmRLaVJ6MmdROXB3SkhmSWZpcm9WRzUyRFhBV3dSMXd1MGlhR0pBSURCVnkrMkg1eksrVVNHemc3MCtFSGF6SHp0d3JhWmtTVzlUbStlSm9qYXJLYmUvZVF6WTAwSzNRZXhlaCswSmJ1cHBHbERhaE85ZHVscFRjUld3cHFMWnRNUDdwU2RNVDBoZ0MyZjdRdDg3VUpOMTNNK3Z3RHpST3VqL1ZhdWhPdVRUaU91WjVXcVJ4QTVrR1htTEFheW8vSXdrV3pHeEdhbHFnS3dtVlZIM2pCdHBxMElBeUlIc3hmUlZ1eUdKaEVPR2VMUWxKcEUyTWtESnZvdVdmclFSb2VNb2c2dXNSc29Da05WQkVocWtPNWJYdjJGRzZuaEFxQ2g1VHp4WFN6akFSZ2dtS0R0RjA0VjlrRU1OQmtZVm05UXFGNWRVc3NZWXAwRGRhQm5hak9vRTlqTTZoekRzcGw2N3FHdm9Ta3lsT2JRQ0k0TnR6Z1V1NzIzT2VQVGhrS0YzVnFTMUxKQ2JGTHhNSXVVTHI0OEJyd3J1UVVKdEwyNWY2b1JqM0J4UFN2RkJTaTErQzVwZ0t2Z3VyaUsxUTMvL0N6YkdJUnI4YS9QZ1d5c3dIWHowOWtoTmV6dm1abVdBejBUbXptMVl3L0RabWFnMDNCWVFQMGRNcnQyNHhQanhWaVl4cXRyV0RyRDFtNUdtVXFHUy9UQiswRjgxTUZ1bGRrZ3Rhd1JtMUJ0bG9TUU5YSkRQeXF1akJKL25hT3o0aFdDZjZkWlhRQW5CV3Ewdm5Fb0JVaDdzdG5jOElHcEpCc0NRRkRaU3YzS1VnbkxnZW5qK3NpbnR4TkJHRGJUV0RsSzEyYjdhdXBDc1prWklCMmRGZU85SGgva296UHJ3cGpXcEdrM1BEeFExK2RVSDdoNVYxWEc1KzNpL1ZUWTNWTnRXYkV4c1hoeHVSMjVRWFo3Zm5wclhsUkphQnBaVnFNN0w1cmZ1YlJIbXNWczJqS2hCWTRqQ1NERHhzL0g1Y21XdVJ2bFFBQldCWmg0MmpwTng1RnhUaStxUStjN0dqWnpDMG1nRnh0WFVXSGF6TStENWk3Y3lDZjN6Znpnb3RvZlkxUzNVUVRzWVBSQ2N6cStzQnU4azdEdDVuTGVwVUtwWlcyTjBXeTNMVUszVE10MUIvQUV4QVVJb2hZTkYzdjJPYWV5YThlTjhOTEh2MXpFMHlvMVNMb3FrVWhnSXZOeVc1SzJtUGVwdS94Y1JtNjJSbmZaWGwwTGo3WWc0cmJDRkNhM0d3cmRYZWZvVE8zUks1dEpzeGtVaFZYWkNXNGNyTXVnZXgyTHV4UjRKaFhOODhXNEtMRWlGOS9MSy9wY0VjeDhmS3U1cEszSWJ2TmxqRHFiaUdUN2dHNnR1dFg0MHRQbEg3clhaUWxWTnJSdk4vYTlid3oyc3loSnBUQitxWS92Z3B6L0ZMdi9nNlNYcnZyUXFKV3lXbkZLNndMWjFNaFpLU1FvQ04zMUoxR1pqOEdzcTFCMHNuR2F4SjFHRUhZMnMxcHhTc3RtTnJWZVBtMVdKUjdJVEl4YlM5dTQxaWVhSGtDeko0ejBRbWp3RUxDYzVVdzN1L1hrKy91dmNkNVdqZmRxTjgzckxCTnZaYXdGRUdtSmd3cHlXOEk4TkpsRFVOZ2NQL0Z6OFV5R3Y1ZS9GbVVpa2ZsM1djK0NhWllIeFRqR2FzQTYxUlo1NmNpYktTelhyaFRMdDJrdTIyY3M0TUZ0dG9vNTlNekwxR1p1ZFdhdzJiT3p4K21RSnVKQkU2V0t0NnZKbEpERjRtbUZxNXpJQnZVdFpoZVBITXd1NVFySEExbFhDSEtvMEhtUWVrQ0YxWmpWc1p2Ym9rTldkanRtaUUxY3BCalQ3SElRTUFJaE5OUDNXSlVCdVVsRmdNRmdPWVBhR0hCM3JqaEtLTjdJeE84NXhkd2VNaDRVbjR4ZGxnWm9zNm1DMkxaYW5hdWR6YXpXei9UaVFnVklMcTVqTklUajY5bnRvVmVQZWtuQ2JoNVVZS2lyVDdWNllsTXVGSjZBYzFrSXJVdFUxTzM4ak5XOHQ2WnM4d09QTFAzM21uWE00cVlxOG51amRlalpQVGJzdDdjT1AyN1NEeng5N3VENjl5cy9tWGY3MUcrOHNLdzhwSnVtVWd6a3lSNzJXNkY4Wm1aQTZtQ3FWVGJNNS9jdFk4cGkyVzRxeXEvTjdDcmlCU2t2REpIY1NnV3BWdm9OZ1dqYWJSNno2SmNZbHQyT09XSlRCZ3NHcDJzWFhDK0lWeDlnZTE1NW5lMTQ4aG0yNjQyM1F2OGVKOCs4bGcyOGFTYUxGblYxM083d1J4dlp4bC9NU3p1bmd1SVlPM2ZEZTY2ZjE4UjhWWlZxRE9RcWNVTXRDa2hWR1U5dnNjOHFoMnMvUlJCRnpNK05JODV6dlZQY0xzanpWWTRiTktHV2kyT1hhOTR6RTRUSG8yTzNXZVpZVjB2WjdaZ2lOcE94WlhkUlh5N3FnZFh2c1lNZmJtUzdYM281aFRoeUV3bVd3MThTK1UxeC91WGpxY1FTajJmOEhRcGlNVFo0MWs5WTV5c3VaZEgrL1ZMK1YvdlNLMnpubjU5aFc1YS9sSHl2S1JKaGpaR2psNkhINlY5bjMzeGhtVzl5TzdUaHc2cmR6enczZitOOWkwc3ZPdmg1bGNtK0plSkpQOW8wOE4rMFNwNWtRRzVlYjFMNVlKdHNjYVBoaGx6aGxOelJUVWk1bk84c3J6VldvbGYvWE9ZL1hsZ2x2dDk4UC9Fb1liY3BRaEMwbE4zbXR4YVYxbXFKeldiZ3dQZ3hmc1BlMEhUd1VNb0ZBSUUxVlZlenBzcHQ3UEMyYmV6TDE4dFRDQ3FYRTFkT0l0NWk1NTlmVk15Nmpoak9HcXFxV1BXNmRYb3VjeVNYZGVma052alpKOUtJMFkzUS8zWEg3NnlVYWFYeTJxYit6WW12VXZNNnpOTlUwMlVpTmxTZXdUV1BpV3RlNVlWb3hFMjYzS01DcVJDRVZoN0FPSjNNOUpxZ1ZncENXQkZreGpETGRxdGtQaXNKaU5oTWVLRnpMeU9UMXFteGtYVnNhbVE1TE1GVldCTnJyd0FwOXIveE90Wmx4dFVzVWxSazc5WSt0WXp0ZnVMUGJDY250QVNMc3ZxYzVwcnJ1bWpVeXlDdEZEZDV0ZmhaeFVtdjNFWk5mOTJrNExEOSs4ekRtcSt0SUtTUk1RRzdFRVdKeVVaVndrNlZMWmtwRE1odVMxdXFoS05kRTF2UHVscFdrR2hreHhKNmZPYzdyR2pNMmFrdVo4VUd0dTl2YjdMNjZuMnVDaENBdTl2czl1YXdwbWdrK2JlR3ExU2hxRDFMMG12RmFuK01oVUlyYjAyeElMSWJFZHN4UzJ4aFFoSWZGSjVVZk9hNFgzc2pQVUw3Unk2WndCdjZUWnZLaXE2NGxPVU5QWVUxYmQvSmpyeTltbFd0ZUpFZDJWckpEbTNkMHVhK2ozeElGRWl2WHZIdW15SlIxc2pKVHFxN3VweGNodlJMZmJPYkc3TjRzdU1CWk9YZWd1eTBZM29FQWltMkxBRXhyNU5XL1pYbGNrS3psUERWMWV6andjTmNYY1AyQWtsNlBwUmVoVkI3YjZvRWFNN2dFZ2p0bXRnNG9jbHNqN0ZxZGtzUjJ5bXJYbUg1WjUxaC9ONzR3VWZzeTEvZndUb05IOGE2enJrcHVjMk9DOGF6UFcrOEVacFNMQncybEJVTU80WEZxMnZZNXNrL2JyVWtpamdlQ0s0K0VtMG13R2hVTjZaWExranZmWEp0Q2UzR0ZlVWtObHlRbU15OERXY2h6MGpRUWRIcHB5ZEpEUUNwZmY2WDVZenhGeFk5VThsTmRWY2xhcm03dXVPZSs1TkUxR25nSU5aaFlBa3JISGc4Mi9uWUVtUC9nRjFKQ0pJSFBSKytMK1c5dk9KWXF5VTJaS3R6dWM5YWFGYTFuT1RxMlZGbEp4TVpTZ1pYdXJZVFRLNHR4Zk1JYllQWStJQXRFUU5aa3RnWXUyMVJsNmI1eEE4RlBTYWtOdjVycktwTy9yNzVsdm5zcE9NSHNDYitIdFRhU1VzZll4MHZTKzFyQmxJODZjTHZzay9HZm85OXRlelBLU1RaYWRSWnllMmhCRDg0L1Z0cHh6K3d0b0xWdjdNNjVYT1p4dk1rdVFKZTZ1d3ljZzhTY1ZhQW91aUV2V3ZySTU1bkpqMXlid25aSXphaHhqQTRSNHVmYVVvTU13TXdRNkNncVpIbDg1c2dOM0cwVnUzTC9JNHRSbXhteE1aZm1PSnlmako1V2xLcHFTUzEvYW9aYk5CN3pXdkJJalozM0EvSHM2aXBKazBsUVd3RGRXWjJaNkhNb1Bva3NZSGtWSFVJY3NSK0Q3LzlEdHY5Nk9PdVN1NzRHMmV5NHQvZWRuVC9mSC9WWXk5b1VadWlrRHFIazE2QkpMMm0ralRTczRubnhld2Vpb0w0MUppZWRIY1pxVDBpdGt3VTJRUW5Jb01Ta3lTV2wyalpXUUpPUU0yWU9zR3A4K1dUV05IU0o1SXFCNjVrYk93b2xtc2lMZncvdm1ObmNnWkJBVmQyaDE5OG1YVVZDUWo4YitOcFo3SWg2OTlOYnRQcHRHR3VjVHJFMkFCVkhTSjVVZmo5QzFqWHl5ODFsQ0hJcmRjUEpySnVWMTdPU2ErTDhabWFsUzhacnUrZXY3ekF1bkgzV1JiK2dqUmJNNUtrcDVtNUJSVDNkcmpKeloycmtKNUtmREtES3hVZmtkL1Jlem1taElaZ2wwWEhGTEZ4QTJEd3lIbWVKV1kxVnRERUIyZThrVCtWNDIxcTFnRGlhVDI1QXBNWlVSQUNsSmhVVGxKSkhWaHdkNHI2UWlhMWNkdDJsbTh6TlFyL0F3SEZ1UnNyaWExdTZ6YkxiUXZQUHVxRzFtLzRJRTBkN245Z3NSR0h3M0Y3WDNVbHl4c3d3Smkxa0xJUFRueElRSHg2dzA5VDNxL2o1NEg5Z1hqM2xLM01pbHVhRGFVblkzb0pMdXlReUpCcVQzRnhyWWpQclBoVThtT0s4cE5rQ0xUcFVoYmhUY1hFQzcvTFRqY3haakZQbUc5ZkVSYnBDMEZVa3VuK2N3TTJUa3FIMFk2TlRXMlN5S3dBdDNMZ3F5K2tURzlTWTE2WTJsUmQvblpLSWtFdEQ0R2krbnpKbjFqSkh4OUt2d2hLQ1lrYXYzTkNsM0hmVC9tOG1sd0FlYWt1N3U1THJtUmZ1ZnQyZ3p3TnN1UEVwbjZQN3IvOFdaSlljZjdZM2tpT0NEVXFZNHo0Zm1GbGZjT082U1VUR2Nvd2xNU25LanlaMERDVnJxZzN0NVBiYXlZOCtmZjdwczFWb2pURGMyeFFDQW9ybEpnRXh2SEszNWFrWlljdzQ5eUtJQm9qem1saXExRnMvR0pVZ01tbHNYclZIV2xYY3ptaFlsQ25OdkMrdXd6MUpJa0FIVHYyUC81a2NucFQ0VFhYc3g1MzNHWVFoeVFzS0x1ZE44NWhQWDV3VVFvWm9zZ1g3cUpUL000Z1VLNzhVaElIM0RYTzUrUWxnWE9BbXduRlpkeWNuRVJWRnhVa0pVdFRzSzNNd2liM3QvSmx3NzJXWkFmM0ZaOHhKMEx3K2U2Y3dHVk0wUXc1OVF2N1FWa0tYRnljeTdaN0ZyVnU0bU5LZ2JJRjVPd01sZXdrQVRiL25uTERXOFg4Sm5pODBiT3NlcHRqMjgxMmFDNmxRbmdvd3QvS1ozSERUa0JRY1c2WE1GVVo1NUt5VmtOc0FtT0ZhaHYrWlg0aDYxbGYyNjdJRGNSbGQxTkxJSWIxNytkV0dGMDlBSFZHd3BITmxVbEZsVHVnSHp2NDRzc3N0MXZNSUI5SktqbXg5QW52VUg0cWlqajVnY2pnV2tvWHM0RzdrOGJBNUlUeXhXMTNNTGtJSVBZTE54UFpXM1pMOHdxSVpqS0ZhM29LLzV3a3p6Zy9IOVhWQlRIdnZmOWgxdnVaeDQzMytyMzFqdkU5emFUVy81VVZxWVRNOTRjNG9rcHMwdVdWQkMyVllXdEdzbTR5NGI2dGpQa2xGYmlGeXBGeFFFc1NqWHBmT0M0L0hyY3NTTTJKcHphS1VBa3M1WHRseDlVZEk0aHNPTFB2SkNJNy9MYXVHQnNrTlA4U0JybnhpOWt1eVUyWEFLMWNOcnh2cFY3TUpHRUc2dVprRWdBcUR4bFFmRVl0RlpIeE5NVGJVQjZpa2lYY1ZLa2l0M3h6Tk9zOCt1aUVlalhEcXNiKzFEbzhFRlJ2UlRGS1lsS0I3OXZBOXozZzBRZFRYR3NrUjZUcU5NL2NRRUttRzFlUUd5ZjhNUGtleWxDNm5QWjFnL0JyMXIrZkV1K0QwdXh6eXk4TUlnZGg3djNOblVuYjRYUDRURXZIQjJYTTd5aDVXTEZmZmJzZCt5TFJJRjNLMGN5aUZsV050Nk5Mei82OEFrbis4NE1xMFFrOEs5b1d5RTI2RmtkakxjM0I1VEFnSlgycTBiMWxnS0ZxckpRTjFHT1BwVThtTzM4Z0NTQnY5SzNuWDVRU0U4UlBrQjJ5dDNBN3pjaFQ0M3pWcVhFK2tCL2NTcG5BZ05LeWM5Zk5uNU9sSjBob3FQRkdlVTRncWNHM3pqVVVKZFNjR2l2c0tXS1hXNitmYmV4SGZoKzQwL2djdGdYNVFRbWY4TGVYV0tSckYxYlJveDhqWkkzRTFCWk5veTFpZW1sRVpvNjNLKzV0ZVpEWjFsREtQVnFDM016dGVkVGVaSnB6R0ZzTTV1NitNczVoL0M2YVp0cjFuNE5Tc2xLSE1pWllmTTVvSTc0bTJ4ekJSWTRkcUVrU0h0UVlpRVZOSmlDanF0Yk5nZlNxbjNqYUlFNm9OU2YzTVNVUnNuMW44dmZPRjM0MytYdk5nNDhZKzVJa2htN0RuWmI4S1cxMkJRQkZPcUNxMm1nMElNL3h5L3NlWlAyRkc0N0VCdUtOSURXUXVSZEFBZWJGbXNXRVVRUjlqTXp6RFFCTFJKek0yblhuWXhZZHF2UDRlQzNnTDd1SCtLRm9ublM5QTNOQlF5VzJNTW50Y0U0dXEwdEVyZXFWdEZHYlNPeXRUY1QzcXUvdGJxemZGSVlkZXVmbW4yaCtyMHMwMmkrSFJUcXFjUmlWZU91aStkcEVhQTcycW1vUU42cWMrcFZDaElPR0pPTmlpQUhDaFpNQmY2bW9NQVVNc3lWQVZQaWZKQjI0dWpKV1owVVVacGRXZFdkVHJvRlMxb0pFVEsrcC8zbjBjMkl1TG1KNjBzM2V2ZWozUjVYYzlUT083cGVUR3RUYmw5ZGM3OGtOSFZMMlhESkdDWVE1ejdjZG9rU04yVWtTeS9kUS9ZQ005SUc4NW5HK282RytiRUg5L2k2dG10ajZSU0k0VzZ4djFuM0dvUy82ZkNVU1hYcFRZZmZ1bmFMUi9pQzM0K3FQWkZTSWV5algrcFJ4ZXpkd2JtZ1FDcTFidlBuR1gxRzcveDc4ZktVcEhPSnlSWVA3SnQvT3llM2ZsVVdOMVdjN1JhSWQrMGJ5K3h1a0ZZbDJLT2IvdysrRmtXajN3a2lrdTVrSTdVaFFEam8xZ0N6Vm53d2FKMi9rcmRielZGSG9pOWtTc3JSRXpteXdJclIrOXl4Z3VhYlltNm9DelZQQ01FODJPY2hSWEt6VTZjVkZKcmUzc2k5TS81SmxLekxHQmxVSlJRY0Y2QmFubEFDWkE4aGs5LzcrQlVSUlB0Q3R2bzUxNUdNcWtzRjl2RCtuT2E1MktCN2Z3VW50NzB3VVJiZDJ4VFlDeElaZnZrakVELyt4YnQ5RDEzWG9jYnRSR1I3SjRVYnhicEJPalEyc2tUTzhtbUU2d24vOUlpZkNySEk3M2NRaFdvelFQT0R2VFkwN1RKcXlRb2NJajR2a2RvOUZjbnVveWxDcXdTYVpqWXMyTzdKMkxvTWtQa21FWnNWbkVJWUxhU0RHaFprTjVqVWFvTFNHY3NMQy9GZlZ0Y1g3SFJVMzljaExyelNyTC9WNkR4eVUrbnlvcWpLSVdMckIrUDlYMTd6VkhQL2I4SUhoVHFzeFJpdnlOZGNobXZkdkpyKzIybU12RzZHVFRFaXROcHJMRHVjMmo4bS8xTzlmeW4rczNabEkxQVI1anFFRW5vUnFHeWZKYlY1QjkydVB5ODBkanJUMGNmV0hmZThYOHZVd0o4WWFUbkJTc2NDOEIvaXZWU2FDTzZHeFdiRngxVGc5eEd1OFcyT2I3cVo3TmlzWUVzM3BQaUNTMDEyU1g1ZWNuTzZkK2QrcThuT0NMQ0dRcnE1QmdocnJUSUFVTUMxTVRpK1RkV3gyL2V6Z2RrcGxLTjFkS0xpNmQvNlJkQldoenQ0WDdyUEUwSFgvWUZGUkdnTkNsVmxnRU4xSHBubXZPUGJKbXpja1NRMzd3MndQOVZ6VzUzVXh5Sy9rdVNkVENCcHEwRHhUUTM1UEpHMVF0SnlpZnRzeEVPaEg2Q2VUMW1HNGh6L1A3MkE4ZERmV0gzbngvb1lEcFp6VW5nLzZYRU9McUV0eSswRnU0VG5uRmhSZGkvZUNMTm85SE0xakIzUHoxS2t4QnNIdEV3VG5nZGdRYTBQK3ZVNzhib3huL2pvb04rQ0czeFdDZlJCVFVPTUtuWlcvWWJzZXl1L2R3eWErN3RHOGZ2blJTRWR6L004cHhnZlNzMUo2anQ5YlRObzN3Z3FtZWppUWxWVWpUM1VtQkNBTGgvZjk5ODNKeWZ5SWtjazZPbk84ekp4dHhmNHd3ME51RDFMODE4aFJoZ0lFK1lINHZyanBGOGtZSCtKMzZubGExZXpWQ3RVcHlSalozSjN6Zm1NVVpjdkVDWklwbjkvN1FJcmJqNXBDSkhlTXNJSkpjYXB6a0Z0RHpWOFF4TFl2dDRPaDF1Q0N6ajd5NWEvNVc4L3orMnR2NEtveUxDUHdrNjIvSTcvbzdSUHpDNDNSMGJXaFB0Q3NhTWQ0QSt0WTMyQmtReEdFaE1HN2NpN3J5Z250UU1SU1dVbmlra1MyQitmWVVvTkVTTzhhajJRSWdpdFFTRkFTb0dmeTJ4aHYycnVSTmUxdE5rVTZMc2pKUDFIRys2VGFrNlFuWTN4VzhUMVY2VWtDVkt2WG5WeGJLRGVzekNYamJYQnZkOTE2ZXdvUndPV1VwSFpvL1laa0lUSlVvcFZiYWFoTlUrd1BCSUg5SkxmbnFoSEpDNm5vb05oNi91cm5Sd25taWt0VENBZWsyVWtoVlJtelF4SUd4QVlWQ3RLV1JOa281aG5EV2dQNS8wR2lEZnVxMGxwWUdTR1VuMHkzYkcrRm1yL3VGbXEwTGNIR0JkMGJ4ckZDYlZzMEpML0RZbkFRQm52WGtJb1M4ZVRvMnRDY0hUM0VGUndrYnRkRUNvSDhvYjI0QW02RFFLamtIZ3J4U1NMczdmVllSMk9UdFJYbUJJZ1Y2Y1dpT1VhTVR5cG9LOUtETzVzYmIxWjJNb3VyUHZrUjA5dHNrM0ZWQWZkUXVyZVNOQ1RKR0hOMlRZa1FjM2NXeE9mVVpJVVpocXZLVlp6Y2Q5MkdqOUsyd2ZGam5JU2syNG9DNm55UlZkNXk4V1hOeWs0b09SUWd5dzdNSURva1FuclB2RENsSXpPT2g3OXhQRXpidys5NEgvczZjVlB6VkZPOEJ4WFhscG9VcUM0b0NuR05jZHhVLy9lL056Vlc4UEc4TnF6amhlYUt2dEM1RithQ0xRL0tCWVV5YytpOGFnZDBXZTFHNFY1TDB1c1R0SnY3RlU1Mnc2TzUvVlQzdGxNMGFtVEVkVnhibEExRTBLbERNNTVuZHVlY0p1bmJ1Ym1TeUtvZVdKd2tSN2ltT3lkZGFTZy8xTW5aa2EyNXI1MFJEbGx3dDdHOVhCZFdFcWlxdnVBcTkzMzBnU1FwNG04Y0N4MWpjR3pVNDJIMmhWU2EyV28vSDZZckNtTDdNcS9RZVBBMXNjVGhUZlcxRi8yOHZ2cHZiWXJZeExTSzlmeFYwcVdoa1JVMTFXcC9GcVNGV1FDTm9yZVdUbkd0ckVzN21HamFXOVBVWktpYVRmSGFUL1ltNGgrV05UV1VFcTFwdWJoUzRhbS9CeDdUR3hBdDZGL0VmNktNUlNlUm9icTJYdU41S2Z2aFJBTWxoRG02UmdhM3FFdVNiQ1NabUtlRFNXQWFtcFZLc2twS1lBb1psS2ZhUUVET2xMQWp0bHJUdERJUXRZenZxZjM4MmpLeG1jbU5OUmZsamtYempMYmtpaUtBVVlKQjJEVnU3NEppd2pES1B4cEFaamxSUndXR1lHTURTeHhCSVcwdFovenQ4Ym9kMnptUklWYmtjQjU3aWJhMFhWeThLaTBJcjd1aThOUUVoeWNrWTNvVzVUZXlmT1hFYU9GSjVuaWVrMnNyU1U5SDZWazFNRUFTUUcyTGp0aVcycjFGVHY2M2MvMnd6NE5QTGt2TzAwWENRYzVlQUlFbUZhRnBpaG9LakdVTkhnRFNnNklFY3ZqbkVQTkxEdURmM0ptUytMRHEvdEpXZ0Rocno0WmFTVzRRUDZ0UXhCOEd1UVd1MkVSdkphTXZtNW5aNFU3V0dTc1c1WEExRnJWc2dRS1pXaE9QN3dTQlZTVWE5M3lhcU4rWlh1ZWxqZDM4cGwxSjFCV0tTNnVTWHUrd2p1ZVV4SEQ2WEZMZGlaaWVkSGY5cUQwM0pZZ095Q0FxbFRqTm1WaTFLWUVzY1ZFN0p5ZkprcE1wRkdXaFRmR3dWZWxMVzFGczJWUnVrWUJKTGNVRjdSUkgxakxLRHVmbVdhb3hsY1ErUzlUdjJCaHYyT0dpd0lqWVdyYzdxNnE3ME92M3JFaFB0MDR2U1hTQytGSjZrZ1hVemtjdW1BTlZpQ0pteE54UTF5ZlhwUUFwb2psQXg3T2J5MTlrNjNhOFArRFdYeGxUM0ZBaXNuZnBrNGJLZy9KRENVbExGUTMvbXhOYmZRREVsZzF5QzVyWTVnazMxRFlXdGlmZXNHbEhZOTBuR1NveElyYTJwZTU2bXhSZTZKRHVMV0o2aFZ6ZHlaa1pNbnVycGNhRXE2dE9TMU83dGFobExPMEJSbEtPSGUwZWJMY21iRkJyKzRaSmJvRVJtNWp0djlYME5rNjJiSHREM2FZVmpUVXNZRFZHeE5aMkNhOVB0bHhaWGVLVGlpK1BSVHE0WlhHZFNOQlFnL0ZVZDlmY3ZTVWJwR2h1ZUdsdXpTV2JTSmpXZjNBRjRwZzlHbW9ETy9ld3lDMUlZcE51YUNWL29Td2IvWlVxeEZQNzRtdzlxWW5ZeUpVTjB0WEZUNnM1dVg0SlVCZFdaSmhDQ0I0SlNRZWdxcnBJODg5NnJ0QndmTFVtRkVYMlFkV2pRaDBlanVZWUJHc0tVd1ZDYnBFc0ROaHY4eDlEVzJoc0VyRzFIMWRXTFVkcGRaQWtDRWdWS1ArVzA5WFU3YjI0eEw0VW00aGZwOXdNU21zdUpPYjY1eGFjMUM4bi85djdveEcyMThTUjNlTXMyU0VISkl1T0hwbTRuMGJDRUZVUTBWeTd4Q0dJckJ5aUtJZ1ZzSEpESHBoOXNreHFjcnFVeEI2aWg3WUxNZVZ0bDNpWjFaMGt1b3pLVUlKQ1NoZVpBRHJLcUsyc3RJN3BBOWRCaGVha0U4SlhtaEtzZzFCcVdHbXVXMU9kSjljellaUnhSUTNYMTBLUkpZbjNZRHorUmxFMDUzbmgzVlVHcW5oRGZ0cU96bFJ4aVo5eVlLdVQwMnVDYm5WQ2FET0VwOWJkclRVOVNOV1pGUzFPZUg2UmhjUmFHanB6N2pvdW5qQWljNFlieWwxUFZEWTRLa05PWGcyQ3hCcEZQYXBWUVQwU2h3ZWFtblo4RnEvZjlHSDh5Q2JsKzYzbTE3TXk2TzhTcG1JYm9UbW85Z3JDa2o4UGh0Rk5nM0JNRUo0NmJ0YmFLTHd1eXUvNVpEVVV6aVpZN3liR09zbHNienpPaWh2cVVncWRaY1lVNmt0bVM1MEs2cXZpVFp2MmNmTDZJbDYvNDUveHVrME9pY014L1ByZzJnWGFOekVVWW5Od1FmZXFMeUl3UWdzb1BLdXhtbThpdlRhcjlEeWdwa01rYW5nOE1TVkJnSGhhWVZNanE4bko0K1JWb0RXbFVTVXhuMlZjSUxmNklKVmJXSzNCUnl1dTVDNHhxSGExWkpzZ0FzRkY1Vm1SbmlRNnRWbUE3SmdTU3ArOGdKRnMwU1YrN2hVaEhFTTlsZVFWbkdUK0FFaE1ya1dRNG5LS1pBUUlyQzdCZmNsNDdTY2FVeG9kaVZXY3oyN0JEWUdXZ29XaDJIRFIvMDVFUm1nSHBLZjJ6S3QwZUppclRVT3RDSytQelVkMXlOR3VTN01rSy9OMmRYNUlRamFTcUk4bkR1K05OeGpaVkpBWGZnYlFYbCtTYXRaRVRvU0dMNEZ3YkdKYWJzSDVuTFJLQXQ3dGJ2RXdxQkcvdDBoRDExeTZ2QVRDc1FsT2FsQlBYb2x0dCtKS3l0ZEIxc0lkcVluWUNBU0NTbEpyM1Z4ZlN2SVJDQVFDZ1VBZ0VBZ0VBb0ZBSUJBSUJBS0JRQ0FRQ0FRQ2dVQWdFQWdFQW9GQUlCQUlCQUtCUUNBUUNBUUNnVUFnRUFnRUFvRkFJQkFJQkFLQlFDQVFDQVFDZ1VBZ0VBZ0VBb0ZBSUJBSUJBS0JRQ0FRQ0FRQ2dVQWdFQWdFQW9GQUlCQUlCQUtCUUNBUUNBUUNnVUFnRUFnRUFvRkFJQkFJQkFLQlFDQVFDQVFDZ1VBZ0VBZ0VBb0ZBSUJBSUJBS0JRQ0FRQ0FRQ2dVQWdFQWdFQW9GQUlCQUlCQUtCUUNBUUNBUUNnVUFnRU5vdS9yOEFBd0I1cmFGL2pISitBZ0FBQUFCSlJVNUVya0pnZ2c9PQ=="
        
        load = ft.AlertDialog(
            modal=False,
            content=ft.Column(
                height=400,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                     ft.Text("Imagen Guardada", size=20, weight= ft.FontWeight.BOLD),
                    ft.Image(src=f"data:image/png;base64,{Img}", width=350, height=350),
                ]
            )
        )
        return load
        
    def show_load_img_view(self, viewer):
        self.page.open(viewer)
    
    def hide_load_img_view(self, viewer):
        self.page.close(viewer)
