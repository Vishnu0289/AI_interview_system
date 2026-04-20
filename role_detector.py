import re

# ------------------ ROLE KEYWORDS ------------------
ROLE_MAP = {
    "Data Scientist": [
        "python", "machine learning", "pandas", "numpy",
        "data analysis", "statistics", "sql"
    ],
    "Web Developer": [
        "html", "css", "javascript", "react",
        "django", "flask", "node", "frontend", "backend"
    ],
    "AI Engineer": [
        "deep learning", "nlp", "tensorflow",
        "pytorch", "computer vision", "transformers"
    ]
}


# ------------------ ROLE DETECTION ------------------
def detect_roles(skills):
    scores = {}

    skills = [s.lower() for s in skills]

    for role, keywords in ROLE_MAP.items():
        score = 0

        for skill in skills:
            for keyword in keywords:
                # Partial match (important upgrade)
                if keyword in skill or skill in keyword:
                    score += 1

        scores[role] = score

    # Sort roles by score
    sorted_roles = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    primary_role = sorted_roles[0][0]

    # Clean secondary roles (remove zero scores)
    secondary_roles = [r for r, s in sorted_roles[1:] if s > 0]

    return {
        "primary": primary_role,
        "secondary": secondary_roles,
        "scores": scores
    }


# ------------------ EXPERIENCE DETECTION ------------------
def detect_experience(text):
    text = text.lower()

    # Match patterns like:
    # "2 years", "3+ years", "5 yrs"
    match = re.search(r"(\d+)\s*\+?\s*(years|yrs)", text)

    if match:
        years = int(match.group(1))

        if years <= 1:
            return "Fresher"
        elif years <= 3:
            return "Junior"
        elif years <= 6:
            return "Mid-Level"
        else:
            return "Senior"

    # Fallback keywords
    if "intern" in text:
        return "Fresher"

    return "Fresher"