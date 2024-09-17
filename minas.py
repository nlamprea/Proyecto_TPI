import pygame
import random
import pyautogui
import pyttsx3

# Inicializar Pygame y pyttsx3
pygame.init()
engine = pyttsx3.init()

# Definir dimensiones de la cuadrícula
ROWS, COLS = 9, 9
CELL_SIZE = 90
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE

# Inicializar la ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Busca Minas")

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
DARK_GRAY = (160, 160, 160)
RED = (255, 0, 0)

# Cargar sonidos
pygame.mixer.init()
sounds = [pygame.mixer.Sound(f'sounds/soundsB/sonido_{i+1}.wav') for i in range(9)]  # Sonidos de 1 a 9
explosion_sound = pygame.mixer.Sound('sounds/soundsB/explosion.wav')

# Inicializar canales de sonido
channel = pygame.mixer.Channel(0)


# Estados iniciales
revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
sound_grid = [[None for _ in range(COLS)] for _ in range(ROWS)]  # Grilla que contiene los índices de sonido
first_click = False  # Para determinar si ya se hizo el primer clic

# Crear una matriz de minas y números
mines = [[0 for _ in range(COLS)] for _ in range(ROWS)]
revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]

# Colocar minas aleatoriamente
NUM_MINES = 10
mines_pos = random.sample([(r, c) for r in range(ROWS) for c in range(COLS)], NUM_MINES)

for r, c in mines_pos:
    mines[r][c] = -1  # -1 representa una mina


# Función para asignar sonidos a la grilla alrededor de la central
def assign_sounds_to_grid(center_row, center_col):
    # Lista de sonidos en el orden especificado
    sound_order = [2, 3, 4, 5, 1, 6, 7, 8, 9]

    directions = [(-1, -1), (-1, 0), (-1, 1),  # Filas superiores
                  (0, -1),  (0, 0),  (0, 1),  # Fila del medio
                  (1, -1),  (1, 0),  (1, 1)]  # Filas inferiores

    # Asignar sonidos a las celdas alrededor del centro
    for idx, (dr, dc) in enumerate(directions):
        new_row = center_row + dr
        new_col = center_col + dc
        if 0 <= new_row < ROWS and 0 <= new_col < COLS:
            sound_grid[new_row][new_col] = sound_order[idx]


# Calcular los números que indican cuántas minas hay alrededor de cada celda
def calculate_mines_around():
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

calculate_mines_around()

# Dibujar la cuadrícula
def draw_grid():
    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if revealed[r][c]:
                pygame.draw.rect(screen, GRAY, rect)
                if mines[r][c] == -1:
                    pygame.draw.circle(screen, RED, rect.center, CELL_SIZE // 4)
                elif mines[r][c] > 0:
                    font = pygame.font.SysFont(None, 36)
                    text = font.render(str(mines[r][c]), True, BLACK)
                    screen.blit(text, (c * CELL_SIZE + 20, r * CELL_SIZE + 15))
            else:
                pygame.draw.rect(screen, DARK_GRAY, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)


# Reproducir sonido espacial basado en la posición del mouse
def play_sound_based_on_mouse(mouse_x, mouse_y, sound):
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
    channel.set_volume(left_volume * distance_factor, right_volume * distance_factor)

    # Reproducir el sonido en el canal
    if not channel.get_busy():
        channel.play(sound)

# Decir cuántas minas hay alrededor de la celda
def speak_mines_around(row, col):
    if mines[row][col] != -1:
        num_mines = mines[row][col]
        engine.say(f"Hay {num_mines} minas alrededor")
        engine.runAndWait()

# Función para obtener la celda debajo del cursor
def get_cell_under_mouse():
    x, y = pygame.mouse.get_pos()
    row = y // CELL_SIZE
    col = x // CELL_SIZE
    return row, col

# Terminar el juego cuando explote una mina
def game_over():
    explosion_sound.play()
    engine.say("Has explotado una mina. Fin del juego.")
    engine.runAndWait()
    explosion_sound.stop()
    pygame.quit()
    exit()

# Función para verificar si el mouse está dentro de la ventana
def is_mouse_inside_window(mouse_x, mouse_y):
    if (1 <= mouse_x < WIDTH - 1 and 1 <= mouse_y < HEIGHT - 1):
        return True
    else:
        return False


# Función para manejar clics en la grilla
def handle_click(pos):
    global first_click

    x, y = pos
    row = y // CELL_SIZE
    col = x // CELL_SIZE

    # Si es el primer clic, configurar los sonidos en torno a la grilla seleccionada
    if not first_click:
        assign_sounds_to_grid(row, col)
        first_click = True

    # Si la celda tiene un sonido asignado y no ha sido revelada
    if sound_grid[row][col] is not None and not revealed[row][col]:
        revealed[row][col] = True
        sound_index = sound_grid[row][col] - 1  # Ajuste para índice de lista de sonidos
        sounds[sound_index].play()

# Main loop
running = True
last_cell = (-1, -1)  # Para evitar repetir el sonido al quedarse en la misma celda
mouse_inside_window = True  # Variable para verificar si el mouse estaba dentro de la ventana
while running:
    screen.fill(WHITE)
    draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            row, col = get_cell_under_mouse()
            if not revealed[row][col]:
                revealed[row][col] = True
                if mines[row][col] == -1:
                    game_over()
                else:
                    speak_mines_around(row, col)

    # Obtener la posición del mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Verificar si el mouse está dentro de la ventana
    if is_mouse_inside_window(mouse_x, mouse_y):
        if not mouse_inside_window:  # Si el mouse acaba de volver a la ventana
            mouse_inside_window = True  # Actualizamos el estado del mouse
        # Obtener la celda actual bajo el cursor
        row, col = get_cell_under_mouse()
        
        # Solo reproducir sonido si el mouse está en una nueva celda

        play_sound_based_on_mouse(mouse_x, mouse_y, sounds[mines[row][col]])
        last_cell = (row, col)  # Actualizar la última celda visitada
    else:
        if mouse_inside_window:  # Si el mouse acaba de salir de la ventana
            channel.stop()  # Detenemos el sonido
            mouse_inside_window = False  # Actualizamos el estado del mouse

    pygame.display.flip()

pygame.quit()
