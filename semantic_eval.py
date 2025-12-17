from bert_score import score
from langdetect import detect
import os

def load_text(path):
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def semantic_similarity(ref, hyp):
    if not ref or not hyp:
        return None

    # BERTScore expects English
    try:
        if detect(ref) != "en" or detect(hyp) != "en":
            return None
    except:
        return None

    P, R, F1 = score(
        [hyp],
        [ref],
        model_type="roberta-large",
        lang="en",
        verbose=False
    )
    return F1.item()

reference = load_text("original_text.txt")

systems = {
    "EasyOCR": load_text("easyocr_output.txt"),
    "Tesseract": load_text("tesseract_output.txt"),
    "Gemini": load_text("gemini_output.txt")
}

print("\n=== Semantic Similarity (Higher is Better) ===\n")

for name, text in systems.items():
    sim = semantic_similarity(reference, text)

    if sim is None:
        print(f"{name}: N/A (non-English or empty)")
    else:
        print(f"{name}: {sim:.3f}")
