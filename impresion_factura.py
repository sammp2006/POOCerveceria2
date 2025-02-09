import pdfkit
import os
import platform
import subprocess

# Path de la plantilla para facturas
path_plantilla_factura = "src/templates/invoicetemplate.html"

# Path donde se guardan las facturas generadas
path_facturas = "facturas"

# Lee el contenido de la plantilla
with open(path_plantilla_factura, encoding='utf-8') as archivo_factura:
    plantilla_factura: str = archivo_factura.read()


def generar_factura_html(pedido: dict) -> str:
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
    factura_generada: str = plantilla_factura

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


def generar_factura_pdf(pedido: dict) -> str:
    """
    Genera un archivo PDF con la factura de un pedido.

    ### Parámetros:
    - `pedido` (dict): Diccionario con los detalles del pedido.

    ### Retorna:
    - `str`: Ruta del archivo PDF generado.
    """
    no_factura: int = pedido["no_factura"] 
    html_factura: str = generar_factura_html(pedido)
    path_pdf: str = f"{path_facturas}/{no_factura}.pdf"
    pdfkit.from_string(html_factura, path_pdf)    
    return path_pdf


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



"""
# Ejemplo de uso (Borrar)
datos = {'cliente': {'apellido': 'Vargas',
             'correo': 'vargasmjaviermiguel@gmail.com',
             'direccion': 'calle 30 #20',
             'id_cliente': 4274182,
             'nombre': 'Javier',
             'telefono': 3772717809},
 'no_factura': '284719272',
 'precio_total': 50000,
 'productos': {1: {'cantidad': 20,
                   'fecha_venta': '2025-01-29 07:20:42',
                   'nombre': 'Cerveza Premium',
                   'precio': 10000,
                   'total': 200000},
               2: {'cantidad': 500,
                   'fecha_venta': '2025-01-29 07:47:39',
                   'nombre': 'Wisky',
                   'precio': 1111,
                   'total': 555500}}}

path_factura = generar_factura_pdf(datos)
abrir_factura_pdf(path_factura)
"""
