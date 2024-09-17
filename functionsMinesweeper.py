import os
import pygame
import random
import pyttsx3

# Inicialización de variables globales
engine = pyttsx3.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(9)

channels = [pygame.mixer.Channel(i) for i in range(9)]  # Asignar un canal para cada sonido

# Función para cargar los sonidos
def cargar_sonidos(ruta_base):
    sounds = [
        pygame.mixer.Sound(ruta_base + '/sounds/sonido_1.wav'),
        pygame.mixer.Sound(ruta_base + '/sounds/sonido_2.wav'),
        pygame.mixer.Sound(ruta_base + '/sounds/sonido_3.wav'),
        pygame.mixer.Sound(ruta_base + '/sounds/sonido_4.wav'),
        pygame.mixer.Sound(ruta_base + '/sounds/sonido_5.wav'),
        pygame.mixer.Sound(ruta_base + '/sounds/sonido_6.wav'),
        pygame.mixer.Sound(ruta_base + '/sounds/sonido_7.wav'),
        pygame.mixer.Sound(ruta_base + '/sounds/sonido_8.wav'),
        pygame.mixer.Sound(ruta_base + '/sounds/sonido_9.wav')
    ]
    explosion_sound = pygame.mixer.Sound(ruta_base + '/sounds/explosion.wav')
    return sounds, explosion_sound

# Función para calcular las minas alrededor
def calcular_minas_alrededor(mines, ROWS, COLS):
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for r in range(ROWS):
        for c in range(COLS):
            if mines[r][c] == -1:
                continue
            count = 0
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS and mines[nr][nc] == -1:
                    count += 1
            mines[r][c] = count

# Función para hablar las minas alrededor
def hablar_minas_alrededor(row, col, mines):
    if mines[row][col] != -1:
        num_mines = mines[row][col]
        engine.say(f"Hay {num_mines} minas alrededor")
        engine.runAndWait()

# Función de fin de juego
def fin_del_juego(explosion_sound):
    explosion_sound.play()
    engine.say("Has explotado una mina. Fin del juego.")
    engine.runAndWait()
    explosion_sound.stop()
    pygame.quit()
    exit()


# Asignar sonidos a la grilla
def asignar_sonidos_a_grilla(center_row, center_col, sound_grid, ROWS, COLS):
    sound_order = [2, 3, 4, 5, 1, 6, 7, 8, 9]
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
    for r in range(ROWS):
        for c in range(COLS):
            sound_grid[r][c] = None
    for idx, (dr, dc) in enumerate(directions):
        new_row = center_row + dr
        new_col = center_col + dc
        if 0 <= new_row < ROWS and 0 <= new_col < COLS:
            sound_grid[new_row][new_col] = sound_order[idx]

# Función para dibujar la grilla
def dibujar_grilla(screen, ROWS, COLS, CELL_SIZE, revealed, mines, GRAY, DARK_GRAY, RED, BLACK):
    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if revealed[r][c]:
                pygame.draw.rect(screen, GRAY, rect)
                if mines[r][c] == -1:
                    pygame.draw.circle(screen, RED, rect.center, CELL_SIZE // 4)
            else:
                pygame.draw.rect(screen, DARK_GRAY, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)

# Función para reproducir sonido según el mouse
def reproducir_sonido(mouse_x, mouse_y, sound_index, WIDTH, HEIGHT, channels, sounds):
    x = (mouse_x / WIDTH) * 2 - 1
    y = mouse_y / HEIGHT
    left_volume = max(0, 1 - x)
    right_volume = max(0, 1 + x)
    distance_factor = max(0.2, 1 - y)
    channels[sound_index].set_volume(left_volume * distance_factor, right_volume * distance_factor)
    if not channels[sound_index].get_busy():
        channels[sound_index].play(sounds[sound_index])


def is_mouse_inside_window(mouse_x, mouse_y, WIDTH, HEIGHT):
    if (1 <= mouse_x < WIDTH - 1 and 1 <= mouse_y < HEIGHT - 1):
        return True
    else:
        return False  
    
def play_sound_based_on_mouse1(mouse_x, mouse_y, sound, WIDTH, HEIGHT, channel1):
    # Normalizar la posición x del mouse a un rango de [-1, 1]
    x = (mouse_x / WIDTH) * 2 - 1  # Izquierda = -1, Derecha = 1
    # Normalizar la posición y del mouse a un rango de [0, 1] (para simular distancia)
    y = mouse_y / HEIGHT  # Arriba = cercano, Abajo = lejano

    # Controlar el balance estéreo en función de la posición en el eje X
    left_volume = max(0, 1 - x)
    right_volume = max(0, 1 + x)

    # Reducir volumen en función de la distancia (simulación simple en Y)
    distance_factor = max(0.1, 1 - y)

    # Ajustar el volumen para el balance estéreo
    channel1.set_volume(left_volume * distance_factor, right_volume * distance_factor)

    # Reproducir el sonido en el canal
    if not channel1.get_busy():
        channel1.play(sound)

def get_cell_under_mouse(CELL_SIZE):
    x, y = pygame.mouse.get_pos()
    row = y // CELL_SIZE
    col = x // CELL_SIZE
    return row, col


def assign_sounds_to_grid(center_row, center_col, ROWS, COLS, sound_grid):
    global current_center
    # Lista de sonidos en el orden especificado
    sound_order = [2, 3, 4, 5, 1, 6, 7, 8, 9]

    # Direcciones relativas a la celda central
    directions = [(-1, -1), (-1, 0), (-1, 1),  # Filas superiores
                  (0, -1),  (0, 0),  (0, 1),  # Fila del medio
                  (1, -1),  (1, 0),  (1, 1)]  # Filas inferiores

    # Limpiar la grilla de sonidos
    for r in range(ROWS):
        for c in range(COLS):
            sound_grid[r][c] = None

    # Asignar sonidos a las celdas alrededor del centro
    for idx, (dr, dc) in enumerate(directions):
        new_row = center_row + dr
        new_col = center_col + dc
        if 0 <= new_row < ROWS and 0 <= new_col < COLS:
            sound_grid[new_row][new_col] = sound_order[idx]
    # Actualizar la celda central
    current_center = (center_row, center_col)


def handle_click(pos, CELL_SIZE,revealed):
    global first_click

    x, y = pos
    row = y // CELL_SIZE
    col = x // CELL_SIZE
    ROWS, COLS = 9, 9
    sound_grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
    # Si es el primer clic, configurar los sonidos en torno a la grilla seleccionada
    if not first_click:
        assign_sounds_to_grid(row, col,ROWS, COLS, sound_grid)
        revealed[row][col] = True  # Revelar la celda central
        first_click = True
    else:
        # Si no es el primer clic, verificar si se hace clic en una celda circundante
        if sound_grid[row][col] is not None and (row, col) != current_center:
            # Establecer la nueva celda como central
            revealed[row][col] = True  # Revelar la nueva celda central
            assign_sounds_to_grid(row, col, ROWS, COLS, sound_grid)  # Redistribuir los sonidos

