import sqlite3
import json
from datetime import datetime

# ------------------ CONNECTION ------------------
conn = sqlite3.connect("interview.db", check_same_thread=False)
cursor = conn.cursor()

# ------------------ TABLE ------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    skills TEXT,
    roles TEXT,
    question TEXT,
    answer TEXT,
    score INTEGER,
    strengths TEXT,
    improvements TEXT,
    model_answer TEXT
)
""")

conn.commit()

# ------------------ SAVE SESSION ------------------
def save_session(skills, roles, question, answer, feedback):
    """
    feedback expected format:
    {
        "score": 7,
        "strengths": "...",
        "improvements": "...",
        "model_answer": "..."
    }
    """

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO sessions (
        timestamp, skills, roles, question, answer,
        score, strengths, improvements, model_answer
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        json.dumps(skills),
        json.dumps(roles),
        question,
        answer,
        feedback.get("score", 0),
        feedback.get("strengths", ""),
        feedback.get("improvements", ""),
        feedback.get("model_answer", "")
    ))

    conn.commit()

# ------------------ GET RAW DATA ------------------
def get_all_sessions():
    cursor.execute("SELECT * FROM sessions")
    return cursor.fetchall()

# ------------------ ANALYTICS ------------------
def get_analytics():
    """
    Returns structured data for charts
    """

    cursor.execute("SELECT score, skills, timestamp FROM sessions")
    rows = cursor.fetchall()

    scores = []
    skills_count = {}

    for score, skills, timestamp in rows:
        scores.append(score)

        try:
            skill_list = json.loads(skills)
            for skill in skill_list:
                skills_count[skill] = skills_count.get(skill, 0) + 1
        except:
            pass

    return {
        "scores": scores,
        "skills": skills_count
    }

# ------------------ AVERAGE SCORE ------------------
def get_average_score():
    cursor.execute("SELECT AVG(score) FROM sessions")
    result = cursor.fetchone()[0]
    return round(result, 2) if result else 0

# ------------------ TOTAL SESSIONS ------------------
def get_total_sessions():
    cursor.execute("SELECT COUNT(*) FROM sessions")
    return cursor.fetchone()[0]