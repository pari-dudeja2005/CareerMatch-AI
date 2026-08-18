# CareerMatch AI

An AI-powered resume analysis and job recommendation system that analyzes resumes, extracts skills, evaluates ATS compatibility, and ranks suitable job roles using semantic similarity, skill matching, and weighted scoring.

## Live Demo

[Open CareerMatch AI](https://careermatch-ai-05.streamlit.app/)

## Overview

CareerMatch AI helps candidates understand which job roles best match their resume.

The application takes a resume in PDF format and processes it through multiple stages:

```text
Resume PDF
    |
    v
Resume Parsing
    |
    v
Skill Extraction
    |
    v
Resume Embeddings
    |
    v
Job Description Analysis
    |
    v
Semantic Similarity
    |
    v
Skill Matching
    |
    v
Weighted Scoring
    |
    v
Job Ranking
    |
    v
ATS Analysis
```

The final output provides ranked job recommendations along with resume and ATS insights.

## Key Features

### Resume Parsing

Extracts text from uploaded PDF resumes and prepares it for further analysis.

### Skill Extraction

Identifies relevant technical skills from resumes using NLP-based processing and a predefined skill database.

### Semantic Matching

Uses transformer-based sentence embeddings to measure semantic similarity between resume content and job descriptions.

### Skill Matching

Compares the skills present in a resume with the skills associated with different job roles.

### Weighted Scoring

Combines semantic similarity and skill-based signals to calculate an overall job compatibility score.

### Job Ranking

Ranks job roles according to their calculated compatibility scores and returns the most relevant positions.

### ATS Analysis

Analyzes resumes for ATS-related factors and provides insights that can help improve resume compatibility.

### Model Evaluation

Includes an evaluation pipeline to measure the ranking and classification performance of the system.

## Supported Job Roles

The current system evaluates resumes across the following roles:

* Software Development Engineer
* AI Engineer
* Machine Learning Engineer
* Data Scientist
* Data Engineer
* Computer Vision Engineer
* Generative AI Engineer
* DevOps Engineer
* Cybersecurity Analyst
* Python Software Engineer

## Model Evaluation

The model was evaluated on a dataset of **50 resumes** across 10 job categories.

| Metric               |   Score |
| -------------------- | ------: |
| Total Resumes        |      50 |
| Top-1 Accuracy       |  94.00% |
| Top-3 Accuracy       | 100.00% |
| Top-5 Accuracy       | 100.00% |
| Mean Reciprocal Rank |  0.9700 |
| Precision            |  94.73% |
| Recall               |  94.00% |
| F1 Score             |  94.02% |

### Evaluation Summary

* **94% Top-1 accuracy** means the expected job role was ranked first for 47 out of 50 resumes.
* **100% Top-3 accuracy** means the expected job role appeared within the top three recommendations for every evaluated resume.
* **100% Top-5 accuracy** means every expected role appeared within the top five recommendations.
* **MRR of 0.9700** indicates that the correct job role was generally ranked very highly.

The detailed evaluation results are available in:

```text
data/evaluation_results.csv
```

## Technologies Used

### Programming

* Python

### Machine Learning and NLP

* Sentence Transformers
* PyTorch
* spaCy
* Hugging Face Transformers
* Scikit-learn

### Data Processing

* Pandas
* NumPy

### Resume Processing

* PyMuPDF

### Application

* Streamlit

## Project Structure

```text
CareerMatch-AI/
│
├── app.py
├── evaluate_model.py
├── generate_test_resumes.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── evaluation.csv
│   ├── jobs.csv
│   ├── skills.csv
│   └── skill_weights.csv
│
├── src/
│   ├── __init__.py
│   ├── ats_analyzer.py
│   ├── embeddings.py
│   ├── evaluator.py
│   ├── jd_analyzer.py
│   ├── parser.py
│   ├── ranking.py
│   ├── scoring.py
│   ├── skill_extractor.py
│   └── skills.py
│
└── test_resume.pdf
```

## How the Ranking Works

CareerMatch AI uses multiple signals instead of relying on a single similarity score.

### 1. Resume Representation

The uploaded resume is parsed and converted into structured text.

### 2. Skill Extraction

Technical skills are extracted from the resume using NLP processing.

### 3. Semantic Embeddings

Resume content and job descriptions are represented using transformer-based embeddings.

### 4. Similarity Calculation

Semantic similarity is calculated between the candidate's resume and each available job role.

### 5. Skill Compatibility

The candidate's extracted skills are compared with the skills required for each role.

### 6. Weighted Score

The different matching signals are combined into a final compatibility score.

### 7. Ranking

All available job roles are sorted according to their final scores.

The highest-ranked roles are presented as the candidate's best matches.

## Installation

Clone the repository:

```bash
git clone https://github.com/pari-dudeja2005/CareerMatch-AI.git
cd CareerMatch-AI
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

### macOS / Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Running Locally

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will be available at the local Streamlit URL shown in the terminal.

## Running Model Evaluation

To evaluate the model on the evaluation dataset:

```bash
python evaluate_model.py
```

The evaluation script reports:

* Top-1 Accuracy
* Top-3 Accuracy
* Top-5 Accuracy
* Mean Reciprocal Rank
* Precision
* Recall
* F1 Score

Detailed results are saved to:

```text
data/evaluation_results.csv
```

## Example Workflow

1. Upload a resume in PDF format.
2. CareerMatch AI extracts the resume text.
3. Relevant skills are identified.
4. The resume is converted into semantic embeddings.
5. The system compares the resume against available job roles.
6. Skill compatibility and semantic similarity are combined.
7. Job roles are ranked according to their compatibility.
8. ATS-related resume insights are displayed.

## Why CareerMatch AI?

Traditional job searching often requires candidates to manually compare their resumes with multiple job descriptions.

CareerMatch AI automates this process by combining:

* NLP
* Semantic embeddings
* Skill extraction
* Skill weighting
* Resume analysis
* Job ranking
* ATS analysis

This provides candidates with a data-driven way to understand which roles are most aligned with their existing skills.

## Future Improvements

Potential improvements include:

* Expanding the job-role dataset
* Adding more diverse resumes for evaluation
* Improving skill extraction
* Adding experience-level matching
* Adding education and qualification matching
* Incorporating job-description keyword analysis
* Improving ranking explainability
* Providing personalized resume improvement suggestions
* Expanding ATS analysis
* Supporting additional job categories
* Adding recruiter-side candidate ranking

## Project Status

CareerMatch AI is currently available as a Streamlit application.

Live application:

https://careermatch-ai-05.streamlit.app/

## Author

**Pari Dudeja**

B.Tech in Artificial Intelligence and Machine Learning

GitHub: [pari-dudeja2005](https://github.com/pari-dudeja2005)

## License

This project is intended for educational and portfolio purposes.
