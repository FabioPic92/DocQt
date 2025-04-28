import cv2
import numpy as np
import glob
from imutils.perspective import four_point_transform

output_image = "Data/Result/ImagePreprocessed.jpg"

font = cv2.FONT_HERSHEY_SIMPLEX


def scan_detection(image):
    global document_contour

    WIDTH, HEIGHT = image.shape[:2]

    document_contour = np.array([[0, 0], [WIDTH, 0], [WIDTH, HEIGHT], [0, HEIGHT]])

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, threshold = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    max_area = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.03 * peri, True)
            if area > max_area and len(approx) == 4:
                document_contour = approx
                max_area = area
    return document_contour


def scan(img, DocumentData):
    document_contour = scan_detection(img)
    warped = four_point_transform(img, document_contour.reshape(4, 2))

    DocumentData.filename_image_processed = output_image
    cv2.imwrite(output_image, warped)
    return warped, document_contour

# def order_points(pts):
#     rect = np.zeros((4, 2), dtype='float32')
#     pts = np.array(pts)
#     s = pts.sum(axis=1)

#     rect[0] = pts[np.argmin(s)]
#     rect[2] = pts[np.argmax(s)]

#     diff = np.diff(pts, axis=1)

#     rect[1] = pts[np.argmin(diff)]
#     rect[3] = pts[np.argmax(diff)]

#     return rect.astype('int').tolist()

# def scan(img, DocumentData):
#     dim_limit = 2160
#     max_dim = max(img.shape)
#     if max_dim > dim_limit:
#         resize_scale = dim_limit / max_dim
#         img = cv2.resize(img, None, fx=resize_scale, fy=resize_scale)

#     orig_img = img.copy()

#     kernel = np.ones((5, 5), np.uint8)
#     img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=5)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     gray = cv2.GaussianBlur(gray, (11, 11), 0)

#     canny = cv2.Canny(gray, 0, 200)
#     canny = cv2.dilate(canny, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21)))

#     contours, hierarchy = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
#     page = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

#     if len(page) == 0:
#         return orig_img
#     for c in page:
#         epsilon = 0.02 * cv2.arcLength(c, True)
#         corners = cv2.approxPolyDP(c, epsilon, True)

#         if len(corners) == 4:
#             break

#     corners = sorted(np.concatenate(corners).tolist())
#     corners = order_points(corners)

#     w1 = np.sqrt((corners[0][0] - corners[1][0]) ** 2 + (corners[0][1] - corners[1][1]) ** 2)
#     w2 = np.sqrt((corners[2][0] - corners[3][0]) ** 2 + (corners[2][1] - corners[3][1]) ** 2)
#     w = max(int(w1), int(w2))

#     h1 = np.sqrt((corners[0][0] - corners[2][0]) ** 2 + (corners[0][1] - corners[2][1]) ** 2)
#     h2 = np.sqrt((corners[1][0] - corners[3][0]) ** 2 + (corners[1][1] - corners[3][1]) ** 2)
#     h = max(int(h1), int(h2))

#     destination_corners = order_points(np.array([[0, 0], [w - 1, 0], [0, h - 1], [w - 1, h - 1]]))

#     h, w = orig_img.shape[:2]

#     homography, mask = cv2.findHomography(np.float32(corners), np.float32(destination_corners), method=cv2.RANSAC,
#                                           ransacReprojThreshold=3.0)
    
#     un_warped = cv2.warpPerspective(orig_img, np.float32(homography), (w, h), flags=cv2.INTER_LINEAR)

#     final = un_warped[:destination_corners[2][1], :destination_corners[2][0]]
#     DocumentData.filename_image_processed = output_image
#     cv2.imwrite(output_image, final)
#     return final
