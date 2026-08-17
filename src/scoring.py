import numpy as np

from src.embeddings import generate_embedding
from src.skill_extractor import find_similar_skills


# ============================================================
# COSINE / SEMANTIC SCORE
# ============================================================

def cosine_similarity(vector_a, vector_b):
    vector_a = np.asarray(vector_a)
    vector_b = np.asarray(vector_b)

    denominator = (
        np.linalg.norm(vector_a)
        * np.linalg.norm(vector_b)
    )

    if denominator == 0:
        return 0.0

    return float(
        np.dot(vector_a, vector_b) / denominator
    )


def calculate_semantic_score(resume_text, job_description):
    resume_embedding = generate_embedding(resume_text)
    job_embedding = generate_embedding(job_description)

    similarity = cosine_similarity(
        resume_embedding,
        job_embedding
    )

    return round(
        max(0, min(similarity * 100, 100)),
        2
    )


# ============================================================
# NORMALIZE SKILLS
# ============================================================

def normalize_skill(skill):
    skill = str(skill).strip().lower()

    for old, new in [
        ("-", " "),
        ("_", " "),
        ("/", " ")
    ]:
        skill = skill.replace(old, new)

    return " ".join(skill.split())


# ============================================================
# EXTRACT SKILLS
# ============================================================

def extract_skills(text):
    results = find_similar_skills(
        text,
        threshold=0.55
    )

    skills = {}

    for result in results:
        original_skill = result["skill"]
        normalized_skill = normalize_skill(original_skill)

        if normalized_skill not in skills:
            skills[normalized_skill] = original_skill

    return skills


# ============================================================
# MATCH A SKILL LIST AGAINST RESUME
# ============================================================

def match_skill_list(resume_skills, target_skills):
    matched = []
    missing = []

    for skill in target_skills:
        normalized = normalize_skill(skill)

        if normalized in resume_skills:
            matched.append(resume_skills[normalized])
        else:
            missing.append(skill)

    return sorted(set(matched), key=str.lower), sorted(
        set(missing),
        key=str.lower
    )


def percentage(matched, total):
    if total == 0:
        return 100.0
    return round((len(matched) / total) * 100, 2)


# ============================================================
# SKILL MATCH
#
# Supports jobs.csv with:
# required_skills
# preferred_skills
#
# Also safely falls back to job_description if these columns
# are absent.
# ============================================================

def calculate_skill_match(
    resume_text,
    job_description,
    required_skills=None,
    preferred_skills=None
):
    resume_skills = extract_skills(resume_text)

    required_skills = required_skills or []
    preferred_skills = preferred_skills or []

    matched_required, missing_required = match_skill_list(
        resume_skills,
        required_skills
    )

    matched_preferred, missing_preferred = match_skill_list(
        resume_skills,
        preferred_skills
    )

    # If structured required/preferred skills exist, use them.
    if required_skills or preferred_skills:
        required_score = percentage(
            matched_required,
            len(required_skills)
        )

        preferred_score = percentage(
            matched_preferred,
            len(preferred_skills)
        )

        # Required skills matter substantially more.
        score = (
            required_score * 0.70
            +
            preferred_score * 0.30
        )

        matched_skills = sorted(
            set(matched_required + matched_preferred),
            key=str.lower
        )

        missing_skills = sorted(
            set(missing_required + missing_preferred),
            key=str.lower
        )

        return {
            "score": round(score, 2),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "matched_count": len(matched_skills),
            "missing_count": len(missing_skills),
            "total_job_skills": (
                len(required_skills)
                + len(preferred_skills)
            ),
            "matched_required": matched_required,
            "missing_required": missing_required,
            "matched_preferred": matched_preferred,
            "missing_preferred": missing_preferred,
            "required_skill_score": required_score,
            "preferred_skill_score": preferred_score
        }

    # Backward-compatible fallback for old jobs.csv.
    job_skills = extract_skills(job_description)

    resume_set = set(resume_skills)
    job_set = set(job_skills)

    matched = resume_set.intersection(job_set)
    missing = job_set.difference(resume_set)

    matched_skills = sorted(
        [resume_skills[x] for x in matched],
        key=str.lower
    )

    missing_skills = sorted(
        [job_skills[x] for x in missing],
        key=str.lower
    )

    score = percentage(
        matched,
        len(job_set)
    )

    return {
        "score": score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "matched_count": len(matched),
        "missing_count": len(missing),
        "total_job_skills": len(job_set),
        "matched_required": [],
        "missing_required": [],
        "matched_preferred": [],
        "missing_preferred": [],
        "required_skill_score": score,
        "preferred_skill_score": 0.0
    }


# ============================================================
# OVERALL SCORE
# ============================================================

def calculate_overall_score(
    semantic_score,
    skill_score,
    semantic_weight=0.40,
    skill_weight=0.60
):
    overall = (
        semantic_score * semantic_weight
        +
        skill_score * skill_weight
    )

    return round(
        max(0, min(overall, 100)),
        2
    )


# ============================================================
# COMPLETE JOB MATCH
# ============================================================

def calculate_job_match(
    resume_text,
    job_description,
    required_skills=None,
    preferred_skills=None
):
    semantic_score = calculate_semantic_score(
        resume_text,
        job_description
    )

    skill_result = calculate_skill_match(
        resume_text,
        job_description,
        required_skills=required_skills,
        preferred_skills=preferred_skills
    )

    skill_score = skill_result["score"]

    overall_score = calculate_overall_score(
        semantic_score,
        skill_score
    )

    return {
        "semantic_match": semantic_score,
        "skill_match": skill_score,
        "overall_match": overall_score,

        "matched_skills":
            skill_result["matched_skills"],

        "missing_skills":
            skill_result["missing_skills"],

        "matched_count":
            skill_result["matched_count"],

        "missing_count":
            skill_result["missing_count"],

        "total_job_skills":
            skill_result["total_job_skills"],

        "matched_required":
            skill_result["matched_required"],

        "missing_required":
            skill_result["missing_required"],

        "matched_preferred":
            skill_result["matched_preferred"],

        "missing_preferred":
            skill_result["missing_preferred"],

        "required_skill_score":
            skill_result["required_skill_score"],

        "preferred_skill_score":
            skill_result["preferred_skill_score"]
    }