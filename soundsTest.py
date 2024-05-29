import pygame
import numpy as np


pygame.init()
sound = pygame.mixer.Sound('sounds\Alarm01.wav')
# Obtén la frecuencia original del sonido
original_frequency = sound.get_frequency('sounds\Alarm01.wav')

# Establece la nueva frecuencia (por ejemplo, para aumentar el pitch en 2 semitonos)
new_frequency = original_frequency * 2**(2/12)

# Crea una nueva versión del sonido con la nueva frecuencia
new_sound = pygame.mixer.Sound(np.resize(sound.get_raw(), (int(sound.get_length() * new_frequency), 1)))
new_sound.set_volume(sound.get_volume())
