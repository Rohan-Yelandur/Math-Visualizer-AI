from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai
import os
import re
import subprocess
import uuid
from prompts import SYSTEM_PROMPT

load_dotenv()
app = Flask(__name__)
CORS(app)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MEDIA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media')
os.makedirs(MEDIA_DIR, exist_ok=True)

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
    gemini_query = f"System instructions: {SYSTEM_PROMPT} User Prompt: {user_prompt}"

    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents=gemini_query
    )

    response_extracted = extract_manim_code(response.text)
    
    # Generate a unique ID for this job
    job_id = str(uuid.uuid4())
    python_file = os.path.join(MEDIA_DIR, f"{job_id}.py")
    
    # Write the extracted code to a file
    with open(python_file, "w", encoding="utf-8") as f:
        f.write(response_extracted)
    
    # Render the Manim video
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

def extract_manim_code(response_text):
    # Look for Python code blocks in markdown format
    python_blocks = re.findall(r'```python(.*?)```', response_text, re.DOTALL)
    if python_blocks:
        return python_blocks[0].strip()
    
    # Look for code blocks without language specifier
    code_blocks = re.findall(r'```(.*?)```', response_text, re.DOTALL)
    if code_blocks:
        return code_blocks[0].strip()
    
    # Check if the entire response is already Python code
    if response_text.strip().startswith("from manim import") or "class" in response_text and "Scene):" in response_text:
        return response_text
    
    # Look for class definitions that match Manim patterns
    class_match = re.search(r'class\s+\w+\(Scene\):(.*?)(?=$|class\s+\w+\()', response_text, re.DOTALL)
    if class_match:
        # If we find a class definition, ensure it has the necessary imports
        code = class_match.group(0).strip()
        if "from manim import" not in code:
            return f"from manim import *\n\n{code}"
        return code
    
    # If we can't identify code clearly, return empty string
    return ""

def render_manim_video(python_file, job_id):
    """Render the Manim video using the provided Python file."""
    output_dir = os.path.join(MEDIA_DIR, job_id)
    os.makedirs(output_dir, exist_ok=True)
    
    # Run manim with -ql flag (quality low) for faster rendering
    # The -o flag tells manim to render all scenes to the output file
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
    
    # Manim creates files in a nested directory structure
    # This will find the .mp4 file regardless of its exact location
    for root, _, files in os.walk(output_dir):
        for file in files:
            if file.endswith(".mp4"):
                return os.path.join(root, file)
    
    raise Exception("No video file was generated")

@app.route("/videos/<job_id>/<filename>", methods=["GET"])
def serve_video(job_id, filename):
    """Serve the rendered video file."""
    # Look for the video file in the job directory
    for root, _, files in os.walk(os.path.join(MEDIA_DIR, job_id)):
        for file in files:
            if file.endswith(".mp4"):
                return send_from_directory(root, file)
    
    return jsonify({"error": "Video not found"}), 404


port = int(os.getenv("PORT", 4000))
app.run(host="0.0.0.0", port=port)