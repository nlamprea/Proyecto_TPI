import pygame

# Inicializar pygame y el mezclador de sonido
pygame.init()
pygame.mixer.init()

# Dimensiones de la ventana (opcional)
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sonido solo en el audífono derecho")

# Cargar el sonido
sound1 = pygame.mixer.Sound('sounds/sonido_1.wav')

# Usamos un canal de audio para poder ajustar el balance estéreo
channel = pygame.mixer.Channel(0)

# Configurar el sonido para que solo salga por el audífono derecho
channel.set_volume(0, 1)  # Volumen en el izquierdo = 0, Volumen en el derecho = 1

# Reproducir el sonido en el canal
channel.play(sound1)

# Mantener la ventana abierta por un tiempo para escuchar el sonido
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Cerrar pygame
pygame.quit()
