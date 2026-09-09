import os
from google import genai

MODEL = "gemini-3.8-flash"

SYSTEM_PROMPT = """
You are an AI HR Policy Assistant.

Your job is to answer employee and HR questions using the provided HR policy.

Rules:
1. Give clear and professional answers.
2. Do not invent company policies.
3. If the policy does not contain the answer, say:
   "I could not find this information in the provided HR policy."
4. Explain policies in simple language.
5. If a question involves disciplinary action, salary, termination,
   leave, harassment, benefits, or legal matters, advise the user
   to confirm with HR.
6. Do not make decisions about hiring, firing, promotion, or employee
   eligibility.
7. Protect employee privacy.
"""

def load_policy():
    path = os.path.join("policies", "hr_policy.txt")

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as file:
            return file.read()

    return "No HR policy document has been uploaded yet."


def ask_hr_policy(question):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "Error: GEMINI_API_KEY is not configured."

    client = genai.Client(api_key=api_key)

    policy = load_policy()

    prompt = f"""
{SYSTEM_PROMPT}

HR POLICY:
----------------
{policy}
----------------

EMPLOYEE QUESTION:
{question}

Answer based primarily on the HR policy.
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text
