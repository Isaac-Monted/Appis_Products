import flet as ft

class Home:
    def __init__(self, page: ft.Page, controller):
        """Paguina de Inicio"""
        self.page = page
        self.controller = controller
        
        self.Estados_de_productos = ['ACTIVO', 'INACTIVO', 'DESCONOCIDO']
        
        # Componentes
        self.table_productos = ft.DataTable(
            expand=True,
            #width=1200,
            height=400,
            heading_row_color=ft.Colors.PRIMARY,
            columns=[
                ft.DataColumn(
                    label=ft.Text("Id", color=ft.Colors.SURFACE, size=15, weight=ft.FontWeight.BOLD),
                    on_sort=self.on_sort_table,
                    visible=False,
                ),
                ft.DataColumn(
                    label=ft.Text("Producto", color=ft.Colors.SURFACE, size=15, weight=ft.FontWeight.BOLD),
                    on_sort=self.on_sort_table,
                    tooltip="Nombre del producto",
                ),
                ft.DataColumn(
                    label=ft.Text("Clave", color=ft.Colors.SURFACE, size=15, weight=ft.FontWeight.BOLD),
                    on_sort=self.on_sort_table,
                    tooltip="Clave del producto"
                ),
                ft.DataColumn(
                    label=ft.Text("Presentacion", color=ft.Colors.SURFACE, size=15, weight=ft.FontWeight.BOLD),
                    on_sort=self.on_sort_table,
                    tooltip="Presentacion del producto"
                ),
                ft.DataColumn(
                    label=ft.Text("Marca", color=ft.Colors.SURFACE, size=15, weight=ft.FontWeight.BOLD),
                    on_sort=self.on_sort_table,
                    tooltip="Marca del producto"
                ),
            ],
            rows=[]
        )
        
        self.container_table = ft.Column(
                alignment=ft.MainAxisAlignment.START,
                #expand=True,
                height=400,
                controls=[
                    ft.Row(
                        expand=True,
                        controls=[
                            self.table_productos
                        ]
                    )
                ]
            )

        self.BtnAgregar = ft.FilledButton(text="Agregar Producto", icon=ft.Icons.SAVE, col={"xs":12, "sm":6, "md":5, "lg":2}, data="Agregar", on_click=self.on_click_buttons_form)
        self.BtnLimpiar_All = ft.FilledButton(text="Limpiar Producto", icon=ft.Icons.CLEANING_SERVICES, col={"xs":12, "sm":6, "md":5, "lg":2}, data="Limpiar Todo", on_click=self.on_click_buttons_form)
        self.BtnEditar = ft.FilledButton(text="Editar Producto", icon=ft.Icons.EDIT, col={"xs":12, "sm":6, "md":5, "lg":2}, data="Editar", on_click=self.on_click_buttons_form)
        self.BtnEliminar= ft.FilledButton(text="Eliminar Producto", icon=ft.Icons.DELETE, col={"xs":12, "sm":6, "md":5, "lg":2}, data="Eliminar", on_click=self.on_click_buttons_form)
        
        # Datos generales
        self.TxtNombre  = ft.TextField(label="Nombre del Producto", )
        self.TxtClave = ft.TextField(label="Clave del Producto", )
        self.TxtPresentacion = ft.TextField(label="Presentacion del Producto", )
        self.TxtMarca = ft.TextField(label="Marca del Producto", )
        
        self.TxtHistoria = ft.TextField(label="Historia", multiline=True, min_lines=1, max_lines=3, )
        
        self.BtnEtiqueta = ft.FilledButton(text="Carcar Etiqueta del Producto", icon=ft.Icons.ATTACH_FILE,data="Add Etiqueta", on_click=self.on_click_buttons_form)
        self.BtnImagen = ft.FilledButton(text="Cargar Imagen del Producto", icon=ft.Icons.ATTACH_FILE, data="Add Imagen", on_click=self.on_click_buttons_form)
        self.BtnLimpiar_General = ft.FilledButton(text="Limpiar Contenido", icon=ft.Icons.CLEANING_SERVICES, data="Limpiar Producto", on_click=self.on_click_buttons_form)
        
        self.Estado_Producto = ft.Dropdown(
            label="Estado del Producto",
            options=[ft.dropdown.Option(estado) for estado in self.Estados_de_productos]
        )

        #Tabla Alimenticia
        self.TxtPorcion = ft.TextField(label="Porcion", )
        self.TxtContenido_Energetico = ft.TextField(label="Contenido Energetico", )
        self.TxtProteina = ft.TextField(label="Proteina", )
        self.TxtGrasas_Totales = ft.TextField(label="Grasas Totales", )
        self.TxtGrasas_Saturadas = ft.TextField(label="Grasas Saturadas", )
        self.TxtGrasas_Trans = ft.TextField(label="Grasas Trans", )
        self.TxtCarbohidratos = ft.TextField(label="Carbohidrato", )
        self.TxtAzucares_Totales = ft.TextField(label="Azucares Totales", )
        self.TxtAzucares_Anadidos = ft.TextField(label="Azucares Añadidos", )
        self.TxtFibra_Dietetica = ft.TextField(label="Fibra Dietetica", )
        self.TxtSodio = ft.TextField(label="Sodio", )
        self.TxtHumedad = ft.TextField(label="Humedad", )
        self.TxtGrasa_Butirica_Min = ft.TextField(label="Grasa Butirica Min", )
        self.TxtProteina_Min = ft.TextField(label="Proteina Min", )
        
        self.TxtIngredientes = ft.TextField(label="Ingredientes", multiline=True, min_lines=1, max_lines=3, )
        self.TxtDescripcion = ft.TextField(label="Descripcion", multiline=True, min_lines=1, max_lines=3, )
        
        self.BtnLimpiar_Tabla_Alimentacia = ft.FilledButton(text="Limpiar Contenido", icon=ft.Icons.CLEANING_SERVICES, data="Limpiar Nutrimental", on_click=self.on_click_buttons_form)
        
        # Llenar la tabla con los registros
        print(self.Read_Dates("Tabla"))
    
    def build_page(self):
        """Constructor de la pagina de inicio"""
        Page = ft.View(
            route="/",
            appbar=self.controller.Start_App_Bar("Productos", False),
            controls=[
                ft.Container(
                    padding=10,
                    expand=True,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.START,
                        scroll=ft.ScrollMode.ADAPTIVE,
                        expand=True,
                        controls=[
                            ft.Text("Productos Registrados", size=20, weight= ft.FontWeight.BOLD),
                            self.container_table,
                            ft.ResponsiveRow(controls=[
                                self.BtnAgregar,
                                self.BtnLimpiar_All,
                                self.BtnEditar,
                                self.BtnEliminar,
                            ]),
                            ft.Tabs(
                                selected_index=0,
                                animation_duration=500,
                                height=500,
                                tabs=[
                                    ft.Tab(
                                        text="Datos Generales",
                                        content=ft.Container(
                                            padding=20,
                                            content=ft.Column(
                                                scroll=ft.ScrollMode.ADAPTIVE,
                                                controls=[
                                                    ft.Text("Datos del Producto", size=20, weight= ft.FontWeight.BOLD),
                                                    self.TxtNombre,
                                                    self.TxtClave,
                                                    self.TxtPresentacion,
                                                    self.TxtMarca,
                                                    ft.Divider(height=2,color=ft.Colors.TRANSPARENT),
                                                    self.TxtHistoria,
                                                    ft.Divider(height=2,color=ft.Colors.TRANSPARENT),
                                                    self.BtnEtiqueta,
                                                    self.BtnImagen,
                                                    ft.Divider(height=2,color=ft.Colors.TRANSPARENT),
                                                    self.Estado_Producto,
                                                    ft.Divider(height=2,color=ft.Colors.TRANSPARENT),
                                                    self.BtnLimpiar_General,
                                                ]
                                            )
                                        )
                                    ),
                                    ft.Tab(
                                        text="Etiqueta Alimenticia",
                                        content=ft.Container(
                                            padding=20,
                                            content=ft.Column(
                                                scroll=ft.ScrollMode.ADAPTIVE,
                                                controls=[
                                                    ft.Text("Informacion Nutrimental", size=20, weight= ft.FontWeight.BOLD),
                                                    self.TxtPorcion,
                                                    self.TxtContenido_Energetico,
                                                    self.TxtProteina,
                                                    self.TxtGrasas_Totales,
                                                    self.TxtGrasas_Saturadas,
                                                    self.TxtGrasas_Trans,
                                                    self.TxtCarbohidratos,
                                                    self.TxtAzucares_Totales,
                                                    self.TxtAzucares_Anadidos,
                                                    self.TxtFibra_Dietetica,
                                                    self.TxtSodio,
                                                    self.TxtHumedad,
                                                    self.TxtGrasa_Butirica_Min,
                                                    self.TxtProteina_Min,
                                                    ft.Divider(height=2,color=ft.Colors.TRANSPARENT),
                                                    self.TxtIngredientes,
                                                    self.TxtDescripcion,
                                                    ft.Divider(height=2,color=ft.Colors.TRANSPARENT),
                                                    self.BtnLimpiar_Tabla_Alimentacia,
                                                ]
                                            )
                                        )
                                    )
                                ]
                            ),
                            ft.Text("Acceder a", size=20),
                            ft.ResponsiveRow(
                                controls=[
                                    ft.FilledButton("Contactos", on_click= lambda e: self.controller.navigate_to("/contactos"),  col={"xs":12, "sm":6, "md":5, "lg":2}),
                                    ft.FilledButton("Categorias", on_click= lambda e: self.controller.navigate_to("/categorias"),  col={"xs":12, "sm":6, "md":5, "lg":2}),
                                    ft.FilledButton("Resetas", on_click= lambda e: self.controller.navigate_to("/resetas"),  col={"xs":12, "sm":6, "md":5, "lg":2}),
                                ]
                            )
                        ]
                    )
                )
            ]
        )
        
        return Page
    
    def get_page(self):
        """Mostrar la pagina de inicio"""
        return self.build_page()
    
    # Funcionalidades
    
    def on_selected_table(self, e):
        pass
    
    def on_sort_table(self, e):
        pass
    
    def on_click_buttons_form(self, e):
        print("boton presionado:", e.control.data)
        match e.control.data:
            case "Agregar":
                self.Create_Register()
            case "Limpiar Todo":
                self.Clear_Form_All()
            case "Editar":
                self.Update_Registrer()
            case "Eliminar":
                self.Delete_Register()
            case "Add Etiqueta":
                self.controller.Start_file_picker("Abrir", "Etiqueta")
            case "Add Imagen":
                self.controller.Start_file_picker("Abrir", "Imagen")
            case "Limpiar Producto":
                self.Clear_Form_General()
            case "Limpiar Nutrimental":
                self.Clear_Form_Nutrimental()
            case _:
                ...
                
    def Create_Register(self):
        ...
        
    def Clear_Form_All(self):
        self.Clear_Form_General()
        self.Clear_Form_Nutrimental()
        
    def Clear_Form_General(self):
        self.TxtNombre.value = ""
        self.TxtClave.value = ""
        self.TxtPresentacion.value = ""
        self.TxtMarca.value = ""
        self.TxtHistoria.value = ""
        self.Estado_Producto.value = ""
        
        self.page.update()
        
    def Clear_Form_Nutrimental(self):
        self.TxtPorcion.value = ""
        self.TxtContenido_Energetico.value = ""
        self.TxtProteina.value = ""
        self.TxtGrasas_Totales.value = ""
        self.TxtGrasas_Saturadas.value = ""
        self.TxtGrasas_Trans.value = ""
        self.TxtCarbohidratos.value = ""
        self.TxtAzucares_Totales.value = ""
        self.TxtAzucares_Anadidos.value = ""
        self.TxtFibra_Dietetica.value = ""
        self.TxtSodio.value = ""
        self.TxtHumedad.value = ""
        self.TxtGrasa_Butirica_Min.value = ""
        self.TxtProteina_Min.value = ""
        self.TxtIngredientes.value = ""
        self.TxtDescripcion.value = ""
        
        self.page.update()
        
    def Read_Dates(self, Mode:str):
        match Mode:
            case "Tabla":
                Datos = self.controller.Execute_Query("""
                SELECT
                    PRODUCTOS.ID_PRODUCTOS,
                    PRODUCTOS.NOMBRE,
                    PRODUCTOS.CLAVE,
                    PRODUCTOS.PRESENTACION,
                    PRODUCTOS.MARCA
                FROM
                    PRODUCTOS;
            """)
            case "General":
                Datos = self.controller.Execute_Query("""
                SELECT
                    PRODUCTOS.ID_PRODUCTOS,
                    PRODUCTOS.NOMBRE,
                    PRODUCTOS.CLAVE,
                    PRODUCTOS.PRESENTACION,
                    PRODUCTOS.MARCA,
                    PRODUCTOS.HISTORIA,
                    PRODUCTOS.STATUS,
                    TABLA_ALIMENTICIA.PORCION,
                    TABLA_ALIMENTICIA.CONTENIDO_ENERGETICO,
                    TABLA_ALIMENTICIA.PROTEINA,
                    TABLA_ALIMENTICIA.GRASAS_TOTALES,
                    TABLA_ALIMENTICIA.GRASAS_SATURADAS,
                    TABLA_ALIMENTICIA.GRASAS_TRANS,
                    TABLA_ALIMENTICIA.CARBOHIDRATOS,
                    TABLA_ALIMENTICIA.AZUCARES_TOTALES,
                    TABLA_ALIMENTICIA.AZUCARES_AÑADIDOS,
                    TABLA_ALIMENTICIA.FIBRA_DIETETICA,
                    TABLA_ALIMENTICIA.SODIO,
                    TABLA_ALIMENTICIA.HUMEDAD,
                    TABLA_ALIMENTICIA.GRASA_BUTIRICA_MIN,
                    TABLA_ALIMENTICIA.PROTEINA_MIN,
                    TABLA_ALIMENTICIA.INGREDIENTES,
                    TABLA_ALIMENTICIA.DESCRIPCION,
                    CATEGORIAS.NOMBRE
                FROM
                    PRODUCTOS
                INNER JOIN
                    TABLA_ALIMENTICIA
                ON PRODUCTOS.ID_PRODUCTOS = TABLA_ALIMENTICIA.ID_PRODUCTO

                INNER JOIN
                    CATEGORIAS
                ON TABLA_ALIMENTICIA.ID_CATEGORIA = CATEGORIAS.ID_CATEGORIA;
            """)
            case "Producto":
                Datos = self.controller.Execute_Query("""
                SELECT
                    PRODUCTOS.ID_PRODUCTOS,
                    PRODUCTOS.NOMBRE,
                    PRODUCTOS.CLAVE,
                    PRODUCTOS.PRESENTACION,
                    PRODUCTOS.MARCA,
                    PRODUCTOS.HISTORIA,
                    PRODUCTOS.STATUS
                    
                FROM
                    PRODUCTOS;
            """)
            case "Nutrimental":
                Datos = self.controller.Execute_Query("""
                SELECT
                    PRODUCTOS.ID_PRODUCTOS,
                    TABLA_ALIMENTICIA.PORCION,
                    TABLA_ALIMENTICIA.CONTENIDO_ENERGETICO,
                    TABLA_ALIMENTICIA.PROTEINA,
                    TABLA_ALIMENTICIA.GRASAS_TOTALES,
                    TABLA_ALIMENTICIA.GRASAS_SATURADAS,
                    TABLA_ALIMENTICIA.GRASAS_TRANS,
                    TABLA_ALIMENTICIA.CARBOHIDRATOS,
                    TABLA_ALIMENTICIA.AZUCARES_TOTALES,
                    TABLA_ALIMENTICIA.AZUCARES_AÑADIDOS,
                    TABLA_ALIMENTICIA.FIBRA_DIETETICA,
                    TABLA_ALIMENTICIA.SODIO,
                    TABLA_ALIMENTICIA.HUMEDAD,
                    TABLA_ALIMENTICIA.GRASA_BUTIRICA_MIN,
                    TABLA_ALIMENTICIA.PROTEINA_MIN,
                    TABLA_ALIMENTICIA.INGREDIENTES,
                    TABLA_ALIMENTICIA.DESCRIPCION,
                    CATEGORIAS.NOMBRE
                FROM
                    PRODUCTOS
                INNER JOIN
                    TABLA_ALIMENTICIA
                ON PRODUCTOS.ID_PRODUCTOS = TABLA_ALIMENTICIA.ID_PRODUCTO

                INNER JOIN
                    CATEGORIAS
                ON TABLA_ALIMENTICIA.ID_CATEGORIA = CATEGORIAS.ID_CATEGORIA;
            """)
            case _:
                Datos = []
                
        return Datos
        
    def Update_Registrer(self):
        ...
        
    def Delete_Register(self):
        ...