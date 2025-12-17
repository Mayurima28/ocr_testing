import jiwer

def load_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

original_text = load_text("original_text.txt")

systems = {
    "EasyOCR": load_text("easyocr_output.txt"),
    "Tesseract": load_text("tesseract_output.txt"),
    "Gemini": load_text("gemini_output.txt")
}

print("\n=== OCR Evaluation (Lower is Better) ===\n")

for name, text in systems.items():
    cer = jiwer.cer(original_text, text)
    wer = jiwer.wer(original_text, text)
    print(f"{name}")
    print(f"  CER: {cer:.3f}")
    print(f"  WER: {wer:.3f}\n")
