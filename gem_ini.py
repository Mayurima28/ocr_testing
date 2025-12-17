from flask import Flask, request, render_template_string
import google.generativeai as genai
from PIL import Image
import io

# ---------------- CONFIG ----------------
API_KEY = "AIzaSyAn5or8RDID5qFEXdVXsKx5703PpXKXM8g"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

app = Flask(__name__)

# ---------------- HTML TEMPLATE ----------------
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Bengali OCR & Translation</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #0f172a;
            color: #e5e7eb;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .card {
            background: #020617;
            padding: 25px;
            width: 500px;
            border-radius: 12px;
            box-shadow: 0 0 20px rgba(0,0,0,0.6);
        }
        h2 {
            text-align: center;
            margin-bottom: 15px;
        }
        input[type=file] {
            width: 100%;
            margin-bottom: 15px;
        }
        button {
            width: 100%;
            padding: 10px;
            background: #2563eb;
            border: none;
            color: white;
            font-size: 16px;
            border-radius: 6px;
            cursor: pointer;
        }
        button:hover {
            background: #1d4ed8;
        }
        textarea {
            width: 100%;
            height: 120px;
            margin-top: 10px;
            background: #020617;
            color: #e5e7eb;
            border: 1px solid #334155;
            border-radius: 6px;
            padding: 8px;
        }
        label {
            margin-top: 10px;
            display: block;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="card">
        <h2>Bengali OCR + English Translation</h2>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="image" required>
            <button type="submit">Process Image</button>
        </form>

        {% if bengali %}
            <label>Bengali Text</label>
            <textarea readonly>{{ bengali }}</textarea>

            <label>English Translation</label>
            <textarea readonly>{{ english }}</textarea>
        {% endif %}
    </div>
</body>
</html>
"""

# ---------------- ROUTE ----------------
@app.route("/", methods=["GET", "POST"])
def index():
    bengali_text = ""
    english_text = ""

    if request.method == "POST":
        file = request.files["image"]
        image = Image.open(io.BytesIO(file.read()))

        prompt = """
        Extract the Bengali text from this image.
        Then translate it into English.
        Respond strictly in this format:

        Bengali:
        <bengali text>

        English:
        <english translation>
        """

        response = model.generate_content([prompt, image])
        output = response.text

        # Simple parsing
        if "Bengali:" in output and "English:" in output:
            bengali_text = output.split("Bengali:")[1].split("English:")[0].strip()
            english_text = output.split("English:")[1].strip()
        else:
            bengali_text = output
            english_text = "Could not parse translation"

    return render_template_string(
        HTML,
        bengali=bengali_text,
        english=english_text
    )

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
