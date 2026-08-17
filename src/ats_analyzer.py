import re


def calculate_ats_score(resume_text):
    """
    Calculate a simple explainable ATS/resume quality score.

    This is NOT pretending to be a proprietary ATS.
    It evaluates resume structure, readability, sections,
    contact information, measurable achievements, etc.
    """

    text = resume_text or ""

    if not text.strip():
        return {
            "score": 0,
            "breakdown": {},
            "suggestions": []
        }

    lower_text = text.lower()

    score = 0
    suggestions = []

    breakdown = {}

    # =========================================================
    # 1. Resume sections
    # =========================================================

    sections = {
        "Education": [
            "education",
            "academic"
        ],

        "Experience": [
            "experience",
            "internship",
            "employment"
        ],

        "Projects": [
            "projects",
            "project"
        ],

        "Skills": [
            "skills",
            "technical skills"
        ],

        "Certifications": [
            "certifications",
            "certification"
        ]
    }

    section_score = 0

    for section, keywords in sections.items():

        found = any(
            keyword in lower_text
            for keyword in keywords
        )

        if found:
            section_score += 4

        else:
            suggestions.append(
                f"Consider adding a clear {section} section."
            )

    section_score = min(section_score, 20)

    breakdown["Section Completeness"] = section_score

    score += section_score


    # =========================================================
    # 2. Contact information
    # =========================================================

    contact_score = 0

    email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'

    phone_pattern = r'(\+?\d[\d\s\-]{8,}\d)'

    linkedin_found = (
        "linkedin.com" in lower_text
    )

    github_found = (
        "github.com" in lower_text
    )

    if re.search(
        email_pattern,
        text
    ):
        contact_score += 3

    else:
        suggestions.append(
            "Add a professional email address."
        )

    if re.search(
        phone_pattern,
        text
    ):
        contact_score += 2

    else:
        suggestions.append(
            "Add a phone number."
        )

    if linkedin_found:
        contact_score += 2

    else:
        suggestions.append(
            "Consider adding your LinkedIn profile."
        )

    if github_found:
        contact_score += 2

    else:
        suggestions.append(
            "Consider adding your GitHub profile."
        )

    contact_score = min(
        contact_score,
        9
    )

    breakdown["Contact Information"] = contact_score

    score += contact_score


    # =========================================================
    # 3. Quantifiable achievements
    # =========================================================

    number_patterns = [
        r'\d+%',
        r'\d+\+',
        r'\d+\s*(users|projects|models|datasets|records)',
        r'\d+\s*(seconds|minutes|hours)',
        r'\d+\s*(years|months)'
    ]

    quantified = any(
        re.search(
            pattern,
            text,
            re.IGNORECASE
        )
        for pattern in number_patterns
    )

    if quantified:

        impact_score = 10

    else:

        impact_score = 3

        suggestions.append(
            "Add measurable results to projects and experience, such as accuracy, performance improvements, scale, or time saved."
        )

    breakdown["Quantifiable Impact"] = impact_score

    score += impact_score


    # =========================================================
    # 4. Action verbs
    # =========================================================

    action_verbs = [
        "developed",
        "built",
        "implemented",
        "designed",
        "created",
        "optimized",
        "deployed",
        "automated",
        "analyzed",
        "engineered",
        "integrated",
        "trained",
        "improved"
    ]

    action_count = sum(
        lower_text.count(
            verb
        )
        for verb in action_verbs
    )

    action_score = min(
        action_count * 1.5,
        10
    )

    breakdown["Action-Oriented Writing"] = round(
        action_score,
        1
    )

    score += action_score

    if action_count < 3:

        suggestions.append(
            "Use stronger action verbs such as Built, Developed, Implemented, Optimized, and Deployed."
        )


    # =========================================================
    # 5. Resume length
    # =========================================================

    word_count = len(
        text.split()
    )

    if 300 <= word_count <= 1200:

        length_score = 8

    elif word_count < 300:

        length_score = 4

        suggestions.append(
            "Your resume appears short. Consider adding relevant project or experience details."
        )

    else:

        length_score = 5

        suggestions.append(
            "Consider reducing unnecessary content and keeping the resume concise."
        )

    breakdown["Content Length"] = length_score

    score += length_score


    # =========================================================
    # 6. Technical keywords
    # =========================================================

    technical_keywords = [
        "python",
        "java",
        "c++",
        "sql",
        "machine learning",
        "deep learning",
        "data structures",
        "algorithms",
        "aws",
        "docker",
        "git",
        "tensorflow",
        "pytorch"
    ]

    technical_count = sum(
        1
        for skill in technical_keywords
        if skill in lower_text
    )

    technical_score = min(
        technical_count * 1.5,
        12
    )

    breakdown["Technical Keyword Coverage"] = round(
        technical_score,
        1
    )

    score += technical_score


    # =========================================================
    # Final score
    # =========================================================

    score = min(
        round(score),
        100
    )

    return {
        "score": score,
        "breakdown": breakdown,
        "suggestions": suggestions
    }