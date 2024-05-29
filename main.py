import tkinter as tk

# Función para obtener la sección según la posición del ratón
def obtener_seccion(x, y, width, height):
    if x < width // 3:
        if y < height // 2:
            return 1  # Sección superior izquierda
        else:
            return 4  # Sección inferior izquierda
    elif x < 2 * width // 3:
        if y < height // 2:
            return 2  # Sección superior central
        else:
            return 5  # Sección inferior central
    else:
        if y < height // 2:
            return 3  # Sección superior derecha
        else:
            return 6  # Sección inferior derecha

# Función para manejar el movimiento del ratón
def mover_ratón(event):
    seccion = obtener_seccion(event.x, event.y, ventana.winfo_width(), ventana.winfo_height())
    etiqueta.config(text=f"Sección: {seccion}")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("División en Secciones")

# Obtener el tamaño de la pantalla
screen_width = ventana.winfo_screenwidth()
screen_height = ventana.winfo_screenheight()

# Configurar la ventana para ocupar toda la pantalla
ventana.geometry(f"{screen_width}x{screen_height}")

# Etiqueta para mostrar la sección
etiqueta = tk.Label(ventana, text="Mueve el ratón", font=("Helvetica", 32))
etiqueta.pack(pady=20)

# Vincular el evento de movimiento del ratón a la función
ventana.bind('<Motion>', mover_ratón)

# Iniciar el bucle principal de la aplicación
ventana.mainloop()
