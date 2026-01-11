import easyocr
import re

# Initialize once (important for performance)
reader = easyocr.Reader(['en'], gpu=False)

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
