import flet as ft
import json as js

class Home:
    def __init__(self, page: ft.Page, controller):
        """Paguina de Inicio"""
        self.page = page
        self.controller = controller
        
        self.Estados_de_productos = ['ACTIVO', 'INACTIVO', 'DESCONOCIDO']
        self.Categoria_de_Productos = self.controller.Execute_Query("SELECT CATEGORIAS.ID_CATEGORIA, CATEGORIAS.NOMBRE FROM CATEGORIAS WHERE STATUS = 'ACTIVO';")
        self.Recetas_de_Productos = self.controller.Execute_Query("SELECT RECETAS.ID_RESETA, RECETAS.NOMBRE FROM RECETAS WHERE STATUS = 'ACTIVO';")
        
        # Componentes
        self.table_productos = ft.DataTable(
            expand=True,
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
        
        self.container_table = ft.Container(
            padding=10,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.START,
                #expand=True,
                scroll=ft.ScrollMode.AUTO,
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
        )

        self.BtnAgregar = ft.FilledButton(text="Agregar Producto", icon=ft.Icons.SAVE, col={"xs":12, "sm":6, "md":5, "lg":2}, data="Agregar", on_click=self.on_click_buttons_form)
        self.BtnLimpiar_All = ft.FilledButton(text="Limpiar Producto", icon=ft.Icons.CLEANING_SERVICES, col={"xs":12, "sm":6, "md":5, "lg":2}, data="Limpiar Todo", on_click=self.on_click_buttons_form)
        self.BtnEditar = ft.FilledButton(text="Editar Producto", icon=ft.Icons.EDIT, col={"xs":12, "sm":6, "md":5, "lg":2}, data="Editar", on_click=self.on_click_buttons_form)
        self.BtnEliminar= ft.FilledButton(text="Eliminar Producto", icon=ft.Icons.DELETE, col={"xs":12, "sm":6, "md":5, "lg":2}, data="Eliminar", on_click=self.on_click_buttons_form)
        
        # Datos generales
        self.TxtID = ft.TextField(label="Id del Producto", visible=False)
        self.TxtNombre  = ft.TextField(label="Nombre del Producto", )
        self.LabelNombre = ft.Text(value="Producto Seleccionado: ", size=18)
        self.TxtClave = ft.TextField(label="Clave del Producto", )
        self.TxtPresentacion = ft.TextField(label="Presentacion del Producto", )
        self.TxtMarca = ft.TextField(label="Marca del Producto", )
        
        self.TxtHistoria = ft.TextField(label="Historia", multiline=True, min_lines=1, max_lines=3, )
        
        self.BtnEtiqueta = ft.FilledButton(text="Carcar Etiqueta del Producto", icon=ft.Icons.ATTACH_FILE,data="Add Etiqueta", on_click=self.on_click_buttons_form)
        self.BtnImagen = ft.FilledButton(text="Cargar Imagen del Producto", icon=ft.Icons.ATTACH_FILE, data="Add Imagen", on_click=self.on_click_buttons_form)
        self.BtnLimpiar_General = ft.FilledButton(text="Limpiar Contenido", icon=ft.Icons.CLEANING_SERVICES, data="Limpiar Producto", on_click=self.on_click_buttons_form)
        self.BtnVerEtiqueta = ft.IconButton(icon=ft.Icons.IMAGE, data="Ver Etiqueta", tooltip="Ver Etiqueta", on_click=self.on_click_buttons_form)
        self.BtnVerImagen = ft.IconButton(icon=ft.Icons.IMAGE, data="Ver Imagen", tooltip="Ver Imagen", on_click=self.on_click_buttons_form)
        self.BtnLimpiarEtiqueta = ft.IconButton(icon=ft.Icons.CLEANING_SERVICES, data="Limpiar Etiqueta", tooltip="Limpiar Etiqueta", on_click=self.on_click_buttons_form)
        self.BtnLimpiarImagen = ft.IconButton(icon=ft.Icons.CLEANING_SERVICES, data="Limpiar Imagen", tooltip="Limpiar Imagen", on_click=self.on_click_buttons_form)
        
        self.Estado_Producto = ft.Dropdown(
            label="Estado del Producto",
            options=[ft.dropdown.Option(estado) for estado in self.Estados_de_productos]
        )
        
        self.Categorias_Producto = ft.Dropdown(
            label="Categoria del Producto",
            options=[ft.dropdown.Option(categoria[0],categoria[1]) for categoria in self.Categoria_de_Productos]
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
        
        self.table_recetas = ft.DataTable(
            expand=True,
            heading_row_color=ft.Colors.PRIMARY,
            columns=[
                ft.DataColumn(
                    label=ft.Text("Id", color=ft.Colors.SURFACE, size=15, weight=ft.FontWeight.BOLD),
                    on_sort=self.on_sort_table,
                    visible=False,
                ),
                ft.DataColumn(
                    label=ft.Text("Receta", color=ft.Colors.SURFACE, size=15, weight=ft.FontWeight.BOLD),
                    on_sort=self.on_sort_table,
                    tooltip="Nombre del producto",
                ),
                ft.DataColumn(
                    label=ft.Text("Descripcion", color=ft.Colors.SURFACE, size=15, weight=ft.FontWeight.BOLD),
                    on_sort=self.on_sort_table,
                    tooltip="Clave del producto"
                ),
                
            ],
            rows=[]
        )
        self.container_table_resetas = ft.Container(
            padding=10,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.START,
                #expand=True,
                scroll=ft.ScrollMode.AUTO,
                height=300,
                controls=[
                    ft.Row(
                        expand=True,
                        controls=[
                            self.table_recetas
                        ]
                    )
                ]
            )
        )
        self.BtnAgregar_receta = ft.FilledButton(text="Agregar Receta", icon=ft.Icons.SAVE, col={"xs":12, "sm":6, "md":5, "lg":2}, data="Agregar receta", on_click=self.on_click_buttons_form)
        self.BtnLimpiar_receta = ft.FilledButton(text="Limpiar Receta", icon=ft.Icons.CLEANING_SERVICES, col={"xs":12, "sm":6, "md":5, "lg":2}, data="Limpiar receta", on_click=self.on_click_buttons_form)
        self.BtnEliminar_receta= ft.FilledButton(text="Eliminar Receta", icon=ft.Icons.DELETE, col={"xs":12, "sm":6, "md":5, "lg":2}, data="Eliminar receta", on_click=self.on_click_buttons_form)
        self.TxtID_receta = ft.TextField(label="Id de la Receta", visible=False)
        self.LabelNombre_receta = ft.Text(value="Receta Seleccionada: ", size=18)
        self.Recetas_Producto = ft.Dropdown(
            label="Receta del Producto",
            options=[ft.dropdown.Option(receta[0],receta[1]) for receta in self.Recetas_de_Productos]
        )
        
        # Llenar la tabla con los registros
        self.Write_Table_Productos()
    
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
                            ft.Divider(height=2,color=ft.Colors.TRANSPARENT),
                            ft.ResponsiveRow(controls=[
                                self.BtnAgregar,
                                self.BtnLimpiar_All,
                                self.BtnEditar,
                                self.BtnEliminar,
                            ]),
                            self.LabelNombre,
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
                                                    self.TxtID,
                                                    self.TxtNombre,
                                                    self.TxtClave,
                                                    self.TxtPresentacion,
                                                    self.TxtMarca,
                                                    ft.Divider(height=2,color=ft.Colors.TRANSPARENT),
                                                    self.TxtHistoria,
                                                    ft.Divider(height=2,color=ft.Colors.TRANSPARENT),
                                                    ft.Row(controls=[
                                                        self.BtnEtiqueta,
                                                        self.BtnVerEtiqueta,
                                                        self.BtnLimpiarEtiqueta
                                                    ]),
                                                    ft.Row(controls=[
                                                        self.BtnImagen,
                                                        self.BtnVerImagen,
                                                        self.BtnLimpiarImagen
                                                    ]),
                                                    ft.Divider(height=2,color=ft.Colors.TRANSPARENT),
                                                    self.Estado_Producto,
                                                    self.Categorias_Producto,
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
                                    ),
                                    ft.Tab(
                                        text="Resetas",
                                        content=ft.Container(
                                            padding=20,
                                            content=ft.Column(
                                                scroll=ft.ScrollMode.ADAPTIVE,
                                                controls=[
                                                    ft.Text("Resetas con este Producto", size=20, weight= ft.FontWeight.BOLD),
                                                    self.container_table_resetas,
                                                    ft.Divider(height=2,color=ft.Colors.TRANSPARENT),
                                                    ft.ResponsiveRow(controls=[
                                                        self.BtnAgregar_receta,
                                                        self.BtnLimpiar_receta,
                                                        self.BtnEliminar_receta,
                                                    ]),
                                                    self.TxtID_receta,
                                                    self.LabelNombre_receta,
                                                    self.Recetas_Producto,
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
    
    def Write_Table_Productos(self):
        Array =  self.Read_Dates("Tabla")
        Rows = []
        for registr in Array:
            if registr[1] == "" or registr[1] == " " :
                continue
            
            Rows.append(
                ft.DataRow(
                    selected=True,
                    on_select_changed=self.on_selected_table,
                    cells=[
                        ft.DataCell(content=ft.Text(value=str(registr[0])), visible=False),
                        ft.DataCell(content=ft.Text(value=registr[1])),
                        ft.DataCell(content=ft.Text(value=registr[2])),
                        ft.DataCell(content=ft.Text(value=registr[3])),
                        ft.DataCell(content=ft.Text(value=registr[4])),
                    ]
                )
            )
            
        self.table_productos.rows = Rows
        self.page.update()
        
    def Write_Table_Recetas(self, Id):
        Array =  self.Read_Dates("Tabla Recetas", Id)
        print(Array)
        Rows = []
        for registr in Array:
            if registr[1] == "" or registr[1] == " ":
                continue
            
            Rows.append(
                ft.DataRow(
                    selected=True,
                    on_select_changed=self.on_selected_table_recetas,
                    cells=[
                        ft.DataCell(content=ft.Text(value=str(registr[0])), visible=False),
                        ft.DataCell(content=ft.Text(value=registr[1])),
                        ft.DataCell(content=ft.Text(value=registr[2])),
                    ]
                )
            )
            
        self.table_recetas.rows = Rows
        self.page.update()
        
    def on_selected_table(self, e):
        id = e.control.cells[0].content.value
        if id != None or id != "0":
            valores = self.Read_Dates("General", id)[0]
            
            print(valores)
            self.TxtID.value = valores[0]
            self.TxtNombre.value = valores[1]
            self.LabelNombre.value = f"Producto Seleccionado: {valores[1]}"
            self.TxtClave.value = valores[2]
            self.TxtPresentacion.value = valores[3]
            self.TxtMarca.value = valores[4]
            self.TxtHistoria.value = valores[5]
            
            self.Estado_Producto.value = valores[6]
            self.Categorias_Producto.value = valores[23]
            
            self.TxtPorcion.value = valores[7]
            self.TxtContenido_Energetico.value = valores[8]
            self.TxtProteina.value = valores[9]
            self.TxtGrasas_Totales.value = valores[10]
            self.TxtGrasas_Saturadas.value = valores[11]
            self.TxtGrasas_Trans.value = valores[12]
            self.TxtCarbohidratos.value = valores[13]
            self.TxtAzucares_Totales.value = valores[14]
            self.TxtAzucares_Anadidos.value = valores[15]
            self.TxtFibra_Dietetica.value = valores[16]
            self.TxtSodio.value = valores[17]
            self.TxtHumedad.value = valores[18]
            self.TxtGrasa_Butirica_Min.value = valores[19]
            self.TxtProteina_Min.value = valores[20]
            self.TxtIngredientes.value = valores[21]
            self.TxtDescripcion.value = valores[22]
            
            self.Write_Table_Recetas(valores[0])
            
        self.page.update()
            
    def on_selected_table_recetas(self, e):
        id = e.control.cells[0].content.value
        if id != None or id != "0":
            valores = self.Read_Dates("Receta", id)[0]
            
            print(valores)
            self.TxtID_receta.value = valores[0]
            self.LabelNombre_receta.value = f"Receta Seleccionada: {valores[1]}"
            self.Recetas_Producto.value = valores[0]
            
        self.page.update()
    
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
            case "Add Etiqueta":
                self.controller.Start_file_picker("Abrir", "Etiqueta", self.TxtID.value)
            case "Ver Etiqueta":
                self.ViewImage(e.control.data)
            case "Limpiar Etiqueta":
                self.controller.Start_alert_dialog(type="options", title="Confirmar", message="Esta seguro de Eliminar la imagen", actions=["Aceptar","Cancelar","Ver"], functions=[lambda: self.ClearImagen("Limpiar Etiqueta"), None, lambda: self.ViewImage("Ver Etiqueta")])
                #self.ClearImagen(e.control.data)
            case "Add Imagen":
                self.controller.Start_file_picker("Abrir", "Imagen", self.TxtID.value)
            case "Ver Imagen":
                self.ViewImage(e.control.data)
            case "Limpiar Imagen":
                self.controller.Start_alert_dialog(type="options", title="Confirmar", message="Esta seguro de Eliminar la imagen", actions=["Aceptar","Cancelar","Ver"], functions=[lambda: self.ClearImagen("Limpiar Imagen"), None, lambda: self.ViewImage("Limpiar Imagen")])
                #self.ClearImagen(e.control.data)
            case "Limpiar Producto":
                self.Clear_Form_General()
            case "Limpiar Nutrimental":
                self.Clear_Form_Nutrimental()
            case "Eliminar":
                self.controller.Start_alert_dialog(type="options", title="Confirmar", message="Esta seguro de Eliminar el producto", actions=["Aceptar","Cancelar","Ocultar"], functions=[lambda: self.Delete_Register("Permanente"), None, lambda: self.Delete_Register("Temporal")])
            case "Agregar receta":
                self.Create_receta()
            case "Limpiar receta":
                self.Clear_recetas()
            case "Eliminar receta":
                self.Delete_recetas()
            case _:
                ...
                
    def Create_Register(self):
        try:
            if self.TxtNombre.value == "" or self.TxtNombre.value == " ":
                self.controller.Start_snackbar("Error al actualizar", ft.Colors.RED, 4000)
                raise ValueError("No se ha seleccionado ningun producto")
            
            categoria = self.Categorias_Producto.value if self.Categorias_Producto.value else 1
            
            self.controller.Execute_Query("""
                INSERT INTO PRODUCTOS (
                    NOMBRE,
                    CLAVE,
                    PRESENTACION,
                    MARCA,
                    HISTORIA
                ) VALUES (%s, %s, %s, %s, %s);
                """,(str(self.TxtNombre.value).upper(), str(self.TxtClave.value).upper(), str(self.TxtPresentacion.value).upper(), str(self.TxtMarca.value).upper(), self.TxtHistoria.value ))
            
            New_id = self.controller.Execute_Query("SELECT PRODUCTOS.ID_PRODUCTOS FROM PRODUCTOS ORDER BY ID_PRODUCTOS DESC LIMIT 1;")[0][0]
            
            self.controller.Execute_Query("""
                INSERT INTO TABLA_ALIMENTICIA (
                    ID_PRODUCTO,
                    PORCION,
                    CONTENIDO_ENERGETICO,
                    PROTEINA,
                    GRASAS_TOTALES,
                    GRASAS_SATURADAS,
                    GRASAS_TRANS,
                    CARBOHIDRATOS,
                    AZUCARES_TOTALES,
                    AZUCARES_AÑADIDOS,
                    FIBRA_DIETETICA,
                    SODIO,
                    HUMEDAD,
                    GRASA_BUTIRICA_MIN,
                    PROTEINA_MIN,
                    INGREDIENTES,
                    DESCRIPCION,
                    ID_CATEGORIA
                ) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """,(New_id, self.TxtPorcion.value, self.TxtContenido_Energetico.value, self.TxtProteina.value, self.TxtGrasas_Totales.value, self.TxtGrasas_Saturadas.value, self.TxtGrasas_Trans.value, self.TxtCarbohidratos.value, self.TxtAzucares_Totales.value, self.TxtAzucares_Anadidos.value, self.TxtFibra_Dietetica.value, self.TxtSodio.value, self.TxtHumedad.value, self.TxtGrasa_Butirica_Min.value, self.TxtProteina_Min.value, self.TxtIngredientes.value, self.TxtDescripcion.value, categoria))
            
            self.Write_Table_Productos()
            self.Clear_Form_All()
            self.controller.Start_snackbar("Registro creado", ft.Colors.GREEN, 4000)
        except Exception as err:
            self.controller.Start_alert_dialog(type="error", title="Error", message="Error al registrar", description=err,)
            
    def Create_receta(self):
        try:
            if self.TxtID.value == "" or self.TxtID.value == " ":
                Id = 1
                lista = ()
                raise ValueError("No se ha seleccionado ningun producto")
            else:
                if self.Recetas_Producto.value == None:
                    raise ValueError("No se ha seleccionado ninguna receta")
                
                Id = self.TxtID.value
                lista = self.Read_Dates("Dict receta", Id)[0]
                print(lista)
                map_recetas = js.loads(lista[0])
                
                for valor in map_recetas:
                    if valor == self.Recetas_Producto.value:
                        raise ValueError("La receta ya esta registrada")
                    
                new_receta = self.Read_Dates("Receta", self.Recetas_Producto.value)[0]
                map_recetas.update({f'{new_receta[0]}':new_receta[1]})
                print(map_recetas)
            try:
                self.controller.Execute_Query(f"""
                    UPDATE PRODUCTOS
                    SET RESETAS = %s
                    WHERE ID_PRODUCTOS = %s;
                """,(js.dumps(map_recetas), Id))
                self.Clear_recetas()
                self.Write_Table_Recetas(Id)
                self.controller.Start_snackbar("Reseta agregada", ft.Colors.GREEN, 4000)
            except:
                self.controller.Start_snackbar("Error al agregar", ft.Colors.RED, 4000)
        except Exception as err:
            self.controller.Start_alert_dialog(type="error", title="Error", message="Error al actualizar", description=err,)
            
    def Read_Dates(self, Mode:str, Id:str = None):
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
                    PRODUCTOS
                ORDER BY PRODUCTOS.NOMBRE;
            """)
            case "General":
                Datos = self.controller.Execute_Query(f"""
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
                    TABLA_ALIMENTICIA.ID_CATEGORIA,
                    CATEGORIAS.NOMBRE
                FROM
                    PRODUCTOS
                INNER JOIN
                    TABLA_ALIMENTICIA
                ON PRODUCTOS.ID_PRODUCTOS = TABLA_ALIMENTICIA.ID_PRODUCTO

                INNER JOIN
                    CATEGORIAS
                ON TABLA_ALIMENTICIA.ID_CATEGORIA = CATEGORIAS.ID_CATEGORIA
                
                WHERE ID_PRODUCTOS = {Id};
            """)
            case "Producto":
                Datos = self.controller.Execute_Query(f"""
                SELECT
                    PRODUCTOS.ID_PRODUCTOS,
                    PRODUCTOS.NOMBRE,
                    PRODUCTOS.CLAVE,
                    PRODUCTOS.PRESENTACION,
                    PRODUCTOS.MARCA,
                    PRODUCTOS.HISTORIA,
                    PRODUCTOS.STATUS
                    
                FROM
                    PRODUCTOS
                WHERE ID_PRODUCTOS = {Id};
            """)
            case "Nutrimental":
                Datos = self.controller.Execute_Query(f"""
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
                ON TABLA_ALIMENTICIA.ID_CATEGORIA = CATEGORIAS.ID_CATEGORIA
                
                WHERE ID_PRODUCTOS = {Id};
            """)
            case "Imagenes":
                Datos = self.controller.Execute_Query(f"""
                SELECT
                    PRODUCTOS.IMAGEN_ETIQUETA,
                    PRODUCTOS.IMAGEN_PRODUCTO
                FROM
                    PRODUCTOS
                WHERE ID_PRODUCTOS = {Id};
            """)
            case "Tabla Recetas":
                Datos = []
                recetas = self.controller.Execute_Query(f"""
                SELECT
                    PRODUCTOS.RESETAS
                FROM
                    PRODUCTOS
                WHERE ID_PRODUCTOS = {Id};
            """)
                dic_recetas = js.loads(recetas[0][0])
                print(dic_recetas)
                for clave, valor in dic_recetas.items():
                    print(f"Clave: {clave}, Valor: {valor}")
                    contenido = self.controller.Execute_Query(f"""
                        SELECT
                            RECETAS.ID_RESETA,
                            RECETAS.NOMBRE,
                            RECETAS.DESCRIPCION
                        FROM
                            RECETAS
                        WHERE ID_RESETA = {clave};
                    """)
                    Datos.append(contenido[0])
            case "Dict receta":
                Datos = self.controller.Execute_Query(f"""
                SELECT
                    PRODUCTOS.RESETAS
                FROM
                    PRODUCTOS
                WHERE ID_PRODUCTOS = {Id};
            """)
            case "Receta":
                Datos = self.controller.Execute_Query(f"""
                SELECT
                    RECETAS.ID_RESETA,
                    RECETAS.NOMBRE,
                    RECETAS.DESCRIPCION
                FROM
                    RECETAS
                WHERE ID_RESETA = {Id};
            """)
            case _:
                Datos = []
                
        return Datos
    
    def Clear_Form_All(self):
        self.Clear_Form_General()
        self.Clear_Form_Nutrimental()
        self.Clear_recetas()
        self.table_recetas.rows = []
        
    def Clear_Form_General(self):
        self.TxtID.value = ""
        self.TxtNombre.value = ""
        self.LabelNombre.value = "Producto Seleccionado: "
        self.TxtClave.value = ""
        self.TxtPresentacion.value = ""
        self.TxtMarca.value = ""
        self.TxtHistoria.value = ""
        self.Estado_Producto.value = ""
        self.Categorias_Producto.value = ""
        
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
    
    def ClearImagen(self, data):
        try:
            if self.TxtID.value == "" or self.TxtID.value == " ":
                Id = 1
                raise ValueError("No se ha seleccionado ningun producto")
            else:
                Id = self.TxtID.value
                
            match data:
                case "Limpiar Etiqueta":
                    self.controller.Execute_Query(f"""
                        UPDATE PRODUCTOS
                        SET IMAGEN_ETIQUETA = %s
                        WHERE ID_PRODUCTOS = %s;
                    """,(None, Id))
                    self.controller.Start_snackbar("Imagen Eliminada", ft.Colors.GREEN, 4000)
                case "Limpiar Imagen":
                    self.Controller.Execute_Query(f"""
                        UPDATE PRODUCTOS
                        SET IMAGEN_PRODUCTO = %s
                        WHERE ID_PRODUCTOS = %s;
                    """,(None, Id))
                    self.controller.Start_snackbar("Imagen Eliminada", ft.Colors.GREEN, 4000)
                case _:
                    self.controller.Start_snackbar("Error al actualizar", ft.Colors.RED, 4000)
        except Exception as err:
            self.controller.Start_alert_dialog(type="error", title="Error", message="Error al actualizar", description=err,)
            
    def Clear_recetas(self):
        self.TxtID_receta.value = ""
        self.LabelNombre_receta.value = "Receta Seleccionada: "
        self.Recetas_Producto.value = ""
        
        self.page.update()
    
    def ViewImage(self, data):
        try:
            if self.TxtID.value == "" or self.TxtID.value == " ":
                Id = 1
                raise ValueError("No se ha seleccionado ningun producto")
            else:
                Id = self.TxtID.value
            
            imagen = self.Read_Dates("Imagenes", Id)
            
            if imagen:
                img = imagen[0]
            else:
                img = [None, None]
            
            match data:
                case "Ver Etiqueta":
                    if img[0] != None:
                        foto = self.controller.Convert_image_to_binary(Mode="Decode_Blob",Imagen_binary=img[0])
                    else:
                        foto = None
                    self.controller.Start_View_Photo(foto)
                case "Ver Imagen":
                    if img[1] != None:
                        foto = self.controller.Convert_image_to_binary("Decode_Blob",img[1])
                    else:
                        foto = None
                    self.controller.Start_View_Photo(foto)
                case _:
                    ...
        except Exception as err:
            self.controller.Start_alert_dialog(type="error", title="Error", message="Error al actualizar", description=err,)
        
    def Update_Registrer(self):
        try:
            if self.TxtID.value == "" or self.TxtID.value == " ":
                self.controller.Start_snackbar("Error al actualizar", ft.Colors.RED, 4000)
                raise ValueError("No se ha seleccionado ningun producto")
            
            categoria = self.Categorias_Producto.value if self.Categorias_Producto.value else 1
            
            queries = [
                """
                UPDATE PRODUCTOS
                SET NOMBRE = %s,
                    CLAVE = %s,
                    PRESENTACION = %s,
                    MARCA = %s,
                    HISTORIA = %s,
                    STATUS = %s
                WHERE ID_PRODUCTOS = %s;
                """,
                """
                UPDATE TABLA_ALIMENTICIA
                SET PORCION = %s,
                    CONTENIDO_ENERGETICO = %s,
                    PROTEINA = %s,
                    GRASAS_TOTALES = %s,
                    GRASAS_SATURADAS = %s,
                    GRASAS_TRANS = %s,
                    CARBOHIDRATOS = %s,
                    AZUCARES_TOTALES = %s,
                    AZUCARES_AÑADIDOS = %s,
                    FIBRA_DIETETICA = %s,
                    SODIO = %s,
                    HUMEDAD = %s,
                    GRASA_BUTIRICA_MIN = %s,
                    PROTEINA_MIN = %s,
                    INGREDIENTES = %s,
                    DESCRIPCION = %s,
                    ID_CATEGORIA = %s,
                    STATUS = %s
                WHERE ID_PRODUCTO = %s;
                """
            ]
            
            lista_valores_insert = [
                (
                    str(self.TxtNombre.value).upper(),
                    str(self.TxtClave.value).upper(),
                    str(self.TxtPresentacion.value).upper(),
                    str(self.TxtMarca.value).upper(),
                    self.TxtHistoria.value,
                    self.Estado_Producto.value,
                    self.TxtID.value,
                ),
                (
                    self.TxtPorcion.value,
                    self.TxtContenido_Energetico.value,
                    self.TxtProteina.value,
                    self.TxtGrasas_Totales.value,
                    self.TxtGrasas_Saturadas.value,
                    self.TxtGrasas_Trans.value,
                    self.TxtCarbohidratos.value,
                    self.TxtAzucares_Totales.value,
                    self.TxtAzucares_Anadidos.value,
                    self.TxtFibra_Dietetica.value,
                    self.TxtSodio.value,
                    self.TxtHumedad.value,
                    self.TxtGrasa_Butirica_Min.value,
                    self.TxtProteina_Min.value,
                    self.TxtIngredientes.value,
                    self.TxtDescripcion.value,
                    categoria,
                    self.Estado_Producto.value,
                    self.TxtID.value
                )
            ]
            
            self.controller.Execute_Multiple_Queries(queries,lista_valores_insert)
            self.Write_Table_Productos()
            self.Clear_Form_All()
            self.controller.Start_snackbar("Registro actualizado", ft.Colors.GREEN, 4000)
        except Exception as err:
            self.controller.Start_alert_dialog(type="error", title="Error", message="Error al actualizar", description=err,)
        
    def Delete_Register(self, Eliminacion):
        try:
            if self.TxtID.value == "" or self.TxtID.value == " ":
                Id = 1
                raise ValueError("No se ha seleccionado ningun producto")
            
            match Eliminacion:
                case "Temporal":
                    querys = [
                    """
                        UPDATE PRODUCTOS
                        SET STATUS = %s
                        WHERE ID_PRODUCTOS = %s;
                    """,
                    """
                        UPDATE TABLA_ALIMENTICIA
                        SET STATUS = %s
                        WHERE ID_PRODUCTO = %s;
                    """
                    ]
                    parameters = [
                        ('INACTIVO', Id),
                        ('INACTIVO', Id)
                    ]
                    
                    self.controller.Execute_Multiple_Queries(querys, parameters)
                    self.controller.Start_snackbar("Imagen Eliminada", ft.Colors.GREEN, 4000)
                case "Permanente":
                    querys = [
                    """
                        DELETE FROM PRODUCTOS
                        WHERE ID_PRODUCTOS = %s;
                    """,
                    """
                        DELETE FROM TABLA_ALIMENTICIA
                        WHERE ID_PRODUCTO = %s;
                    """
                    ]
                    parameters = [
                        (Id),
                        (Id)
                    ]
                    
                    self.controller.Execute_Multiple_Queries(querys, parameters)
                    self.controller.Start_snackbar("Imagen Eliminada", ft.Colors.GREEN, 4000)
                case _:
                    self.controller.Start_snackbar("Error al actualizar", ft.Colors.RED, 4000)
        except Exception as err:
            self.controller.Start_alert_dialog(type="error", title="Error", message="Error al eliminar", description=err,)
            
    def Delete_recetas(self):
        try:
            if self.TxtID.value == "" or self.TxtID.value == " ":
                Id = 1
                lista = ()
                raise ValueError("No se ha seleccionado ningun producto")
            else:
                if self.TxtID_receta.value == "" or self.TxtID_receta.value == " ":
                    raise ValueError("No se ha seleccionado ninguna receta")
                
                Id = self.TxtID.value
                lista = self.Read_Dates("Dict receta", Id)[0]
                print(lista)
                map_recetas = js.loads(lista[0])
                print(map_recetas)

                map_recetas.pop(f'{self.Recetas_Producto.value}')
                print(map_recetas)
            try:
                self.controller.Execute_Query(f"""
                    UPDATE PRODUCTOS
                    SET RESETAS = %s
                    WHERE ID_PRODUCTOS = %s;
                """,(js.dumps(map_recetas), Id))
                self.Clear_recetas()
                self.Write_Table_Recetas(Id)
                self.controller.Start_snackbar("Reseta agregada", ft.Colors.GREEN, 4000)
            except:
                self.controller.Start_snackbar("Error al actualizar", ft.Colors.RED, 4000)
        except Exception as err:
            self.controller.Start_alert_dialog(type="error", title="Error", message="Error al actualizar", description=err,)
        