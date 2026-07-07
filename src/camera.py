# camera.py
import cv2
import os

TEMP_IMG = "temp_image.jpg"

def capture_image(output_path=TEMP_IMG):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise RuntimeError("Camera could not be opened")

    ret, frame = cap.read()
    cap.release()

    if not ret:
        raise RuntimeError("Failed to capture image")

    cv2.imwrite(output_path, frame)
    return output_path
