import os
from programExecutionScreen import run_program
from mainMinas import mainmines

# Función para que el usuario elija la división
def choose_division():
    divisions_options = {
        "1x2": (1, 2),
        "2x1": (2, 1),
        "2x2": (2, 2),
        "2x3": (2, 3),
        "3x2": (3, 2),
        "3x3": (3, 3),
        "3x4": (3, 4),
        "4x3": (4, 3)
    }

    print("Seleccione la división de la pantalla:")
    for option in divisions_options.keys():
        print(f"- {option}")
    choice = input("Ingrese su opción (ej. '3x2'): ")

    return divisions_options.get(choice, (3, 2))  # Por defecto 3x2

def mainScreen():
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    screenshots_dir = os.path.join(ruta_base, 'screenshot')
    output_dir = os.path.join(ruta_base, 'output')

    # Obtener la opción seleccionada por el usuario
    columns, rows = choose_division()

    # Ejecutar el programa principal
    run_program(columns, rows, ruta_base, screenshots_dir, output_dir)


def mainMina():
    mainmines()
