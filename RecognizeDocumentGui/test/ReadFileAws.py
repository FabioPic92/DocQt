import argparse
import boto3
import cv2
import numpy as np

parser = argparse.ArgumentParser(description="Carica un'immagine e un file JSON.")
parser.add_argument('--image', type=str, required=True, help='Path dell\'immagine')

args = parser.parse_args()

textract = boto3.client('textract')

img = cv2.imread(args.image)
h, w = img.shape[:2]

with open(args.image, 'rb') as img_file:
    # Esegui Textract su un'immagine (JPG in questo caso)
    response = textract.analyze_document(
        Document={'Bytes': img_file.read()},
        FeatureTypes=['FORMS', 'TABLES']  # Analizza le forme, come i key-value pairs
    )

for block in response.get("Blocks", []):
    #if block.get("BlockType") == "WORD" or block.get("BlockType") == "LINE":  # Considera anche le righe, se vuoi
    box = block["Geometry"]["Polygon"]
    points = []
    for point in box:
        x_px = int(point["X"] * w)
        y_px = int(point["Y"] * h)
        points.append((x_px, y_px))
    pts = np.array(points, np.int32).reshape((-1, 1, 2))
    cv2.polylines(img, [pts], isClosed=True, color=(0, 255, 0), thickness=2)


cv2.imwrite("output1.jpg", img)