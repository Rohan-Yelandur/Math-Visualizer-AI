from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.route("/", methods=["GET"])
def home():
    return "Math Visualizer AI Backend"

@app.route("/query", methods=["POST"])
def query():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    if not data["prompt"]:
        return jsonify({"error": "No prompt provided"}), 400
    user_prompt = data["prompt"]


    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents=user_prompt
    )
    return response.text

port = 4000
app.run(host="127.0.0.1", port=port)