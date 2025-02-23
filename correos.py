import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

# Path de la plantilla para correos
path_plantilla_correo = "src/templates/mailtemplate.html"

# Lee el contenido de la plantilla
with open(path_plantilla_correo, encoding='utf-8') as archivo_plantilla_correo:
    plantilla_correo = archivo_plantilla_correo.read()


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
    correo_generado: str = plantilla_correo

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
    html_content = generar_correo_html(pedido)
    msg.attach(MIMEText(html_content, "html")) 

    # Configurar servidor SMTP
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    correo_emisor = "lacerveceriaartesanalsa@gmail.com"
    password = "ppxn mzfg iako hzbl" 

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as smtp:
            smtp.login(correo_emisor, password)
            smtp.sendmail(correo_emisor, correo_cliente, msg.as_string())
    except Exception as e:
        print(f"Error al enviar el correo: {e}")




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

enviar_correo(datos)
"""
