import pytesseract
import cv2
import re

def extract_readings_from_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)

    readings = []
    for line in text.split("\n"):
        match = re.match(r'([A-Za-z0-9]+)\s*-\s*(\d+)', line)
        if match:
            flat = match.group(1).upper().replace("I", "1")
            value = int(match.group(2))
            readings.append((flat, value))
    return readings
