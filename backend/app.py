from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai
import os
import re
import subprocess
import uuid
import shutil
from prompts import SYSTEM_PROMPT

load_dotenv()
app = Flask(__name__)
CORS(app)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MEDIA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media')
os.makedirs(MEDIA_DIR, exist_ok=True)

def clear_media_directory():
    """Delete all previously rendered videos from the media directory"""
    try:
        for item in os.listdir(MEDIA_DIR):
            item_path = os.path.join(MEDIA_DIR, item)
            # Only remove directories (each job has its own directory)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            # Also remove Python files that were generated
            elif item.endswith('.py'):
                os.remove(item_path)
        print("Cleared all previous videos")
    except Exception as e:
        print(f"Error clearing media directory: {e}")

def extract_manim_code(response_text):
    python_blocks = re.findall(r'```python(.*?)```', response_text, re.DOTALL)
    if python_blocks:
        return python_blocks[0].strip()
    
    code_blocks = re.findall(r'```(.*?)```', response_text, re.DOTALL)
    if code_blocks:
        return code_blocks[0].strip()
    
    if response_text.strip().startswith("from manim import") or "class" in response_text and "Scene):" in response_text:
        return response_text
    
    class_match = re.search(r'class\s+\w+\(Scene\):(.*?)(?=$|class\s+\w+\()', response_text, re.DOTALL)
    if class_match:
        code = class_match.group(0).strip()
        if "from manim import" not in code:
            return f"from manim import *\n\n{code}"
        return code
    
    return ""

def render_manim_video(python_file, job_id):
    output_dir = os.path.join(MEDIA_DIR, job_id)
    os.makedirs(output_dir, exist_ok=True)
    
    cmd = [
        "manim",
        "-ql",
        "--media_dir", output_dir,
        "-o", "video.mp4",
        python_file
    ]
    
    process = subprocess.run(cmd, capture_output=True, text=True)
    
    if process.returncode != 0:
        raise Exception(f"Manim rendering failed: {process.stderr}")
    
    for root, _, files in os.walk(output_dir):
        for file in files:
            if file.endswith(".mp4"):
                return os.path.join(root, file)
    
    raise Exception("No video file was generated")


# ------------------- Routes-------------------
@app.route("/", methods=["GET"])
def home():
    return "Math Visualizer AI Backend"

@app.route("/query", methods=["POST"])
def query():
    clear_media_directory()

    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    if not data["prompt"]:
        return jsonify({"error": "No prompt provided"}), 400
    user_prompt = data["prompt"]
    gemini_query = f"System instructions: {SYSTEM_PROMPT} User Prompt: {user_prompt}"

    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents=gemini_query
    )

    response_extracted = extract_manim_code(response.text)
    
    job_id = str(uuid.uuid4())
    python_file = os.path.join(MEDIA_DIR, f"{job_id}.py")
    
    with open(python_file, "w", encoding="utf-8") as f:
        f.write(response_extracted)
    
    try:
        video_path = render_manim_video(python_file, job_id)
        return jsonify({
            "code": response_extracted,
            "video_url": f"/videos/{job_id}/video.mp4"
        })
    except Exception as e:
        return jsonify({
            "code": response_extracted,
            "error": f"Failed to render video: {str(e)}"
        }), 500

@app.route("/videos/<job_id>/<filename>", methods=["GET"])
def serve_video(job_id, filename):
    for root, _, files in os.walk(os.path.join(MEDIA_DIR, job_id)):
        for file in files:
            if file.endswith(".mp4"):
                return send_from_directory(root, file)
    
    return jsonify({"error": "Video not found"}), 404


# ------------------- Run Server -------------------
port = int(os.getenv("PORT", 4000))
app.run(host="0.0.0.0",port=port)