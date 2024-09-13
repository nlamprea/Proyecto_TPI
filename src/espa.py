import pygame

# Inicializar pygame y el mezclador de sonido
pygame.init()
pygame.mixer.init()

# Dimensiones de la ventana
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simulación de Sonido Espacial con el Mouse")

# Cargar el sonido
sound1 = pygame.mixer.Sound('sounds/sonido_1.wav')

# Usamos un canal de audio para poder ajustar el balance estéreo
channel = pygame.mixer.Channel(0)

def play_sound_based_on_mouse(mouse_x, mouse_y):
    """
    Ajusta el sonido según la posición del mouse en la pantalla.
    :param mouse_x: Posición X del mouse (entre 0 y screen_width)
    :param mouse_y: Posición Y del mouse (entre 0 y screen_height)
    """

    # Normalizar la posición x del mouse a un rango de [-1, 1]
    x = (mouse_x / screen_width) * 2 - 1  # Izquierda = -1, Derecha = 1

    # Normalizar la posición y del mouse a un rango de [0, 1] (para simular distancia)
    y = mouse_y / screen_height  # Arriba = cercano, Abajo = lejano

    # Controlar el balance estéreo en función de la posición en el eje X
    left_volume = max(0, 1 - x)
    right_volume = max(0, 1 + x)

    # Reducir volumen en función de la distancia (simulación simple en Y)
    distance_factor = max(0.1, 1 - y)  # Para no dejar el volumen a cero

    # Ajustar el volumen para el balance estéreo
    channel.set_volume(left_volume * distance_factor, right_volume * distance_factor)

    # Reproducir el sonido en el canal
    if not channel.get_busy():  # Si el canal no está reproduciendo, reproducir el sonido
        channel.play(sound1)

# Bucle principal
running = True
clock = pygame.time.Clock()

while running:
    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Obtener la posición actual del mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Llamar a la función para ajustar el sonido según la posición del mouse
    play_sound_based_on_mouse(mouse_x, mouse_y)

    # Limitar el FPS para evitar saturar el sistema con sonidos
    clock.tick(5)  # Reproducir sonido cada 200ms (5 FPS)

# Salir de pygame
pygame.quit()
