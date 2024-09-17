import tkinter as tk
from tkinter import PhotoImage

import os

import screenMain
import a

# Función para ejecutar un archivo .py
def ejecutar_archivo(nombre_archivo):
    os.system(f'python {nombre_archivo}')

# Función para cerrar la aplicación
def cerrar_aplicacion():
    ventana.destroy()

# Configurar la ventana
ventana = tk.Tk()
ventana.title("Menú Principal")
ventana.configure(bg="#ffffff")  # Color de fondo oscuro

# Obtener el tamaño del monitor
ancho_monitor = ventana.winfo_screenwidth()
alto_monitor = ventana.winfo_screenheight()

# Ajustar la ventana al 50% del tamaño del monitor y centrarla
ancho_ventana = int(ancho_monitor * 0.5)
alto_ventana = int(alto_monitor * 0.5)
pos_x = (ancho_monitor // 2) - (ancho_ventana // 2)
pos_y = (alto_monitor // 2) - (alto_ventana // 2)
ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{pos_x}+{pos_y}")

# Añadir un logo
# Reemplaza "logo.png" por la ruta de tu imagen
try:
    logo = PhotoImage(file="img/logo.png")
    # Escalar el logo a un tamaño más pequeño
    logo = logo.subsample(3, 3)  # Ajusta estos valores según sea necesario
    logo_label = tk.Label(ventana, image=logo, bg="#ffffff")
    logo_label.pack(pady=10)
except:
    logo_label = tk.Label(ventana, text="Logo", bg="#2c2c2c", fg="white", font=("Arial", 20))
    logo_label.pack(pady=10)

# Crear un frame para los botones, esto permite organizar mejor el espacio
frame_botones = tk.Frame(ventana, bg="#2c2c2c")
frame_botones.pack(pady=20)

# Estilo de los botones
estilo_boton = {
    "bg": "#1a1a1a",  # Fondo del botón
    "fg": "white",    # Texto en blanco
    "font": ("Arial", 14, "bold"),  # Fuente más grande
    "relief": "raised",  # Borde elevado para que el botón sea más visible
    "bd": 4,  # Grosor del borde
    "width": 20,  # Ancho del botón
    "height": 2  # Altura del botón
}

# Botones
boton1 = tk.Button(ventana, text="Pantalla dividida", command=lambda: a.main(), **estilo_boton)
boton1.pack(pady=10)

boton2 = tk.Button(ventana, text="Busca minas", command=lambda: screenMain.mainMina(), **estilo_boton)
boton2.pack(pady=10)

# Botón para salir
boton_salir = tk.Button(ventana, text="Salir", command=cerrar_aplicacion, bg="#ff1a1a", fg="white", font=("Arial", 14, "bold"), relief="raised", bd=4, width=20, height=2)
boton_salir.pack(pady=20)

# Ejecutar el bucle principal de tkinter
ventana.mainloop()
