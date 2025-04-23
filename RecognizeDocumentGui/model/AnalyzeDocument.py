import json
import cv2
import numpy as np

from data import P1_x, P1_y, P2_x, P2_y, P3_x, P3_y, P4_x, P4_y, P5_x, P5_y, P6_x, P6_y

output_file_name = "output.json" 
model_data_document = "response.json"

def search_min(block_points):
    min_point = min(block_points, key=lambda point: (point["X"], point["Y"]))
    return ((min_point["X"], min_point["Y"]))

def search_max(block_points):
    max_point = max(block_points, key=lambda point: (point["X"], point["Y"]))
    return ((max_point["X"], max_point["Y"]))

def find_left_top_point(data_blocks):

    lines = [
        blocks for blocks in data_blocks
         if blocks.get("BlockType") == "LINE"
    ]

    blocks_top_left = min(
        lines,
        key=lambda b: (b["Geometry"]["BoundingBox"]["Top"], b["Geometry"]["BoundingBox"]["Left"]),
        default=None
    )

    left = blocks_top_left["Geometry"]["BoundingBox"]["Left"]
    top = blocks_top_left["Geometry"]["BoundingBox"]["Top"]

    return left, top

def shift_error(document_data):

    with open(model_data_document, 'r') as file:
        model_data = json.load(file)

    model_data_blocks = model_data["Blocks"]
    document_data_blocks = document_data["Blocks"]

    model_y, model_x = find_left_top_point(model_data_blocks)
    document_y, document_x = find_left_top_point(document_data_blocks)

    error_y = abs(model_y - document_y)
    error_x = abs(model_x - document_x)

    return error_x, error_y

def processing_image(document_data):

    document_data.image_proc = document_data.image.copy()

    height, width = document_data.image_proc.shape[:2] 

    print(f"{height} {width}")

    with open(output_file_name, 'r') as file:
        document_data = json.load(file)

    error_x, error_y = shift_error(document_data)

    P1_x = P1_x - error_x
    P1_y = P1_y - error_y
    P2_x = P2_x + error_x
    P2_y = P2_y + error_y
    P3_x = P3_x - error_x
    P3_y = P3_y - error_y
    P4_x = P4_x + error_x
    P4_y = P4_y + error_y
    P5_x = P5_x - error_x
    P5_y = P5_y - error_y
    P6_x = P6_x + error_x
    P6_y = P6_y + error_y

    P1 = {"X": P1_x, "Y": P1_y}
    P2 = {"X": P2_x, "Y": P2_y}

    P3 = {"X": P3_x, "Y": P3_y}
    P4 = {"X": P4_x, "Y": P4_y}

    P5 = {"X": P5_x, "Y": P5_y}
    P6 = {"X": P6_x, "Y": P6_y}

    x1 = int(P1["X"] * width)
    y1 = int(P1["Y"] * height)
    x2 = int(P2["X"] * width)
    y2 = int(P2["Y"] * height)

    x3 = int(P3["X"] * width)
    y3 = int(P3["Y"] * height)
    x4 = int(P4["X"] * width)
    y4 = int(P4["Y"] * height)

    x5 = int(P5["X"] * width)
    y5 = int(P5["Y"] * height)
    x6 = int(P6["X"] * width)
    y6 = int(P6["Y"] * height)

    cv2.rectangle(document_data.image_proc, (x1, y1), (x2, y2), (0, 255, 0), 1)
    cv2.rectangle(document_data.image_proc, (x3, y3), (x4, y4), (0, 255, 0), 1)
    cv2.rectangle(document_data.image_proc, (x5, y5), (x6, y6), (0, 255, 0), 1)

    cv2.imwrite("output2.jpg", document_data.image_proc)