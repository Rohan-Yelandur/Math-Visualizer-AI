import os
from google import genai
from dotenv import load_dotenv

class GeminiClient:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        self.client = genai.Client(api_key=api_key)

    def query_gemini(self):
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents="Write a short haiku about fish."
        )

        print(response.text)

gm = GeminiClient()
gm.query_gemini()