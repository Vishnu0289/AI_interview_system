import openai
import json
import re

# Optional: use environment variable
# import os
# openai.api_key = os.getenv("OPENAI_API_KEY")

def safe_json_load(content):
    try:
        return json.loads(content)
    except:
        content = re.sub(r"```json|```", "", content)
        return json.loads(content)


def generate_questions(skills, roles, experience, difficulty):
    prompt = f"""
You are an expert interviewer.

Generate exactly 5 interview questions.

Context:
- Roles: {roles}
- Skills: {skills}
- Experience: {experience}
- Difficulty: {difficulty}

Rules:
- Mix of:
  1. Technical (2 questions)
  2. Scenario-based (2 questions)
  3. HR (1 question)
- Keep questions clear and concise
- Make them realistic and role-specific
- Do NOT include explanations

Return ONLY valid JSON in this format:

{{
    "questions": [
        "Question 1",
        "Question 2",
        "Question 3",
        "Question 4",
        "Question 5"
    ]
}}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            temperature=0.7,
            messages=[
                {"role": "system", "content": "You are a professional interviewer."},
                {"role": "user", "content": prompt}
            ]
        )

        content = response["choices"][0]["message"]["content"]

        data = safe_json_load(content)

        questions = data.get("questions", [])

        # Ensure exactly 5 questions
        if len(questions) < 5:
            questions += default_questions()

        return questions[:5]

    except Exception as e:
        return default_questions()


# ------------------ FALLBACK ------------------
def default_questions():
    return [
        "Explain a project you have worked on.",
        "What are your strengths and weaknesses?",
        "Describe a challenging situation and how you solved it.",
        "Explain a key concept related to your skills.",
        "Why should we hire you?"
    ]