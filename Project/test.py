from flask import Flask, jsonify, request
from google import genai
from dotenv import load_dotenv
from prompt import SYSTEM_PROMPT
import os

# Load environment variables
load_dotenv()

# Gemini Client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

app = Flask(__name__)

# ---------------------- HOME ----------------------

@app.route("/")
def home():
    return "Backend is running!"

# ---------------------- HEALTH ----------------------

@app.route("/health")
def health():
    return jsonify({
        "success": True,
        "status": "Backend is healthy"
    }), 200

# ---------------------- ASK ----------------------

@app.route("/ask", methods=["POST"])
def ask():
    try:

        # Receive JSON
        data = request.get_json()

        # Check JSON
        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON data received."
            }), 400

        # User Question
        question = data.get("question", "").strip()

        # Phone Type
        phone = data.get("phone", "").strip()

        # Empty Question
        if not question:
            return jsonify({
                "success": False,
                "error": "Question cannot be empty."
            }), 400

        # ---------------- LOGGING ----------------

        print("\n========== NEW REQUEST ==========")
        print("Phone :", phone if phone else "Not Provided")
        print("Question :", question)

        # ---------------- PROMPT ----------------

        prompt = f"""
{SYSTEM_PROMPT}

Phone Type:
{phone if phone else "Not specified"}

User Question:
{question}
"""

        # ---------------- GEMINI ----------------

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        print("Response :", response.text)
        print("=================================\n")

        # ---------------- RETURN ----------------

        return jsonify({
            "success": True,
            "model": "gemini-2.5-flash",
            "answer": response.text
        }), 200

    except Exception as e:

        print("\nERROR:", e)

        return jsonify({
            "success": False,
            "error": "Something went wrong while processing your request.",
            "details": str(e)
        }), 500


# ---------------------- MAIN ----------------------

if __name__ == "__main__":
    app.run(debug=True)