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

    # 🔥 CLEAN AI OUTPUT (remove ```python blocks)
    def clean_ai_output(self, code):
        if not code:
            return ""
        if "```" in code:
            code = code.replace("```python", "").replace("```", "")
        return code.strip()

    def ai_optimize(self, code):
        try:
            print("🧠 Calling Gemini AI...")

            prompt = f"""
You are a professional Python code optimizer.

Rules:
- Improve readability and make the code more optimize 
- Reduce complexity
- Keep same functionality
- Return ONLY valid Python code (no markdown, no explanation , no comments)

Code:
{code}
"""

            response = model.generate_content(prompt)

            return self.clean_ai_output(response.text)

        except Exception as e:
            print(f"❌ AI Error: {e}")
            return None

    def optimize(self):
        print("🚀 Formatting code...")
        formatted_code = self.format_code()

        print("🧠 Running AI optimization...")
        ai_code = self.ai_optimize(formatted_code)

        # 🔥 fallback if AI failed
        if not ai_code:
            return formatted_code, "Formatting only (AI failed)"

        # 🔥 syntax validation
        if not self.validate_syntax(ai_code):
            print("⚠️ AI returned invalid code, skipping...")
            return formatted_code, "Formatting only (invalid AI output)"

        # 🔥 IMPORTANT: avoid rewriting same code (fix infinite loop)
        if ai_code.strip() == self.code.strip():
            print("⚠️ No real change detected, skipping write")
            return self.code, "No changes"

        return ai_code, "Gemini AI optimization applied"- Optimize performance
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
