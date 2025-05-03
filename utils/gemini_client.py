import os
from google import genai
from dotenv import load_dotenv
import re

class GeminiClient:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        self.client = genai.Client(api_key=api_key)

    def generate_manim_code(self, user_prompt):

        system_prompt = """
            You are an AI tutor that helps to visualize math concepts.
            Return ONLY executable Python code without any explanations, comments about the scene code, or formatting.
            The Scene class MUST be named 'ManimVisualization' (exactly this name).
            Include only necessary imports and the scene class definition.
            Ensure that the code you output is correct and will render in manim. Take your time to ensure accuracy.
        """

        model_query = f"""
            System prompt: {system_prompt}.
            User prompt: {user_prompt}
        """

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[model_query]
        )
        raw_text = response.text

        # Remove possible unncessary formatting in Gemini's resposne
        code_block_pattern = r"```python\s*(.*?)```"
        code_matches = re.findall(code_block_pattern, raw_text, re.DOTALL)
        if code_matches:
            return code_matches[0].strip()
        lines = raw_text.split('\n')
        code_lines = []
        in_code = False  
        for line in lines:
            if not in_code and (line.startswith('from') or line.startswith('import') or line.startswith('class')):
                in_code = True      
            if in_code:
                if line and not line.strip().startswith('#') and not any(keyword in line for keyword in ['import', 'class', 'def', '    ', '(', ')', '=', '+', '-', '*', '/', '[', ']']):
                    if not line.strip():
                        continue
                    break
                code_lines.append(line)
        if code_lines:
            return '\n'.join(code_lines)
        
        return raw_text