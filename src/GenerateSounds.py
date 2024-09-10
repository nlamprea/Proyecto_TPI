import os
import numpy as np
import sounddevice as sd
import wave

# Crear la carpeta 'sounds' si no existe
if not os.path.exists('sounds'):
    os.makedirs('sounds')

# Función para generar un tono de frecuencia específica
def generar_sonido(frecuencia=440, duracion=1.0, volumen=0.5, sample_rate=44100):
    samples = np.linspace(0, duracion, int(sample_rate * duracion), endpoint=False)
    onda = 0.5 * np.sin(2 * np.pi * frecuencia * samples)
    return (onda * volumen).astype(np.float32)

# Función para guardar el sonido en formato WAV
def guardar_sonido_wav(sonido, archivo, sample_rate=44100):
    with wave.open(archivo, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono (1 canal), o estéreo (2 canales) si quieres agregar spatial audio
        wav_file.setsampwidth(2)  # 16 bits por muestra
        wav_file.setframerate(sample_rate)
        wav_file.writeframes((sonido * 32767).astype(np.int16).tobytes())  # Convertir a 16-bit PCM

# Generar y guardar 6 sonidos con diferentes frecuencias
frecuencias = [440, 550, 660, 770, 880, 990]  # Frecuencias de los tonos
volumen = 0.5  # Volumen común para los 6 sonidos
duracion = 11.0  # Duración en segundos

for i in range(6):
    sonido = generar_sonido(frecuencia=frecuencias[i], duracion=duracion, volumen=volumen)
    archivo_salida = f"sounds/sonido_{i+1}.wav"  # Ruta de guardado en la carpeta sounds
    guardar_sonido_wav(sonido, archivo_salida)
    print(f"Sonido {i+1} generado y guardado en: {archivo_salida}")
