import openai
import json

# Set your API key (or use env variable)
# openai.api_key = "YOUR_API_KEY"

def evaluate_answer(question, answer):
    prompt = f"""
You are an expert technical interviewer.

Evaluate the candidate's answer.

Question: {question}
Answer: {answer}

Return ONLY valid JSON in this format:

{{
    "score": (integer between 1-10),
    "strengths": "short explanation",
    "improvements": "what to improve",
    "model_answer": "ideal answer in simple terms"
}}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            temperature=0.3,
            messages=[
                {"role": "system", "content": "You are a strict but helpful interviewer."},
                {"role": "user", "content": prompt}
            ]
        )

        content = response["choices"][0]["message"]["content"]

        # Convert string → JSON
        feedback = json.loads(content)

        return feedback

    except Exception as e:
        # Fallback (VERY IMPORTANT)
        return {
            "score": 5,
            "strengths": "Could not evaluate properly",
            "improvements": "Try again",
            "model_answer": "N/A"
        }