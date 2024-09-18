import tkinter as tk
import ScreenMain

def main():
    # Configurar la ventana
    def cerrar_aplicacion():
        ventana.destroy()
    
    ventana = tk.Tk()
    ventana.title("Menú Principal")
    ventana.configure(bg="#ffffff")

    # Obtener el tamaño del monitor
    ancho_monitor = ventana.winfo_screenwidth()
    alto_monitor = ventana.winfo_screenheight()

    # Ajustar la ventana al 50% del tamaño del monitor y centrarla
    ancho_ventana = int(ancho_monitor * 0.5)
    alto_ventana = int(alto_monitor * 0.5)
    pos_x = (ancho_monitor // 2) - (ancho_ventana // 2)
    pos_y = (alto_monitor // 2) - (alto_ventana // 2)
    ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{pos_x}+{pos_y}")

    # Crear un marco para centrar los botones
    marco = tk.Frame(ventana, bg="#ffffff")
    marco.place(relx=0.5, rely=0.5, anchor="center")

    # Tamaño de los botones
    boton_tamaño = 5  # Tamaño del botón en unidades (no en píxeles)

    # Crear los botones en una disposición 2x4
    boton1 = tk.Button(marco, text="1x2", command=lambda: ScreenMain.mainScreen(1, 2), width=boton_tamaño, height=boton_tamaño)
    boton1.grid(row=0, column=0, padx=20, pady=20)

    boton2 = tk.Button(marco, text="2x1", command=lambda: ScreenMain.mainScreen(2, 1), width=boton_tamaño, height=boton_tamaño)
    boton2.grid(row=0, column=1, padx=20, pady=20)

    boton3 = tk.Button(marco, text="2x2", command=lambda: ScreenMain.mainScreen(2, 2), width=boton_tamaño, height=boton_tamaño)
    boton3.grid(row=0, column=2, padx=20, pady=20)

    boton4 = tk.Button(marco, text="2x3", command=lambda: ScreenMain.mainScreen(2, 3), width=boton_tamaño, height=boton_tamaño)
    boton4.grid(row=0, column=3, padx=20, pady=20)

    boton5 = tk.Button(marco, text="3x2", command=lambda: ScreenMain.mainScreen(3, 2), width=boton_tamaño, height=boton_tamaño)
    boton5.grid(row=1, column=0, padx=20, pady=20)

    boton6 = tk.Button(marco, text="3x3", command=lambda: ScreenMain.mainScreen(3, 3), width=boton_tamaño, height=boton_tamaño)
    boton6.grid(row=1, column=1, padx=20, pady=20)

    boton7 = tk.Button(marco, text="3x4", command=lambda: ScreenMain.mainScreen(3, 4), width=boton_tamaño, height=boton_tamaño)
    boton7.grid(row=1, column=2, padx=20, pady=20)

    boton8 = tk.Button(marco, text="4x3", command=lambda: ScreenMain.mainScreen(4, 3), width=boton_tamaño, height=boton_tamaño)
    boton8.grid(row=1, column=3, padx=20, pady=20)

    boton_salir = tk.Button(ventana, text="Salir", command=cerrar_aplicacion, bg="#ff1a1a", fg="white", font=("Arial", 14, "bold"), relief="raised", bd=4, width=20, height=2)
    boton_salir.pack(pady=20)

    # Iniciar el bucle de la ventana
    ventana.mainloop()
