import dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import stream
import os
import subprocess

dotenv.load_dotenv()

elevenlabs = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY"),
)

audio = elevenlabs.text_to_speech.convert(
    voice_id="tnSpp4vdxKPjI9w0GnoV", 
    output_format="mp3_44100_128",
    text="Integration is a complex process, but its purpose is to find the area under a curve. Would you like me to go more in depth?",
    model_id="eleven_multilingual_v2",
    voice_settings={
        "stability": 1.0,
        "similarity_boost": 1.0,
        "style": 0.0,
        "use_speaker_boost": True,
        "speed": 1
    }
)

audio_bytes = b''
for chunk in audio:
    audio_bytes += chunk

# Save audio to a file
audio_file = "narration.mp3"
with open(audio_file, "wb") as f:
    f.write(audio_bytes)

try:
    # To actually play with ffmpeg, use ffplay
    subprocess.run(["ffplay", audio_file])
    print("Audio played with ffplay")
except Exception as e:
    print(f"Could not play audio with ffplay: {e}")
    os.system(f"start {audio_file}")