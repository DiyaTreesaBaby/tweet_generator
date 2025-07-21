from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_KEY = ""  # Replace with secure method for production
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    topic = data['topic']
    tone = data['tone']
    audience = data['audience']
    hashtags = data['hashtags']

    prompt = f"""
    You are an expert Content Writer.
    Generate a tweet about the topic "{topic}".
    Use a tone: {tone}.
    Generate it for the audience: {audience}.
    Include the hashtags: {hashtags}.
    Keep it under 280 characters.
    """

    try:
        response = model.generate_content(prompt)
        tweet = response.text.strip()
        return jsonify({"tweet": tweet})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
