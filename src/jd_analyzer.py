import re

from src.skill_extractor import (
    find_similar_skills
)


def analyze_job_description(job_description):

    text = job_description or ""

    lower_text = text.lower()

    # =========================================================
    # Extract skills
    # =========================================================

    detected = find_similar_skills(
        text,
        threshold=0.55
    )

    skills = {}

    for item in detected:

        skill = item["skill"]

        skills[
            skill.lower()
        ] = skill


    # =========================================================
    # Preferred section detection
    # =========================================================

    preferred_keywords = [
        "preferred",
        "nice to have",
        "good to have",
        "bonus",
        "plus",
        "preferred qualifications",
        "desirable"
    ]

    required_keywords = [
        "required",
        "requirements",
        "must have",
        "mandatory",
        "qualifications"
    ]


    preferred_skills = set()
    required_skills = set()


    # =========================================================
    # Split JD into lines
    # =========================================================

    lines = text.splitlines()

    current_section = "required"


    for line in lines:

        clean = line.strip()

        if not clean:
            continue

        lower = clean.lower()


        # -----------------------------------------------
        # Detect preferred section
        # -----------------------------------------------

        if any(
            keyword in lower
            for keyword in preferred_keywords
        ):

            current_section = "preferred"


        elif any(
            keyword in lower
            for keyword in required_keywords
        ):

            current_section = "required"


        # -----------------------------------------------
        # Extract skills from line
        # -----------------------------------------------

        line_skills = find_similar_skills(
            clean,
            threshold=0.55
        )

        for item in line_skills:

            skill = item["skill"]

            normalized = skill.lower()

            if current_section == "preferred":

                preferred_skills.add(
                    normalized
                )

            else:

                required_skills.add(
                    normalized
                )


    # =========================================================
    # If sections weren't explicitly detected
    # =========================================================

    all_detected = set(
        skills.keys()
    )

    if not required_skills and not preferred_skills:

        required_skills = all_detected


    # Remove overlaps
    preferred_skills -= required_skills


    return {
        "required_skills": sorted(
            [
                skills.get(
                    skill,
                    skill.title()
                )
                for skill in required_skills
            ]
        ),

        "preferred_skills": sorted(
            [
                skills.get(
                    skill,
                    skill.title()
                )
                for skill in preferred_skills
            ]
        )
    }