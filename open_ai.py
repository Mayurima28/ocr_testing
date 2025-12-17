import base64
from openai import OpenAI

client = OpenAI()

IMAGE_PATH = "test_image.jpeg"   # your handwritten image


def image_to_data_url(image_path):
    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/jpeg;base64,{b64}"


def analyze_handwritten_image(image_path):
    image_data_url = image_to_data_url(image_path)

    response = client.responses.create(
        model="gpt-4o",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "This is a scanned handwritten grievance letter. "
                            "The text may be in Bengali, English, or mixed.\n\n"
                            "Tasks:\n"
                            "1. Accurately read the handwritten text\n"
                            "2. Identify the language (Bengali / English / Mixed)\n"
                            "3. Provide a clear English summary"
                        )
                    },
                    {
                        "type": "input_image",
                        "image_url": image_data_url
                    }
                ]
            }
        ]
    )

    return response.output_text


if __name__ == "__main__":
    result = analyze_handwritten_image(IMAGE_PATH)
    print("\n=== GPT-4o Vision Output ===\n")
    print(result)
