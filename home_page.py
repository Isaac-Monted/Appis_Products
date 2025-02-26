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
            rows=[
                ft.DataRow(
                    selected=True,
                    on_select_changed=self.on_selected_table,
                    cells=[
                        ft.DataCell(
                            content=ft.Text(value="0"),
                        ),
                        ft.DataCell(
                            content=ft.Text(value="0"),
                        ),
                        ft.DataCell(
                            content=ft.Text(value="0"),
                        ),
                        ft.DataCell(
                            content=ft.Text(value="0"),
                        ),
                    ]
                )
            ]
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

        self.BtnLimpiar_All = ft.IconButton(icon=ft.Icons.CLEANING_SERVICES)
        
        # Datos generales
        self.TxtNombre  = ft.TextField(label="Nombre del Producto", )
        self.TxtClave = ft.TextField(label="Clave del Producto", )
        self.TxtPresentacion = ft.TextField(label="Presentacion del Producto", )
        self.TxtMarca = ft.TextField(label="Marca del Producto", )
        
        self.TxtHistoria = ft.TextField(label="Historia", multiline=True, )
        
        self.BtnEtiqueta = ft.IconButton(icon=ft.Icons.ATTACH_FILE)
        self.BtnImagen = ft.IconButton(icon=ft.Icons.ATTACH_FILE)
        self.BtnLimpiar_General = ft.IconButton(icon=ft.Icons.CLEANING_SERVICES)
        
        self.Estado_Producto = ft.Dropdown(
            label="Estado del Producto",
            options=[ft.dropdown.Option(estado) for estado in self.Estados_de_productos]
        )

        #Tabla Alimenticia
        self.TxtPorcion = ft.TextField(label="Nombre del Producto", )
        self.TxtContenido_Energetico = ft.TextField(label="Nombre del Producto", )
        self.TxtProteina = ft.TextField(label="Nombre del Producto", )
        self.TxtGrasas_Totales = ft.TextField(label="Nombre del Producto", )
        self.TxtGrasas_Saturadas = ft.TextField(label="Nombre del Producto", )
        self.TxtGrasas_Trans = ft.TextField(label="Nombre del Producto", )
        self.TxtCarbohidratos = ft.TextField(label="Nombre del Producto", )
        self.TxtAzucares_Totales = ft.TextField(label="Nombre del Producto", )
        self.TxtAzucares_Anadidos = ft.TextField(label="Nombre del Producto", )
        self.TxtFibra_Dietetica = ft.TextField(label="Nombre del Producto", )
        self.TxtSodio = ft.TextField(label="Nombre del Producto", )
        self.TxtHumedad = ft.TextField(label="Nombre del Producto", )
        self.TxtGrasa_Butirica_Min = ft.TextField(label="Nombre del Producto", )
        self.TxtProteina_Min = ft.TextField(label="Nombre del Producto", )
        
        self.TxtIngredientes = ft.TextField(label="Nombre del Producto", )
        self.TxtDescripcion = ft.TextField(label="Nombre del Producto", )
        
        self.BtnLimpiar_Tabla_Alimentacia = ft.IconButton(icon=ft.Icons.CLEANING_SERVICES)
        
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
                            ft.Row(controls=[ft.Text("Limpiar Producto", size=18,),self.BtnLimpiar_All]),
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
                                                    self.TxtNombre,
                                                    self.TxtClave,
                                                    self.TxtPresentacion,
                                                    self.TxtMarca,
                                                    self.TxtHistoria,
                                                    self.BtnEtiqueta,
                                                    self.BtnImagen,
                                                    self.Estado_Producto,
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
                                                    
                                                ]
                                            )
                                        )
                                    )
                                ]
                            ),
                            ft.FilledButton("Contactos", on_click= lambda e: self.controller.navigate_to("/contactos"))
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