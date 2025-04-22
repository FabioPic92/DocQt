import cv2
import numpy as np
import json

img = cv2.imread("DocumentScanner.jpg") 

with open('response.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

with open('output.json', 'r', encoding='utf-8') as file:
    data1 = json.load(file)

blocchi1 = data1["Blocks"]
blocchi = data["Blocks"]

linee1 = [
    blocco1 for blocco1 in blocchi1
    if blocco1.get("BlockType") == "LINE"
]

blocco1_top_left = min(
    linee1,
    key=lambda b: (b["Geometry"]["BoundingBox"]["Top"], b["Geometry"]["BoundingBox"]["Left"]),
    default=None
)

if blocco1_top_left:
    print("Testo più in alto e a sinistra:", blocco1_top_left["Text"])
    print("Posizione (Top, Left):", 
          blocco1_top_left["Geometry"]["BoundingBox"]["Top"],
          blocco1_top_left["Geometry"]["BoundingBox"]["Left"])
    
error_x1 = blocco1_top_left["Geometry"]["BoundingBox"]["Top"]
error_y1 = blocco1_top_left["Geometry"]["BoundingBox"]["Left"]

linee = [
    blocco for blocco in blocchi
    if blocco.get("BlockType") == "LINE"
]

# Trova il blocco con il valore minimo di Left
blocco_top_left = min(
    linee,
    key=lambda b: (b["Geometry"]["BoundingBox"]["Top"], b["Geometry"]["BoundingBox"]["Left"]),
    default=None
)

if blocco_top_left:
    print("Testo più in alto e a sinistra:", blocco_top_left["Text"])
    print("Posizione (Top, Left):", 
          blocco_top_left["Geometry"]["BoundingBox"]["Top"],
          blocco_top_left["Geometry"]["BoundingBox"]["Left"])
    
error_x = blocco_top_left["Geometry"]["BoundingBox"]["Top"]
error_y = blocco_top_left["Geometry"]["BoundingBox"]["Left"]

height, width = img.shape[:2]

p1_x_err = abs(error_x1 - error_x)
p1_y_err = abs(error_y1 - error_y)


print(p1_x_err)
print(p1_y_err)

P1_x_error = 0.04616007208824158 
P1_y_error = 0.2436360865831375

P2_x_error = 0.3395560383796692
P2_y_error = 0.2930818498134613

P1 = {"X": P1_x_error, "Y": P1_y_error}
P2 = {"X": P2_x_error, "Y": P2_y_error}

# Converti le coordinate in pixel
x1 = int(P1["X"] * width)
y1 = int(P1["Y"] * height)
x2 = int(P2["X"] * width)
y2 = int(P2["Y"] * height)

cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)

# Mostra l'immagine
cv2.imwrite("immagine_output.jpg", img)