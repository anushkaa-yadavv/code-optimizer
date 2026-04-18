import autopep8
import ast
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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
            print("🧠 Calling AI model...")

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": f"""
You are a code optimizer.

Improve this Python code:
- better structure
- remove bad practices
- keep same functionality

Code:
{code}
"""
                    }
                ]
            )

            return response.choices[0].message.content

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

        # fallback safety
        final_code = formatted_code

        if self.validate_syntax(final_code):
            return final_code, "AI + Formatting applied"
        else:
            return self.code, "Fallback used (syntax issue)"