import cv2
import numpy as np
from imutils.perspective import four_point_transform



font = cv2.FONT_HERSHEY_SIMPLEX

WIDTH, HEIGHT = 1920, 1080

def image_processing(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    white_ratio = np.sum(threshold == 255) / (threshold.shape[0] * threshold.shape[1])
    if white_ratio < 0.5:
        threshold = cv2.bitwise_not(threshold)

    return threshold


def scan_detection(image):
    global document_contour

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

def center_text(image, text):
    text_size = cv2.getTextSize(text, font, 2, 5)[0]
    text_x = (image.shape[1] - text_size[0]) // 2
    text_y = (image.shape[0] + text_size[1]) // 2
    cv2.putText(image, text, (text_x, text_y), font, 2, (255, 0, 255), 5, cv2.LINE_AA)


img =cv2.imread("Test4.jpg")

scan_detection(img)

warped = four_point_transform(img, document_contour.reshape(4, 2))

cv2.imwrite("scanned_output1.jpg", warped)

processed = image_processing(warped)
processed = processed[10:processed.shape[0] - 10, 10:processed.shape[1] - 10]

kernel = np.ones((2, 2), np.uint8)
processed = cv2.morphologyEx(processed, cv2.MORPH_OPEN, kernel)
processed = cv2.morphologyEx(processed, cv2.MORPH_CLOSE, kernel)

cv2.imwrite("scanned_output.jpg", processed)