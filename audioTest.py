from gtts import gTTS
import os

# Texto que deseas convertir a audio
text = "Hola, este es un ejemplo de conversión de texto a audio usando Python."

# Especifica el idioma (es = español, en = inglés, etc.)
language = 'es'

# Crea el objeto gTTS
speech = gTTS(text=text, lang=language, slow=False)

# Guarda el archivo de audio
output_file = "output.mp3"
speech.save(output_file)

# Reproduce el archivo de audio (opcional)
os.system(f"start {output_file}")
