# main.py
import time
import pygame
import pyautogui
import keyboard
from archivo2 import take_screenshot, audioScreenshot, play_sound, play_sound_based_on_mouse

# Inicializar Pygame
pygame.init()

# Obtener dimensiones de pantalla
screen_width, screen_height = pyautogui.size()

# Configurar ventana
screen = pygame.display.set_mode((screen_width, screen_height))

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Definir secciones
section_width = screen_width // 3
section_height = screen_height // 2

# Obtener la sección en la que se encuentra el mouse
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

# Función principal que contiene el bucle del programa
def main(running):
    #running = True
    last_section = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Detectar combinación de teclas para captura de pantalla
        if keyboard.is_pressed('ctrl+shift+f'):
            x, y = pyautogui.position()
            take_screenshot(x, y, section_width, section_height)
            print("Captura de pantalla tomada.")
            
        # Detectar combinación para generar audio de la captura
        if keyboard.is_pressed('ctrl+j'):
            audioScreenshot()
            print("Output generado.")

        # Detectar combinación para salir
        if keyboard.is_pressed('ctrl+e'):
            print("Programa finalizado por el usuario.")
            running = False

        # Obtener posición actual del mouse
        x, y = pyautogui.position()
        section = get_section(x, y)

        if section != last_section:
            last_section = section
            play_sound(section)
            mouse_x, mouse_y = pygame.mouse.get_pos()
            play_sound_based_on_mouse(mouse_x, mouse_y, section, screen_width, screen_height)
            print(f"Sección: {section}")

        # Dibujar divisiones en la pantalla
        screen.fill(WHITE)
        pygame.draw.line(screen, BLACK, (section_width, 0), (section_width, screen_height), 5)
        pygame.draw.line(screen, BLACK, (2 * section_width, 0), (2 * section_width, screen_height), 5)
        pygame.draw.line(screen, BLACK, (0, section_height), (screen_width, section_height), 5)

        # Mostrar números de sección
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

# Esto permite que el archivo sea ejecutable directamente o importado
# if __name__ == "__main__":
#     main()
