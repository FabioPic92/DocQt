import argparse
import json
import cv2
import numpy as np

# Parser degli argomenti da riga di comando
parser = argparse.ArgumentParser(description="Carica un'immagine e un file JSON.")
parser.add_argument('--image', type=str, required=True, help='Path dell\'immagine')
parser.add_argument('--json', type=str, required=True, help='Path del file JSON')

args = parser.parse_args()

with open(args.json, 'r') as f:
    data = json.load(f)

img = cv2.imread(args.image)
h, w = img.shape[:2]

min_left, min_top = w, h
max_right, max_bottom = 0, 0


for block in data.get("Blocks", []):
    #if block.get("BlockType") == "WORD" or block.get("BlockType") == "LINE":  # Considera anche le righe, se vuoi
    box = block["Geometry"]["Polygon"]
    points = []
    for point in box:
        x_px = int(point["X"] * w)
        y_px = int(point["Y"] * h)
        points.append((x_px, y_px))
    pts = np.array(points, np.int32).reshape((-1, 1, 2))
    cv2.polylines(img, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

cv2.imwrite("output.jpg", img)
