from skills_db import SKILLS_DB
from sentence_transformers import SentenceTransformer, util
import re

# ------------------ LOAD MODEL ------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# ------------------ PRECOMPUTE EMBEDDINGS ------------------
skill_embeddings = {
    skill: model.encode(skill, convert_to_tensor=True)
    for skill in SKILLS_DB
}

# ------------------ TEXT CLEANING ------------------
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return text

# ------------------ MAIN FUNCTION ------------------
def extract_skills(text):
    text = preprocess_text(text)

    found_skills = set()

    # ----------- 1. KEYWORD MATCH (FAST + ACCURATE) -----------
    for skill in SKILLS_DB:
        if skill.lower() in text:
            found_skills.add(skill)

    # ----------- 2. SEMANTIC MATCH (SMART AI) -----------
    text_chunks = split_text(text)

    for chunk in text_chunks:
        chunk_embedding = model.encode(chunk, convert_to_tensor=True)

        for skill, emb in skill_embeddings.items():
            score = util.cos_sim(chunk_embedding, emb).item()

            if score > 0.6:  # stricter threshold
                found_skills.add(skill)

    return sorted(list(found_skills))


# ------------------ SPLIT TEXT INTO CHUNKS ------------------
def split_text(text, max_len=200):
    words = text.split()
    chunks = []

    for i in range(0, len(words), max_len):
        chunk = " ".join(words[i:i+max_len])
        chunks.append(chunk)

    return chunks