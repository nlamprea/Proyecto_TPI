import time
import pygame
import pyautogui
import keyboard
import cv2
import easyocr
import matplotlib.pyplot as plt
from gtts import gTTS
import os

ruta_base = os.path.dirname(os.path.abspath(__file__))
screenshots_dir = os.path.join(ruta_base, 'screenshot')
output_dir = os.path.join(ruta_base, 'output')

numS = 1

# Inicializar Pygame
pygame.init()

# Obtener las dimensiones de la pantalla
screen_width, screen_height = pyautogui.size()

# Configurar la ventana
screen = pygame.display.set_mode((screen_width, screen_height))

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Inicializar el mezclador de sonido de Pygame
pygame.mixer.init()

# Cargar sonidos (hasta 12 sonidos)
sounds = [pygame.mixer.Sound(f"sounds/sonido_{i+1}.wav") for i in range(12)]

# Usamos un canal de audio para ajustar el balance estéreo
channel = pygame.mixer.Channel(0)

# Definir las opciones de divisiones disponibles
divisions_options = {
    "1x2": (1, 2),
    "2x2": (2, 2),
    "2x3": (2, 3),
    "3x2": (3, 2),
    "3x3": (3, 3),
    "3x4": (3, 4),
    "4x3": (4, 3)
}

# Función para que el usuario elija la división
def choose_division():
    print("Seleccione la división de la pantalla:")
    for option in divisions_options.keys():
        print(f"- {option}")
    choice = input("Ingrese su opción (ej. '3x2'): ")
    return divisions_options.get(choice, (3, 2))  # Por defecto 3x2

# Obtener la opción seleccionada por el usuario
columns, rows = choose_division()

# Calcular las dimensiones de las secciones
section_width = screen_width // columns
section_height = screen_height // rows

def play_sound_based_on_mouse(mouse_x, mouse_y, sound_index):
    x = (mouse_x / screen_width) * 2 - 1  # Izquierda = -1, Derecha = 1
    y = mouse_y / screen_height  # Arriba = cercano, Abajo = lejano

    left_volume = max(0, 1 - x)
    right_volume = max(0, 1 + x)

    distance_factor = max(0.1, 1 - y)

    channel.set_volume(left_volume * distance_factor, right_volume * distance_factor)

    if not channel.get_busy():
        channel.play(sounds[sound_index])

current_sound = None

# Actualizar la función get_section para trabajar con diferentes divisiones
def get_section(x, y):
    col = x // section_width
    row = y // section_height
    return row * columns + col + 1  # Devuelve el número de la sección

def play_sound(section):
    global current_sound

    if current_sound:
        current_sound.stop()

    # Reproducir el sonido correspondiente a la sección (hasta 12 secciones)
    if 1 <= section <= 12:
        current_sound = sounds[section - 1]  # El índice es 0-based
        current_sound.play(loops=-1)

def num_Global():
    global numS
    os.makedirs(screenshots_dir, exist_ok=True)
    
    while os.path.exists(os.path.join(screenshots_dir, f'screenshot_{numS}.png')):
        numS += 1
    
    return numS

def take_screenshot(x, y, section_width, section_height):
    numS = num_Global()
    left = (x // section_width) * section_width
    top = (y // section_height) * section_height
    width = section_width
    height = section_height
    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    screenshot.save(screenshots_dir + f'/screenshot_{numS}.png')

def audioScreenshot():
    num = num_Global() - 1
    os.makedirs(screenshots_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    archivo_screenshot = os.path.join(screenshots_dir, f'screenshot_{num}.png')

    if os.path.exists(archivo_screenshot):
        res_list = []
        reader = easyocr.Reader(["es"], gpu=False)
        image = cv2.imread(archivo_screenshot)
        result = reader.readtext(image, paragraph=False)

        for res in result:
            res_list.append(res[1])

        words_string = " ".join(res_list)
        language = 'es'
        speech = gTTS(text=words_string, lang=language, slow=False)

        output_file = output_dir + "output.mp3"
        if os.path.exists(output_file):
            os.remove(output_file)
        
        speech.save(output_file)
        os.system(f"start {output_file}")

running = True
last_section = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if keyboard.is_pressed('ctrl+shift+f'):
        x, y = pyautogui.position()
        take_screenshot(x, y, section_width, section_height)
        print("Captura de pantalla tomada.")

    if keyboard.is_pressed('ctrl+j'):
        audioScreenshot()
        print("Output.")

    if keyboard.is_pressed('ctrl+e'):
        print("Programa finalizado por el usuario.")
        running = False

    mouse_x, mouse_y = pygame.mouse.get_pos()
    x, y = pyautogui.position()
    section = get_section(x, y)

    if section != last_section:
        last_section = section
        play_sound(section)
        play_sound_based_on_mouse(mouse_x, mouse_y, section - 1)  # El índice es 0-based
        print(f"Sección: {section}")

    screen.fill(WHITE)

    # Dibujar líneas de separación
    for i in range(1, columns):
        pygame.draw.line(screen, BLACK, (i * section_width, 0), (i * section_width, screen_height), 5)
    for j in range(1, rows):
        pygame.draw.line(screen, BLACK, (0, j * section_height), (screen_width, j * section_height), 5)

    pygame.display.flip()
    time.sleep(0.1)

pygame.quit()
