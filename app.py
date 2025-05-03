import streamlit as st

st.title("Math Visualizer AI")
st.write("Enter a math concept, and the AI will draw it out for you.")
with st.form("prompt_form"):
    user_input = st.text_area("Describe the mathematical concept you want to visualize", 
                              height=100,
                              placeholder="Example: Show the unit circle and animate the relationship between sine and cosine functions")
    submitted = st.form_submit_button("Generate Visualization")

if submitted:
    st.write(f"submitted text: {user_input}")