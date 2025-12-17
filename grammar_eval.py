from spellchecker import SpellChecker
import re

spell_en = SpellChecker(language='en')

def load_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().lower()

def grammar_error_rate(text):
    words = re.findall(r"[a-z]+", text)
    if not words:
        return 1.0
    incorrect = sum(1 for w in words if w not in spell_en)
    return incorrect / len(words)

systems = {
    "EasyOCR": load_text("easyocr_output.txt"),
    "Tesseract": load_text("tesseract_output.txt"),
    "Gemini": load_text("gemini_output.txt")
}

print("\n=== Grammar Error Rate (Lower is Better) ===\n")

for name, text in systems.items():
    ger = grammar_error_rate(text)
    print(f"{name}: GER = {ger:.3f}")
