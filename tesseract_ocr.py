import pytesseract
from PIL import Image
import cv2
import numpy as np
import os

# -----------------------------
# 1. TESSERACT PATH (Windows)
# -----------------------------
# Change this only if Tesseract is not in PATH
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# -----------------------------
# 2. IMAGE PREPROCESSING
# -----------------------------
def preprocess_image(image_path):
    img = cv2.imread(image_path)

    if img is None:
        raise FileNotFoundError("Image not found")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Noise reduction
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Adaptive threshold (important for handwriting)
    thresh = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11
    )

    return thresh


# -----------------------------
# 3. OCR FUNCTION
# -----------------------------
def run_tesseract(image_path):
    processed = preprocess_image(image_path)

    # OCR config
    config = r'--oem 1 --psm 6'

    text = pytesseract.image_to_string(
        processed,
        lang='ben+eng',
        config=config
    )

    return text


# -----------------------------
# 4. MAIN
# -----------------------------
if __name__ == "__main__":
    image_path = "test_image.jpeg"   # <-- change if needed

    ocr_text = run_tesseract(image_path)

    print("\n--- TESSERACT OCR OUTPUT ---\n")
    print(ocr_text)

    # Save for evaluation
    with open("tesseract_output.txt", "w", encoding="utf-8") as f:
        f.write(ocr_text)

    print("\nSaved output to tesseract_output.txt")
