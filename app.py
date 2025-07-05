# Smart Resume Analyzer with Modern UI, PDF Report, and Features
import streamlit as st
from PyPDF2 import PdfReader
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_lottie import st_lottie
import requests
from fpdf import FPDF
import tempfile

# Load Lottie animation
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_url = "https://assets2.lottiefiles.com/packages/lf20_tfb3estd.json"
lottie_json = load_lottieurl(lottie_url)

# Define job descriptions and role skills
job_descriptions = {
    "Data Analyst": "Analyze datasets using SQL, Python, Excel, Tableau, and Power BI.",
    "Web Developer": "Build responsive websites and apps using HTML, CSS, JavaScript, React, and Node.js.",
    "AI Engineer": "Develop machine learning models using Python, TensorFlow, and NLP tools like spaCy.",
    "DevOps Engineer": "Manage CI/CD pipelines using Docker, Kubernetes, AWS, Jenkins, and Linux.",
    "UI/UX Designer": "Design user experiences using Figma, Adobe XD, Sketch, and usability testing."
}

role_skills = {
    "Data Analyst": ["SQL", "Excel", "Tableau", "Power BI", "Python", "Pandas"],
    "Web Developer": ["HTML", "CSS", "JavaScript", "React", "Node.js", "Django"],
    "AI Engineer": ["Python", "TensorFlow", "PyTorch", "Machine Learning", "NLP", "spaCy"],
    "DevOps Engineer": ["Docker", "Kubernetes", "Jenkins", "AWS", "CI/CD", "Linux"],
    "UI/UX Designer": ["Figma", "Adobe XD", "Sketch", "Wireframes", "Usability Testing"]
}

# Streamlit UI setup
st.set_page_config(page_title="Smart Resume Analyzer", layout="wide")
st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    .block-container {padding: 2rem 3rem;}
    </style>
    """, unsafe_allow_html=True)

st_lottie(lottie_json, height=250)

st.markdown("""
    <style>
    .main-title-container {
        text-align: center;
        padding: 1rem 1rem 0.5rem;
    }

    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #222222;  /* Dark gray, visible on light bg */
        margin-bottom: 0.2rem;
    }

    .subtitle {
        font-size: 1.3rem;
        font-weight: 500;
        color: #444444;
        margin-top: 0;
    }

    @media (prefers-color-scheme: dark) {
        .main-title, .subtitle {
            color: #ffffff; /* fallback for dark mode */
        }
    }

    @media screen and (max-width: 768px) {
        .main-title {
            font-size: 6vw;
        }
        .subtitle {
            font-size: 4vw;
        }
    }
    </style>

    <div class="main-title-container">
        <div class="main-title">🧠 Smart Resume Analyzer</div>
        <div class="subtitle">for Job Matching</div>
    </div>
""", unsafe_allow_html=True)

st.write("Upload your resume and discover which job role suits you best.")

# File upload
uploaded_file = st.file_uploader("\U0001F4C4 Upload Your Resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    reader = PdfReader(uploaded_file)
    resume_text = ""
    for page in reader.pages:
        resume_text += page.extract_text()

    resume_lower = resume_text.lower()
    roles = list(role_skills.keys())

    similarity_scores = []
    for role in roles:
        keywords = role_skills[role]
        match_count = sum(1 for keyword in keywords if keyword.lower() in resume_lower)
        score = (match_count / len(keywords)) * 100
        similarity_scores.append(round(score, 2))

    role_score_pairs = list(zip(roles, similarity_scores))
    sorted_roles = sorted(role_score_pairs, key=lambda x: x[1], reverse=True)
    top_matches = sorted_roles[:3]
    best_role, best_score = top_matches[0]
    jd_text = job_descriptions[best_role]

    tab1, tab2, tab3, tab4 = st.tabs(["\U0001F3C6 Best Match", "\U0001F4CA All Scores", "\U0001F9E0 Skill Match Chart", "\U0001F4C3 Download Report"])

    with tab1:
        st.subheader("\U0001F3C6 Top 3 Matched Roles")
        for i, (role, score) in enumerate(top_matches, 1):
            st.success(f"**{i}. {role}** — {score}% match")

    with tab2:
        st.subheader("\U0001F4CA Match Scores for All Roles")
        df = pd.DataFrame({
            'Role': roles,
            'Match Score': similarity_scores
        })
        st.dataframe(df.sort_values(by='Match Score', ascending=False))
        st.bar_chart(df.set_index('Role'))

    with tab3:
        st.subheader("\U0001F9E0 Resume vs Job Description Skill Match")
        keywords = ['Python', 'SQL', 'Machine Learning', 'Communication', 'HTML', 'CSS']
        resume_scores = [resume_text.lower().count(k.lower()) for k in keywords]
        jd_scores = [jd_text.lower().count(k.lower()) for k in keywords]

        x = range(len(keywords))
        plt.figure(figsize=(8, 4))
        plt.bar(x, resume_scores, width=0.4, label='Resume', align='center', color='skyblue')
        plt.bar([i + 0.4 for i in x], jd_scores, width=0.4, label='Job Description', align='center', color='orange')
        plt.xticks([i + 0.2 for i in x], keywords, rotation=30)
        plt.legend()
        plt.title('Skill Match Comparison')
        plt.tight_layout()
        st.pyplot(plt)

    with tab4:
        st.subheader("\U0001F4C3 Download Match Report")
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Smart Resume Analyzer - Match Report", ln=True, align='C')
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Best Matched Role: {best_role} ({best_score}%)", ln=True)
        pdf.ln(5)
        pdf.cell(200, 10, txt="Match Scores:", ln=True)
        for i, role in enumerate(roles):
            score = similarity_scores[i]
            pdf.cell(200, 10, txt=f"{role}: {score}%", ln=True)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
            pdf.output(tmpfile.name)
            st.download_button(label="Download PDF Report", data=open(tmpfile.name, "rb"), file_name="match_report.pdf", mime="application/pdf")

    st.markdown("""
    <hr>
    <div style='text-align: center; color: gray;'>
    Created by Poojitha | Powered by Python, Streamlit, and AI
    </div>
    """, unsafe_allow_html=True)

else:
    st.info("Please upload a PDF resume to get started.")
