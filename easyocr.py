import easyocr
from langdetect import detect
from openai import OpenAI
import os

# ---------------------------
#  CONFIGURE YOUR API KEY
# ---------------------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------------------
# FUNCTION: LLM SUMMARY
# ---------------------------
def summarize_with_llm(text):
    prompt = f"""
    Summarize the following complaint in clear and short English.
    If the text is in Bengali, translate while summarizing.
    Ignore OCR noise and broken sentences.

    Text:
    {text}
    """

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    return response.output_text


# ---------------------------
# OCR + LANGUAGE DETECTION
# ---------------------------
def run_ocr(image_path):
    print("Running OCR…")
    reader = easyocr.Reader(['bn', 'en'])

    results = reader.readtext(image_path, detail=1)

    text_blocks = []
    for bbox, text, conf in results:
        text_blocks.append(text)

    return " ".join(text_blocks)


# ---------------------------
# MAIN PROGRAM
# ---------------------------
if __name__ == "__main__":
    image_path = "test_image.jpeg"  # CHANGE THIS

    extracted_text = run_ocr(image_path)
    print("\n---- OCR OUTPUT ----")
    print(extracted_text)

    # Detect language
    try:
        language = detect(extracted_text)
    except:
        language = "unknown"

    print("\nDetected Language:", language)

    # LLM Summary
    print("\n---- LLM SUMMARY ----")
    summary = summarize_with_llm(extracted_text)
    print(summary)