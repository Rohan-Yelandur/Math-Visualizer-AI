import streamlit as st
import os
import tempfile
import shutil
from utils.gemini_client import GeminiClient
from utils.manim_renderer import ManimRenderer
import sys

st.set_page_config(
    page_title="Math Visualizer AI",
    page_icon="🧮",
    layout="wide",
)

def init_session_state():
    if "history" not in st.session_state:
        st.session_state.history = []
    if "gemini_client" not in st.session_state:
        try:
            st.session_state.gemini_client = GeminiClient()
        except ValueError as e:
            st.error(f"Error initializing Gemini client: {str(e)}")
            st.session_state.gemini_client = None
    if "manim_renderer" not in st.session_state:
        st.session_state.manim_renderer = ManimRenderer()

def main():
    init_session_state()
    
    st.title("Math Visualizer AI 🧮")
    st.write("Enter a mathematical concept, and the AI will generate a visualization using Manim.")
    
    # Input area
    with st.form("prompt_form"):
        prompt = st.text_area("Describe the mathematical concept you want to visualize", 
                              height=100,
                              placeholder="Example: Show the unit circle and animate the relationship between sine and cosine functions")
        submitted = st.form_submit_button("Generate Visualization")
    
    # When form is submitted
    if submitted:
        if not st.session_state.gemini_client:
            st.error("Please set up your Google API key in the .env file.")
            return
            
        with st.spinner("Generating Manim code with Gemini..."):
            manim_code = st.session_state.gemini_client.generate_manim_code(prompt)
        
        if manim_code.startswith("Error"):
            st.error(manim_code)
            return
            
        with st.expander("Generated Manim Code", expanded=True):
            st.code(manim_code, language="python")
        
        with st.spinner("Rendering animation with Manim..."):
            video_path, error = st.session_state.manim_renderer.render_manim_code(manim_code)
        
        st.session_state.history.append({
            "prompt": prompt,
            "code": manim_code,
            "video_path": video_path
        })
        
        # Only try to display the video if a path was returned
        if video_path:
            st.success("Visualization generated successfully!")
            with open(video_path, "rb") as file:
                video_bytes = file.read()
                st.video(video_bytes)
        else:
            st.warning("No video was generated. You can try different parameters or check if Manim is installed correctly.")
    
    # Show history with error handling
    if st.session_state.history:
        st.write("---")
        st.subheader("Previous Visualizations")
        for i, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"{i+1}. {item['prompt'][:50]}..."):
                # Only try to show video if path exists
                if item['video_path'] and os.path.exists(item['video_path']):
                    with open(item['video_path'], "rb") as file:
                        video_bytes = file.read()
                        st.video(video_bytes)
                elif item['video_path'] is None:
                    st.info("No video was generated for this visualization.")
                else:
                    st.info("Video file no longer exists.")
                
                st.code(item['code'], language="python")

if __name__ == "__main__":
    main()