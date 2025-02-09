# Módulo: `productos.py`
# Descripción: Este módulo gestiona la interfaz gráfica y la lógica relacionada con los productos.
# Permite:
# - **Ver la lista de productos** registrados en la base de datos.
# - **Registrar nuevos productos** con detalles como nombre, medida, fecha de vencimiento, precio de producción y precio de venta.
# Utiliza `tkinter` para la interfaz gráfica y se conecta con la base de datos a través del módulo `sql.py`.

import sqlite3
import tkinter as tk
from tkinter import messagebox
from sql import crear_producto, ver_productos
from datetime import datetime

def main_productos(func_regresar):
    """
    Inicia la interfaz gráfica del módulo de productos.

    Parámetros:
    - func_regresar (función): Función que se ejecuta al regresar al menú principal.

    Comportamiento:
    1. Crea una ventana con fondo blanco y título "Productos".
    2. Muestra un botón **Regresar** para volver al menú principal.
    3. Muestra un botón **Ver Productos** para listar los productos registrados.
    4. Muestra un botón **Agregar Producto** para registrar un nuevo producto.
    """
    ventana_productos = tk.Tk()
    ventana_productos.title("Productos")
    ventana_productos.geometry("300x250")
    ventana_productos.config(bg="white")  # Fondo blanco
    
    # Función para regresar al menú principal
    def regresar():
        ventana_productos.destroy() 
        func_regresar() 

    btn_regresar = tk.Button(ventana_productos, text="Regresar", command=regresar, bg="yellow", fg="black")
    btn_regresar.pack(pady=20, fill="x")

    # Botón para ver la lista de productos
    btn_ver_productos = tk.Button(ventana_productos, text="Ver Productos", command=mostrar_productos, bg="yellow", fg="black")
    btn_ver_productos.pack(pady=5, fill="x")
    
    # Botón para agregar un nuevo producto
    btn_agregar_producto = tk.Button(ventana_productos, text="Agregar Producto", command=registrar_producto, bg="yellow", fg="black")
    btn_agregar_producto.pack(pady=5, fill="x")
    
    # Ejecutar la ventana de productos
    ventana_productos.mainloop()

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
    productos = ver_productos()  # Asumiendo que esta función te devuelve una lista de productos
    
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

    tk.Label(ventana_toplevel, text="Medida:").pack(pady=5)
    entry_kilolitro = tk.Entry(ventana_toplevel)
    entry_kilolitro.pack(pady=5)

    tk.Label(ventana_toplevel, text="Fecha Vencimiento (d/m/a):").pack(pady=5)
    entry_fecha_vencimiento = tk.Entry(ventana_toplevel)
    entry_fecha_vencimiento.pack(pady=5)

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
        precio_produccion = float(entry_precio_produccion.get())
        precio_venta = float(entry_precio_venta.get())
        str_fecha = entry_fecha_vencimiento.get()
        fecha_vencimiento = datetime.strptime(str_fecha, "%d/%m/%Y").date()
        resultado = crear_producto(nombre, medida, fecha_vencimiento, precio_produccion, precio_venta)
        if resultado:
            messagebox.showinfo("", "Se ha creado correctamente el producto")
        else:
            messagebox.showerror("", "Error insertando el producto")
        ventana_toplevel.destroy()

    # Botón para registrar el producto
    btn_registrar = tk.Button(ventana_toplevel, text="Registrar Producto", command=registrar)
    btn_registrar.pack(pady=20)