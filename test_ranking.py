from src.parser import extract_text_from_pdf
from src.ranking import rank_jobs


resume_path = "test_resume.pdf"

with open(resume_path, "rb") as f:
    resume_text = extract_text_from_pdf(f)


results = rank_jobs(
    resume_text,
    "data/jobs.csv",
    top_n=10
)


print("\n")
print("=" * 70)
print("           TOP JOB RECOMMENDATIONS")
print("=" * 70)


for i, job in enumerate(results, start=1):

    print(f"\n{i}. {job['job_title']}")

    print(
        f"   Overall Match : {job['overall_match']:.2f}%"
    )

    print(
        f"   Semantic Match: {job['semantic_match']:.2f}%"
    )

    print(
        f"   Skill Match   : {job['skill_match']:.2f}%"
    )

    print(
        "   Matched Skills:",
        ", ".join(job["matched_skills"])
    )

    if job["missing_skills"]:
        print(
            "   Skill Gaps    :",
            ", ".join(job["missing_skills"])
        )
    else:
        print("   Skill Gaps    : None")


print("\n" + "=" * 70)