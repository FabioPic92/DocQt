import cv2
import numpy as np
import glob


def order_points(pts):
    '''Rearrange coordinates to order:
       top-left, top-right, bottom-right, bottom-left'''
    rect = np.zeros((4, 2), dtype='float32')
    pts = np.array(pts)
    s = pts.sum(axis=1)
    # Top-left point will have the smallest sum.
    rect[0] = pts[np.argmin(s)]
    # Bottom-right point will have the largest sum.
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    # Top-right point will have the smallest difference.
    rect[1] = pts[np.argmin(diff)]
    # Bottom-left will have the largest difference.
    rect[3] = pts[np.argmax(diff)]
    # return the ordered coordinates
    return rect.astype('int').tolist()

# def find_document_corners(canny):
#     contours, _ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
#     page = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

#     for c in page:
#         epsilon = 0.02 * cv2.arcLength(c, True)
#         corners = cv2.approxPolyDP(c, epsilon, True)
#         if len(corners) == 4:
#             return order_points(np.concatenate(corners).tolist())
#     return None

# def find_corners_with_hough(canny):
#     lines = cv2.HoughLinesP(canny, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=20)
#     if lines is None:
#         return None

#     points = []
#     for line in lines:
#         x1, y1, x2, y2 = line[0]
#         points.append([x1, y1])
#         points.append([x2, y2])
    
#     points = np.array(points)

#     if len(points) < 4:
#         return None

#     points = np.array(points)
#     rect = cv2.minAreaRect(points)
#     box = cv2.boxPoints(rect)

#     return order_points(box)

# def draw_detected_corners(image, corners, color=(0, 255, 0)):
#     img_debug = image.copy()
#     for i, point in enumerate(corners):
#         x, y = map(int, point)
#         cv2.circle(img_debug, (x, y), 10, color, -1)
#         cv2.putText(img_debug, str(i), (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
#     return img_debug

# def scan(img):
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

#     # Adaptive threshold + Canny
#     thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                                    cv2.THRESH_BINARY, 15, 10)
#     canny = cv2.Canny(thresh, 50, 200)
#     canny = cv2.dilate(canny, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21)))

#     # 🔍 Prova con i contorni classici
#     corners = find_document_corners(canny)

#     # 🔁 Se fallisce, prova con Hough Lines
#     if corners is None:
#         print("Fallback con HoughLines...")
#         corners = find_corners_with_hough(canny)

#     if corners is None or len(corners) != 4:
#         print("Documento non rilevato. Ritorno immagine originale.")
#         return orig_img

#     debug_img = draw_detected_corners(orig_img, corners)
#     cv2.imwrite("debug_corners.jpg", debug_img)

#     # Calcolo dimensioni
#     w1 = np.linalg.norm(np.array(corners[0]) - np.array(corners[1]))
#     w2 = np.linalg.norm(np.array(corners[2]) - np.array(corners[3]))
#     h1 = np.linalg.norm(np.array(corners[0]) - np.array(corners[2]))
#     h2 = np.linalg.norm(np.array(corners[1]) - np.array(corners[3]))
#     w = max(int(w1), int(w2))
#     h = max(int(h1), int(h2))

#     print("Warping size:", w, h)

#     destination_corners = order_points(np.array([[0, 0], [w - 1, 0], [w - 1, h - 1], [0, h - 1]]))

#     print("Detected corners:", corners)
#     print("Destination corners:", destination_corners)

#     # Omografia e warping
#     homography, _ = cv2.findHomography(np.float32(corners), np.float32(destination_corners), cv2.RANSAC, 3.0)

#     if homography is None:
#         print("⚠️ Homography fallita!")
#         return orig_img

#     un_warped = cv2.warpPerspective(orig_img, homography, (w, h))

#     return un_warped


def scan(img):
    # Resize image to workable size
    dim_limit = 2160
    max_dim = max(img.shape)
    if max_dim > dim_limit:
        resize_scale = dim_limit / max_dim
        img = cv2.resize(img, None, fx=resize_scale, fy=resize_scale)

    # Create a copy of resized original image for later use
    orig_img = img.copy()
    # Repeated Closing operation to remove text from the document.
    kernel = np.ones((5, 5), np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=5)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (11, 11), 0)
    # Edge Detection.
    canny = cv2.Canny(gray, 0, 200)
    canny = cv2.dilate(canny, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21)))

    # Finding contours for the detected edges.
    contours, hierarchy = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # Keeping only the largest detected contour.
    page = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

    # Detecting Edges through Contour approximation
    if len(page) == 0:
        return orig_img
    # loop over the contours
    for c in page:
        # approximate the contour
        epsilon = 0.02 * cv2.arcLength(c, True)
        corners = cv2.approxPolyDP(c, epsilon, True)
        # if our approximated contour has four points
        if len(corners) == 4:
            break
    # Sorting the corners and converting them to desired shape.
    corners = sorted(np.concatenate(corners).tolist())
    # For 4 corner points being detected.
    # Rearranging the order of the corner points.
    corners = order_points(corners)

    # Finding Destination Co-ordinates
    w1 = np.sqrt((corners[0][0] - corners[1][0]) ** 2 + (corners[0][1] - corners[1][1]) ** 2)
    w2 = np.sqrt((corners[2][0] - corners[3][0]) ** 2 + (corners[2][1] - corners[3][1]) ** 2)
    # Finding the maximum width.
    w = max(int(w1), int(w2))

    h1 = np.sqrt((corners[0][0] - corners[2][0]) ** 2 + (corners[0][1] - corners[2][1]) ** 2)
    h2 = np.sqrt((corners[1][0] - corners[3][0]) ** 2 + (corners[1][1] - corners[3][1]) ** 2)
    # Finding the maximum height.
    h = max(int(h1), int(h2))

    # Final destination co-ordinates.
    destination_corners = order_points(np.array([[0, 0], [w - 1, 0], [0, h - 1], [w - 1, h - 1]]))

    h, w = orig_img.shape[:2]
    # Getting the homography.
    homography, mask = cv2.findHomography(np.float32(corners), np.float32(destination_corners), method=cv2.RANSAC,
                                          ransacReprojThreshold=3.0)
    # Perspective transform using homography.
    un_warped = cv2.warpPerspective(orig_img, np.float32(homography), (w, h), flags=cv2.INTER_LINEAR)
    # Crop
    final = un_warped[:destination_corners[2][1], :destination_corners[2][0]]
    return final


img = cv2.imread("Test.jpg")

scanned_img = scan(img)

# cv2.imshow("scanner", scanned_img)    
cv2.imwrite("outputs1.jpg", scanned_img)
print("scanned")

cv2.destroyAllWindows()