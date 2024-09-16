import pygame
import random
import pyautogui
import pyttsx3

# Inicializar Pygame y pyttsx3
pygame.init()
engine = pyttsx3.init()

# Definir dimensiones de la cuadrícula
ROWS, COLS = 9, 9
CELL_SIZE = 60
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE

# Inicializar la ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Busca Minas Sonoro")

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
DARK_GRAY = (160, 160, 160)
RED = (255, 0, 0)

# Cargar sonidos
pygame.mixer.init()
sound0 = pygame.mixer.Sound('sounds/soundsB/sonido_0.wav')  # Sonido inicial espacial
sounds = [pygame.mixer.Sound(f'sounds/soundsB/sonido_{i+1}.wav') for i in range(9)]  # Sonidos de 1 a 9

# Inicializar canales de sonido
channel = pygame.mixer.Channel(0)

# Crear una matriz de minas y números
mines = [[0 for _ in range(COLS)] for _ in range(ROWS)]
revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]

# Colocar minas aleatoriamente
NUM_MINES = 10
mines_pos = random.sample([(r, c) for r in range(ROWS) for c in range(COLS)], NUM_MINES)

for r, c in mines_pos:
    mines[r][c] = -1  # -1 representa una mina

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

# Detener el sonido `sound0` y comenzar con los sonidos de la matriz
def stop_initial_sound():
    sound0.stop()

# Reproducir sonido espacial basado en la casilla presionada y los sonidos alrededor
def play_spatial_sounds(row, col):
    # Matriz de sonidos alrededor
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
    for i, (dr, dc) in enumerate(directions):
        nr, nc = row + dr, col + dc
        if 0 <= nr < ROWS and 0 <= nc < COLS:
            sound = sounds[i]  # Asignar sonido correspondiente de la matriz
            play_sound_based_on_mouse(nc * CELL_SIZE, nr * CELL_SIZE, sound)

# Función para obtener la celda debajo del cursor
def get_cell_under_mouse():
    x, y = pygame.mouse.get_pos()
    row = y // CELL_SIZE
    col = x // CELL_SIZE
    return row, col

# Main loop
running = True
last_cell = (-1, -1)  # Para evitar repetir el sonido al quedarse en la misma celda
initial_sound_playing = True  # Para controlar el sonido inicial
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
                if initial_sound_playing:
                    stop_initial_sound()  # Detener sonido inicial
                    initial_sound_playing = False
                play_spatial_sounds(row, col)

    # Obtener la celda actual bajo el cursor
    row, col = get_cell_under_mouse()
    
    # Solo reproducir sonido si el mouse está en una nueva celda
    if (row, col) != last_cell and 0 <= row < ROWS and 0 <= col < COLS:
        last_cell = (row, col)  # Actualizar la última celda visitada

    pygame.display.flip()

pygame.quit()
