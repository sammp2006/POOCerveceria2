# Módulo: `clientes.py`
# Descripción: Este módulo gestiona la interfaz gráfica y la lógica relacionada con los clientes.
# Permite registrar nuevos clientes, ver detalles, actualizar direcciones, registrar ventas y ver el historial de ventas.

import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from sql import obtener_data_factura, crear_cliente, listar_clientes, accion_cliente_detalle, accion_cliente_cambiar_direccion, accion_ver_historico_ventas_cliente, accion_registrar_venta_cliente, accion_borrar_venta
from impresion_factura import generar_factura_html, generar_factura_pdf
from correos import generar_correo_html, enviar_correo

def main_clientes(func_regresar):
    """
    Función principal del módulo de clientes. Crea la ventana principal de clientes.

    Parámetros:
    - func_regresar (función): Función para regresar al menú principal.
    """
    ventana_clientes = tk.Tk()
    ventana_clientes.title("Clientes")
    ventana_clientes.geometry("300x250")
    ventana_clientes.config(bg="white")  # Fondo blanco

    def regresar():
        """
        Función para regresar a la ventana anterior.
        """
        ventana_clientes.destroy()
        func_regresar()

    # Botón para regresar al menú principal
    btn_regresar = tk.Button(ventana_clientes, text="Regresar", command=regresar, bg="yellow", fg="black")
    btn_regresar.pack(pady=20, fill="x")

    # Botón para ver la lista de clientes
    lista_de_clientes = tk.Button(ventana_clientes, text="Ver Lista de Clientes", command=mostrar_clientes, bg="yellow", fg="black")
    lista_de_clientes.pack(pady=5, fill="x")

    # Botón para crear un nuevo cliente
    btn_crear_cliente = tk.Button(ventana_clientes, text="Crear Cliente Nuevo", command=registrar_cliente, bg="yellow", fg="black")
    btn_crear_cliente.pack(pady=5, fill="x")

    # Mensaje informativo para el usuario
    frame_informativo = tk.Label(ventana_clientes, text="Para cambiar la dirección o ver \n el detalle del cliente abre la lista primero", bg="white", fg="black")
    frame_informativo.pack(pady=20, fill="x")

    # Ejecutar la ventana de clientes
    ventana_clientes.mainloop()

def boton_ver_detalle(id_cliente):
    """
    Muestra los detalles de un cliente específico en una ventana emergente.

    Parámetros:
    - id_cliente (int): ID del cliente cuyos detalles se desean ver.
    """
    cliente = accion_cliente_detalle(id_cliente)

    if not cliente:
        messagebox.showerror("Error", "Cliente no encontrado.")
        return

    # Crear la ventana emergente para mostrar los detalles del cliente
    ventana_detalle = tk.Toplevel()
    ventana_detalle.title(f"Detalles del Cliente - ID: {id_cliente}")
    ventana_detalle.geometry("350x300")

    # Mostrar los detalles del cliente en etiquetas
    tk.Label(ventana_detalle, text=f"ID Cliente: {cliente[0]}", font=("Arial", 12)).pack(pady=5)
    tk.Label(ventana_detalle, text=f"Nombre: {cliente[1]} {cliente[2]}", font=("Arial", 12)).pack(pady=5)
    tk.Label(ventana_detalle, text=f"Dirección: {cliente[3]}", font=("Arial", 12)).pack(pady=5)
    tk.Label(ventana_detalle, text=f"Teléfono: {cliente[4]}", font=("Arial", 12)).pack(pady=5)
    tk.Label(ventana_detalle, text=f"Correo: {cliente[5]}", font=("Arial", 12)).pack(pady=5)

    # Botón para cerrar la ventana de detalles
    btn_cerrar = tk.Button(ventana_detalle, text="Cerrar", command=ventana_detalle.destroy)
    btn_cerrar.pack(pady=10)

    ventana_detalle.mainloop()

def boton_cambiar_direccion(id_cliente):
    """
    Permite cambiar la dirección de un cliente.

    Parámetros:
    - id_cliente (int): ID del cliente cuya dirección se desea cambiar.
    """
    ventana_cambiar_direccion = tk.Toplevel()
    ventana_cambiar_direccion.title(f"Cambiar Dirección - Cliente ID: {id_cliente}")
    ventana_cambiar_direccion.geometry("300x200")

    tk.Label(ventana_cambiar_direccion, text="Nueva Dirección:").pack(pady=10)
    entry_nueva_direccion = tk.Entry(ventana_cambiar_direccion, width=40)
    entry_nueva_direccion.pack(pady=5)

    def actualizar_direccion():
        """
        Función para actualizar la dirección del cliente en la base de datos.
        """
        nueva_direccion = entry_nueva_direccion.get().strip()

        if not nueva_direccion:
            messagebox.showerror("Error", "La dirección no puede estar vacía.")
            return

        accion_cliente_cambiar_direccion(nueva_direccion, id_cliente)
        messagebox.showinfo("Éxito", "Dirección actualizada correctamente.")
        ventana_cambiar_direccion.destroy()

    btn_actualizar = tk.Button(ventana_cambiar_direccion, text="Actualizar Dirección", command=actualizar_direccion)
    btn_actualizar.pack(pady=20)

    btn_cerrar = tk.Button(ventana_cambiar_direccion, text="Cerrar", command=ventana_cambiar_direccion.destroy)
    btn_cerrar.pack(pady=5)

    ventana_cambiar_direccion.mainloop()

def boton_registrar_venta(id_cliente):
    """
    Permite registrar una venta para un cliente.

    Parámetros:
    - id_cliente (int): ID del cliente para el cual se registra la venta.
    """
    ventana_toplevel = tk.Toplevel()
    ventana_toplevel.title("Registrar Venta")
    ventana_toplevel.geometry("400x300")

    # Mostrar el id del cliente en la ventana
    label_cliente = tk.Label(ventana_toplevel, text=f"Registrar Venta para Cliente ID: {id_cliente}")
    label_cliente.pack(pady=10)

    # Preguntar por el producto (puede ser una entrada de texto o una lista desplegable)
    tk.Label(ventana_toplevel, text="ID del Producto:").pack(pady=5)
    entry_producto = tk.Entry(ventana_toplevel)
    entry_producto.pack(pady=5)

    tk.Label(ventana_toplevel, text="Cantidad:").pack(pady=5)
    entry_cantidad = tk.Entry(ventana_toplevel)
    entry_cantidad.pack(pady=5)

    # Mostrar la fecha actual automáticamente
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    tk.Label(ventana_toplevel, text=f"Fecha de Venta: {fecha_actual}").pack(pady=5)

    def registrar_venta():
        """
        Función para registrar la venta en la base de datos.
        """
        producto_id = entry_producto.get()
        if not producto_id.isdigit():
            messagebox.showerror("Error", "El ID del producto debe ser un número válido")
            return
        
        cantidad_str = entry_cantidad.get()
        if not cantidad_str.isdigit():
            messagebox.showerror("Error", "La cantidad debe ser un número válido")
            return

        producto_id = int(producto_id)
        cantidad = int(cantidad_str)
        fecha_venta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Insertar en la base de datos
        if accion_registrar_venta_cliente(fecha_venta, producto_id, id_cliente, cantidad):
            messagebox.showinfo("", "Venta Registrada correctamente")
        else:
            messagebox.showerror("", "Error registrando venta")    
        ventana_toplevel.destroy()        

    # Botón para registrar la venta
    btn_registrar = tk.Button(ventana_toplevel, text="Registrar Venta", command=registrar_venta)
    btn_registrar.pack(pady=20)

    ventana_toplevel.mainloop()

def boton_ver_historico_ventas(id_cliente):
    """
    Muestra el historial de ventas de un cliente.

    Parámetros:
    - id_cliente (int): ID del cliente cuyo historial de ventas se desea ver.
    """
    ventana_toplevel = tk.Toplevel()
    ventana_toplevel.title("Histórico de Ventas")
    ventana_toplevel.geometry("600x400")

    # Mostrar el id del cliente en la ventana
    label_cliente = tk.Label(ventana_toplevel, text=f"Histórico de Ventas para Cliente ID: {id_cliente}")
    label_cliente.pack(pady=10)

    # Crear un canvas y un frame para los botones
    canvas = tk.Canvas(ventana_toplevel)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    frame = tk.Frame(canvas)
    scroll_y = tk.Scrollbar(canvas, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side=tk.RIGHT, fill="y")
    canvas.create_window((0, 0), window=frame, anchor="nw")
    
    ventas = accion_ver_historico_ventas_cliente(id_cliente)

    if not ventas:
        messagebox.showinfo("Sin Ventas", "Este cliente no tiene ventas registradas.")
        ventana_toplevel.destroy()
        return

    for venta in ventas:
        noIdVentas, fecha, producto_id = venta[0], venta[1], venta[2]
        
        # Crear un frame para cada venta
        venta_frame = tk.Frame(frame)
        venta_frame.pack(fill="x", pady=5)

        # Mostrar la venta con fecha y producto
        label_venta = tk.Label(venta_frame, text=f"Venta ID: {noIdVentas} | Fecha: {fecha} | Producto ID: {producto_id}")
        label_venta.pack(side=tk.LEFT)

        # Crear un frame para los botones de cada venta
        botones_frame = tk.Frame(venta_frame)
        botones_frame.pack(side=tk.LEFT, padx=10)

        # Botón para borrar la venta
        btn_borrar_venta = tk.Button(botones_frame, text="Borrar Venta", command=lambda id_venta=noIdVentas: boton_borrar_venta(id_venta))
        btn_borrar_venta.pack(side=tk.LEFT, padx=5)

    # Actualizar el tamaño del canvas
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    
    ventana_toplevel.mainloop()

def boton_facturar(id_cliente):
    """
    Genera los datos necesarios para facturar las ventas de un cliente.

    Parámetros:
    - id_cliente (int): ID del cliente cuyas ventas se desean facturar.
    """
    dicc = obtener_data_factura(id_cliente)
    correo = dicc["cliente"]["correo"]
    try:
        print(dicc)
        path = generar_factura_pdf(dicc)
        messagebox.showinfo("Exito", f"Factura guardada en {path}")
        print()
    except Exception as e:
        print(e)
        messagebox.showerror("Error", f"Sucedio la siguiente excepcion {e}")

    try:
        enviar_correo(pedido=dicc)
        messagebox.showinfo("Exito", f"Exito enviando a {correo}")
    except Exception as e:
        print(e)
        messagebox.showerror("Error", f"Sucedio la siguiente excepcion {e}")

def boton_borrar_venta(id_venta):
    """
    Borra una venta específica.

    Parámetros:
    - id_venta (int): ID de la venta que se desea borrar.
    """
    confirmacion = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas borrar esta venta?")
    if not confirmacion:
        return  

    try:
        ret = accion_borrar_venta(id_venta)

        if ret:
            messagebox.showinfo("Éxito", f"Venta con ID: {id_venta} eliminada correctamente.")
        else:
            messagebox.showwarning("No encontrado", f"No se encontró una venta con ID: {id_venta}.")

    except Exception as e:
        messagebox.showerror("Error", f"Error al borrar la venta: {e}")

def mostrar_clientes():
    """
    Muestra una lista de todos los clientes registrados en la base de datos.
    """
    ventana_toplevel = tk.Toplevel()
    ventana_toplevel.title("Listado de Clientes")
    ventana_toplevel.geometry("1000x500")  # Aumentar el tamaño de la ventana

    # Etiqueta de encabezado
    tk.Label(ventana_toplevel, text="Lista de Clientes Registrados", font=("Arial", 14)).pack(pady=10)

    # Obtener la lista de clientes
    clientes = listar_clientes()

    if not clientes:
        messagebox.showinfo("Sin Clientes", "No hay clientes registrados.")
        ventana_toplevel.destroy()
        return

    # Crear un área de desplazamiento para visualizar los clientes
    canvas = tk.Canvas(ventana_toplevel)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    frame = tk.Frame(canvas)
    scroll_y = tk.Scrollbar(canvas, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side=tk.RIGHT, fill="y")
    canvas.create_window((0, 0), window=frame, anchor="nw")

    # Agregar cada cliente a la lista
    for cliente in clientes:
        id_cliente, nombre, apellido = cliente[0], cliente[1], cliente[2]
        
        # Crear un frame para cada cliente
        cliente_frame = tk.Frame(frame)
        cliente_frame.pack(fill="x", pady=5)

        # Etiqueta con la información del cliente
        label_cliente = tk.Label(cliente_frame, text=f"ID: {id_cliente} | Nombre: {nombre} {apellido}", width=40, anchor="w")
        label_cliente.pack(side=tk.LEFT)

        # Crear un frame para los botones horizontales
        botones_frame = tk.Frame(cliente_frame)
        botones_frame.pack(side=tk.LEFT, padx=10)

        # Botón para ver los detalles del cliente
        btn_ver_detalle = tk.Button(botones_frame, text="Ver Detalles", command=lambda id_cliente=id_cliente: boton_ver_detalle(id_cliente))
        btn_ver_detalle.pack(side=tk.LEFT, padx=5)

        # Botón para cambiar la dirección del cliente
        btn_cambiar_direccion = tk.Button(botones_frame, text="Cambiar Dirección", command=lambda id_cliente=id_cliente: boton_cambiar_direccion(id_cliente))
        btn_cambiar_direccion.pack(side=tk.LEFT, padx=5)

        # Botón para registrar una venta del cliente
        btn_registrar_venta = tk.Button(botones_frame, text="Registrar Venta", command=lambda id_cliente=id_cliente: boton_registrar_venta(id_cliente))
        btn_registrar_venta.pack(side=tk.LEFT, padx=5)

        # Botón para ver el histórico de ventas
        btn_ver_historico = tk.Button(botones_frame, text="Historico Ventas", command=lambda id_cliente=id_cliente: boton_ver_historico_ventas(id_cliente))
        btn_ver_historico.pack(side=tk.LEFT, padx=5)

        # Botón para facturar el carrito
        btn_ver_historico = tk.Button(botones_frame, text="Facturar Carrito", command=lambda id_cliente=id_cliente: boton_facturar(id_cliente))
        btn_ver_historico.pack(side=tk.LEFT, padx=5)

    # Botón para cerrar la ventana emergente
    btn_cerrar = tk.Button(ventana_toplevel, text="Cerrar", command=ventana_toplevel.destroy)
    btn_cerrar.pack(pady=10)

    ventana_toplevel.mainloop()

def registrar_cliente():
    """
    Permite registrar un nuevo cliente en la base de datos.
    """
    ventana_toplevel = tk.Toplevel()
    ventana_toplevel.title("Registrar Cliente")
    ventana_toplevel.geometry("300x400")

    tk.Label(ventana_toplevel, text="Nombre:").pack(pady=5)
    entry_nombre = tk.Entry(ventana_toplevel)
    entry_nombre.pack(pady=5)

    tk.Label(ventana_toplevel, text="Apellido:").pack(pady=5)
    entry_apellido = tk.Entry(ventana_toplevel)
    entry_apellido.pack(pady=5)

    tk.Label(ventana_toplevel, text="Dirección:").pack(pady=5)
    entry_direccion = tk.Entry(ventana_toplevel)
    entry_direccion.pack(pady=5)

    tk.Label(ventana_toplevel, text="Teléfono:").pack(pady=5)
    entry_telefono = tk.Entry(ventana_toplevel)
    entry_telefono.pack(pady=5)

    tk.Label(ventana_toplevel, text="Correo:").pack(pady=5)
    entry_correo = tk.Entry(ventana_toplevel)
    entry_correo.pack(pady=5)

    tk.Label(ventana_toplevel, text="Después de presionar el botón, se registrará al cliente").pack(pady=5)

    def registrar():
        """
        Función para registrar el cliente en la base de datos.
        """
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        direccion = entry_direccion.get()
        telefono = entry_telefono.get()
        correo = entry_correo.get()

        if not nombre or not apellido or not direccion or not telefono or not correo:
            messagebox.showerror("Error", "Por favor complete todos los campos.")
            return

        try:
            telefono = int(telefono)  # Verificamos que el teléfono sea un número
        except ValueError:
            messagebox.showerror("Error", "El teléfono debe ser un número.")
            return

        crear_cliente(nombre, apellido, direccion, telefono, correo)

        # Mensaje de éxito
        messagebox.showinfo("Éxito", "Cliente registrado correctamente.")
        ventana_toplevel.destroy()

    # Botón para registrar al cliente
    btn_registrar = tk.Button(ventana_toplevel, text="Registrar Cliente", command=registrar)
    btn_registrar.pack(pady=20)

    ventana_toplevel.mainloop()