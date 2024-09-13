def audioScreenshot(num):
    
    # directorios existen
    os.makedirs(screenshots_dir, exist_ok=True)
    os.makedirs(ouput_dir, exist_ok=True)
    
    archivo_screenshot = os.path.join(screenshots_dir, f'screenshot_{num}.png')

    if os.path.exists(archivo_screenshot):
        res_list = []

        reader = easyocr.Reader(["es"], gpu=False)
        image = cv2.imread(archivo_screenshot)

        result = reader.readtext(image, paragraph=False)

        for res in result:
            print("res:", res)
            pt0 = res[0][0]
            pt1 = res[0][1]
            pt2 = res[0][2]
            pt3 = res[0][3]
            res_list.append(res[1])

        words_string = " ".join(res_list)
        #Imprimir la cadena de texto resultante
        print("Contenido de words_string:")
        print(words_string)

        language = 'es'

        #Crea el objeto gTTS
        speech = gTTS(text=words_string, lang=language, slow=False)

        #Guarda el archivo de audio
        output_file = ouput_dir + "output.mp3"
        
        if os.path.exists(output_file):
            os.remove(output_file)
        
        speech.save(output_file)

        #Reproduce el archivo de audio (opcional)
        os.system(f"start {output_file}")