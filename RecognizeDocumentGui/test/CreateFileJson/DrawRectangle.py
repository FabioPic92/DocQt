import cv2
import numpy as np
import json
import os

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
            if (
                min_point[0] >= P1["X"] and min_point[1] >= P1["Y"] and
                max_point[0] <= P2["X"] and max_point[1] <= P2["Y"]
            ):
                print(block["Text"])

def find_left_top_point(data_blocks):
    lines = [
    blocks for blocks in data_blocks
        if blocks.get("BlockType") == "WORD"
    ]

    blocks_top_left = min(
        lines,
        key=lambda b: (b["Geometry"]["BoundingBox"]["Top"], b["Geometry"]["BoundingBox"]["Left"]),
        default=None
    )

    left = blocks_top_left["Geometry"]["BoundingBox"]["Left"]
    top = blocks_top_left["Geometry"]["BoundingBox"]["Top"]
    text = blocks_top_left.get("Text", "")

    return left, top, text

def find_top_left_point(data_blocks):
    lines = [
    blocks for blocks in data_blocks
        if blocks.get("BlockType") == "WORD"
    ]


    blocks_left_top = min(
        lines,
        key=lambda b: (b["Geometry"]["BoundingBox"]["Left"], b["Geometry"]["BoundingBox"]["Top"]),
        default=None
    )

    left = blocks_left_top["Geometry"]["BoundingBox"]["Left"]
    top = blocks_left_top["Geometry"]["BoundingBox"]["Top"]
    text = blocks_left_top.get("Text", "")

    return left, top, text

def find_bottom_right_point(data_blocks):
    lines = [
    blocks for blocks in data_blocks
        if blocks.get("BlockType") == "WORD"
    ]


    blocks_bottom_right = max(
        lines,
        key=lambda b: (b["Geometry"]["BoundingBox"]["Left"], b["Geometry"]["BoundingBox"]["Top"]),
        default=None
    )

    right = blocks_bottom_right["Geometry"]["BoundingBox"]["Left"]
    bottom = blocks_bottom_right["Geometry"]["BoundingBox"]["Top"]
    text = blocks_bottom_right.get("Text", "")

    return right, bottom, text

def find_right_bottom_point(data_blocks):
    lines = [
    blocks for blocks in data_blocks
        if blocks.get("BlockType") == "WORD"
    ]


    blocks_right_bottom = max(
        lines,
        key=lambda b: (b["Geometry"]["BoundingBox"]["Top"], b["Geometry"]["BoundingBox"]["Left"]),
        default=None
    )

    right = blocks_right_bottom["Geometry"]["BoundingBox"]["Left"]
    bottom = blocks_right_bottom["Geometry"]["BoundingBox"]["Top"]
    text = blocks_right_bottom.get("Text", "")


    return right, bottom, text

def find_points(data_blocks):


    bottom1, right1, text1 =  find_bottom_right_point(data_blocks)
    
    bottom, right, text2 = find_right_bottom_point(data_blocks)

    left, top, text = find_left_top_point(data_blocks)

    left1, top1, text4 = find_top_left_point(data_blocks) 

    print(left, top)
    print("Top Left",text)
    print(left1, top1)
    print("Top Left",text4)
    print(right, bottom)
    print("Bottom Right",text2)
    print(bottom1, right1)
    print("Right Bottom",text1)

def get_document_corners(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Threshold per evidenziare contorni
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Trova contorni
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            corners = approx.reshape(4, 2).astype("float32")
            return corners

    return None  # Se non trova 4 angoli

def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]      # Top-left
    rect[2] = pts[np.argmax(s)]      # Bottom-right

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]   # Top-right
    rect[3] = pts[np.argmax(diff)]   # Bottom-left

    return rect

#loaded_contour = np.loadtxt("Test3/document_contour.txt")
#loaded_contour = loaded_contour.reshape((4, 1, 2)).astype(np.int32)

loaded_contour = np.array([
    [0, 0],           # top-left
    [1427, 0],        # top-right
    [1427, 1991],     # bottom-right
    [0, 1991]  
], dtype="float32")

#loaded_contour = order_points(loaded_contour)

img_orig = cv2.imread("Test1.png") # Foto al documento

#pts_originale = get_document_corners(img_orig)

h, w = img_orig.shape[:2] 
print(h,w)

img = cv2.imread("Test3/ImagePreprocessed.jpg") # documento ricavato dall'immagine
image_document = cv2.imread("Test3/Test21.jpg") # Documento originale

h_doc, w_doc = image_document.shape[:2] 

P1_x = 0.04616007208824158
P1_y = 0.2436360865831375
P2_x = 0.3395560383796692
P2_y = 0.2930818498134613

P1_x = P1_x * w_doc
P1_y = P1_y * h_doc
P2_x = P2_x * w_doc
P2_y = P2_y * h_doc

campo = np.array([
    [[P1_x, P1_y]],
    [[P2_x, P2_y]]
], dtype="float32")

# M = cv2.getPerspectiveTransform(
#     loaded_contour.reshape(4, 2).astype(np.float32),
#     np.array([[0, 0], [w, 0], [w, h], [0, h]], dtype=np.float32)
# )

# # Trasforma i punti nella nuova prospettiva
# campo_nuovo = cv2.perspectiveTransform(campo, M)

#print("Campo trasformato:", campo_nuovo)

#(x1, y1), (x2, y2) = campo_nuovo.reshape(2, 2)

#start_point = (int(x1), int(y1))
#end_point = (int(x2), int(y2))

color = (0, 0, 255)  # rosso
thickness = 2

s = (int(P1_x),int(P1_y))
e = (int(P2_x), int(P2_y))

print(s)
print(e)

#cv2.rectangle(img, start_point, end_point, color, thickness)

cv2.rectangle(img, s, e, color, thickness)

cv2.imwrite("Campo_trasformato2.jpg", img)

# P2_x_error = 0.3395560383796692 + p1_x_err
# P2_y_error = 0.2930818498134613 + p1_y_err

# base_dir = os.path.dirname(os.path.abspath(__file__)) 
# p = os.path.join(base_dir, 'Test3', 'output.json')

# with open('response.json', 'r', encoding='utf-8') as file:
#     data = json.load(file)

# with open(p, 'r', encoding='utf-8') as file:
#     data1 = json.load(file)

# blocchi1 = data1["Blocks"]
# blocchi = data["Blocks"]

# # error_x1, error_y1 = find_left_top_point(blocchi1)
# # error_x, error_y = find_left_top_point(blocchi)

# find_points(blocchi)

# height, width = img.shape[:2]

# p1_x_err = abs(error_x1 - error_x)
# p1_y_err = abs(error_y1 - error_y)


# print(p1_x_err)
# print(p1_y_err)

# P1_x_error = 0.04616007208824158 - p1_x_err
# P1_y_error = 0.2436360865831375 - p1_y_err

# P2_x_error = 0.3395560383796692 + p1_x_err
# P2_y_error = 0.2930818498134613 + p1_y_err

# P3_x = 0.1115032434463501 - p1_x_err
# P3_y = 0.8902167677879333 - p1_y_err
# P4_x = 0.9303025007247925
# P4_y = 0.9041821956634521 

# P5_x = 0.7805507183074951 - p1_x_err
# P5_y = 0.9298563003540039 - p1_y_err
# P6_x = 0.9161749482154846 + p1_x_err
# P6_y = 0.9413824081420898 + p1_y_err

# P3 = {"X": P3_x, "Y": P3_y}
# P4 = {"X": P4_x, "Y": P4_y}

# P5 = {"X": P5_x, "Y": P5_y}
# P6 = {"X": P6_x, "Y": P6_y}

# P1 = {"X": P1_x_error, "Y": P1_y_error}
# P2 = {"X": P2_x_error, "Y": P2_y_error}

# # Converti le coordinate in pixel
# x1 = int(P1["X"] * width)
# y1 = int(P1["Y"] * height)
# x2 = int(P2["X"] * width)
# y2 = int(P2["Y"] * height)

# x3 = int(P3["X"] * width)
# y3 = int(P3["Y"] * height)
# x4 = int(P4["X"] * width)
# y4 = int(P4["Y"] * height)

# x5 = int(P5["X"] * width)
# y5 = int(P5["Y"] * height)
# x6 = int(P6["X"] * width)
# y6 = int(P6["Y"] * height)

# cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
# cv2.rectangle(img, (x3, y3), (x4, y4), (0, 255, 0), 1)
# cv2.rectangle(img, (x5, y5), (x6, y6), (0, 255, 0), 1)

# search_line(data1, P1, P2)
# search_line(data1, P3, P4)
# search_line(data1, P5, P6)

# cv2.imwrite("Test3/immagine_output.jpg", img)