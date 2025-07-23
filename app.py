from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.json
        user_input = data.get("message", "")

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        body = {
            "model": "mistralai/mistral-7b-instruct",  
            "messages": [{"role": "user", "content": user_input}]
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=body
        )

        reply = response.json()["choices"][0]["message"]["content"]
        return jsonify({"response": reply})
    
    except Exception as e:
        return jsonify({"response": "Error: " + str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
