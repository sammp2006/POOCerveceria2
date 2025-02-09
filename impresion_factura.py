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
    Funcion que recibe un diccionario con los datos de un pedido como argumento
    y retorna un string con el contenido html de la factura correspondiente

    """

    # Copia la plantilla para facturas
    factura_generada: str = plantilla_factura

    # Toma los datos del pedido
    productos: dict = pedido["productos"]
    atributos_cliente: dict = pedido["cliente"]
    nombre_cliente = atributos_cliente["nombre"]
    apellido_cliente = atributos_cliente["apellido"]
    direccion_cliente = atributos_cliente["direccion"]
    telefono_cliente = str(atributos_cliente["telefono"])
    precio_total = str(pedido["precio_total"])

    # Genera la tabla de productos
    tabla_productos: str = ""
    for id, atributos in productos.items():
        nombre_producto = atributos["nombre"]
        cantidad = atributos["cantidad"]
        precio = atributos["precio"]
        total = atributos["total"]

        tabla_productos += f"<tr><td>{nombre_producto}</td><td>{cantidad}</td>"
        tabla_productos += f"<td>{precio}</td><td>{total}</td></tr>"

    # Inserta los datos del pedido en la plantilla
    factura_generada = factura_generada.replace("{{Customer_First_Name}}", nombre_cliente)
    factura_generada = factura_generada.replace("{{Customer_Second_Name}}", apellido_cliente)
    factura_generada = factura_generada.replace("{{Address}}", direccion_cliente)
    factura_generada = factura_generada.replace("{{Phone}}", telefono_cliente)
    factura_generada = factura_generada.replace("{{Total_Amount}}", precio_total)
    factura_generada = factura_generada.replace("{{Invoice_Items}}", tabla_productos)
    
    # Retorna la factura generada
    return factura_generada


def generar_factura_pdf(pedido: dict) -> str:
    """
    Funcion que toma como argumento los datos de un pedido en un diccionario
    genera un archivo pdf del recibo y retorna un string que contiene el path hacia el archivo generado
    """

    no_factura: int = pedido["no_factura"] 

    # Genera el string con el html correspondiente a la factura
    html_factura: str = generar_factura_html(pedido)
    
    # Genera el archivo pdf correspondiente a la factura
    path_pdf: str = f"{path_facturas}/{no_factura}.pdf"
    pdfkit.from_string(html_factura, path_pdf)    
    
    # Retorna el path al archivo generado
    return path_pdf


def abrir_factura_pdf(pdf_path: str):
    """
    Funcion que toma como argumento el path de un pdf
    y abre en el navegador el pdf

    """

    # Se asegura que la ubicacion exista
    if not os.path.isfile(pdf_path):
        print(f"No se encontro el archivo: {pdf_path}")
        return
    
    # Nombre del directorio que contiene al pdf
    dir_path = os.path.dirname(pdf_path)
    
    # Abre el PDF con Firefox
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
