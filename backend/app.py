from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai
import os
import re
import subprocess
import uuid
import shutil
from elevenlabs.client import ElevenLabs
from prompts import SYSTEM_PROMPT

load_dotenv()
app = Flask(__name__)
CORS(app)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
elevenlabs = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
MEDIA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media')
os.makedirs(MEDIA_DIR, exist_ok=True)

def generate_audio_narration(text, output_file):
    """Generate audio narration using ElevenLabs"""
    audio_generator = elevenlabs.text_to_speech.convert(
        voice_id="tnSpp4vdxKPjI9w0GnoV", 
        output_format="mp3_44100_128",
        text=text,
        model_id="eleven_multilingual_v2",
        voice_settings={
            "stability": 1.0,
            "similarity_boost": 0.8,
            "style": 0.3,
            "use_speaker_boost": True
        }
    )
    
    # Collect all audio chunks
    audio_bytes = b''
    for chunk in audio_generator:
        audio_bytes += chunk
    
    # Save audio to file
    with open(output_file, "wb") as f:
        f.write(audio_bytes)
    
    return output_file

def combine_audio_with_video(video_path, audio_path, output_path):
    """Combine video and audio using ffmpeg"""
    cmd = [
        "ffmpeg",
        "-i", video_path,     # Video input
        "-i", audio_path,     # Audio input
        "-c:v", "copy",       # Copy video stream
        "-c:a", "aac",        # Re-encode audio to AAC
        "-map", "0:v:0",      # Use video from first input
        "-map", "1:a:0",      # Use audio from second input
        "-shortest",          # End when shortest input ends
        output_path           # Output file
    ]
    
    process = subprocess.run(cmd, capture_output=True, text=True)
    
    if process.returncode != 0:
        raise Exception(f"Audio-video combination failed: {process.stderr}")
    
    return output_path


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

    # Get content from Gemini
    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents=gemini_query
    )

    # Extract Manim code
    response_extracted = extract_manim_code(response.text)
    
    # Generate a narration prompt for Gemini
    narration_prompt = f"""Based on this user prompt: "{user_prompt}", 
    create a brief, clear narration script (1-3 paragraphs) that explains the mathematical concept being visualized. 
    The narration should accompany the visualization and help explain what is being shown. 
    Keep it concise, educational and engaging."""
    
    # Get narration text from Gemini
    narration_response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents=narration_prompt
    )
    narration_text = narration_response.text
    
    # Create job ID and file paths
    job_id = str(uuid.uuid4())
    python_file = os.path.join(MEDIA_DIR, f"{job_id}.py")
    output_dir = os.path.join(MEDIA_DIR, job_id)
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the Manim code to a file
    with open(python_file, "w", encoding="utf-8") as f:
        f.write(response_extracted)
    
    try:
        # Render the Manim video
        video_path = render_manim_video(python_file, job_id)
        
        # Generate audio narration
        audio_path = os.path.join(output_dir, "narration.mp3")
        generate_audio_narration(narration_text, audio_path)
        
        # Combine video and audio
        combined_video_path = os.path.join(output_dir, "video_with_audio.mp4")
        combine_audio_with_video(video_path, audio_path, combined_video_path)
        
        # Return the combined video URL
        video_filename = os.path.basename(combined_video_path)
        return jsonify({
            "code": response_extracted,
            "narration": narration_text,
            "video_url": f"/videos/{job_id}/{video_filename}"
        })
    except Exception as e:
        return jsonify({
            "code": response_extracted,
            "error": f"Failed to process: {str(e)}"
        }), 500
    
@app.route("/videos/<job_id>/<filename>", methods=["GET"])
def serve_video(job_id, filename):
    for root, _, files in os.walk(os.path.join(MEDIA_DIR, job_id)):
        for file in files:
            if file.endswith(".mp4"):
                return send_from_directory(root, file)
    
    return jsonify({"error": "Video not found"}), 404


# ------------------- Run Server -------------------
if __name__ == "__main__":
    port = int(os.getenv("PORT", 4000))
    app.run(host="0.0.0.0", port=port)