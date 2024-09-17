import os
import pygame
import pyautogui
import easyocr
import cv2
from gtts import gTTS

# Definir sonidos
sounds = []
current_sound = None
# Inicializar el sistema de sonido
def init_sounds(ruta_base):
    global sounds
    sounds = [
        pygame.mixer.Sound(ruta_base + '/sounds/sonido_1.wav'),
        pygame.mixer.Sound(ruta_base + '/sounds/sonido_2.wav'),
        pygame.mixer.Sound(ruta_base + '/sounds/sonido_3.wav'),
        pygame.mixer.Sound(ruta_base + '/sounds/sonido_4.wav'),
        pygame.mixer.Sound(ruta_base + '/sounds/sonido_5.wav'),
        pygame.mixer.Sound(ruta_base + '/sounds/sonido_6.wav'),
        pygame.mixer.Sound(ruta_base + '/sounds/sonido_7.wav'),
        pygame.mixer.Sound(ruta_base + '/sounds/sonido_8.wav'),
        pygame.mixer.Sound(ruta_base + '/sounds/sonido_9.wav'),
        pygame.mixer.Sound(ruta_base + '/sounds/sonido_10.wav'),
        pygame.mixer.Sound(ruta_base + '/sounds/sonido_11.wav'),
        pygame.mixer.Sound(ruta_base + '/sounds/sonido_12.wav')
    ]

# Inicializar la mezcla de sonido de pygame
def init_pygame():
    pygame.init()
    pygame.mixer.init()

# Reproducir sonido basado en la posición del mouse
def play_sound_based_on_mouse(mouse_x, mouse_y, sound_index, screen_width, screen_height, channel):
    x = (mouse_x / screen_width) * 2 - 1  # Izquierda = -1, Derecha = 1
    y = mouse_y / screen_height  # Arriba = cercano, Abajo = lejano

    left_volume = max(0, 1 - x)
    right_volume = max(0, 1 + x)

    distance_factory = max(0.1, 1 - y)
    distance_factorx = max(0.1, 1 + y)

    channel.set_volume(left_volume * distance_factory, right_volume * distance_factorx)

    if not channel.get_busy():
        channel.play(sounds[sound_index])

# Determinar en qué sección está el mouse
def get_section(x, y, section_width, section_height, columns):
    col = x // section_width
    row = y // section_height
    return row * columns + col + 1  # Devuelve el número de la sección

# Reproducir sonido por sección
def play_sound(section):
    global current_sound
    if current_sound:
        current_sound.stop()

    if 1 <= section <= 12:
        current_sound = sounds[section - 1]  # El índice es 0-based
        current_sound.play(loops=-1)

# Tomar captura de pantalla
def take_screenshot(x, y, section_width, section_height, screenshots_dir, numS):
    left = (x // section_width) * section_width
    top = (y // section_height) * section_height
    width = section_width
    height = section_height
    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    screenshot.save(screenshots_dir + f'/screenshot_{numS}.png')

# Generar el número de captura de pantalla
def num_Global(screenshots_dir):
    numS = 1
    os.makedirs(screenshots_dir, exist_ok=True)
    while os.path.exists(os.path.join(screenshots_dir, f'screenshot_{numS}.png')):
        numS += 1
    return numS

# Función para extraer texto de la captura y reproducirlo como audio
def audioScreenshot(screenshots_dir, output_dir):
    numS = num_Global(screenshots_dir) - 1
    archivo_screenshot = os.path.join(screenshots_dir, f'screenshot_{numS}.png')

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

        output_file = os.path.join(output_dir, "output.mp3")
        if os.path.exists(output_file):
            os.remove(output_file)

        speech.save(output_file)
        os.system(f"start {output_file}")

# Dibujar líneas de las secciones
def draw_grid(screen, columns, rows, section_width, section_height, screen_width, screen_height, BLACK):
    screen.fill((255, 255, 255))  # Fondo blanco
    for i in range(1, columns):
        pygame.draw.line(screen, BLACK, (i * section_width, 0), (i * section_width, screen_height), 5)
    for j in range(1, rows):
        pygame.draw.line(screen, BLACK, (0, j * section_height), (screen_width, j * section_height), 5)
