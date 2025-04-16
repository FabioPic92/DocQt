import os
import json
import cv2
import numpy as np
from PIL import Image

output_file_name = 'output.json' 

def processing_image(document_data):

    img = np.array(document_data.image)

    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    h, w = img.shape[:2]

    with open(output_file_name, 'r') as file:
        data = json.load(file)

    for block in data.get("Blocks", []):
        box = block["Geometry"]["Polygon"]
        points = []
        for point in box:
            x_px = int(point["X"] * w)
            y_px = int(point["Y"] * h)
            points.append((x_px, y_px))
        pts = np.array(points, np.int32).reshape((-1, 1, 2))
        cv2.polylines(img, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

    cv2.imwrite("output1.jpg", img)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img = Image.fromarray(img)

    document_data.image_proc = img