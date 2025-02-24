# Módulo: `main.py`
# Descripción: Este archivo es el punto de entrada del programa. Contiene la interfaz gráfica principal,
# desde donde los usuarios pueden acceder a los diferentes módulos del sistema, como **Productos**, **Clientes**,
# **Ventas** y **Facturación**. Utiliza la librería `tkinter` para la interfaz gráfica y `Pillow` para manejar imágenes.

import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
from productos import VentanaMainProductos
from clientes import VentanaMainClientes

"""
Para iniciar el programa

Dependencias:

Antes de poder usar la interfaz se necesita instalar Python y Tkinter

##########################################################################################

Instalar Python y Tkinter para Windows:

Descarga e instala la última versión de Python desde python.org.
Durante el proceso de instalación, asegúrate de seleccionar la opción "Install Tcl/Tk".

Con la herramienta pip se instalan las librerías necesarias para el correcto funcionamiento del programa

Link de descarga: https://wkhtmltopdf.org/downloads.html

Asegúrese de tener instalado la última versión de wkhtmltopdf:
    wkhtmltopdf  - -version
    Verifique que la ruta de wkhtmltopdf se haya agregado correctamente al sistema:
    
    - Abre el Panel de Control y ve a Sistema y Seguridad > Sistema > Configuración avanzada del sistema.
    - Haz clic en Variables de entorno.
    - En la sección Variables del sistema, busca la variable Path y selecciónala.
    - Haz clic en Editar.
    - Si no ves la ruta de wkhtmltopdf en la lista, haz clic en Nuevo y agrega la ruta donde instalaste wkhtmltopdf. Por ejemplo, si lo instalaste en C:\Program Files\wkhtmltopdf\bin, agrega esa ruta.
    
    Haz clic en Aceptar para guardar los cambios.

################################################################333

Instalar Python, Tkinter y SQLITE en Linux: 

Tutorial para distribuciones basadas en Debian o Ubuntu:

sudo apt update
sudo apt install python3
sudo apt install python3-pip
sudo apt install python3-tk
sudo apt install sqlite3
sudo apt-get install wkhtmltopdf  

##################################################################################3

Instalar dependencias 


Instalar librerias dependencias

En el repositorio hay un archivo llamado dependencias.txt, abrir una terminal y ejecutar lo siguiente

pip install -r dependencias.txt

Ahora para iniciar el programa:

python3 main.pyw ## OJO CON LA EXTENSIÓN

LINK DEL REPOSITORIO:  https://github.com/sammp2006/POOCerveceria2

"""


def iniciar_programa():
    """
    Inicia la interfaz gráfica principal del programa.

    Comportamiento:
    1. Crea una ventana principal con fondo amarillo claro (`#FFEC99`).
    2. Muestra un mensaje de bienvenida.
    3. Intenta cargar y mostrar el logo de la cervecería desde la ruta `./static/logo.png`.
    4. Si el logo no se puede cargar, muestra un mensaje de error en la consola.
    5. Crea botones para acceder a los módulos de **Productos**, **Clientes**, **Ventas** y **Facturación**.
    6. Muestra una nota informativa sobre cómo registrar ventas y facturar.
    7. Incluye un botón para cerrar la aplicación.
    """
    # Configuración de la ventana principal
    ventana = tk.Tk()
    ventana.title("Programa Principal")
    ventana.geometry("400x400")
    ventana.config(bg="#FFEC99")

    # Mensaje de bienvenida
    bienvenida = tk.Label(ventana, text="Bienvenido a la cerveceria artesanal", font=("Helvetica", 16), bg="#FFEC99", fg="black")
    bienvenida.pack(pady=10)

    # Carga del logo
    try:
        logo_imagen = Image.open("./static/logo.png")
        logo_imagen = logo_imagen.resize((100, 100))
        logo_imagen_tk = ImageTk.PhotoImage(logo_imagen)

        canvas = tk.Canvas(ventana, width=120, height=120, bg="#FFEC99", bd=0, highlightthickness=2)
        canvas.create_rectangle(0, 0, 120, 120, outline="black", width=4)
        canvas.create_image(60, 60, image=logo_imagen_tk)
        canvas.pack(pady=10)
    except Exception as e:
        print(f"Error al cargar el logo: {e}")

    # Función para abrir secciones
    def abrir_seccion(seccion):
        """
        Redirige al módulo correspondiente según la sección seleccionada por el usuario.

        Parámetros:
        - seccion (str): Nombre de la sección a la que se desea acceder. Puede ser:
          - "Productos": Abre el módulo de productos.
          - "Clientes": Abre el módulo de clientes.
          - "Facturacion": Abre el módulo de facturación.
          - "Ventas": Abre el módulo de ventas.

        Comportamiento:
        1. Cierra la ventana actual.
        2. Llama a la función correspondiente para abrir el módulo seleccionado.
        3. Si la sección no es válida, muestra un mensaje de error en la consola.
        """
        ventana.destroy()
        if seccion == "Productos":
            ventana_productos = VentanaMainProductos(iniciar_programa)
            ventana_productos.mainloop()
        elif seccion == "Clientes":
            ventana_clientes = VentanaMainClientes(iniciar_programa)
            ventana_clientes.mainloop()
            # main_clientes(iniciar_programa)
        print(f"Abrir {seccion}")

    # Botones para acceder a los módulos
    boton_productos = tk.Button(ventana, text="Modulo de Productos", command=lambda: abrir_seccion("Productos"), bg="yellow", fg="black", relief="solid", bd=2)
    boton_productos.pack(pady=5, fill="x")

    boton_clientes = tk.Button(ventana, text="Modulo de Clientes (+ Ventas y Facturacion)", command=lambda: abrir_seccion("Clientes"), bg="yellow", fg="black", relief="solid", bd=2)
    boton_clientes.pack(pady=5, fill="x")

    # Nota informativa
    nota_pie_pagina = tk.Label(ventana, text="Para registrar una venta o facturarla \n primero seleccione el cliente en cuestion", relief="solid", bd=2)
    nota_pie_pagina.pack(pady=5, fill="x")

    # Botón para cerrar la aplicación
    boton_cerrar = tk.Button(ventana, text="Cerrar", command=ventana.destroy, bg="red", fg="black", relief="solid", bd=2)
    boton_cerrar.pack(pady=10, fill="x")

    ventana.mainloop()

def run():
    """
    Ejecuta el programa principal llamando a `iniciar_programa()`.

    Comportamiento:
    1. Llama a la función `iniciar_programa()` para iniciar la interfaz gráfica.
    """
    iniciar_programa()

if __name__ == "__main__":
    run()


"""
Nuevos Cambios:
Correcciones parcial anterior y anotaciones adicionales*** IMPLEMENTACIÓN CARRITO DE COMPRAS*** EXPLICACIÓN DETALLADA DE LOS FORMATOS*** MEJORA DOCUMENTACIÓN TÉCNICA 
main.py -> main.pyw ## No visualizar la terminal, solo la interfaz gráfica.Implementación POO para Clientes y Productos. 
Herencia y polimorfismo clase Objeto, tkinter.Tk y Db.Implementación POO para ventanas de Tkinter.Implementación POO para manejo de base de datos.
Mejora impresión factura y envío de correo.
"""