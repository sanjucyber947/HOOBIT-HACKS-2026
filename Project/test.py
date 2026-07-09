from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Backend is running!"

@app.route("/ask", methods=["POST"])
def ask():
    return jsonify({
        "answer": "Hello! This is a test response."
    })

if __name__ == "__main__":
    app.run(debug=True)