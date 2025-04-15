import os
import json
import cv2
import numpy as np

output_file_path = 'output.txt' 

def processing_image(img, pathJson):

    h, w = img.shape[:2]

    with open(pathJson, 'r') as file:
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