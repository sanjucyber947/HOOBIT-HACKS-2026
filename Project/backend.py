import os
import json
from difflib import SequenceMatcher
from flask import Flask, jsonify, request
from google import genai
from dotenv import load_dotenv
from prompt import SYSTEM_PROMPT  # Imported from your initial setup

# Load environment variables
load_dotenv()

# Initialize Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)

# Name of the local JSON storage file
FEEDBACK_FILE = "feedback.json"

# ---------------- FAQ LIST ---------------- #

FAQ = [
    {
        "question": "How do I connect to WiFi?",
        "answer": "Open Settings > Wi-Fi > Turn Wi-Fi ON > Select your network > Enter the password."
    },
    {
        "question": "How do I increase the volume?",
        "answer": "Press the Volume Up button on the side of your phone."
    },
    {
        "question": "How do I send a WhatsApp message?",
        "answer": "Open WhatsApp, choose a contact, type your message, and tap the Send button."
    }
]

# ---------------- HELPERS ---------------- #

def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def find_previous_feedback(question):
    # If the JSON file doesn't exist yet, there is no historical history to search
    if not os.path.exists(FEEDBACK_FILE):
        return None
        
    try:
        with open(FEEDBACK_FILE, "r") as file:
            rows = json.load(file)
    except (json.JSONDecodeError, ValueError):
        # Fallback if file exists but is corrupted or empty
        return None

    best = None
    best_score = 0

    for item in rows:
        q = item.get("question", "")
        ans = item.get("answer", "")
        rating = item.get("rating", "")
        
        score = similarity(question, q)
        if score > best_score:
            best_score = score
            best = (q, ans, rating)

    if best_score > 0.75:
        return best

    return None

# ---------------- ROUTES ---------------- #

@app.route("/")
def home():
    return "Backend is running!"

@app.route("/health")
def health():
    return jsonify({
        "success": True,
        "status": "Backend is healthy"
    }), 200

# Ask AI Endpoint
@app.route("/ask", methods=["POST"])
def ask():
    try:
        # Receive and validate JSON payload
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON data received."
            }), 400

        # Extract values (with .strip() parsing from initial code)
        question = data.get("question", "").strip()
        phone = data.get("phone", "").strip()

        if not question:
            return jsonify({
                "success": False,
                "error": "Question cannot be empty."
            }), 400

        # ---------------- LOGGING ----------------
        print("\n========== NEW REQUEST ==========")
        print("Phone :", phone if phone else "Not Provided")
        print("Question :", question)

        # Check for historical feedback matching this question from JSON
        previous = find_previous_feedback(question)
        
        # Determine prompt structure based on database rating history
        if previous and previous[2].lower() == "bad":
            # Target pivot to senior citizen instructions if previous help failed
            print("Using SIMPLE prompt (previous feedback was BAD)")
            prompt = f"""
            {SYSTEM_PROMPT}
The previous explanation for this question was confusing.

Please explain like you're talking to a senior citizen who has never used a smartphone.

Use:
- Very simple English
- Numbered steps
- No technical jargon
- Return plain text only.
- Do NOT use Markdown formatting such as **bold**, headings (#), bullet symbols (*), or horizontal lines (---).

Phone Type:
{phone if phone else "Not specified"}

Question:
{question}
"""
        else:
            # Standard structural fallback context from your initial system prompt setup
            print("Using NORMAL prompt")
            prompt = f"""
{SYSTEM_PROMPT}

IMPORTANT:
- Return plain text only.
- Do NOT use Markdown formatting such as **bold**, headings (#), bullet symbols (*), or horizontal lines (---).
Phone Type:
{phone if phone else "Not specified"}

User Question:
{question}
"""

        # ---------------- GEMINI API CALL ----------------
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        print("Response :", response.text)
        print("=================================\n")

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

# Save feedback Endpoint (JSON Auto-Creation Version)
@app.route("/feedback", methods=["POST"])
def feedback():
    try:
        data = request.get_json()
        
        new_feedback = {
            "question": data["question"],
            "answer": data["answer"],
            "rating": data["rating"],
            "comments": data.get("comments", "")
        }

        file_data = []

        # 1. Read existing data if the file already exists
        if os.path.exists(FEEDBACK_FILE):
            with open(FEEDBACK_FILE, "r") as file:
                try:
                    file_data = json.load(file)
                except json.JSONDecodeError:
                    # Handle edge-case where file is blank
                    file_data = []

        # 2. Append the new piece of feedback
        file_data.append(new_feedback)

        # 3. Write everything back. "w" mode handles file creation automatically.
        with open(FEEDBACK_FILE, "w") as file:
            json.dump(file_data, file, indent=4)

        return jsonify({
            "success": True,
            "message": "Feedback saved successfully to JSON file."
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to save feedback.",
            "details": str(e)
        }), 500

# Static FAQ Endpoint
@app.route("/faq", methods=["GET"])
def faq():
    return jsonify(FAQ)

if __name__ == "__main__":
    app.run(debug=True)