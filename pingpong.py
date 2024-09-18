import pygame
import sys
import os
import math


def int_pingpong():
# Inicialización de pygame
    global WHITE, BLACK, ruta_base, screen_info, SCREEN_WIDTH, SCREEN_HEIGHT
    global screen, hit_sound, bounce_sound, continuous_sound, channel, continuous_channel
    global sounds, sound_index, font

    pygame.init()

    # Definir colores
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    # Definir dimensiones de la pantalla
    screen_info = pygame.display.Info()
    SCREEN_WIDTH = screen_info.current_w
    SCREEN_HEIGHT = screen_info.current_h
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)

    # Sonidos
    pygame.mixer.init()
    hit_sound = pygame.mixer.Sound(ruta_base + "/sounds/hit.wav")

    bounce_sound = pygame.mixer.Sound(ruta_base +"/sounds/sonido_1.wav")
    continuous_sound = pygame.mixer.Sound(ruta_base +"/sounds/sonido_10.wav")  # Sonido continuo para la pelota

    channel = pygame.mixer.Channel(0)  # Canal de sonido para la pelota
    continuous_channel = pygame.mixer.Channel(1)

    # Lista de sonidos para el canal
    sounds = [hit_sound, bounce_sound]
    sound_index = 0

    # Definir la fuente para mostrar el puntaje
    font = pygame.font.Font(None, 74)

# Clase de la pelota
class Ball:
    def __init__(self):
        self.width = 20
        self.height = 20
        self.reset()

    def reset(self):
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT // 2 - self.height // 2
        self.speed_x = 5 if pygame.time.get_ticks() % 2 == 0 else -5  # Velocidad inicial aleatoria
        self.speed_y = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        if self.y <= 0 or self.y >= SCREEN_HEIGHT - self.height:
            self.speed_y *= -1
            play_sound_based_on_mouse(self.x, self.y)  # Reproducir sonido espacial al rebotar

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

# Clase de la raqueta
class Paddle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, pos_y):
        self.y = pos_y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)


# Función adaptada para el sonido espacial basado en la posición de la pelota y raqueta
def play_sound_based_on_mouse(object_x, object_y):
    # Normalizar la posición x del objeto a un rango de [-1, 1]
    x = (object_x / SCREEN_WIDTH) * 2 - 1  # Izquierda = -1, Derecha = 1
    # Normalizar la posición y del objeto a un rango de [0, 1] (para simular distancia)
    y = object_y / SCREEN_HEIGHT  # Arriba = cercano, Abajo = lejano

    # Controlar el balance estéreo en función de la posición en el eje X
    left_volume = max(0, 1 - x)
    right_volume = max(0, 1 + x)

    # Reducir volumen en función de la distancia (simulación simple en Y)
    distance_factor = max(0.2, 1 - y)

    # Ajustar el volumen para el balance estéreo
    channel.set_volume(left_volume * distance_factor, right_volume * distance_factor)

    # Reproducir el sonido en el canal si no está ya ocupado
    if not channel.get_busy():
        channel.play(sounds[sound_index])

# Función para reproducir sonido continuo basado en la distancia entre la pelota y la raqueta del jugador
def play_continuous_sound_based_on_distance(ball, paddle):
    # Calcular la distancia entre la pelota y la raqueta del jugador
    distance_x = abs(ball.x - paddle.x)
    distance_y = abs(ball.y - paddle.y)
    distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

    # Normalizar la distancia
    max_distance = SCREEN_WIDTH // 2
    normalized_distance = min(distance / max_distance, 1)

    # Controlar el volumen en función de la distancia (más cerca, más fuerte)
    volume = max(0.2, 1 - normalized_distance)

    # Balance estéreo en función de la posición en el eje X
    left_volume = max(0, 1 - (ball.x / SCREEN_WIDTH))
    right_volume = max(0, 1 + (ball.x / SCREEN_WIDTH))

    # Ajustar el volumen para el sonido continuo
    continuous_channel.set_volume(left_volume * volume, right_volume * volume)

    # Reproducir el sonido continuo si no está ya ocupado
    if not continuous_channel.get_busy():
        continuous_channel.play(continuous_sound, loops=-1)  # Repetir el sonido en bucle

# Función para actualizar el puntaje y reiniciar la pelota
def check_point():
    global player_score, ai_score

    # Si la pelota sale por la izquierda (la máquina gana)
    if ball.x <= 0:
        ai_score += 1
        ball.reset()
    # Si la pelota sale por la derecha (el jugador gana)
    elif ball.x >= SCREEN_WIDTH - ball.width:
        player_score += 1
        ball.reset()


def ballpingpong():
    global ball, player_paddle, ai_paddle, player_score, ai_score
    # Crear pelota y raquetas con raquetas más grandes
    ball = Ball()
    player_paddle = Paddle(20, SCREEN_HEIGHT // 2 - 140, 10, 280)  # Raqueta del jugador el doble de grande
    ai_paddle = Paddle(SCREEN_WIDTH - 30, SCREEN_HEIGHT // 2 - 140, 10, 280)  # Raqueta de la máquina el doble de grande

    # Variables de puntuación
    player_score = 0
    ai_score = 0
# Bucle principal


def mainpingpong():
    int_pingpong()
    ballpingpong()
    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Movimiento de la pelota
        ball.move()

        # Movimiento de la raqueta del jugador con el mouse
        mouse_y = pygame.mouse.get_pos()[1]
        player_paddle.move(mouse_y - player_paddle.height // 2)

        # Movimiento básico de la raqueta de la máquina
        if ball.y > ai_paddle.y + ai_paddle.height // 2:
            ai_paddle.move(ai_paddle.y + 5)
        else:
            ai_paddle.move(ai_paddle.y - 5)

        # Detección de colisiones entre la pelota y las raquetas
        if ball.rect.colliderect(player_paddle.rect) or ball.rect.colliderect(ai_paddle.rect):
            ball.speed_x *= -1
            play_sound_based_on_mouse(ball.x, ball.y)  # Sonido espacial cuando la pelota golpea la raqueta

        # Verificar si la pelota ha salido de la pantalla y actualizar el puntaje
        check_point()

        # Sonido continuo basado en la distancia entre la pelota y la raqueta del jugador
        play_continuous_sound_based_on_distance(ball, player_paddle)

        # Dibujar objetos en la pantalla
        ball.draw(screen)
        player_paddle.draw(screen)
        ai_paddle.draw(screen)

        # Dibujar el puntaje
        player_text = font.render(str(player_score), True, WHITE)
        ai_text = font.render(str(ai_score), True, WHITE)
        screen.blit(player_text, (SCREEN_WIDTH // 4, 20))
        screen.blit(ai_text, (SCREEN_WIDTH * 3 // 4, 20))

        # Actualizar la pantalla
        pygame.display.flip()

        # Establecer el FPS
        clock.tick(60)

    # Cerrar pygame
    pygame.quit()
