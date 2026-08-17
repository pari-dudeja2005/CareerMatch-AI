from src.parser import extract_text_from_pdf

from src.scoring import (
    calculate_semantic_score,
    calculate_skill_match,
    calculate_overall_score
)


# =========================================
# LOAD ACTUAL RESUME PDF
# =========================================

PDF_PATH = "test_resume.pdf"


with open(PDF_PATH, "rb") as pdf_file:

    resume = extract_text_from_pdf(
        pdf_file
    )


# =========================================
# JOB DESCRIPTION
# =========================================

job = """
We are looking for a Machine Learning Engineer
with experience in Python, machine learning,
deep learning, NLP, PyTorch, TensorFlow and
Generative AI.

The candidate should be comfortable building,
training and deploying machine learning models.
"""


# =========================================
# SEMANTIC MATCH
# =========================================

semantic_score = calculate_semantic_score(
    resume,
    job
)


# =========================================
# SKILL MATCH
# =========================================

skill_result = calculate_skill_match(
    resume,
    job
)


skill_score = skill_result["score"]


# =========================================
# OVERALL SCORE
# =========================================

overall_score = calculate_overall_score(
    semantic_score,
    skill_score
)


# =========================================
# FINAL RESULT
# =========================================

print(
    "\n========== JOB MATCH ANALYSIS ==========\n"
)

print(
    f"Semantic Match : {semantic_score}%"
)

print(
    f"Skill Match    : {skill_score}%"
)

print(
    f"Overall Match  : {overall_score}%"
)


print(
    "\n---------- MATCHED SKILLS ----------"
)

for skill in skill_result["matched_skills"]:

    print(
        f"✓ {skill}"
    )


print(
    "\n---------- SKILL GAP ----------"
)

for skill in skill_result["missing_skills"]:

    print(
        f"⚠ {skill}"
    )


print(
    "\n========================================"
)