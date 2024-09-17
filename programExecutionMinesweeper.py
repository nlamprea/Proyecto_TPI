from functionsMinesweeper import *
import pygame
import random
import os

def main():
    # Inicializar pygame y cargar sonidos
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    pygame.init()
    screen = pygame.display.set_mode((450, 450))
    pygame.display.set_caption("Grilla de Sonidos Espaciales")

    # Variables del juego
    ROWS, COLS, CELL_SIZE = 9, 9, 50
    WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE
    revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
    sound_grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
    mines = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    first_click = False

    sounds, explosion_sound = cargar_sonidos(ruta_base)
    sound1 = pygame.mixer.Sound(ruta_base+'/sounds/sonido_1.wav')
    channel1 = pygame.mixer.Channel(0)

    # Generar minas
    NUM_MINES = 10
    mines_pos = random.sample([(r, c) for r in range(ROWS) for c in range(COLS)], NUM_MINES)
    for r, c in mines_pos:
        mines[r][c] = -1

    calcular_minas_alrededor(mines, ROWS, COLS)
    
    running = True
    mouse_inside_window = True
    while running:
        screen.fill((192, 192, 192))
        dibujar_grilla(screen, ROWS, COLS, CELL_SIZE, revealed, mines, (192, 192, 192), (160, 160, 160), (255, 0, 0), (0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                row, col = get_cell_under_mouse(CELL_SIZE)
                if not revealed[row][col]:
                    revealed[row][col] = True
                    if mines[row][col] == -1:
                        fin_del_juego(explosion_sound)
                    else:
                            hablar_minas_alrededor(row, col, mines)
                    #x1, y1= pygame.mouse.get_pos()
                    handle_click(pygame.mouse.get_pos(),CELL_SIZE,revealed)
        # Verificar si el mouse está dentro de la ventana
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if is_mouse_inside_window(mouse_x, mouse_y, WIDTH, HEIGHT) and first_click == False:
            if not mouse_inside_window:  # Si el mouse acaba de volver a la ventana
                mouse_inside_window = True  # Actualizamos el estado del mouse
            play_sound_based_on_mouse1(mouse_x, mouse_y, sound1, WIDTH, HEIGHT, channel1)
        
        else:
            if mouse_inside_window:  # Si el mouse acaba de salir de la ventana
                channel1.stop()  # Detenemos el sonido
                mouse_inside_window = False

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
