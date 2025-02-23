import sqlite3
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import pdfkit
import uuid
import os
import platform
import subprocess

class Db:
    def __init__(self):
        """
        Abre una conexión a la base de datos e inicia el objeto de conexión y cursor.

        ### Parámetros:
        - No recibe parámetros.

        ### Comportamiento:
        1. Conecta a la base de datos `data.db`.
        2. Inicia el atributo de conexión y cursor.
        """
        self.conexion = sqlite3.connect("data.db")
        self.cursor = self.conexion.cursor()

    def cerrar(self):
        """
        Cerrar la conexion de la base de datos
        """
        self.conexion.close()


    def verificar_conexion(self):
        """
        Reabrir la conexión por si no está disponible la variable de conexión o cursor.
        """
        try:
            # Realizamos una consulta simple para verificar la conexión
            self.cursor.execute("SELECT 1")
        except (sqlite3.ProgrammingError, sqlite3.DatabaseError) as e:
            # Si ocurre un error, se reabre la conexión
            print("Conexión cerrada o no disponible. Reabriendo...")
            self.conexion = sqlite3.connect("data.db")
            self.cursor = self.conexion.cursor()


    def ejecutar_sql(self, sql):
        """
        Ejecutar cadena sql
        """
        self.verificar_conexion()
        self.cursor.execute(sql)
        self.conexion.commit()

    @staticmethod
    def iniciar_tablas(self):
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
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                    noIdProducto INTEGER PRIMARY KEY AUTOINCREMENT,
                    NombreProducto text NOT NULL,
                    medida text NOT NULL,
                    Fechavencimiento date NOT NULL,
                    PrecioProduccion integer NOT NULL,
                    PrecioVenta integer NOT NULL
            )''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Clientes (
                noIdCliente INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre text NOT NULL,
                apellido text NOT NULL,
                direccion text NOT NULL,
                telefono integer NOT NULL,
                correo text NOT NULL
            )
        ''')

        self.cursor.execute('''
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
        self.conexion.commit()

        self.cerrar()
        return

class Objeto:
    def __init__(self):
        self.db = Db()
    
    @staticmethod
    def crear_objeto(self):
        pass

    
class Producto(Objeto):
    def __init__(self, id):
        super().__init__()
        self.id = id
        tupla = Producto.obtener_producto_detalle(id)
        self.nombre = tupla[0]
        self.volumen = tupla[1]
        self.precio_produccion = tupla[2]
        self.precio_venta = tupla[3]
        self.fecha_vencimiento = tupla[4]

    @staticmethod
    def obtener_producto_detalle(id_producto):
        db = Db()
        db.cursor.execute("SELECT * FROM Productos WHERE noIdProducto = ?", (id_producto,))
        producto = db.cursor.fetchone()
        db.cerrar()
        return producto

    @staticmethod
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
            db = Db()
            db.verificar_conexion()
            db.cursor.execute("UPDATE productos SET NombreProducto = ? WHERE noIdProducto = ?", (nuevo_nombre, id_producto))
            db.conexion.commit()
            exito = db.cursor.rowcount > 0  # Retorna True si se actualizó algún registro
            db.cerrar()
            return exito
        except Exception as e:
            print(f"Error al actualizar el nombre del producto: {e}")
            return False

    @staticmethod
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
            db = Db()
            db.cursor.execute("SELECT * FROM Productos")
            productos = db.cursor.fetchall()

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

            db.cerrar()

            return productos_lista
        except:
            return None


    @staticmethod
    def buscar_producto(id):
        """
        Retornar objeto producto
        """
        db = Db()
        db.cursor.execute("SELECT * FROM productos WHERE id = ?", (id,))
        tupla = db.cursor.fetchone()
        
        if tupla:  # Si el producto existe en la base de datos
            return Producto(*tupla)
        return None  # Si no se encontró el producto

    @staticmethod
    def crear_producto(nombre, medida, fecha_vencimiento, precio_produccion, precio_venta):
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
        db = Db()
        try:
            db.cursor.execute('''
                    INSERT INTO productos (NombreProducto, medida, Fechavencimiento, PrecioProduccion, PrecioVenta)
                    VALUES(?, ?, ?, ?, ?)
                ''', (nombre, medida, fecha_vencimiento, precio_produccion, precio_venta))

            db.conexion.commit()
            db.cerrar()
            return True
        except Exception as e:
            print(e)
            return False


class Cliente(Objeto):
    def __init__(self, id):
        super().__init__()
        self.id = id
        tupla = Cliente.accion_cliente_detalle(id)
        self.nombre = tupla[1]
        self.apellido = tupla[2]
        self.direccion = tupla[3]
        self.telefono = tupla[4]
        self.correo = tupla[5]
    
    @staticmethod
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
        cad = "SELECT noIdCliente, nombre, apellido, direccion, telefono, correo FROM Clientes"
        db = Db()
        db.ejecutar_sql(cad)
        lista = db.cursor.fetchall()
        db.cerrar()
        return lista

    @staticmethod
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
        db = Db()
        db.cursor.execute("SELECT noIdCliente, nombre, apellido, direccion, telefono, correo FROM Clientes WHERE noIdCliente = ?", (id_cliente,))
        cliente = db.cursor.fetchone()
        db.cerrar()
        return cliente

    @staticmethod
    def accion_cliente_cambiar_direccion(id_cliente, nueva_direccion):
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
        db = Db()
        db.cursor.execute("UPDATE Clientes SET direccion = ? WHERE noIdCliente = ?", (nueva_direccion, id_cliente))
        db.conexion.commit()
        db.cerrar()

    @staticmethod
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
        db = Db()
        db.cursor.execute('''
            SELECT V.noIdVentas, V.fecha, V.producto, V.cantidad
            FROM Ventas V
            WHERE V.cliente = ?
        ''', (id_cliente,))
        ventas_cliente = db.cursor.fetchall()
        db.cerrar()
        return ventas_cliente

    @staticmethod
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
        db = Db()
        # Inicializamos el diccionario que tendrá toda la información
        dicc = {}

        # 1. Obtener los datos del cliente
        db.cursor.execute('''
            SELECT nombre, apellido, direccion, telefono, correo 
            FROM Clientes WHERE noIdCliente = ?
        ''', (id_cliente,))
        cliente_data = db.cursor.fetchone()

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
        db.cursor.execute('''
            SELECT V.noIdVentas, V.fecha, V.producto, V.cantidad
            FROM Ventas V
            WHERE V.cliente = ?
        ''', (id_cliente,))
        ventas_cliente = db.cursor.fetchall()

        productos = {}
        precio_total = 0

        for venta in ventas_cliente:
            noIdVentas, fecha, id_producto, cantidad = venta

            db.cursor.execute('''
                SELECT NombreProducto, PrecioVenta
                FROM Productos
                WHERE noIdProducto = ?
            ''', (id_producto,))
            producto_data = db.cursor.fetchone()

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

        db.cerrar()

        return dicc

  

    @staticmethod
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
        try:
            db = Db()
            db.cursor.execute('''
                INSERT INTO Ventas (fecha, producto, cliente, cantidad)
                VALUES (?, ?, ?, ?)
            ''', (fecha_venta, producto_id, id_cliente, cantidad))
            db.conexion.commit()

            db.cerrar()
            return True
        
        except:
            return False


class Venta:
    def __init__(self):
        self.db = Db()

    @staticmethod
    def obtener_objeto_venta(id_venta):
        pass

    @staticmethod
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
        db = Db()
        db.cursor.execute('''
            DELETE FROM Ventas WHERE noIdVentas = ?
        ''', (id_venta,))
        db.conexion.commit()
        db.cerrar()
        return True

class Correo:
    
    path_plantilla_correo = "src/templates/mailtemplate.html"

    with open(path_plantilla_correo, encoding='utf-8') as archivo_plantilla_correo:
        plantilla_correo = archivo_plantilla_correo.read()

    @staticmethod
    def generar_correo_html(pedido: dict) -> str:
        """
        Genera el contenido HTML de un correo de confirmación de pedido.

        ### Parámetros:
        - `pedido` (dict): Diccionario con los detalles del pedido, incluyendo:
        - `productos`: Lista de productos comprados.
        - `cliente`: Datos del cliente (nombre, apellido, dirección, teléfono, etc.).
        - `precio_total`: Total a pagar.
        - `no_factura`: Número de factura.

        ### Retorna:
        - `str`: HTML del correo con los datos insertados.
        """
        correo_generado: str = Correo.plantilla_correo

        # Extraer datos del pedido
        productos: dict = pedido["productos"]
        atributos_cliente: dict = pedido["cliente"]
        nombre_cliente = atributos_cliente["nombre"]
        apellido_cliente = atributos_cliente["apellido"]
        direccion_cliente = atributos_cliente["direccion"]
        telefono_cliente = str(atributos_cliente["telefono"])
        precio_total = str(pedido["precio_total"])
        no_factura = pedido["no_factura"]

        # Generar la tabla de productos
        tabla_productos: str = ""
        for _, atributos in productos.items():
            nombre_producto = atributos["nombre"]
            cantidad = atributos["cantidad"]
            precio = atributos["precio"]
            total = atributos["total"]
            tabla_productos += f"<tr><td>{nombre_producto}</td><td>{cantidad}</td><td>{precio}</td><td>{total}</td></tr>"

        # Insertar datos en la plantilla
        correo_generado = correo_generado.replace("{{Customer_First_Name}}", nombre_cliente)
        correo_generado = correo_generado.replace("{{Customer_Last_Name}}", apellido_cliente)
        correo_generado = correo_generado.replace("{{Address}}", direccion_cliente)
        correo_generado = correo_generado.replace("{{Phone}}", telefono_cliente)
        correo_generado = correo_generado.replace("{{Total_Amount}}", precio_total)
        correo_generado = correo_generado.replace("{{Invoice_Items}}", tabla_productos)
        correo_generado = correo_generado.replace("{{Invoice_Number}}", no_factura)
        correo_generado = correo_generado.replace("{{Invoice_Date}}", datetime.now().strftime("%m/%d/%Y"))
        correo_generado = correo_generado.replace("{{Year}}", str(datetime.now().year))
        
        return correo_generado

    @staticmethod
    def enviar_correo(pedido: dict):
        """
        Envía un correo de confirmación del pedido al cliente.

        ### Parámetros:
        - `pedido` (dict): Datos del pedido.

        ### Comportamiento:
        1. Genera el contenido del correo a partir del pedido.
        2. Configura el servidor SMTP de Gmail.
        3. Intenta enviar el correo y maneja errores en caso de falla.
        """
        atributos_cliente: dict = pedido["cliente"]
        no_pedido = pedido["no_factura"] 
        correo_cliente = [atributos_cliente["correo"]]

        # Crear mensaje
        msg = MIMEMultipart()
        msg['From'] = "lacerveceriaartesanalsa@gmail.com"  # Cambiar según necesidad
        msg['To'] = ', '.join(correo_cliente)
        msg['Subject'] = f"Recibo de su pedido No {no_pedido} - Cerveceria Artesanal"

        # Adjuntar contenido HTML
        html_content = Correo.generar_correo_html(pedido)
        msg.attach(MIMEText(html_content, "html")) 

        # Configurar servidor SMTP
        smtp_server = "smtp.gmail.com"
        smtp_port = 465
        correo_emisor = "lacerveceriaartesanalsa@gmail.com"
        password = "contraseña_aquí"  # No almacenar contraseñas en código fuente

        try:
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as smtp:
                smtp.login(correo_emisor, password)
                smtp.sendmail(correo_emisor, correo_cliente, msg.as_string())
        except Exception as e:
            print(f"Error al enviar el correo: {e}")

class Factura:
    path_plantilla_factura = "src/templates/invoicetemplate.html"

    # Path donde se guardan las facturas generadas
    path_facturas = "facturas"

    # Lee el contenido de la plantilla
    with open(path_plantilla_factura, encoding='utf-8') as archivo_factura:
        plantilla_factura: str = archivo_factura.read()

    @classmethod
    def generar_factura_html(cls, pedido: dict) -> str:
        """
        Genera el contenido HTML de una factura de compra.

        ### Parámetros:
        - `pedido` (dict): Diccionario con los detalles del pedido:
        - `productos`: Lista de productos comprados.
        - `cliente`: Datos del cliente (nombre, dirección, teléfono, etc.).
        - `precio_total`: Total a pagar.
        - `no_factura`: Número de factura.

        ### Retorna:
        - `str`: HTML de la factura con los datos insertados.
        """
        factura_generada: str = cls.plantilla_factura

        # Extraer datos del pedido
        productos: dict = pedido["productos"]
        atributos_cliente: dict = pedido["cliente"]
        nombre_cliente = atributos_cliente["nombre"]
        apellido_cliente = atributos_cliente["apellido"]
        direccion_cliente = atributos_cliente["direccion"]
        telefono_cliente = str(atributos_cliente["telefono"])
        precio_total = str(pedido["precio_total"])

        # Generar la tabla de productos
        tabla_productos: str = ""
        for _, atributos in productos.items():
            nombre_producto = atributos["nombre"]
            cantidad = atributos["cantidad"]
            precio = atributos["precio"]
            total = atributos["total"]
            tabla_productos += f"<tr><td>{nombre_producto}</td><td>{cantidad}</td><td>{precio}</td><td>{total}</td></tr>"

        # Insertar datos en la plantilla
        factura_generada = factura_generada.replace("{{Customer_First_Name}}", nombre_cliente)
        factura_generada = factura_generada.replace("{{Customer_Second_Name}}", apellido_cliente)
        factura_generada = factura_generada.replace("{{Address}}", direccion_cliente)
        factura_generada = factura_generada.replace("{{Phone}}", telefono_cliente)
        factura_generada = factura_generada.replace("{{Total_Amount}}", precio_total)
        factura_generada = factura_generada.replace("{{Invoice_Items}}", tabla_productos)
        
        return factura_generada

    @classmethod
    def generar_factura_pdf(cls, pedido: dict) -> str:
        """
        Genera un archivo PDF con la factura de un pedido.

        ### Parámetros:
        - `pedido` (dict): Diccionario con los detalles del pedido.

        ### Retorna:
        - `str`: Ruta del archivo PDF generado.
        """
        no_factura: int = pedido["no_factura"] 
        html_factura: str = cls.generar_factura_html(pedido)
        path_pdf: str = f"{cls.path_facturas}/{no_factura}.pdf"
        pdfkit.from_string(html_factura, path_pdf)    
        return path_pdf

    @staticmethod
    def abrir_factura_pdf(pdf_path: str):
        """
        Abre un archivo PDF de factura en el navegador predeterminado.

        ### Parámetros:
        - `pdf_path` (str): Ruta del archivo PDF a abrir.
        """
        if not os.path.isfile(pdf_path):
            print(f"No se encontró el archivo: {pdf_path}")
            return
        
        if platform.system() == "Windows":
            subprocess.run(["C:\\Program Files\\Mozilla Firefox\\firefox.exe", pdf_path])
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", "-a", "Firefox", pdf_path])
        elif platform.system() == "Linux":
            subprocess.run(["firefox", pdf_path])
        else:
            print(f"Sistema operativo no soportado: {platform.system()}")

