import os
import pyautogui
import pygame
import cv2
import easyocr
from gtts import gTTS

# Inicializar Pygame
pygame.init()

# Rutas de carpetas
ruta_base = os.path.dirname(os.path.abspath(__file__))
screenshots_dir = os.path.join(ruta_base, 'screenshot')
output_dir = os.path.join(ruta_base, 'output')

# Inicializar mezclador de sonido de Pygame
pygame.mixer.init()

# Cargar sonidos
sound1 = pygame.mixer.Sound(ruta_base+'/sounds/sonido_1.wav')
sound2 = pygame.mixer.Sound(ruta_base+'/sounds/sonido_2.wav')
sound3 = pygame.mixer.Sound(ruta_base+'/sounds/sonido_3.wav')
sound4 = pygame.mixer.Sound(ruta_base+'/sounds/sonido_4.wav')
sound5 = pygame.mixer.Sound(ruta_base+'/sounds/sonido_5.wav')
sound6 = pygame.mixer.Sound(ruta_base+'/sounds/sonido_6.wav')

channel = pygame.mixer.Channel(0)
current_sound = None

# Obtener el número global de captura de pantalla
def num_Global():
    numS = 1
    os.makedirs(screenshots_dir, exist_ok=True)
    
    while os.path.exists(os.path.join(screenshots_dir, f'screenshot_{numS}.png')):
        numS += 1
    
    return numS

# Capturar una sección de pantalla
def take_screenshot(x, y, section_width, section_height):
    numS = num_Global()
    left = (x // section_width) * section_width
    top = (y // section_height) * section_height
    screenshot = pyautogui.screenshot(region=(left, top, section_width, section_height))
    screenshot.save(os.path.join(screenshots_dir, f'screenshot_{numS}.png'))

# Generar audio desde la captura de pantalla
def audioScreenshot():
    num = num_Global() - 1
    archivo_screenshot = os.path.join(screenshots_dir, f'screenshot_{num}.png')
    
    if os.path.exists(archivo_screenshot):
        res_list = []
        reader = easyocr.Reader(["es"], gpu=False)
        image = cv2.imread(archivo_screenshot)
        result = reader.readtext(image, paragraph=False)

        for res in result:
            res_list.append(res[1])

        words_string = " ".join(res_list)
        speech = gTTS(text=words_string, lang='es', slow=False)

        output_file = os.path.join(output_dir, "output.mp3")
        if os.path.exists(output_file):
            os.remove(output_file)
        speech.save(output_file)
        os.system(f"start {output_file}")

# Reproducir sonido basado en la posición del mouse
def play_sound_based_on_mouse(mouse_x, mouse_y, soundSection, screen_width, screen_height):
    x = (mouse_x / screen_width) * 2 - 1
    y = mouse_y / screen_height
    left_volume = max(0, 1 - x)
    right_volume = max(0, 1 + x)
    distance_factor = max(0.1, 1 - y)

    channel.set_volume(left_volume * distance_factor, right_volume * distance_factor)
    if not channel.get_busy():
        channel.play(globals()[f'sound{soundSection}'])

# Reproducir sonido según la sección
def play_sound(section):
    global current_sound
    if current_sound:
        current_sound.stop()

    current_sound = globals()[f'sound{section}']
    current_sound.play(loops=-1)
