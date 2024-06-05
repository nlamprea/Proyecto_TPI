import pyautogui
import time
import random
import getpass

import cv2
import easyocr
import matplotlib.pyplot as plt

# texto a audio
from gtts import gTTS
import os

# Esperar 3 segundos
time.sleep(3)

# Tomar la captura de pantalla
screenshot = pyautogui.screenshot()

# Especificar la carpeta de destino
#carpeta_destino = "screenshot"
user = getpass.getuser()
num= random.randint(10,100)

ruta_archivo = f"/Users/{user}/Documents/PROYECTO_TPI/src/screenshot{num}.jpg"

# Crear la ruta completa al archivo
#ruta_archivo = os.path.join(carpeta_destino, "dasd.jpg")


# Guardar la captura de pantalla en la carpeta especificada
# if os.path.exists(ruta_archivo):
#     print(f"El elemento '{ruta_archivo}' existe en la carpeta '{carpeta_destino}'.")
# else:
screenshot.save(ruta_archivo)

res_list = []

reader = easyocr.Reader(["es"], gpu=False)
image = cv2.imread(ruta_archivo)

result = reader.readtext(image, paragraph=False)

for res in result:
     print("res:", res)
     pt0 = res[0][0]
     pt1 = res[0][1]
     pt2 = res[0][2]
     pt3 = res[0][3]

     res_list.append(res[1])

     # cv2.rectangle(image, pt0, (pt1[0], pt1[1] - 23), (166, 56, 242), -1)
     # cv2.putText(image, res[1], (pt0[0], pt0[1] -3), 2, 0.8, (255, 255, 255), 1)
     # cv2.rectangle(image, pt0, pt2, (166, 56, 242), 2)
     # cv2.circle(image, pt0, 2, (255, 0, 0), 2)
     # cv2.circle(image, pt1, 2, (0, 255, 0), 2)
     # cv2.circle(image, pt2, 2, (0, 0, 255), 2)
     # cv2.circle(image, pt3, 2, (0, 255, 255), 2)
     # cv2.imshow("Image", image)
     # cv2.waitKey(0)
# cv2.destroyAllWindows()


# print("Contenido de res_list:")
# for item in res_list:
#     print(item)

words_string = " ".join(res_list)
# Imprimir la cadena de texto resultante
print("Contenido de words_string:")
print(words_string)


language = 'es'

# Crea el objeto gTTS
speech = gTTS(text=words_string, lang=language, slow=False)

# Guarda el archivo de audio
output_file = "output.mp3"
speech.save(output_file)

# Reproduce el archivo de audio (opcional)
os.system(f"start {output_file}")