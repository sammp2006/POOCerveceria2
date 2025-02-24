# Módulo: `productos.py`
# Descripción: Este módulo gestiona la interfaz gráfica y la lógica relacionada con los productos.
# Permite:
# - **Ver la lista de productos** registrados en la base de datos.
# - **Registrar nuevos productos** con detalles como nombre, medida, fecha de vencimiento, precio de producción y precio de venta.
# Utiliza `tkinter` para la interfaz gráfica y se conecta con la base de datos a través del módulo `sql.py`.

import tkinter as tk
from tkinter import messagebox
from poo import Producto
from datetime import datetime
from verificacion import formato_peso_volumen 

class VentanaMainProductos(tk.Tk):
    def __init__(self, func_regresar):
        super().__init__()  # Llamar al inicializador de la clase base Tk
        self.func_regresar = func_regresar
        self.title("Productos")
        self.geometry("300x250")
        self.config(bg="white")  # Fondo blanco
        
        # Configuración de los botones
        self._configurar_botones()
        
    def _configurar_botones(self):
        """
        Configura los botones para las acciones en la ventana de productos.
        """
        # Botón para regresar al menú principal
        btn_regresar = tk.Button(self, text="Regresar", command=self.regresar, bg="yellow", fg="black")
        btn_regresar.pack(pady=20, fill="x")

        # Botón para ver la lista de productos
        btn_ver_productos = tk.Button(self, text="Ver Productos", command=mostrar_productos, bg="yellow", fg="black")
        btn_ver_productos.pack(pady=5, fill="x")
        
        # Botón para agregar un nuevo producto
        btn_agregar_producto = tk.Button(self, text="Agregar Producto", command=registrar_producto, bg="yellow", fg="black")
        btn_agregar_producto.pack(pady=5, fill="x")
        
        # Botón para actualizar el nombre de un producto
        btn_actualizar_nombre = tk.Button(self, text="Actualizar Nombre", command=actualizar_nombre_producto_ui, bg="yellow", fg="black")
        btn_actualizar_nombre.pack(pady=5, fill="x")
    
    def regresar(self):
        """
        Función para regresar a la ventana anterior.
        """
        self.destroy()
        self.func_regresar()

def mostrar_productos():
    """
    Muestra una lista de todos los productos registrados en la base de datos.

    Comportamiento:
    1. Crea una ventana emergente con título "Lista de Productos".
    2. Muestra los productos en un formato organizado, con detalles como:
       - Nombre del producto.
       - Medida.
       - Fecha de vencimiento (formateada como `dd/mm/aaaa`).
       - Precio de producción.
       - Precio de venta.
    3. Si no hay productos registrados, muestra un mensaje informativo.
    """
    # Crear ventana emergente (Toplevel)
    ventana_toplevel = tk.Toplevel()
    ventana_toplevel.title("Lista de Productos")
    ventana_toplevel.geometry("500x400")
    
    # Crear un frame principal con fondo gris
    main_frame = tk.Frame(ventana_toplevel, bg="#f0f0f0", padx=10, pady=10)
    main_frame.pack(fill="both", expand=True)
    
    # Crear canvas para permitir desplazamiento
    canvas = tk.Canvas(main_frame)
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")  # Mismo fondo gris que el frame
    
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    
    # Obtener la lista de productos desde la base de datos
    productos = Producto.listar_objetos()  # Asumiendo que esta función te devuelve una lista de productos
    
    if productos:
        for producto in productos:
            # Crear un frame para cada producto con bordes y fondo blanco
            product_frame = tk.Frame(scrollable_frame, bg="white", relief="solid", bd=1, padx=10, pady=10, width=450)
            product_frame.pack(fill="x", pady=5, padx=10)
            
            for campo, valor in producto.items():
                if campo == 'fecha_vencimiento' and isinstance(valor, str):
                    try:
                        fecha_obj = datetime.strptime(valor, "%Y-%m-%d")  # Suponiendo que el formato de fecha es YYYY-MM-DD
                        fecha_formateada = fecha_obj.strftime("%d/%m/%Y")  # Convertir a formato d/m/año
                        valor = fecha_formateada
                    except ValueError:
                        valor = "Fecha inválida"  # En caso de que la fecha no sea válida

                # Crear etiquetas con el nombre del campo y su valor
                label = tk.Label(product_frame, text=f"{campo.capitalize()}: {valor}", font=("Arial", 10), anchor="w", bg="white")
                label.pack(fill="x", pady=2)
            
        scrollable_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
    else:
        messagebox.showinfo("No hay productos", "No se encontraron productos en la base de datos.")
        
def registrar_producto():
    """
    Permite registrar un nuevo producto en la base de datos.

    Comportamiento:
    1. Crea una ventana emergente con título "Registrar Producto".
    2. Solicita los siguientes datos:
       - **Nombre del Producto**.
       - **Medida** (ejemplo: litros, mililitros).
       - **Fecha de Vencimiento** (formato: `dd/mm/aaaa`).
       - **Precio de Producción**.
       - **Precio de Venta**.
    3. Valida los datos ingresados y los registra en la base de datos.
    4. Muestra un mensaje de éxito o error según el resultado.
    """
    # Crear una nueva ventana emergente para el registro de productos
    ventana_toplevel = tk.Toplevel()
    ventana_toplevel.title("Registrar Producto")
    ventana_toplevel.geometry("300x600")

    # Crear campos de entrada para la información del producto
    tk.Label(ventana_toplevel, text="Nombre del Producto:").pack(pady=5)
    entry_nombre = tk.Entry(ventana_toplevel)
    entry_nombre.pack(pady=5)

    tk.Label(ventana_toplevel, text="Formato Medida: \n<Volumen> ml o <Peso> g\n Ejemplo 500 ml").pack(pady=10)


    tk.Label(ventana_toplevel, text="Medida:").pack(pady=5)
    entry_kilolitro = tk.Entry(ventana_toplevel)
    entry_kilolitro.pack(pady=5)

    tk.Label(ventana_toplevel, text="Formato Fecha: Dia/Mes/Año \n Sepaparar fechas por / \n importante escribir 4 digitos en el año \n Ejemplo: 1/1/2026 o 05/05/2025").pack(pady=10)

    tk.Label(ventana_toplevel, text="Fecha Vencimiento (DD/MM/AAAA):").pack(pady=5)
    entry_fecha_vencimiento = tk.Entry(ventana_toplevel)
    entry_fecha_vencimiento.pack(pady=5)

    tk.Label(ventana_toplevel, text="** Escribir precio sin signos ni comas").pack(pady=10)


    tk.Label(ventana_toplevel, text="Precio de Producción:").pack(pady=5)
    entry_precio_produccion = tk.Entry(ventana_toplevel)
    entry_precio_produccion.pack(pady=5)

    tk.Label(ventana_toplevel, text="Precio de Venta:").pack(pady=5)
    entry_precio_venta = tk.Entry(ventana_toplevel)
    entry_precio_venta.pack(pady=5)
    
    # Mensaje de confirmación antes de registrar
    tk.Label(ventana_toplevel, text="Después de presionar el botón, regresa a la ventana principal para continuar").pack(pady=5)

    # Función para registrar el producto en la base de datos
    def registrar():
        nombre = entry_nombre.get()
        medida = entry_kilolitro.get()

        if not formato_peso_volumen(medida):
            messagebox.showerror("Error", "No se pudo insertar la medida, escribir en el siguiente formato: 100 ml o 500 o 300 g, por ejemplo")
            return

        precio_produccion = float(entry_precio_produccion.get())
        precio_venta = float(entry_precio_venta.get())
        str_fecha = entry_fecha_vencimiento.get()
        try:
            fecha_vencimiento = datetime.strptime(str_fecha, "%d/%m/%Y").date()
        except Exception as e:
            messagebox.showerror("Error", "No se pudo insertar la fecha de vencimiento, revise el formato (Dia/Mes/Año) y que la fecha sea valida")
            ventana_toplevel.destroy()
            return 
        producto_info = {
            'nombre': nombre,
            'medida': medida,
            'fecha_vencimiento': fecha_vencimiento,
            'precio_produccion': precio_produccion,
            'precio_venta': precio_venta
        }

        resultado = Producto.crear_objeto(**producto_info)
        if resultado:
            messagebox.showinfo("", "Se ha creado correctamente el producto")
        else:
            messagebox.showerror("", "Error insertando el producto")
        ventana_toplevel.destroy()

    # Botón para registrar el producto
    btn_registrar = tk.Button(ventana_toplevel, text="Registrar Producto", command=registrar)
    btn_registrar.pack(pady=20)
    
def actualizar_nombre_producto_ui():
    """
    Muestra una ventana para actualizar el nombre de un producto usando su ID.
    ### Comportamiento:
    1. Solicita el ID del producto y el nuevo nombre.
    2. Valida la entrada y actualiza el nombre en la base de datos.
    3. Muestra un mensaje de éxito o error según el resultado.
    """
    ventana_toplevel = tk.Toplevel()
    ventana_toplevel.title("Actualizar Nombre de Producto")
    ventana_toplevel.geometry("300x200")

    tk.Label(ventana_toplevel, text="ID del Producto:").pack(pady=5)
    entry_id_producto = tk.Entry(ventana_toplevel)
    entry_id_producto.pack(pady=5)

    tk.Label(ventana_toplevel, text="Nuevo Nombre del Producto:").pack(pady=5)
    entry_nuevo_nombre = tk.Entry(ventana_toplevel)
    entry_nuevo_nombre.pack(pady=5)

    def actualizar():
        id_producto = entry_id_producto.get().strip()
        nuevo_nombre = entry_nuevo_nombre.get().strip()

        if not id_producto.isdigit() or not nuevo_nombre:
            messagebox.showerror("Error", "Debe ingresar un ID válido y un nuevo nombre")
            return

        if Producto.actualizar_nombre_producto(int(id_producto), nuevo_nombre):
            messagebox.showinfo("Éxito", "Nombre actualizado correctamente")
        else:
            messagebox.showerror("Error", "No se encontró el producto o no se pudo actualizar")

        ventana_toplevel.destroy()

    btn_actualizar = tk.Button(ventana_toplevel, text="Actualizar", command=actualizar)
    btn_actualizar.pack(pady=10)
