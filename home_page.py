import flet as ft

class Home:
    def __init__(self, page: ft.Page, controller):
        """Paguina de Inicio"""
        self.page = page
        self.controller = controller
        
        
        # Componentes
        self.table_productos = ft.DataTable(
            expand=True,
            width=1200,
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
        
        self.container_table = ft.Container(
            expand=True,
            content=ft.Column(
                expand=True,
                scroll=ft.ScrollMode.ADAPTIVE,
                controls=[ft.Row(
                    expand=True,
                    scroll=ft.ScrollMode.ADAPTIVE,
                    controls=[
                        self.table_productos
                    ]
                )]
            )
        )
        
    def build_page(self):
        """Constructor de la pagina de inicio"""
        Page = ft.View(
            route="/",
            appbar=self.controller.Start_App_Bar("Productos", False),
            controls=[
                ft.Container(padding=10, content=ft.Column(
                    expand=True,
                    controls=[
                        ft.Text("Productos Registrados", size=20, weight= ft.FontWeight.BOLD),
                        #ft.FilledButton("Contactos", on_click= lambda e: self.controller.navigate_to("/contactos"))
                        self.container_table
                    ]
                ))
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