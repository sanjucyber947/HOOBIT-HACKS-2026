# HOOBIT-HACKS-2026
## Our Project for the HOOBIT HACKS Hackathon
# ElderAsk_AI

##  AI-Powered Smartphone Assistant for Senior Citizens

ElderAsk_AI is an AI-powered Android application designed to help senior citizens use smartphones with confidence. The app provides simple, step-by-step guidance for everyday smartphone tasks using Google's Gemini AI, making technology more accessible and less intimidating.

---

##  Features

-  AI-powered assistance using Google Gemini
-  Floating assistant overlay for quick access
-  Senior-friendly explanations in simple English
-  Step-by-step guidance for smartphone tasks
-  Feedback system to improve future responses
-  Adaptive AI responses based on previous feedback
-  Built-in Frequently Asked Questions (FAQ)

---

##  Tech Stack

### Frontend
- Android
- Kotlin
- Retrofit
- Gson

### Backend
- Python
- Flask
- Google Gemini API
- python-dotenv

### Data Storage
- JSON (feedback history)

---

##  Project Structure

```
EduAsk_AI/
│
├── backend/
│   ├── backend.py
│   ├── prompt.py
│   ├── requirements.txt
│   └── feedback.json
│
├── android/
│   ├── MainActivity.kt
│   ├── OverlayService.kt
│   ├── NetworkModule.kt
│   └── AndroidManifest.xml
│
└── README.md
```

---

##  How It Works

1. The user opens the app.
2. A floating assistant appears on the screen.
3. The user asks a smartphone-related question.
4. The Android app sends the request to the Flask backend.
5. The backend forwards the request to Google Gemini.
6. Gemini generates a clear, easy-to-understand response.
7. The answer is displayed to the user.
8. The user can provide feedback, allowing the system to improve future explanations.

---

##  Backend API

### Health Check

```
GET /health
```

### Ask AI

```
POST /ask
```

Example Request

```json
{
  "question": "How do I increase the volume?",
  "phone": "Samsung Galaxy S23"
}
```

### Submit Feedback

```
POST /feedback
```

Example Request

```json
{
  "question": "How do I increase the volume?",
  "answer": "Press the Volume Up button on the side of your phone.",
  "rating": "good",
  "comments": "Easy to understand"
}
```

### FAQ

```
GET /faq
```

Returns a list of common smartphone-related questions and answers.

---

##  Running the Backend

Install dependencies

```bash
pip install -r requirements.txt
```

Start the server

```bash
python backend.py
```

The backend runs on:

```
http://localhost:5000
```

For testing on a physical Android device, update the `BASE_URL` in `NetworkModule.kt` with your computer's local IPv4 address.

---


## Team

**ElderAsk_AI Development Team**

- Backend Development - Sanjai
- Android Development - Mithraa
- AI Integration - Ruchika
- UI/UX Design - Shivani

---

## Mission

Our mission is to empower senior citizens with technology by providing a friendly AI companion that patiently answers smartphone-related questions, promotes independent digital learning, and makes technology easier for everyone.
