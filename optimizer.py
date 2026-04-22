import autopep8
import ast
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# 🔑 Gemini API setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")
class CodeOptimizer:
    def __init__(self, code):
        self.code = code

    def format_code(self):
        return autopep8.fix_code(self.code)

    def validate_syntax(self, code):
        try:
            ast.parse(code)
            return True
        except:
            return False

    def ai_optimize(self, code):
        try:
            print("🧠 Calling Gemini AI...")

            prompt = f"""
You are a professional Python code optimizer.

Tasks:
- Improve code readability
- Remove bad practices
- Optimize performance
- DO NOT change functionality

Return ONLY valid Python code.

Code:
{code}
"""

            response = model.generate_content(prompt)

            return response.text

        except Exception as e:
            return f"AI error: {e}"

    def optimize(self):
        print("🚀 Step 1: Formatting code...")
        formatted_code = self.format_code()

        print("🧠 Step 2: AI optimization running...")
        ai_code = self.ai_optimize(formatted_code)

        print("\n----- AI OUTPUT START -----")
        print(ai_code)
        print("------ AI OUTPUT END ------\n")

        # 🔥 IMPORTANT FIX (use AI output properly)
        final_code = ai_code if self.validate_syntax(ai_code) else formatted_code

        if self.validate_syntax(final_code):
            return final_code, "Gemini AI + Formatting applied"
        else:
            return self.code, "Fallback used (syntax issue)"
