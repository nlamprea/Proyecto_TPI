import time
import pygame
import pyautogui
import keyboard

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

# Cargar sonidos
sound1 = pygame.mixer.Sound('sounds/sonido_1.wav')
sound2 = pygame.mixer.Sound('sounds/sonido_2.wav')
sound3 = pygame.mixer.Sound('sounds/sonido_3.wav')
sound4 = pygame.mixer.Sound('sounds/sonido_4.wav')
sound5 = pygame.mixer.Sound('sounds/sonido_5.wav')
sound6 = pygame.mixer.Sound('sounds/sonido_6.wav')

# Definir las secciones de la pantalla
section_width = screen_width // 3
section_height = screen_height // 2

# Variable para guardar el sonido activo
current_sound = None

def get_section(x, y):
    if y < section_height:
        if x < section_width:
            return 1
        elif x < 2 * section_width:
            return 2
        else:
            return 3
    else:
        if x < section_width:
            return 4
        elif x < 2 * section_width:
            return 5
        else:
            return 6

def play_sound(section):
    global current_sound

    # Detener el sonido actual si existe
    if current_sound:
        current_sound.stop()

    # Asignar y reproducir el nuevo sonido en bucle
    if section == 1:
        current_sound = sound1
    elif section == 2:
        current_sound = sound2
    elif section == 3:
        current_sound = sound3
    elif section == 4:
        current_sound = sound4
    elif section == 5:
        current_sound = sound5
    elif section == 6:
        current_sound = sound6

    # Reproducir el sonido en bucle (loops=-1 para bucle indefinido)
    current_sound.play(loops=-1)

def take_screenshot(x, y, section_width, section_height):
    left = (x // section_width) * section_width
    top = (y // section_height) * section_height
    width = section_width
    height = section_height
    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    screenshot.save(f'screenshot_{int(time.time())}.png')

running = True
last_section = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Detectar combinación de teclas Ctrl+Shift+S para tomar captura de pantalla
    if keyboard.is_pressed('ctrl+shift+f'):
        x, y = pyautogui.position()
        take_screenshot(x, y, section_width, section_height)
        print("Captura de pantalla tomada.")

    # Detectar la combinación de teclas Ctrl+E para salir del programa
    if keyboard.is_pressed('ctrl+e'):
        print("Programa finalizado por el usuario.")
        running = False

    # Obtener la posición actual del mouse
    x, y = pyautogui.position()
    section = get_section(x, y)

    if section != last_section:
        last_section = section
        play_sound(section)
        print(f"Sección: {section}")

    # Dibujar las secciones en la pantalla
    screen.fill(WHITE)
    pygame.draw.line(screen, BLACK, (section_width, 0), (section_width, screen_height), 5)
    pygame.draw.line(screen, BLACK, (2 * section_width, 0), (2 * section_width, screen_height), 5)
    pygame.draw.line(screen, BLACK, (0, section_height), (screen_width, section_height), 5)

    # Mostrar el número de la sección en el centro de cada sección
    font = pygame.font.Font(None, 74)
    for i in range(1, 7):
        text = font.render(str(i), True, BLACK)
        if i == 1:
            screen.blit(text, (section_width // 2 - text.get_width() // 2, section_height // 2 - text.get_height() // 2))
        elif i == 2:
            screen.blit(text, (3 * section_width // 2 - text.get_width() // 2, section_height // 2 - text.get_height() // 2))
        elif i == 3:
            screen.blit(text, (5 * section_width // 2 - text.get_width() // 2, section_height // 2 - text.get_height() // 2))
        elif i == 4:
            screen.blit(text, (section_width // 2 - text.get_width() // 2, 3 * section_height // 2 - text.get_height() // 2))
        elif i == 5:
            screen.blit(text, (3 * section_width // 2 - text.get_width() // 2, 3 * section_height // 2 - text.get_height() // 2))
        elif i == 6:
            screen.blit(text, (5 * section_width // 2 - text.get_width() // 2, 3 * section_height // 2 - text.get_height() // 2))

    pygame.display.flip()
    time.sleep(0.1)

pygame.quit()
