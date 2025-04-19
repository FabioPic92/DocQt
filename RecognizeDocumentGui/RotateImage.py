from PIL import Image
import numpy as np
import cv2

# Funzione per correggere la prospettiva (raddrizzare il documento)
def correct_document_perspective(image_pil, pts1, width, height):
    # Converti l'immagine PIL in formato OpenCV (array NumPy)
    image = np.array(image_pil)

    # Punti finali (quelli che vogliamo ottenere)
    # Immagina di voler un documento rettangolare di dimensioni (width, height)
    pts2 = np.float32([[0, 0], [width, 0], [width, height], [0, height]])

    # Calcolare la matrice di trasformazione prospettica
    matrix = cv2.getPerspectiveTransform(pts1, pts2)

    # Applica la trasformazione prospettica per "raddrizzare" il documento
    result = cv2.warpPerspective(image, matrix, (width, height))

    # Converti il risultato di nuovo in un'immagine PIL
    result_pil = Image.fromarray(result)
    
    return result_pil

# Esempio di punti di riferimento (p1, p2, p3, p4)
# Punti che rappresentano i 4 angoli del documento deformato
pts1 = np.float32([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])

# Carica l'immagine con PIL
image_pil = Image.open("documento.jpg")

# Imposta la larghezza e altezza desiderate del documento
width = 500  # Imposta la larghezza desiderata del documento raddrizzato
height = 700  # Imposta l'altezza desiderata del documento raddrizzato

# Correggi la prospettiva del documento
corrected_image = correct_document_perspective(image_pil, pts1, width, height)

# Mostra l'immagine corretta
corrected_image.show()