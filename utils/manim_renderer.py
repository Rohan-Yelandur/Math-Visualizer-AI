import os
import sys
import tempfile
import subprocess
from pathlib import Path
import glob

class ManimRenderer:
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        
    def render_manim_code(self, manim_code):
        # Validate the scene class name
        if "class ManimVisualization" not in manim_code:
            manim_code = self._fix_scene_class_name(manim_code)
            
        # Create a temporary Python file with the Manim code
        temp_file = Path(self.temp_dir) / "manim_scene.py"
        with open(temp_file, "w") as f:
            f.write(manim_code)
        
        # Create output directory if it doesn't exist
        output_dir = Path(self.temp_dir) / "media"
        output_dir.mkdir(exist_ok=True)

        # Try different quality options if needed
        for quality_option in ["-qm", "-ql"]:  # Try medium quality first, then low quality
            try:
                # Execute manim command to render the scene
                cmd = [
                    sys.executable, "-m", 
                    "manim", str(temp_file), "ManimVisualization", 
                    quality_option, "--media_dir", str(output_dir)
                ]
                
                # Execute the command and capture output
                result = subprocess.run(
                    cmd, 
                    capture_output=True, 
                    text=True, 
                    check=False
                )
                
                # If the command succeeded, look for the video
                if result.returncode == 0:
                    # Search more broadly for any video files
                    video_path = self._find_video_file(output_dir)
                    if video_path:
                        return video_path, ""
                    else:
                        print(f"No video found after successful rendering with {quality_option}")
                else:
                    print(f"Manim error: {result.stderr}")
            
            except Exception as e:
                print(f"Exception during rendering with {quality_option}: {str(e)}")
        
        return None, "No video file was generated. Please check the terminal for more information."
    
    def _find_video_file(self, output_dir):
        """Search for video files in the output directory structure."""
        # Check common resolution directories
        for res_dir in ["480p15", "1080p60", "720p30", "480p30", "240p15"]:
            # Check both manim_scene and any other potential directory names
            for scene_dir in ["manim_scene", ".", "scene"]:
                # Construct potential directory path
                video_dir = output_dir / "videos" / scene_dir
                if not video_dir.exists():
                    continue
                    
                if res_dir == ".":
                    # Look directly in the videos directory
                    pattern = str(video_dir / "*.mp4")
                else:
                    # Look in the resolution subdirectory
                    pattern = str(video_dir / res_dir / "*.mp4")
                
                # Use glob to find any mp4 files
                video_files = glob.glob(pattern)
                if video_files:
                    return video_files[0]
        
        # If no files found in typical locations, search more broadly
        all_video_files = glob.glob(str(output_dir / "**" / "*.mp4"), recursive=True)
        if all_video_files:
            print(f"Found video at: {all_video_files[0]}")
            return all_video_files[0]
            
        return None