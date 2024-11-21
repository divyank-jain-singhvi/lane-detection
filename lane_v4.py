import cv2
import numpy as np
def roi_mask(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    return cv2.bitwise_and(img, mask)


def detect_lanes(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 140, 270)

    height, width = image.shape[:2]
    roi_vertices = [(0, height), (0, height * 0.25), (width, height * 0.25), (width, height)]
    roi_image = roi_mask(edges, [np.array([roi_vertices], dtype=np.int32)])

    lines = cv2.HoughLinesP(roi_image, rho=1, theta=np.pi / 180, threshold=20, minLineLength=20, maxLineGap=300)
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return gray, edges, roi_image, cv2.addWeighted(image, 0.8, line_image, 1, 0)


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
while True:
    ret, frame = cap.read()
    gray, edges, roi, result = detect_lanes(frame)
    # cv2.imshow('Grayscale', gray)
    # cv2.imshow('Canny Edges', edges)
    # cv2.imshow('ROI Mask', roi)
    cv2.imshow('Live Lane Detection', result)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()