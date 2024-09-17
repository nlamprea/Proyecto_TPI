import pygame
import pyautogui
import keyboard
import time
from functionsScreen import *

def run_program(columns, rows, ruta_base, screenshots_dir, output_dir):
    init_pygame()
    init_sounds(ruta_base)

    screen_width, screen_height = pyautogui.size()
    screen = pygame.display.set_mode((screen_width, screen_height))
    channel = pygame.mixer.Channel(0)

    section_width = screen_width // columns
    section_height = screen_height // rows

    running = True
    last_section = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if keyboard.is_pressed('ctrl+shift+f'):
            x, y = pyautogui.position()
            numS = num_Global(screenshots_dir)
            take_screenshot(x, y, section_width, section_height, screenshots_dir, numS)
            print("Captura de pantalla tomada.")

        if keyboard.is_pressed('ctrl+j'):
            audioScreenshot(screenshots_dir, output_dir)
            print("Output.")

        if keyboard.is_pressed('ctrl+e'):
            print("Programa finalizado por el usuario.")
            running = False

        mouse_x, mouse_y = pygame.mouse.get_pos()
        x, y = pyautogui.position()
        section = get_section(x, y, section_width, section_height, columns)

        if section != last_section:
            last_section = section
            play_sound(section)
            play_sound_based_on_mouse(mouse_x, mouse_y, section - 1, screen_width, screen_height, channel)
            print(f"Sección: {section}")

        draw_grid(screen, columns, rows, section_width, section_height, screen_width, screen_height, (0, 0, 0))
        pygame.display.flip()
        time.sleep(0.1)

    pygame.quit()
