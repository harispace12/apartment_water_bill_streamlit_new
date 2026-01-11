import easyocr
import re
import cv2
import numpy as np

# Initialize once (important for performance)
reader = easyocr.Reader(['en'], gpu=False)
def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Reduce noise
    img = cv2.GaussianBlur(img, (5, 5), 0)

    # Improve contrast for handwriting
    img = cv2.adaptiveThreshold(
        img, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV,
        15, 4
    )

    return img
def extract_meter_readings(image_path):
    processed_img = preprocess_image(image_path)

    results = reader.readtext(processed_img)

    readings = []
    for _, text, confidence in results:
        if confidence < 0.4:
            continue

        numbers = re.findall(r'\d{4,}', text)
        for n in numbers:
            readings.append({
                "reading": int(n),
                "confidence": round(confidence * 100, 2)
            })

    return readings   
def extract_readings_from_image(image_path):
    results = reader.readtext(image_path)

    readings = []
    for bbox, text, confidence in results:
        text = text.upper().replace("I", "1").replace("O", "0")
        match = re.match(r'(G[1-9]|[1-5]0[1-9])\s*[-:]?\s*(\d+)', text)
        if match:
            flat = match.group(1)
            value = int(match.group(2))
            readings.append({
                "flat": flat,
                "reading": value,
                "confidence": round(confidence * 100, 2)
            })

    return readings
