import os
import pandas as pd


# ============================================================
# CONFIG
# ============================================================

JOBS_FILE = "data/jobs.csv"
OUTPUT_FILE = "data/evaluation.csv"


# ============================================================
# 30 SYNTHETIC TEST RESUMES
#
# These intentionally contain overlapping skills so that
# ranking is not based only on exact job-title keywords.
# ============================================================

RESUMES = [

    # --------------------------------------------------------
    # SOFTWARE DEVELOPMENT ENGINEER
    # --------------------------------------------------------

    {
        "resume_id": "R11",
        "expected_job": "Software Development Engineer",
        "resume_text": """
        Software engineer with experience in Java, Python, C++,
        object-oriented programming, data structures and algorithms,
        REST APIs, SQL, Git and software development.
        Built scalable applications and backend services.
        Strong knowledge of problem solving, system design,
        debugging and database management.
        """
    },

    {
        "resume_id": "R12",
        "expected_job": "Software Development Engineer",
        "resume_text": """
        Computer science graduate skilled in Java, Python,
        JavaScript, SQL, Git, REST APIs and application development.
        Developed backend applications and automated testing tools.
        Strong understanding of OOP, DSA, DBMS and software engineering.
        Familiar with Docker and cloud deployment.
        """
    },

    {
        "resume_id": "R13",
        "expected_job": "Software Development Engineer",
        "resume_text": """
        Software developer experienced with Python, Java and C++.
        Worked on application development, APIs, databases,
        debugging and version control using Git.
        Strong programming fundamentals, algorithms and
        object-oriented design. Some exposure to machine learning
        and cloud technologies.
        """
    },


    # --------------------------------------------------------
    # AI ENGINEER
    # --------------------------------------------------------

    {
        "resume_id": "R14",
        "expected_job": "AI Engineer",
        "resume_text": """
        AI engineer with experience in artificial intelligence,
        machine learning, deep learning, Python, TensorFlow,
        PyTorch and model evaluation.
        Built intelligent applications using NLP, computer vision
        and generative AI. Familiar with transformers and LLMs.
        """
    },

    {
        "resume_id": "R15",
        "expected_job": "AI Engineer",
        "resume_text": """
        Machine learning developer experienced in Python,
        scikit-learn, TensorFlow, PyTorch, deep learning,
        NLP and computer vision.
        Built predictive models and AI applications.
        Experience with feature engineering, model training,
        evaluation and deployment.
        """
    },

    {
        "resume_id": "R16",
        "expected_job": "AI Engineer",
        "resume_text": """
        Artificial intelligence enthusiast with strong Python,
        machine learning and deep learning skills.
        Worked with neural networks, transformers, NLP,
        computer vision and generative AI.
        Built intelligent systems using PyTorch and Hugging Face.
        """
    },


    # --------------------------------------------------------
    # DATA SCIENTIST
    # --------------------------------------------------------

    {
        "resume_id": "R17",
        "expected_job": "Data Scientist",
        "resume_text": """
        Data scientist skilled in Python, Pandas, NumPy,
        scikit-learn, statistics, machine learning and data analysis.
        Experienced in exploratory data analysis, feature engineering,
        predictive modeling and model evaluation.
        Worked with SQL and visualization tools.
        """
    },

    {
        "resume_id": "R18",
        "expected_job": "Data Scientist",
        "resume_text": """
        Analytics professional with Python, SQL, statistics,
        machine learning, Pandas and NumPy.
        Built classification and regression models.
        Experience with data preprocessing, exploratory analysis,
        feature selection and model validation.
        """
    },

    {
        "resume_id": "R19",
        "expected_job": "Data Scientist",
        "resume_text": """
        Machine learning and analytics graduate experienced in
        Python, SQL, statistics, scikit-learn and data visualization.
        Performed exploratory data analysis and developed predictive
        models. Familiar with deep learning and NLP.
        """
    },


    # --------------------------------------------------------
    # DATA ENGINEER
    # --------------------------------------------------------

    {
        "resume_id": "R20",
        "expected_job": "Data Engineer",
        "resume_text": """
        Data engineer experienced in ETL pipelines, Apache Spark,
        PySpark, Hadoop, HDFS, SQL and Python.
        Built data processing workflows and data pipelines.
        Familiar with data warehouses, data lakes and Apache Airflow.
        """
    },

    {
        "resume_id": "R21",
        "expected_job": "Data Engineer",
        "resume_text": """
        Data engineering professional skilled in Python, SQL,
        ETL, Apache NiFi, Hadoop, HDFS and data pipelines.
        Developed batch processing workflows and transformed
        large datasets. Familiar with cloud data platforms.
        """
    },

    {
        "resume_id": "R22",
        "expected_job": "Data Engineer",
        "resume_text": """
        Big data developer experienced with Spark, PySpark,
        Hadoop, HDFS, Python, SQL and ETL.
        Built scalable data pipelines and data processing systems.
        Exposure to data lakes, warehouses and Airflow.
        """
    },


    # --------------------------------------------------------
    # COMPUTER VISION ENGINEER
    # --------------------------------------------------------

    {
        "resume_id": "R23",
        "expected_job": "Computer Vision Engineer",
        "resume_text": """
        Computer vision engineer experienced with Python,
        OpenCV, CNNs, image processing, image classification
        and object detection.
        Built deep learning models for image analysis and
        automated visual inspection.
        """
    },

    {
        "resume_id": "R24",
        "expected_job": "Computer Vision Engineer",
        "resume_text": """
        AI developer specializing in computer vision,
        image processing, OpenCV, TensorFlow and PyTorch.
        Worked on object detection, image segmentation,
        classification and convolutional neural networks.
        """
    },

    {
        "resume_id": "R25",
        "expected_job": "Computer Vision Engineer",
        "resume_text": """
        Machine learning engineer with strong computer vision
        experience. Skilled in Python, OpenCV, CNN,
        image classification, image segmentation and object detection.
        Built deep learning models for medical image analysis.
        """
    },


    # --------------------------------------------------------
    # GENERATIVE AI ENGINEER
    # --------------------------------------------------------

    {
        "resume_id": "R26",
        "expected_job": "Generative AI Engineer",
        "resume_text": """
        Generative AI engineer experienced with Python, LLMs,
        transformers, Hugging Face, RAG and natural language processing.
        Built retrieval augmented generation applications and
        AI assistants using vector databases.
        """
    },

    {
        "resume_id": "R27",
        "expected_job": "Generative AI Engineer",
        "resume_text": """
        AI developer specializing in large language models,
        generative AI, NLP, transformers, embeddings and RAG.
        Built document question-answering systems and
        LLM-powered applications using Python.
        """
    },

    {
        "resume_id": "R28",
        "expected_job": "Generative AI Engineer",
        "resume_text": """
        Machine learning engineer with experience in generative AI,
        LLMs, Hugging Face, transformers, semantic similarity
        and retrieval augmented generation.
        Developed intelligent chatbots and document processing systems.
        """
    },


    # --------------------------------------------------------
    # DEVOPS ENGINEER
    # --------------------------------------------------------

    {
        "resume_id": "R29",
        "expected_job": "DevOps Engineer",
        "resume_text": """
        DevOps engineer experienced with Docker, Kubernetes,
        AWS, CI/CD, Jenkins, Git and Linux.
        Built automated deployment pipelines and containerized
        applications. Familiar with EC2, S3 and cloud infrastructure.
        """
    },

    {
        "resume_id": "R30",
        "expected_job": "DevOps Engineer",
        "resume_text": """
        Cloud and DevOps professional skilled in AWS, Docker,
        Kubernetes, Jenkins, Git and Linux.
        Experience with continuous integration, continuous deployment,
        container orchestration and infrastructure automation.
        """
    },


    # --------------------------------------------------------
    # CYBERSECURITY ANALYST
    # --------------------------------------------------------

    {
        "resume_id": "R31",
        "expected_job": "Cybersecurity Analyst",
        "resume_text": """
        Cybersecurity analyst experienced in network security,
        vulnerability assessment, SIEM, incident response,
        threat detection and security monitoring.
        Familiar with Wireshark, Splunk, firewalls and Linux.
        """
    },

    {
        "resume_id": "R32",
        "expected_job": "Cybersecurity Analyst",
        "resume_text": """
        Information security professional skilled in cybersecurity,
        penetration testing, vulnerability management,
        incident response and threat intelligence.
        Experience with Kali Linux, Burp Suite, Wireshark and SIEM.
        """
    },

    {
        "resume_id": "R33",
        "expected_job": "Cybersecurity Analyst",
        "resume_text": """
        Security analyst with experience in network security,
        application security, vulnerability assessment,
        ethical hacking and incident response.
        Familiar with firewalls, IDS, IPS, Splunk and Linux.
        """
    },


    # --------------------------------------------------------
    # PYTHON SOFTWARE ENGINEER
    # --------------------------------------------------------

    {
        "resume_id": "R34",
        "expected_job": "Python Software Engineer",
        "resume_text": """
        Python software engineer experienced in Python,
        object-oriented programming, REST APIs, SQL,
        application development and Git.
        Built automation tools and backend applications.
        Familiar with Docker, FastAPI and data processing.
        """
    },

    {
        "resume_id": "R35",
        "expected_job": "Python Software Engineer",
        "resume_text": """
        Python developer skilled in Python, FastAPI, REST APIs,
        SQL, Git and software development.
        Built backend applications, automation scripts and
        data processing pipelines. Familiar with AWS and Docker.
        """
    },

    {
        "resume_id": "R36",
        "expected_job": "Python Software Engineer",
        "resume_text": """
        Software engineer specializing in Python.
        Experience with APIs, databases, application development,
        testing and Git. Worked with Pandas, NumPy and machine
        learning libraries while building production applications.
        """
    },


    # --------------------------------------------------------
    # MIXED / HARD CASES
    # --------------------------------------------------------

    {
        "resume_id": "R37",
        "expected_job": "AI Engineer",
        "resume_text": """
        Software engineer transitioning into AI with strong Python,
        Java, SQL and REST API experience.
        Built machine learning models using scikit-learn and PyTorch.
        Worked on NLP, transformers and model deployment.
        """
    },

    {
        "resume_id": "R38",
        "expected_job": "Data Engineer",
        "resume_text": """
        Python developer with strong SQL and machine learning skills.
        Built ETL workflows, data pipelines and large-scale data
        processing systems using Spark and Hadoop.
        Some experience with predictive modeling.
        """
    },

    {
        "resume_id": "R39",
        "expected_job": "Software Development Engineer",
        "resume_text": """
        Python and Java developer with experience in machine learning,
        APIs, databases, Docker and Git.
        Built production software applications and automated
        data processing systems. Strong DSA and OOP fundamentals.
        """
    },

    {
        "resume_id": "R40",
        "expected_job": "Generative AI Engineer",
        "resume_text": """
        Python developer with experience in machine learning,
        NLP, transformers, LLMs and RAG.
        Built an AI-powered document assistant using embeddings
        and semantic search. Familiar with PyTorch and Hugging Face.
        """
    }
]


# ============================================================
# VALIDATE JOBS
# ============================================================

def load_jobs():

    if not os.path.exists(JOBS_FILE):
        raise FileNotFoundError(
            f"{JOBS_FILE} not found."
        )

    jobs = pd.read_csv(JOBS_FILE)

    required_columns = {
        "job_title",
        "job_description"
    }

    missing = required_columns - set(jobs.columns)

    if missing:
        raise ValueError(
            f"jobs.csv is missing columns: {missing}"
        )

    return jobs


# ============================================================
# BUILD EVALUATION DATASET
#
# IMPORTANT:
# Each resume is paired with EVERY job.
#
# This is exactly what evaluate_model.py expects.
# ============================================================

def build_evaluation_dataset():

    jobs = load_jobs()

    available_jobs = set(
        jobs["job_title"]
        .astype(str)
        .str.strip()
    )

    rows = []

    for resume in RESUMES:

        expected = resume["expected_job"]

        if expected not in available_jobs:
            print(
                f"WARNING: {resume['resume_id']} expects "
                f"'{expected}', but that job is not in jobs.csv"
            )

            continue

        for _, job in jobs.iterrows():

            rows.append({
                "resume_id":
                    resume["resume_id"],

                "resume_text":
                    resume["resume_text"].strip(),

                "job_title":
                    str(job["job_title"]).strip(),

                "job_description":
                    str(job["job_description"]).strip(),

                "expected_job":
                    expected
            })

    return pd.DataFrame(rows)


# ============================================================
# SAVE
# ============================================================

def main():

    evaluation_df = build_evaluation_dataset()

    if evaluation_df.empty:
        raise ValueError(
            "No evaluation rows were generated."
        )

    os.makedirs(
        os.path.dirname(OUTPUT_FILE),
        exist_ok=True
    )

    evaluation_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print()
    print("=" * 70)
    print("          TEST RESUME DATASET GENERATED")
    print("=" * 70)
    print()

    print(
        f"Unique resumes : "
        f"{evaluation_df['resume_id'].nunique()}"
    )

    print(
        f"Available jobs  : "
        f"{evaluation_df['job_title'].nunique()}"
    )

    print(
        f"Total rows      : "
        f"{len(evaluation_df)}"
    )

    print()
    print("Expected roles:")
    print()

    counts = (
        evaluation_df
        .groupby("resume_id")["expected_job"]
        .first()
        .value_counts()
    )

    for job, count in counts.items():
        print(
            f"  {job:<35} {count} resumes"
        )

    print()
    print(
        f"Saved to: {OUTPUT_FILE}"
    )

    print("=" * 70)
    print()


if __name__ == "__main__":
    main()