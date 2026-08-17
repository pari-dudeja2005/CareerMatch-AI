import pandas as pd

from src.scoring import calculate_job_match


# ============================================================
# DOMAIN SKILLS
# ============================================================

DOMAIN_SKILLS = {

    "cybersecurity": {
        "cybersecurity", "cyber security", "information security",
        "network security", "application security", "cloud security",
        "security operations", "soc", "siem", "splunk", "wireshark",
        "penetration testing", "penetration test", "ethical hacking",
        "vulnerability assessment", "vulnerability management",
        "incident response", "threat detection", "threat intelligence",
        "iam", "identity access management", "firewall", "ids", "ips",
        "kali linux", "burp suite", "metasploit", "cryptography",
        "malware analysis"
    },

    "machine learning": {
        "machine learning", "deep learning", "supervised learning",
        "unsupervised learning", "model training", "model evaluation",
        "feature engineering", "scikit learn", "tensorflow",
        "pytorch", "keras"
    },

    "ai": {
        "artificial intelligence", "machine learning", "deep learning",
        "generative ai", "large language models", "llm",
        "natural language processing", "computer vision",
        "transformers", "rag",
        "retrieval augmented generation"
    },

    "data engineering": {
        "data engineering", "data pipeline", "data pipelines",
        "etl", "elt", "apache spark", "pyspark", "hadoop", "hdfs",
        "apache nifi", "data warehouse", "data lake", "airflow"
    },

    "software engineering": {
        "software engineering", "software development",
        "application development", "backend", "rest api",
        "microservices", "spring boot", "node js", "javascript",
        "typescript", "react", "java", "c++", "python"
    },

    "computer vision": {
        "computer vision", "image processing", "opencv", "cnn",
        "convolutional neural network", "object detection",
        "image classification", "image segmentation"
    },

    "nlp": {
        "natural language processing", "nlp", "transformers",
        "hugging face", "bert", "text classification",
        "text processing", "semantic similarity",
        "large language models"
    },

    "generative ai": {
        "generative ai", "genai", "large language models",
        "llm", "rag", "retrieval augmented generation",
        "prompt engineering", "langchain", "transformers",
        "hugging face", "vector database", "embeddings"
    },

    "cloud": {
        "cloud computing", "aws", "azure", "google cloud", "gcp",
        "ec2", "s3", "lambda", "kubernetes", "docker"
    }
}


# ============================================================
# ROLE ALIASES
# ============================================================

ROLE_ALIASES = {

    "software development engineer": [
        "software development engineer",
        "software engineer",
        "software developer",
        "sde"
    ],

    "python software engineer": [
        "python software engineer",
        "python developer",
        "python engineer"
    ],

    "backend software engineer": [
        "backend software engineer",
        "backend engineer",
        "backend developer"
    ],

    "ai engineer": [
        "ai engineer",
        "artificial intelligence engineer"
    ],

    "machine learning engineer": [
        "machine learning engineer",
        "ml engineer"
    ],

    "data scientist": [
        "data scientist"
    ],

    "data engineer": [
        "data engineer"
    ],

    "computer vision engineer": [
        "computer vision engineer",
        "computer vision"
    ],

    "generative ai engineer": [
        "generative ai engineer",
        "genai engineer"
    ],

    "devops engineer": [
        "devops engineer"
    ],

    "cybersecurity analyst": [
        "cybersecurity analyst",
        "security analyst"
    ]
}


# ============================================================
# ROLE FAMILIES
#
# These help distinguish closely related roles.
# ============================================================

ROLE_FAMILIES = {

    "ai engineer": {
        "artificial intelligence": 3.0,
        "ai": 3.0,
        "machine learning": 2.0,
        "deep learning": 2.0,
        "generative ai": 2.0,
        "llm": 1.5,
        "computer vision": 1.5,
        "natural language processing": 1.5,
        "nlp": 1.5,
        "transformers": 1.0
    },

    "machine learning engineer": {
        "machine learning": 3.0,
        "deep learning": 2.5,
        "model training": 2.0,
        "model evaluation": 2.0,
        "feature engineering": 2.0,
        "tensorflow": 1.5,
        "pytorch": 1.5,
        "scikit learn": 1.5
    },

    "generative ai engineer": {
        "generative ai": 4.0,
        "genai": 4.0,
        "large language models": 3.0,
        "llm": 3.0,
        "rag": 3.0,
        "retrieval augmented generation": 3.0,
        "langchain": 2.0,
        "prompt engineering": 2.0,
        "transformers": 1.5,
        "embeddings": 1.5,
        "vector database": 1.5
    },

    "nlp engineer": {
        "natural language processing": 4.0,
        "nlp": 4.0,
        "text processing": 2.5,
        "text classification": 2.5,
        "bert": 2.0,
        "transformers": 2.0,
        "hugging face": 1.5,
        "semantic similarity": 1.5,
        "large language models": 1.5
    },

    "computer vision engineer": {
        "computer vision": 4.0,
        "image processing": 3.0,
        "opencv": 2.5,
        "object detection": 2.5,
        "image classification": 2.5,
        "image segmentation": 2.5,
        "cnn": 2.0,
        "convolutional neural network": 2.0
    },

    "cybersecurity analyst": {
        "cybersecurity": 4.0,
        "cyber security": 4.0,
        "information security": 3.0,
        "security operations": 3.0,
        "soc": 2.5,
        "siem": 2.5,
        "incident response": 2.5,
        "threat detection": 2.5,
        "threat intelligence": 2.0,
        "vulnerability assessment": 2.0,
        "vulnerability management": 2.0,
        "penetration testing": 1.5,
        "network security": 1.5,
        "firewall": 1.0
    },

    "python software engineer": {
        "python": 4.0,
        "software development": 2.5,
        "software engineering": 2.5,
        "application development": 2.0,
        "rest api": 1.5,
        "api": 1.5,
        "flask": 1.5,
        "fastapi": 1.5,
        "django": 1.5
    },

    "software development engineer": {
        "software development": 3.0,
        "software engineering": 3.0,
        "application development": 2.5,
        "java": 2.0,
        "python": 1.5,
        "c++": 1.5,
        "javascript": 1.5,
        "rest api": 1.5,
        "microservices": 1.5
    }
}


# ============================================================
# GENERIC ROLES
# ============================================================

GENERIC_ROLES = {
    "technical consultant",
    "solutions engineer",
    "technical business analyst",
    "product engineer"
}


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):

    text = str(text).lower()

    replacements = [
        ("-", " "),
        ("_", " "),
        ("/", " "),
        (".", " "),
        ("(", " "),
        (")", " "),
        (",", " ")
    ]

    for old, new in replacements:
        text = text.replace(old, new)

    return " ".join(text.split())


# ============================================================
# SKILL MATCHING
# ============================================================

def contains_skill(text, skill):

    return normalize_text(skill) in normalize_text(text)


# ============================================================
# PARSE SKILLS
# ============================================================

def parse_skills(value):

    if value is None:
        return []

    try:
        if pd.isna(value):
            return []
    except Exception:
        pass

    text = str(value).strip()

    if not text:
        return []

    for separator in [";", "|"]:

        if separator in text:

            return [
                item.strip()
                for item in text.split(separator)
                if item.strip()
            ]

    return [
        item.strip()
        for item in text.split(",")
        if item.strip()
    ]


# ============================================================
# GET JOB SKILLS
# ============================================================

def get_job_skills(job):

    required = parse_skills(
        job.get("required_skills", "")
    )

    preferred = parse_skills(
        job.get("preferred_skills", "")
    )

    return required, preferred


# ============================================================
# DOMAIN DETECTION
# ============================================================

def detect_job_domain(
    job_title,
    job_description
):

    text = normalize_text(
        f"{job_title} {job_description}"
    )

    scores = {}

    for domain, skills in DOMAIN_SKILLS.items():

        scores[domain] = sum(
            1
            for skill in skills
            if contains_skill(text, skill)
        )

    if not scores:
        return None

    best_domain = max(
        scores,
        key=scores.get
    )

    if scores[best_domain] == 0:
        return None

    return best_domain


# ============================================================
# DOMAIN RELEVANCE
# ============================================================

def calculate_domain_relevance(
    resume_text,
    job_title,
    job_description
):

    domain = detect_job_domain(
        job_title,
        job_description
    )

    if domain is None:
        return 1.0, None, 0

    resume_text = normalize_text(
        resume_text
    )

    domain_skills = DOMAIN_SKILLS[
        domain
    ]

    matched = sum(
        1
        for skill in domain_skills
        if contains_skill(
            resume_text,
            skill
        )
    )

    relevance = min(
        matched / min(
            len(domain_skills),
            8
        ),
        1.0
    )

    return (
        relevance,
        domain,
        matched
    )


# ============================================================
# TITLE ALIGNMENT
# ============================================================

def calculate_title_alignment(
    resume_text,
    job_title,
    job_description
):

    resume = normalize_text(
        resume_text
    )

    title = normalize_text(
        job_title
    )

    aliases = ROLE_ALIASES.get(
        title,
        [title]
    )

    for alias in aliases:

        if normalize_text(alias) in resume:
            return 100.0

    return 0.0


# ============================================================
# ROLE FAMILY SCORE
#
# Important for distinguishing:
#
# AI vs ML
# AI vs NLP
# GenAI vs NLP
# Python SWE vs SWE
# Cybersecurity vs Network Security
# ============================================================

def calculate_role_family_score(
    resume_text,
    job_title
):

    normalized_title = normalize_text(
        job_title
    )

    if normalized_title not in ROLE_FAMILIES:
        return 0.0

    resume = normalize_text(
        resume_text
    )

    role_skills = ROLE_FAMILIES[
        normalized_title
    ]

    total_weight = sum(
        role_skills.values()
    )

    matched_weight = 0.0

    for skill, weight in role_skills.items():

        if contains_skill(
            resume,
            skill
        ):

            matched_weight += weight

    if total_weight == 0:
        return 0.0

    return round(
        min(
            matched_weight /
            total_weight *
            100,
            100
        ),
        2
    )


# ============================================================
# ROLE FAMILY BOOST
#
# Gives a controlled advantage to a specialized role when
# the resume contains its characteristic skills.
# ============================================================

def calculate_role_boost(
    resume_text,
    job_title
):

    role_score = calculate_role_family_score(
        resume_text,
        job_title
    )

    normalized_title = normalize_text(
        job_title
    )

    if normalized_title not in ROLE_FAMILIES:
        return 0.0

    # Only apply meaningful boost when there is evidence.
    if role_score >= 70:
        return 8.0

    if role_score >= 50:
        return 5.0

    if role_score >= 30:
        return 2.5

    return 0.0


# ============================================================
# RANK JOBS
# ============================================================

def rank_jobs(
    resume_text,
    csv_path="data/jobs.csv",
    top_n=10
):

    jobs = pd.read_csv(
        csv_path
    )

    results = []

    for _, job in jobs.iterrows():

        job_title = str(
            job.get(
                "job_title",
                "Unknown"
            )
        )

        job_description = str(
            job.get(
                "job_description",
                ""
            )
        )

        required_skills, preferred_skills = (
            get_job_skills(job)
        )

        # ----------------------------------------------------
        # BASE MATCHING
        # ----------------------------------------------------

        score = calculate_job_match(
            resume_text=resume_text,
            job_description=job_description,
            required_skills=required_skills,
            preferred_skills=preferred_skills
        )

        semantic = float(
            score.get(
                "semantic_match",
                0
            )
        )

        skill = float(
            score.get(
                "skill_match",
                0
            )
        )

        required_score = float(
            score.get(
                "required_skill_score",
                0
            )
        )

        preferred_score = float(
            score.get(
                "preferred_skill_score",
                0
            )
        )

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        title_alignment = (
            calculate_title_alignment(
                resume_text,
                job_title,
                job_description
            )
        )

        # ----------------------------------------------------
        # DOMAIN
        # ----------------------------------------------------

        domain_relevance, domain, domain_matches = (
            calculate_domain_relevance(
                resume_text,
                job_title,
                job_description
            )
        )

        # ----------------------------------------------------
        # ROLE FAMILY
        # ----------------------------------------------------

        role_family_score = (
            calculate_role_family_score(
                resume_text,
                job_title
            )
        )

        role_boost = (
            calculate_role_boost(
                resume_text,
                job_title
            )
        )

        # ----------------------------------------------------
        # MAIN SCORE
        #
        # Keep the successful formula mostly intact.
        # Add role-family evidence as a controlled component.
        # ----------------------------------------------------

        final_score = (
            semantic * 0.32
            + required_score * 0.38
            + preferred_score * 0.12
            + title_alignment * 0.08
            + role_family_score * 0.10
        )

        # ----------------------------------------------------
        # GENERIC ROLE PENALTY
        # ----------------------------------------------------

        normalized_title = normalize_text(
            job_title
        )

        if normalized_title in GENERIC_ROLES:

            specialized_score = max(
                required_score,
                preferred_score
            )

            if specialized_score < 60:
                final_score *= 0.90

            if required_score < 50:
                final_score *= 0.90

        # ----------------------------------------------------
        # SPECIALIZED DOMAIN PENALTY
        # ----------------------------------------------------

        specialized_domains = {
            "cybersecurity",
            "computer vision",
            "nlp",
            "generative ai",
            "data engineering",
            "machine learning",
            "ai"
        }

        if domain in specialized_domains:

            if domain_matches == 0:

                final_score *= 0.75

            elif domain_matches == 1:

                final_score *= 0.85

        # ----------------------------------------------------
        # CYBERSECURITY SPECIFIC ADJUSTMENT
        #
        # Prevent network-security-heavy resumes from
        # automatically overpowering Cybersecurity Analyst.
        # ----------------------------------------------------

        if normalized_title == "cybersecurity analyst":

            cyber_score = role_family_score

            if cyber_score >= 50:
                final_score += 4.0

        # ----------------------------------------------------
        # AI ENGINEER SPECIFIC ADJUSTMENT
        #
        # AI Engineer should remain competitive against
        # ML/NLP/CV when the resume demonstrates broad AI.
        # ----------------------------------------------------

        if normalized_title == "ai engineer":

            resume_normalized = normalize_text(
                resume_text
            )

            broad_ai_signals = [
                "artificial intelligence",
                "machine learning",
                "deep learning",
                "generative ai",
                "computer vision",
                "natural language processing",
                "large language models"
            ]

            ai_signal_count = sum(
                1
                for signal in broad_ai_signals
                if signal in resume_normalized
            )

            if ai_signal_count >= 3:
                final_score += 4.0

            elif ai_signal_count >= 2:
                final_score += 2.0

        # ----------------------------------------------------
        # GENERATIVE AI SPECIFIC ADJUSTMENT
        # ----------------------------------------------------

        if normalized_title == "generative ai engineer":

            resume_normalized = normalize_text(
                resume_text
            )

            genai_signals = [
                "generative ai",
                "genai",
                "llm",
                "large language models",
                "rag",
                "retrieval augmented generation",
                "langchain",
                "prompt engineering",
                "vector database",
                "embeddings"
            ]

            genai_count = sum(
                1
                for signal in genai_signals
                if signal in resume_normalized
            )

            if genai_count >= 4:
                final_score += 6.0

            elif genai_count >= 2:
                final_score += 3.0

        # ----------------------------------------------------
        # PYTHON SOFTWARE ENGINEER SPECIFIC ADJUSTMENT
        # ----------------------------------------------------

        if normalized_title == "python software engineer":

            resume_normalized = normalize_text(
                resume_text
            )

            python_signals = [
                "python",
                "flask",
                "fastapi",
                "django",
                "rest api",
                "api",
                "software development"
            ]

            python_count = sum(
                1
                for signal in python_signals
                if signal in resume_normalized
            )

            if python_count >= 4:
                final_score += 5.0

            elif python_count >= 2:
                final_score += 2.5

        # ----------------------------------------------------
        # SOFTWARE DEVELOPMENT ENGINEER
        #
        # Avoid allowing generic Python/software skills to
        # dominate when a specialized Python role exists.
        # ----------------------------------------------------

        if normalized_title == "software development engineer":

            resume_normalized = normalize_text(
                resume_text
            )

            python_specific_signals = [
                "python developer",
                "python engineer",
                "fastapi",
                "flask",
                "django"
            ]

            python_specific_count = sum(
                1
                for signal in python_specific_signals
                if signal in resume_normalized
            )

            if python_specific_count >= 2:

                final_score *= 0.96

        # ----------------------------------------------------
        # FINAL SCORE
        # ----------------------------------------------------

        final_score = round(
            max(
                0,
                min(
                    final_score,
                    100
                )
            ),
            2
        )

        # ----------------------------------------------------
        # STORE RESULT
        # ----------------------------------------------------

        results.append({

            "job_title":
                job_title,

            "job_description":
                job_description,

            "semantic_match":
                round(
                    semantic,
                    2
                ),

            "skill_match":
                round(
                    skill,
                    2
                ),

            "overall_match":
                final_score,

            "matched_skills":
                score.get(
                    "matched_skills",
                    []
                ),

            "missing_skills":
                score.get(
                    "missing_skills",
                    []
                ),

            "matched_required":
                score.get(
                    "matched_required",
                    []
                ),

            "missing_required":
                score.get(
                    "missing_required",
                    []
                ),

            "matched_preferred":
                score.get(
                    "matched_preferred",
                    []
                ),

            "missing_preferred":
                score.get(
                    "missing_preferred",
                    []
                ),

            "required_skill_score":
                required_score,

            "preferred_skill_score":
                preferred_score,

            "title_alignment":
                round(
                    title_alignment,
                    2
                ),

            "role_family_score":
                role_family_score,

            "role_boost":
                role_boost,

            "domain":
                domain,

            "domain_relevance":
                round(
                    domain_relevance * 100,
                    2
                )
        })

    # ========================================================
    # SORT
    # ========================================================

    results.sort(
        key=lambda item:
            item["overall_match"],
        reverse=True
    )

    return results[:top_n]