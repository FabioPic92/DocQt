import json
import cv2
import numpy as np

output_file_name = "Data/Result/output.json" 
model_data_document = "Data/response.json"

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

    model_x, model_y = find_left_top_point(model_data_blocks)
    document_x, document_y = find_left_top_point(document_data_blocks)

    error_y = document_y - model_y
    error_x = document_x - model_x

    return error_x, error_y

def search_line(output, P1, P2):
    for block in output.get("Blocks", []):
        if block.get("BlockType") == "LINE":
            points = block["Geometry"]["Polygon"]
            min_point = search_min(points)
            max_point = search_max(points)
            if (
                min_point[0] >= P1["X"] and min_point[1] >= P1["Y"] and
                max_point[0] <= P2["X"] and max_point[1] <= P2["Y"]
            ):
                print(block["Text"])

def processing_image(document_data):

    #document_data.image_proc = document_data.image.copy()

    height, width = document_data.image_proc.shape[:2] 

    print(f"{height} {width}")

    with open(output_file_name, 'r') as file:
        document_data_json = json.load(file)

    error_x, error_y = shift_error(document_data_json)

    print(error_x)
    print(error_y)

    P1_x = 0.04616007208824158
    P1_y = 0.2436360865831375
    P2_x = 0.3395560383796692
    P2_y = 0.2930818498134613

    P3_x = 0.1115032434463501
    P3_y = 0.8902167677879333
    P4_x = 0.9303025007247925
    P4_y = 0.9041821956634521

    P5_x = 0.7805507183074951
    P5_y = 0.9298563003540039
    P6_x = 0.9161749482154846
    P6_y = 0.9413824081420898

    P1_x_err = P1_x - error_x
    P1_y_err = P1_y - error_y
    P2_x_err = P2_x + error_x
    P2_y_err = P2_y + error_y
    P3_x_err = P3_x - error_x
    P3_y_err = P3_y - error_y
    P4_x_err = P4_x + error_x
    P4_y_err = P4_y + error_y
    P5_x_err = P5_x - error_x
    P5_y_err = P5_y - error_y
    P6_x_err = P6_x + error_x
    P6_y_err = P6_y + error_y

    print(f"P1_x_err {P1_x_err}")

    P1 = {"X": P1_x_err, "Y": P1_y_err}
    P2 = {"X": P2_x_err, "Y": P2_y_err}

    P3 = {"X": P3_x_err, "Y": P3_y_err}
    P4 = {"X": P4_x_err, "Y": P4_y_err}

    P5 = {"X": P5_x_err, "Y": P5_y_err}
    P6 = {"X": P6_x_err, "Y": P6_y_err}

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

    search_line(document_data_json, P1, P2)
    search_line(document_data_json, P3, P4)
    search_line(document_data_json, P5, P6)

    cv2.imwrite("Data/Result/output.jpg", document_data.image_proc)