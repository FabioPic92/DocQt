import cv2
import numpy as np
import json

def search_min(block_points):
    min_point = min(block_points, key=lambda point: (point["X"], point["Y"]))
    return ((min_point["X"], min_point["Y"]))

def search_max(block_points):
    max_point = max(block_points, key=lambda point: (point["X"], point["Y"]))
    return ((max_point["X"], max_point["Y"]))

def search_line(output, P1, P2):
    for block in output.get("Blocks", []):
        if block.get("BlockType") == "LINE":
            points = block["Geometry"]["Polygon"]
            min_point = search_min(points)
            max_point = search_max(points)
            # print(min_point[0], min_point[1], max_point[0], max_point[1])
            # print(P1["X"], P1["Y"], P2["X"], P2["Y"]) 
            # print(block["Text"])
            if (
                min_point[0] >= P1["X"] and min_point[1] >= P1["Y"] and
                max_point[0] <= P2["X"] and max_point[1] <= P2["Y"]
            ):
                print(block["Text"])

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


error = 0.01

img = cv2.imread("ImagePreprocessed.jpg") 

with open('response.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

with open('output.json', 'r', encoding='utf-8') as file:
    data1 = json.load(file)

blocchi1 = data1["Blocks"]
blocchi = data["Blocks"]

error_x1, error_y1 = find_left_top_point(blocchi1)
error_x, error_y = find_left_top_point(blocchi)

height, width = img.shape[:2]

p1_x_err = abs(error_x1 - error_x)
p1_y_err = abs(error_y1 - error_y)


print(p1_x_err)
print(p1_y_err)

P1_x_error = 0.04616007208824158 - p1_x_err
P1_y_error = 0.2436360865831375 - p1_y_err

P2_x_error = 0.3395560383796692 + p1_x_err
P2_y_error = 0.2930818498134613 + p1_y_err

P3_x = 0.1115032434463501 - p1_x_err
P3_y = 0.8902167677879333 - p1_y_err
P4_x = 0.9303025007247925 + p1_x_err
P4_y = 0.9041821956634521 + p1_y_err

P5_x = 0.7805507183074951 - p1_x_err
P5_y = 0.9298563003540039 - p1_y_err
P6_x = 0.9161749482154846 + p1_x_err
P6_y = 0.9413824081420898 + p1_y_err

P3 = {"X": P3_x, "Y": P3_y}
P4 = {"X": P4_x, "Y": P4_y}

P5 = {"X": P5_x, "Y": P5_y}
P6 = {"X": P6_x, "Y": P6_y}

P1 = {"X": P1_x_error, "Y": P1_y_error}
P2 = {"X": P2_x_error, "Y": P2_y_error}

# Converti le coordinate in pixel
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

cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
cv2.rectangle(img, (x3, y3), (x4, y4), (0, 255, 0), 1)
cv2.rectangle(img, (x5, y5), (x6, y6), (0, 255, 0), 1)

search_line(data1, P1, P2)
search_line(data1, P3, P4)
search_line(data1, P5, P6)

cv2.imwrite("immagine_output.jpg", img)