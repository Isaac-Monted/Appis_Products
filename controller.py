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
    
    def Start_file_picker(self,Mode:str, Control:str):
        """Mostrar el selector de archivos de la aplicacion
        Seleccione el tipo de Accion que se va a realizar
        
        Args:
            Mode (str): Configuracion del modo de operar del selector de archivos.
            
                - "Abrir" (str): Configuracion para guardar la ruta seleccionada por el usuario.
                
                - "Guardar" (str): Configuracion para el selecor de archivos pueda guardar el archivo en la ruta seleccionada
            Control (str): Espesificar el control que activo esta funcion.
        """
        self.view.Start_file_picker(Control, Mode)
        
    def Save_selected_file_picker(self, Mode:str, root:str):
        """guardar la ruta del selector de archivos
        
        Seleccione el tipo de Accion que se va a realizar
        
        Args:
            Mode (str): Configuracion del modo de operar del selector de archivos.
            
                - "Abrir" (str): Configuracion para guardar la ruta seleccionada por el usuario.
                
                - "Guardar" (str): Configuracion para el selecor de archivos pueda guardar el archivo en la ruta seleccionada
                
            Root (str): Ruta seleccionada por el usuario.
            
        """
        match Mode:
            case "Etiqueta":
                print(f"Importar de la ruta: {root}")
            case "Producto":
                print(f"Exportar de la ruta: {root}")
            case _:
                print("Se cancela la operacion")
                
    def Start_alert_dialog(self, type=None, title=None, message=None, description=None, actions=None, functions=None, error= None):
        """Mostrar el cuadro de dialogo de la aplicacion"""
        self.view.Start_alert_dialog(type, title, message, description, actions, functions, error)
        
    def Start_snackbar(self, message: str, color: ft.Colors, duration: int):
        """Mostrar el mensaje en barra de la aplicacion"""
        self.view.Start_snackbar(message, color, duration)
        
    # Funiones hacia la base de datos y/o modelo
    
    def Execute_Query(self, query:str):
        """Ejecuta consultas SQL en una base de datos MySQL.

        Esta función permite ejecutar consultas de tipo `INSERT`, `SELECT`, `UPDATE` o `DELETE`. Es importante asegurarse de que la consulta esté correctamente escrita, ya que, de lo contrario, se generará un error.

        Args:
            query (str): Consulta SQL a ejecutar. Puede ser una instrucción para insertar, seleccionar, actualizar o eliminar datos en la base de datos.

        Returns:
            list: En caso de una consulta `SELECT`, devuelve una lista de tuplas, donde cada tupla representa una fila de resultados con sus respectivos valores:
            ```
                [
                    (dato1, valor1),
                    (dato2, valor2),
                    ...
                ]
            ```
            En caso de consultas `INSERT`, `UPDATE` o `DELETE`, la función no retorna ningún valor.

        Examples:
            -"SELECT * FROM tabla;"
            
            -"INSERT INTO tabla (columna1, columna2) VALUES (valor1, valor2);"
        """
        values = self.model.Execute_Query(Query=query)
        
        return values
    
    def Convert_image_to_binary(self,Mode:str, Root:str = None, Imagen_binary: str = None):
        """Mostrar la barra de la aplicacion"""
        match Mode:
            case "":
                ...
    
    