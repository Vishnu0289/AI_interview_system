import streamlit as st
import pandas as pd
from resume_parser import extract_text
from skill_extractor import extract_skills
from role_detector import detect_roles, detect_experience
from question_generator import generate_questions
from feedback import evaluate_answer
from database import save_session, get_analytics

# ------------------ CONFIG ------------------
st.set_page_config(page_title="AI Interview Pro", layout="wide")

# ------------------ CSS ------------------
st.markdown("""
<style>
body { background-color: #0E1117; }
.chat-bubble {
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
}
.question { background-color: #1f77b4; color: white; }
.answer { background-color: #2ca02c; color: white; }
.feedback { background-color: #ff7f0e; color: white; }
.card {
    padding: 20px;
    border-radius: 15px;
    background-color: #1c1c1c;
    margin-bottom: 15px;
}
.stButton>button {
    background-color: #ff4757;
    color: white;
    border-radius: 10px;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# ------------------ SIDEBAR ------------------
st.sidebar.title("🤖 AI Interview Pro")
page = st.sidebar.radio("Navigate", ["Home", "Interview", "Analytics"])

# ------------------ SESSION STATE ------------------
if "chat" not in st.session_state:
    st.session_state.chat = []

if "score" not in st.session_state:
    st.session_state.score = 0

if "total" not in st.session_state:
    st.session_state.total = 0

if "weak_skills" not in st.session_state:
    st.session_state.weak_skills = []

# ------------------ HOME ------------------
if page == "Home":
    st.title("🚀 AI Interview Pro")

    col1, col2, col3 = st.columns(3)
    col1.metric("Users", "1,240")
    col2.metric("Interviews", "3,580")
    col3.metric("Avg Score", "78%")

    st.markdown("""
    <div class="card">
    <h3>💡 About</h3>
    <p>Upload your resume → Get AI-generated questions → Answer → Get smart feedback → Track performance.</p>
    </div>
    """, unsafe_allow_html=True)

# ------------------ INTERVIEW ------------------
elif page == "Interview":
    st.title("🎯 Smart Interview Room")

    uploaded_file = st.file_uploader("📄 Upload Resume", type=["pdf", "docx"])

    if uploaded_file:
        with st.spinner("Analyzing Resume..."):
            text = extract_text(uploaded_file)

        skills = extract_skills(text)
        roles = detect_roles(skills)
        experience = detect_experience(text)

        st.success("Resume Processed ✅")

        difficulty = st.selectbox("Select Difficulty", ["Easy", "Medium", "Hard"])

        if st.button("Start Interview 🚀"):
            questions = generate_questions(skills, roles, experience, difficulty)

            st.session_state.questions = questions
            st.session_state.q_index = 0
            st.session_state.chat = []
            st.session_state.score = 0
            st.session_state.total = 0
            st.session_state.weak_skills = []

    # ---------------- CHAT SYSTEM ----------------
    if "questions" in st.session_state:

        q_index = st.session_state.q_index
        questions = st.session_state.questions

        if q_index < len(questions):
            question = questions[q_index]

            # Show Question
            st.markdown(f"""
            <div class="chat-bubble question">
            🤖 {question}
            </div>
            """, unsafe_allow_html=True)

            answer = st.text_area("Your Answer", key=f"ans_{q_index}")

            if st.button("Submit Answer"):
                feedback = evaluate_answer(question, answer)

                # EXPECTED STRUCTURE:
                # feedback = {
                #   "score": 7,
                #   "strengths": "...",
                #   "improvements": "...",
                #   "model_answer": "..."
                # }

                score = feedback.get("score", 5)

                st.session_state.score += score
                st.session_state.total += 10

                # Weakness tracking
                if score < 6:
                    st.session_state.weak_skills.append(question)

                # Save chat
                st.session_state.chat.append({
                    "q": question,
                    "a": answer,
                    "f": feedback
                })

                save_session(skills, roles, question, answer, feedback)

                st.session_state.q_index += 1
                st.rerun()

        # ---------------- CHAT HISTORY ----------------
        st.subheader("💬 Interview History")

        for item in st.session_state.chat:
            st.markdown(f"""
            <div class="chat-bubble question">🤖 {item['q']}</div>
            <div class="chat-bubble answer">🧑 {item['a']}</div>
            <div class="chat-bubble feedback">
            📊 Score: {item['f'].get('score', '-')}/10 <br>
            ✅ {item['f'].get('strengths', '')} <br>
            ⚠️ {item['f'].get('improvements', '')} <br>
            💡 {item['f'].get('model_answer', '')}
            </div>
            """, unsafe_allow_html=True)

        # ---------------- SCORE ----------------
        if st.session_state.total > 0:
            percent = int((st.session_state.score / st.session_state.total) * 100)

            st.subheader("📊 Performance")
            st.progress(percent)
            st.write(f"Score: {percent}%")

        # ---------------- WEAK AREAS ----------------
        st.subheader("⚠️ Weak Areas")
        for w in st.session_state.weak_skills:
            st.write("-", w)

        # ---------------- DOWNLOAD REPORT ----------------
        if st.session_state.total > 0:
            report = f"""
AI Interview Report

Score: {percent}%

Weak Areas:
{st.session_state.weak_skills}
"""
            st.download_button("📥 Download Report", report, file_name="report.txt")

# ------------------ ANALYTICS ------------------
elif page == "Analytics":
    st.title("📊 Analytics Dashboard")

    data = get_analytics()

    try:
        df = pd.DataFrame(data)

        col1, col2 = st.columns(2)
        col1.metric("Sessions", len(df))
        col2.metric("Avg Score", f"{df['score'].mean():.2f}" if "score" in df else "N/A")

        st.subheader("📈 Score Trends")
        if "score" in df:
            st.line_chart(df["score"])

        st.subheader("📊 Skills Distribution")
        if "skills" in df:
            st.bar_chart(df["skills"])

    except:
        st.warning("No analytics data available yet.")