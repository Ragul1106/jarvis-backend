from flask import Flask, request, jsonify
import requests
from flask_cors import CORS  

app = Flask(__name__)
CORS(app)  

OPENROUTER_API_KEY = "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"

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
