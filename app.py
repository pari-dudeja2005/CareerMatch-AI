import re
import streamlit as st

from src.parser import extract_text_from_pdf
from src.ranking import rank_jobs


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CareerMatch AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background: #f7f8fc;
        color: #172033;
    }

    .main .block-container {
        max-width: 1180px;
        padding: 35px 45px 70px 45px;
    }

    [data-testid="stSidebar"] {
        display: none;
    }

    [data-testid="collapsedControl"] {
        display: none;
    }

    /* ---------- HEADER ---------- */

    .app-title {
        text-align: center;
        font-size: 42px;
        font-weight: 850;
        color: #111827 !important;
        margin-bottom: 4px;
    }

    .app-tagline {
        text-align: center;
        font-size: 16px;
        font-style: italic;
        color: #667085 !important;
        margin-bottom: 38px;
    }

    /* ---------- SECTION HEADINGS ---------- */

    .section-title {
        font-size: 25px;
        font-weight: 800;
        color: #111827 !important;
        margin-top: 35px;
        margin-bottom: 16px;
    }

    .sub-heading {
        font-size: 17px;
        font-weight: 750;
        color: #172033 !important;
        margin-top: 18px;
        margin-bottom: 8px;
    }

    /* ---------- UPLOAD ---------- */

    [data-testid="stFileUploader"] {
        background: #ffffff;
        border: 1px solid #d9dee8;
        border-radius: 12px;
        padding: 10px;
    }

    [data-testid="stFileUploader"] * {
        color: #172033 !important;
    }

    /* ---------- BUTTON ---------- */

    .stButton > button {
        background: #111827 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        min-height: 44px;
        font-weight: 700 !important;
    }

    .stButton > button:hover {
        background: #1f2937 !important;
        color: #ffffff !important;
    }

    .stButton > button p {
        color: #ffffff !important;
    }

    /* ---------- BEST MATCH ---------- */

    .best-card {
        background: #ffffff;
        border: 1px solid #d9dee8;
        border-radius: 14px;
        padding: 25px;
        margin-bottom: 24px;
    }

    .best-role {
        font-size: 29px;
        font-weight: 850;
        color: #111827 !important;
        margin-bottom: 5px;
    }

    .best-description {
        color: #667085 !important;
        font-size: 14px;
    }

    /* ---------- METRIC CARDS ---------- */

    .metric-card {
        background: #ffffff;
        border: 1px solid #d9dee8;
        border-radius: 12px;
        padding: 20px;
        min-height: 105px;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 850;
        color: #111827 !important;
    }

    .metric-label {
        font-size: 13px;
        font-weight: 650;
        color: #667085 !important;
        margin-top: 3px;
    }

    /* ---------- ATS ---------- */

    .ats-container {
        background: #ffffff;
        border: 1px solid #d9dee8;
        border-radius: 14px;
        padding: 25px;
        margin-top: 10px;
    }

    .ats-score {
        font-size: 40px;
        font-weight: 850;
        color: #111827 !important;
    }

    .ats-description {
        font-size: 14px;
        color: #667085 !important;
        margin-top: 3px;
        margin-bottom: 22px;
    }

    .ats-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 0;
        border-bottom: 1px solid #edf0f5;
    }

    .ats-row:last-child {
        border-bottom: none;
    }

    .ats-name {
        font-size: 14px;
        font-weight: 650;
        color: #344054 !important;
    }

    .ats-percent {
        font-size: 14px;
        font-weight: 800;
        color: #111827 !important;
    }

    .insight-box {
        background: #f8fafc;
        border: 1px solid #e4e7ec;
        border-radius: 10px;
        padding: 15px 18px;
        margin-top: 10px;
        color: #344054 !important;
        font-size: 14px;
        line-height: 1.6;
    }

    /* ---------- EXPLAINABLE MATCH ---------- */

    .explain-card {
        background: #ffffff;
        border: 1px solid #d9dee8;
        border-radius: 14px;
        padding: 25px;
        margin-top: 10px;
    }

    .explain-item {
        padding: 15px 0;
        border-bottom: 1px solid #edf0f5;
    }

    .explain-item:last-child {
        border-bottom: none;
    }

    .explain-title {
        font-size: 15px;
        font-weight: 800;
        color: #172033 !important;
        margin-bottom: 5px;
    }

    .explain-text {
        font-size: 14px;
        line-height: 1.6;
        color: #667085 !important;
    }

    /* ---------- JOB RECOMMENDATIONS ---------- */

    .recommendation-intro {
        color: #667085 !important;
        font-size: 14px;
        margin-bottom: 18px;
    }

    .job-card {
        background: #ffffff;
        border: 1px solid #d9dee8;
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 18px;
    }

    .job-card:hover {
        border-color: #b8c0ce;
    }

    .job-title {
        font-size: 21px;
        font-weight: 850;
        color: #111827 !important;
        margin-bottom: 15px;
    }

    .job-metric {
        font-size: 14px;
        color: #344054 !important;
        font-weight: 650;
    }

    .job-metric strong {
        color: #111827 !important;
    }

    .skills-area {
        margin-top: 18px;
        padding-top: 16px;
        border-top: 1px solid #edf0f5;
    }

    .skills-title {
        font-size: 14px;
        font-weight: 800;
        color: #172033 !important;
        margin-bottom: 7px;
    }

    .skills-content {
        font-size: 13px;
        line-height: 1.7;
        color: #667085 !important;
    }

    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        color: #98a2b3 !important;
        font-size: 12px;
        margin-top: 45px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="app-title">CareerMatch AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="app-tagline">'
    'Intelligent resume analysis and personalized job matching'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# UPLOAD RESUME
# ============================================================

st.markdown(
    '<div class="section-title">Upload Resume</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Choose your resume",
    type=["pdf"]
)


if uploaded_file is None:
    st.info("Upload a PDF resume to begin.")
    st.stop()


# ============================================================
# EXTRACT RESUME
# ============================================================

try:

    resume_text = extract_text_from_pdf(
        uploaded_file
    )

except Exception as error:

    st.error(
        f"Unable to read the resume: {error}"
    )

    st.stop()


if not resume_text.strip():

    st.error(
        "No readable text was found in the uploaded PDF."
    )

    st.stop()


st.success(
    f"Resume ready for analysis: {uploaded_file.name}"
)


# ============================================================
# ANALYZE
# ============================================================

if not st.button(
    "Analyze Resume",
    use_container_width=True
):

    st.stop()


with st.spinner("Analyzing resume..."):

    try:

        results = rank_jobs(
            resume_text,
            csv_path="data/jobs.csv",
            top_n=10
        )

    except Exception as error:

        st.error(
            f"Analysis failed: {error}"
        )

        st.stop()


if not results:

    st.warning(
        "No job recommendations were generated."
    )

    st.stop()


# ============================================================
# HELPERS
# ============================================================

def number(value):

    try:
        return float(value)
    except:
        return 0.0


# ============================================================
# BEST JOB MATCH
# ============================================================

best_job = results[0]

overall = number(
    best_job.get("overall_match", 0)
)

semantic = number(
    best_job.get("semantic_match", 0)
)

skill = number(
    best_job.get("skill_match", 0)
)

best_title = best_job.get(
    "job_title",
    "Unknown Role"
)


st.markdown(
    '<div class="section-title">Best Job Match</div>',
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="best-card">
        <div class="best-role">{best_title}</div>
        <div class="best-description">
            Highest-ranked position based on your resume
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# MATCH METRICS
# ============================================================

m1, m2, m3 = st.columns(3)


with m1:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-value">{overall:.2f}%</div>
            <div class="metric-label">Overall Match</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with m2:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-value">{semantic:.2f}%</div>
            <div class="metric-label">Semantic Match</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with m3:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-value">{skill:.2f}%</div>
            <div class="metric-label">Skill Match</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# ATS SCORE
# ============================================================

def calculate_ats_score(text):

    text_lower = text.lower()

    categories = {}

    # Contact information
    email = bool(
        re.search(
            r"[\w\.-]+@[\w\.-]+\.\w+",
            text
        )
    )

    phone = bool(
        re.search(
            r"(?:\+91[\s-]?)?[6-9]\d{9}",
            text
        )
    )

    contact = 0

    if email:
        contact += 5

    if phone:
        contact += 5

    categories["Contact Information"] = (
        contact,
        10
    )

    # Resume sections
    sections = {

        "Education": [
            "education",
            "b.tech",
            "bachelor",
            "university",
            "college"
        ],

        "Experience": [
            "experience",
            "internship",
            "intern"
        ],

        "Skills": [
            "skills",
            "technical skills"
        ],

        "Projects": [
            "projects",
            "project"
        ],

        "Certifications": [
            "certification",
            "certifications"
        ]
    }

    for section, keywords in sections.items():

        found = any(
            keyword in text_lower
            for keyword in keywords
        )

        categories[section] = (
            10 if found else 0,
            10
        )

    # Action verbs
    verbs = [
        "developed",
        "built",
        "implemented",
        "designed",
        "created",
        "engineered",
        "optimized",
        "automated",
        "deployed",
        "integrated",
        "analyzed",
        "improved",
        "managed",
        "led",
        "trained"
    ]

    verb_count = sum(
        text_lower.count(verb)
        for verb in verbs
    )

    categories["Action Verbs"] = (
        min(verb_count * 0.75, 10),
        10
    )

    # Quantified impact
    percentages = len(
        re.findall(
            r"\b\d+(?:\.\d+)?\s?%",
            text
        )
    )

    numbers = len(
        re.findall(
            r"\b\d+(?:\.\d+)?\b",
            text
        )
    )

    impact_count = max(
        percentages,
        min(numbers, 8)
    )

    categories["Quantified Impact"] = (
        min(impact_count * 1.25, 10),
        10
    )

    # Technical keywords
    technical = [

        "python",
        "java",
        "c++",
        "sql",
        "mysql",
        "postgresql",

        "machine learning",
        "deep learning",
        "pytorch",
        "tensorflow",
        "scikit-learn",

        "aws",
        "docker",
        "git",
        "linux",

        "fastapi",
        "flask",

        "pandas",
        "numpy",

        "langchain",
        "generative ai",
        "computer vision",
        "natural language processing",

        "data engineering",
        "apache nifi",
        "hadoop",
        "pyspark",

        "retrieval augmented generation",
        "large language models"
    ]

    technical_count = sum(
        1
        for item in technical
        if item in text_lower
    )

    categories["Technical Keywords"] = (
        min(technical_count * 0.4, 10),
        10
    )

    # Resume length
    words = len(
        text.split()
    )

    if 400 <= words <= 1200:

        length_score = 10

    elif 250 <= words < 400:

        length_score = 7

    elif 1200 < words <= 1600:

        length_score = 7

    else:

        length_score = 4

    categories["Resume Length"] = (
        length_score,
        10
    )

    total = sum(
        value
        for value, maximum in categories.values()
    )

    maximum = sum(
        maximum
        for value, maximum in categories.values()
    )

    final = (
        total / maximum
    ) * 100

    return round(final, 2), categories


ats_score, ats_breakdown = calculate_ats_score(
    resume_text
)


# ============================================================
# ATS SECTION
# ============================================================

st.markdown(
    '<div class="section-title">ATS Resume Score</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="ats-container">',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="ats-score">{ats_score:.0f}/100</div>',
    unsafe_allow_html=True
)


if ats_score >= 85:

    ats_message = "Excellent ATS readiness."

elif ats_score >= 70:

    ats_message = "Good ATS readiness with room for improvement."

elif ats_score >= 55:

    ats_message = "Moderate ATS readiness."

else:

    ats_message = "Low ATS readiness. Resume optimization is recommended."


st.markdown(
    f'<div class="ats-description">{ats_message}</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-heading">Score Breakdown</div>',
    unsafe_allow_html=True
)


for category, values in ats_breakdown.items():

    score, maximum = values

    percentage = (
        score / maximum
    ) * 100

    st.markdown(
        f"""
        <div class="ats-row">
            <div class="ats-name">{category}</div>
            <div class="ats-percent">{percentage:.0f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ATS insights

weak = []
strong = []

for category, values in ats_breakdown.items():

    score, maximum = values

    percentage = (
        score / maximum
    ) * 100

    if percentage >= 80:
        strong.append(category)

    elif percentage < 60:
        weak.append(category)


if strong:

    st.markdown(
        f"""
        <div class="insight-box">
            <strong>Strong areas:</strong>
            {", ".join(strong)}
        </div>
        """,
        unsafe_allow_html=True
    )


if weak:

    st.markdown(
        f"""
        <div class="insight-box">
            <strong>Areas to improve:</strong>
            {", ".join(weak)}
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# EXPLAINABLE MATCH
# ============================================================

st.markdown(
    '<div class="section-title">Explainable Match Score</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="explain-card">',
    unsafe_allow_html=True
)


# Semantic explanation

if semantic >= 75:

    semantic_text = (
        "Strong semantic alignment. "
        "Your resume content closely matches the language "
        "and responsibilities associated with this role."
    )

elif semantic >= 50:

    semantic_text = (
        "Moderate semantic alignment. "
        "Your resume has meaningful overlap with this role, "
        "but some role-specific content could be strengthened."
    )

else:

    semantic_text = (
        "Limited semantic alignment. "
        "The resume may need stronger role-specific content "
        "to match this position."
    )


st.markdown(
    f"""
    <div class="explain-item">
        <div class="explain-title">
            Semantic Alignment
        </div>
        <div class="explain-text">
            {semantic_text}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# Skill explanation

missing_skills = best_job.get(
    "missing_skills",
    []
)


if missing_skills:

    skill_text = (
        f"{len(missing_skills)} detected skill(s) "
        "from the job description are not currently "
        "represented in your resume."
    )

else:

    skill_text = (
        "The detected skills required by this role "
        "are well represented in your resume."
    )


st.markdown(
    f"""
    <div class="explain-item">
        <div class="explain-title">
            Skill Coverage
        </div>
        <div class="explain-text">
            {skill_text}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# Priority improvement

if missing_skills:

    priority = ", ".join(
        str(skill)
        for skill in missing_skills[:5]
    )

    improvement_text = (
        f"Consider strengthening your resume around: "
        f"{priority}."
    )

else:

    improvement_text = (
        "No major skill gaps were detected for this role."
    )


st.markdown(
    f"""
    <div class="explain-item">
        <div class="explain-title">
            Highest-Priority Improvement
        </div>
        <div class="explain-text">
            {improvement_text}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# JOB RECOMMENDATIONS
# ============================================================

st.markdown(
    '<div class="section-title">Job Recommendations</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="recommendation-intro">'
    'Ranked using semantic similarity and skill compatibility.'
    '</div>',
    unsafe_allow_html=True
)


for index, job in enumerate(
    results,
    start=1
):

    title = job.get(
        "job_title",
        "Unknown Role"
    )

    overall = number(
        job.get("overall_match", 0)
    )

    semantic = number(
        job.get("semantic_match", 0)
    )

    skill = number(
        job.get("skill_match", 0)
    )

    matched = job.get(
        "matched_skills",
        []
    )

    gaps = job.get(
        "missing_skills",
        []
    )


    # Card

    st.markdown(
        '<div class="job-card">',
        unsafe_allow_html=True
    )


    st.markdown(
        f'<div class="job-title">'
        f'{index}. {title}'
        f'</div>',
        unsafe_allow_html=True
    )


    # Three metrics

    c1, c2, c3 = st.columns(3)


    with c1:

        st.markdown(
            f"""
            <div class="job-metric">
                <strong>Overall</strong><br>
                {overall:.2f}%
            </div>
            """,
            unsafe_allow_html=True
        )


    with c2:

        st.markdown(
            f"""
            <div class="job-metric">
                <strong>Semantic</strong><br>
                {semantic:.2f}%
            </div>
            """,
            unsafe_allow_html=True
        )


    with c3:

        st.markdown(
            f"""
            <div class="job-metric">
                <strong>Skills</strong><br>
                {skill:.2f}%
            </div>
            """,
            unsafe_allow_html=True
        )


    # Skills

    st.markdown(
        '<div class="skills-area">',
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="skills-title">'
        'Matched Skills'
        '</div>',
        unsafe_allow_html=True
    )


    if matched:

        matched_text = ", ".join(
            str(item)
            for item in matched
        )

        st.markdown(
            f'<div class="skills-content">'
            f'{matched_text}'
            f'</div>',
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            '<div class="skills-content">'
            'No matching skills detected.'
            '</div>',
            unsafe_allow_html=True
        )


    st.markdown(
        '<div style="height:12px;"></div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="skills-title">'
        'Skill Gaps'
        '</div>',
        unsafe_allow_html=True
    )


    if gaps:

        gap_text = ", ".join(
            str(item)
            for item in gaps
        )

        st.markdown(
            f'<div class="skills-content">'
            f'{gap_text}'
            f'</div>',
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            '<div class="skills-content">'
            'None'
            '</div>',
            unsafe_allow_html=True
        )


    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer">'
    'CareerMatch AI | Resume analysis and intelligent job matching'
    '</div>',
    unsafe_allow_html=True
)

