import pygame
import random
import pyautogui

# Inicializar Pygame
pygame.init()

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

# Cargar sonidos (ahora tenemos 9 sonidos diferentes)
pygame.mixer.init()
sounds = [pygame.mixer.Sound(f'sounds/soundsB/sonido_{i+1}.wav') for i in range(9)]  # Asegúrate de tener 9 sonidos generados

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

# Reproducir sonido dependiendo de la celda
def play_sound_for_cell(row, col):
    # Detener todos los sonidos antes de reproducir el nuevo
    pygame.mixer.stop()
    
    if mines[row][col] == -1:
        sound = sounds[8]  # Sonido especial para la mina (sonido 9)
    else:
        sound = sounds[mines[row][col]]  # Sonido correspondiente al número de minas alrededor
    sound.play()

# Función para obtener la celda debajo del cursor
def get_cell_under_mouse():
    x, y = pygame.mouse.get_pos()
    row = y // CELL_SIZE
    col = x // CELL_SIZE
    return row, col

# Main loop
running = True
last_cell = (-1, -1)  # Para evitar repetir el sonido al quedarse en la misma celda
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

    # Obtener la celda actual bajo el cursor
    row, col = get_cell_under_mouse()
    
    # Solo reproducir sonido si el mouse está en una nueva celda
    if (row, col) != last_cell and 0 <= row < ROWS and 0 <= col < COLS:
        play_sound_for_cell(row, col)
        last_cell = (row, col)  # Actualizar la última celda visitada

    pygame.display.flip()

pygame.quit()
