from flask import Flask, jsonify, request
from google import genai
from dotenv import load_dotenv
import os

# Load API key from .env
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)

@app.route("/")
def home():
    return "Backend is running!"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()

    question = data.get("question", "")

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=question
    )

    return jsonify({
        "answer": response.text
    })

if __name__ == "__main__":
    app.run(debug=True)