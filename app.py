from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Replace this with your actual Gemini API key
GEMINI_API_KEY = "AIzaSyDPt5ZqUi_gfoeOUU3GBUcI73tUWqyqBLw"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# In-memory storage for chat history (for demonstration purposes)
chat_history = []

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Step 1: Get user input from the request
        user_input = request.json.get("user_input")
        if not user_input:
            return jsonify({"error": "No user input provided"}), 400

        # Step 2: Add user input to chat history
        chat_history.append({"role": "user", "content": user_input})

        # Step 3: Prepare the payload for Gemini API with chat history
        contents = [
            {"parts": [{"text": entry["content"]}], "role": entry["role"]}
            for entry in chat_history
        ]

        payload = {"contents": contents}

        # Step 4: Call Gemini API
        headers = {"Content-Type": "application/json"}
        response = requests.post(
            GEMINI_API_URL,
            headers=headers,
            params={"key": GEMINI_API_KEY},
            data=json.dumps(payload),
        )

        if response.status_code != 200:
            return (
                jsonify({"error": f"Failed to generate response: {response.text}"}),
                500,
            )

        # Step 5: Parse the response from Gemini API
        gemini_response = response.json()
        candidate = gemini_response.get("candidates", [{}])[0]
        bot_response = (
            candidate.get("content", {}).get("parts", [{}])[0].get("text", "")
        )

        # Step 6: Add bot response to chat history
        chat_history.append({"role": "assistant", "content": bot_response})

        # Step 7: Return the response to the client
        return jsonify(
            {
                "response": bot_response,
                "chat_history": chat_history,
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
