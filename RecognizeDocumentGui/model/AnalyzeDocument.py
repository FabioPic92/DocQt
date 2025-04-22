import json
import cv2
import numpy as np

output_file_name = 'output.json' 

def processing_image(document_data):

    document_data.image_proc = document_data.image.copy()

    h, w = document_data.image_proc.shape[:2] 

    print(f"{h} {w}")

    with open(output_file_name, 'r') as file:
        data = json.load(file)

    for block in data.get("Blocks", []):
        if block.get("BlockType") != "LINE":
            box = block["Geometry"]["Polygon"]
            points = []

            for point in box:
                x_px = int(point["X"] * w)
                y_px = int(point["Y"] * h)
                points.append((x_px, y_px))

            pts = cv2.convexHull(np.array(points)).astype(int)
            cv2.polylines(document_data.image_proc, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

    cv2.imwrite("output2.jpg", document_data.image_proc)