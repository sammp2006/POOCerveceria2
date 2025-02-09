# Módulo: `sql.py`
# Descripción: Este módulo gestiona las operaciones de base de datos, incluyendo la creación de tablas
# y las operaciones CRUD (Crear, Leer, Actualizar, Eliminar) para las tablas de Productos, Clientes y Ventas.
# Utiliza SQLite como motor de base de datos.

import sqlite3
import uuid
from datetime import datetime

def crear_base_de_datos(conexion, cursor):
    """
    ## Función: `crear_base_de_datos`
    Crea las tablas necesarias en la base de datos si no existen.

    ### Parámetros:
    - `conexion`: Objeto de conexión a la base de datos.
    - `cursor`: Objeto cursor para ejecutar consultas SQL.

    ### Comportamiento:
    1. Crea la tabla **Productos** con las siguientes columnas:
       - `noIdProducto` (clave primaria, autoincremental).
       - `NombreProducto` (texto, no nulo).
       - `medida` (texto, no nulo).
       - `Fechavencimiento` (fecha, no nulo).
       - `PrecioProduccion` (entero, no nulo).
       - `PrecioVenta` (entero, no nulo).

    2. Crea la tabla **Clientes** con las siguientes columnas:
       - `noIdCliente` (clave primaria, autoincremental).
       - `nombre` (texto, no nulo).
       - `apellido` (texto, no nulo).
       - `direccion` (texto, no nulo).
       - `telefono` (entero, no nulo).
       - `correo` (texto, no nulo).

    3. Crea la tabla **Ventas** con las siguientes columnas:
       - `noIdVentas` (clave primaria, autoincremental).
       - `fecha` (fecha y hora).
       - `producto` (entero, clave foránea que referencia a `Productos`).
       - `cliente` (entero, clave foránea que referencia a `Clientes`).
       - `cantidad` (entero).

    4. Guarda los cambios y cierra la conexión.
    """
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
                noIdProducto INTEGER PRIMARY KEY AUTOINCREMENT, 
                NombreProducto text NOT NULL, 
                medida text NOT NULL, 
                Fechavencimiento date NOT NULL, 
                PrecioProduccion integer NOT NULL, 
                PrecioVenta integer NOT NULL
        )''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Clientes (
            noIdCliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre text NOT NULL,
            apellido text NOT NULL,
            direccion text NOT NULL,
            telefono integer NOT NULL,
            correo text NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Ventas (
            noIdVentas INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha DATETIME,
            producto INTEGER,
            cliente INTEGER,
            cantidad INTEGER,
            FOREIGN KEY (producto) REFERENCES Productos(noIdProducto),
            FOREIGN KEY (cliente) REFERENCES Clientes(noIdCliente)
        )
    ''')

    conexion.commit()
    conexion.close()

def abrir_conexion():
    """
    ## Función: `abrir_conexion`
    Abre una conexión a la base de datos y devuelve el objeto de conexión y cursor.

    ### Parámetros:
    - No recibe parámetros.

    ### Comportamiento:
    1. Conecta a la base de datos `data.db`.
    2. Devuelve el objeto de conexión y cursor.
    """
    con = sqlite3.connect('data.db')
    cursor = con.cursor()
    return con, cursor

def ver_productos():
    """
    ## Función: `ver_productos`
    Devuelve una lista de todos los productos registrados en la base de datos.

    ### Parámetros:
    - No recibe parámetros.

    ### Comportamiento:
    1. Abre una conexión a la base de datos.
    2. Ejecuta una consulta para obtener todos los productos.
    3. Devuelve una lista de diccionarios, donde cada diccionario contiene los detalles de un producto.
    4. Cierra la conexión.
    """
    try:
        con, cursor = abrir_conexion()

        cursor.execute("SELECT * FROM Productos")
        productos = cursor.fetchall()

        productos_lista = []
        for producto in productos:
            producto_dict = {
                "id": producto[0],
                "nombre": producto[1],
                "medida": producto[2],
                "fecha_vencimiento": producto[3],
                "precio_produccion": producto[4],
                "precio_venta": producto[5]
            }
            productos_lista.append(producto_dict)

        con.close()

        return productos_lista
    except:
        return None

def crear_producto(nombre, medida, fechaVencimiento, precioProduccion, precioVenta):
    """
    ## Función: `crear_producto`
    Inserta un nuevo producto en la base de datos.

    ### Parámetros:
    - `nombre` (str): Nombre del producto.
    - `medida` (str): Medida del producto (ejemplo: litros, mililitros).
    - `fechaVencimiento` (str): Fecha de vencimiento del producto.
    - `precioProduccion` (int): Precio de producción del producto.
    - `precioVenta` (int): Precio de venta del producto.

    ### Comportamiento:
    1. Abre una conexión a la base de datos.
    2. Inserta el producto en la tabla **Productos**.
    3. Guarda los cambios y cierra la conexión.
    4. Devuelve `True` si la operación fue exitosa, de lo contrario, devuelve `False`.
    """
    try:
        con, cursor = abrir_conexion()
        cursor.execute('''
            INSERT INTO productos (NombreProducto, medida, Fechavencimiento, PrecioProduccion, PrecioVenta)
            VALUES(?, ?, ?, ?, ?)
        ''', (nombre, medida, fechaVencimiento, precioProduccion, precioVenta))

        con.commit()

        con.close()

        return True
    except Exception as e:
        print(e)
        return False
    
def actualizar_nombre_producto(id_producto, nuevo_nombre):
    """
    Actualiza el nombre de un producto en la base de datos basado en su ID.

    Parámetros:
    - id_producto (int): ID del producto.
    - nuevo_nombre (str): Nuevo nombre del producto.

    Retorna:
    - True si la actualización fue exitosa, False en caso contrario.
    """
    try:
        con, cursor = abrir_conexion()
        cursor.execute("UPDATE productos SET NombreProducto = ? WHERE noIdProducto = ?", (nuevo_nombre, id_producto))
        con.commit()
        exito = cursor.rowcount > 0  # Retorna True si se actualizó algún registro
        con.close()
        return exito
    except Exception as e:
        print(f"Error al actualizar el nombre del producto: {e}")
        return False


def listar_clientes():
    """
    ## Función: `listar_clientes`
    Devuelve una lista de todos los clientes registrados en la base de datos.

    ### Parámetros:
    - No recibe parámetros.

    ### Comportamiento:
    1. Abre una conexión a la base de datos.
    2. Ejecuta una consulta para obtener todos los clientes.
    3. Devuelve una lista de tuplas, donde cada tupla contiene los detalles de un cliente.
    4. Cierra la conexión.
    """
    conn, cursor = abrir_conexion()
    cursor.execute("SELECT noIdCliente, nombre, apellido, direccion, telefono, correo FROM Clientes")
    clientes = cursor.fetchall()
    conn.close()
    return clientes

def accion_cliente_detalle(id_cliente):
    """
    ## Función: `accion_cliente_detalle`
    Devuelve los detalles de un cliente específico.

    ### Parámetros:
    - `id_cliente` (int): ID del cliente cuyos detalles se desean obtener.

    ### Comportamiento:
    1. Abre una conexión a la base de datos.
    2. Ejecuta una consulta para obtener los detalles del cliente con el ID especificado.
    3. Devuelve una tupla con los detalles del cliente.
    4. Cierra la conexión.
    """
    conn, cursor = abrir_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT noIdCliente, nombre, apellido, direccion, telefono, correo FROM Clientes WHERE noIdCliente = ?", (id_cliente,))
    cliente = cursor.fetchone()
    conn.close()
    return cliente

def accion_cliente_cambiar_direccion(nueva_direccion, id_cliente):
    """
    ## Función: `accion_cliente_cambiar_direccion`
    Actualiza la dirección de un cliente.

    ### Parámetros:
    - `nueva_direccion` (str): Nueva dirección del cliente.
    - `id_cliente` (int): ID del cliente cuya dirección se desea actualizar.

    ### Comportamiento:
    1. Abre una conexión a la base de datos.
    2. Ejecuta una consulta para actualizar la dirección del cliente.
    3. Guarda los cambios y cierra la conexión.
    """
    conn, cursor = abrir_conexion()
    cursor.execute("UPDATE Clientes SET direccion = ? WHERE noIdCliente = ?", (nueva_direccion, id_cliente))
    conn.commit()
    conn.close()

def accion_ver_historico_ventas_cliente(id_cliente):
    """
    ## Función: `accion_ver_historico_ventas_cliente`
    Devuelve el historial de ventas de un cliente.

    ### Parámetros:
    - `id_cliente` (int): ID del cliente cuyo historial de ventas se desea obtener.

    ### Comportamiento:
    1. Abre una conexión a la base de datos.
    2. Ejecuta una consulta para obtener las ventas del cliente.
    3. Devuelve una lista de tuplas, donde cada tupla contiene los detalles de una venta.
    4. Cierra la conexión.
    """
    conn, cursor = abrir_conexion()
    cursor.execute('''
        SELECT noIdVentas, fecha, producto, cantidad FROM Ventas WHERE cliente = ?
    ''', (id_cliente,))
    ventas = cursor.fetchall()
    conn.close()
    return ventas

def obtener_data_factura(id_cliente):
    """
    ## Función: `obtener_data_factura`
    Genera los datos necesarios para facturar las ventas de un cliente.

    ### Parámetros:
    - `id_cliente` (int): ID del cliente cuyas ventas se desean facturar.

    ### Comportamiento:
    1. Abre una conexión a la base de datos.
    2. Obtiene los datos del cliente y sus ventas.
    3. Calcula el precio total de las ventas.
    4. Genera un número de factura único.
    5. Devuelve un diccionario con los datos de facturación.
    6. Cierra la conexión.
    """
    conn, cursor = abrir_conexion()

    # Inicializamos el diccionario que tendrá toda la información
    dicc = {}

    # 1. Obtener los datos del cliente
    cursor.execute('''
        SELECT nombre, apellido, direccion, telefono, correo 
        FROM Clientes WHERE noIdCliente = ?
    ''', (id_cliente,))
    cliente_data = cursor.fetchone()

    if cliente_data:
        dicc["cliente"] = {
            "id_cliente": id_cliente,
            "nombre": cliente_data[0],
            "apellido": cliente_data[1],
            "direccion": cliente_data[2],
            "telefono": cliente_data[3],
            "correo": cliente_data[4]
        }
    
    # 2. Obtener las ventas del cliente
    cursor.execute('''
        SELECT V.noIdVentas, V.fecha, V.producto, V.cantidad
        FROM Ventas V
        WHERE V.cliente = ?
    ''', (id_cliente,))
    ventas_cliente = cursor.fetchall()

    productos = {}
    precio_total = 0

    for venta in ventas_cliente:
        noIdVentas, fecha, id_producto, cantidad = venta

        cursor.execute('''
            SELECT NombreProducto, PrecioVenta
            FROM Productos
            WHERE noIdProducto = ?
        ''', (id_producto,))
        producto_data = cursor.fetchone()

        if producto_data:
            nombre_producto, precio_venta = producto_data
            precio_venta_total = precio_venta * cantidad

            productos[id_producto] = {
                "nombre": nombre_producto,
                "precio": precio_venta,
                "fecha_venta": fecha,
                "cantidad": cantidad,
                "total": precio_venta_total
            }

            precio_total += precio_venta_total

    no_factura = f"{datetime.now().strftime('%Y%m%d%H%M%S')}{id_cliente}{str(uuid.uuid4().int)[:10]}"

    dicc["no_factura"] = no_factura
    dicc["productos"] = productos
    dicc["precio_total"] = precio_total

    conn.close()

    return dicc

def accion_registrar_venta_cliente(fecha_venta, producto_id, id_cliente, cantidad):
    """
    ## Función: `accion_registrar_venta_cliente`
    Registra una venta para un cliente.

    ### Parámetros:
    - `fecha_venta` (str): Fecha y hora de la venta.
    - `producto_id` (int): ID del producto vendido.
    - `id_cliente` (int): ID del cliente que realizó la compra.
    - `cantidad` (int): Cantidad de productos vendidos.

    ### Comportamiento:
    1. Abre una conexión a la base de datos.
    2. Inserta la venta en la tabla **Ventas**.
    3. Guarda los cambios y cierra la conexión.
    4. Devuelve `True` si la operación fue exitosa, de lo contrario, devuelve `False`.
    """
    conn, cursor = abrir_conexion()
    try:
        cursor.execute('''
            INSERT INTO Ventas (fecha, producto, cliente, cantidad)
            VALUES (?, ?, ?, ?)
        ''', (fecha_venta, producto_id, id_cliente, cantidad))
        conn.commit()

        conn.close()
        return True
    
    except:
        return False

def accion_borrar_venta(id_venta):
    """
    ## Función: `accion_borrar_venta`
    Borra una venta específica.

    ### Parámetros:
    - `id_venta` (int): ID de la venta que se desea borrar.

    ### Comportamiento:
    1. Abre una conexión a la base de datos.
    2. Ejecuta una consulta para borrar la venta.
    3. Guarda los cambios y cierra la conexión.
    4. Devuelve `True` si la operación fue exitosa, de lo contrario, devuelve `False`.
    """
    conn, cursor = abrir_conexion()
    cursor.execute('''
            DELETE FROM Ventas WHERE noIdVentas = ?
        ''', (id_venta,))
    conn.commit()
    if cursor.rowcount > 0:
        return True
    else:
        False

def crear_cliente(nombre, apellido, direccion, telefono, correo):
    """
    ## Función: `crear_cliente`
    Registra un nuevo cliente en la base de datos.

    ### Parámetros:
    - `nombre` (str): Nombre del cliente.
    - `apellido` (str): Apellido del cliente.
    - `direccion` (str): Dirección del cliente.
    - `telefono` (int): Teléfono del cliente.
    - `correo` (str): Correo electrónico del cliente.

    ### Comportamiento:
    1. Abre una conexión a la base de datos.
    2. Inserta el cliente en la tabla **Clientes**.
    3. Guarda los cambios y cierra la conexión.
    4. Devuelve `True` si la operación fue exitosa, de lo contrario, devuelve `False`.
    """
    try:
        conn, cursor = abrir_conexion()
        cursor.execute('''
            INSERT INTO Clientes (nombre, apellido, direccion, telefono, correo)
            VALUES (?, ?, ?, ?, ?)
        ''', (nombre, apellido, direccion, telefono, correo))
        conn.commit()
        conn.close()

        return True
    except:
        return False    

if __name__ == "__main__":
    """
    Cuando se ejecuta sql.py entonces se crea la base de datos
    """
    con, cursor = abrir_conexion()
    crear_base_de_datos(con, cursor)