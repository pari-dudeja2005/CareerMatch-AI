import os
import tempfile
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)

from src.ranking import rank_jobs


# ============================================================
# CONFIGURATION
# ============================================================

EVALUATION_FILE = "data/evaluation.csv"


# ============================================================
# LOAD EVALUATION DATA
# ============================================================

def load_evaluation_data():

    if not os.path.exists(EVALUATION_FILE):
        raise FileNotFoundError(
            f"Evaluation file not found: {EVALUATION_FILE}"
        )

    df = pd.read_csv(EVALUATION_FILE)

    required_columns = {
        "resume_id",
        "resume_text",
        "job_title",
        "job_description",
        "expected_job"
    }

    missing_columns = (
        required_columns - set(df.columns)
    )

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    return df


# ============================================================
# EVALUATE ONE RESUME
# ============================================================

def evaluate_resume(
    resume_id,
    resume_text,
    jobs_df,
    expected_job
):

    # Create temporary CSV containing only the
    # candidate jobs for this resume.

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".csv",
        delete=False
    ) as temp_file:

        temp_path = temp_file.name

    try:

        jobs_for_ranking = jobs_df[
            [
                "job_title",
                "job_description"
            ]
        ].copy()

        jobs_for_ranking.to_csv(
            temp_path,
            index=False
        )

        rankings = rank_jobs(
            resume_text=resume_text,
            csv_path=temp_path,
            top_n=len(jobs_for_ranking)
        )

    finally:

        if os.path.exists(temp_path):
            os.remove(temp_path)

    ranked_jobs = [
        result["job_title"]
        for result in rankings
    ]

    # --------------------------------------------------------
    # FIND EXPECTED JOB RANK
    # --------------------------------------------------------

    try:

        rank = (
            ranked_jobs.index(expected_job)
            + 1
        )

    except ValueError:

        rank = None

    # --------------------------------------------------------
    # TOP-K
    # --------------------------------------------------------

    top_1 = (
        expected_job in ranked_jobs[:1]
    )

    top_3 = (
        expected_job in ranked_jobs[:3]
    )

    top_5 = (
        expected_job in ranked_jobs[:5]
    )

    # --------------------------------------------------------
    # RECIPROCAL RANK
    # --------------------------------------------------------

    if rank is None:

        reciprocal_rank = 0.0

    else:

        reciprocal_rank = 1 / rank

    # --------------------------------------------------------
    # BEST RESULT
    # --------------------------------------------------------

    best_result = rankings[0]

    return {

        "resume_id": resume_id,

        "expected_job": expected_job,

        "predicted_job": ranked_jobs[0],

        "rank": rank,

        "top_1": top_1,

        "top_3": top_3,

        "top_5": top_5,

        "reciprocal_rank": reciprocal_rank,

        "predicted_score":
            best_result["overall_match"],

        "predicted_semantic":
            best_result["semantic_match"],

        "predicted_skill":
            best_result["skill_match"],

        "ranked_jobs":
            ranked_jobs
    }


# ============================================================
# MAIN EVALUATION
# ============================================================

def main():

    print()
    print("=" * 70)
    print("              CAREERMATCH AI MODEL EVALUATION")
    print("=" * 70)
    print()

    df = load_evaluation_data()

    results = []

    # --------------------------------------------------------
    # PROCESS EACH RESUME
    # --------------------------------------------------------

    for resume_id, group in df.groupby(
        "resume_id",
        sort=False
    ):

        resume_text = group.iloc[0][
            "resume_text"
        ]

        expected_job = group.iloc[0][
            "expected_job"
        ]

        result = evaluate_resume(
            resume_id=resume_id,
            resume_text=resume_text,
            jobs_df=group,
            expected_job=expected_job
        )

        results.append(result)

    results_df = pd.DataFrame(
        results
    )

    # ========================================================
    # RETRIEVAL METRICS
    # ========================================================

    top_1_accuracy = (
        results_df["top_1"].mean()
        * 100
    )

    top_3_accuracy = (
        results_df["top_3"].mean()
        * 100
    )

    top_5_accuracy = (
        results_df["top_5"].mean()
        * 100
    )

    mean_reciprocal_rank = (
        results_df["reciprocal_rank"].mean()
    )

    # ========================================================
    # CLASSIFICATION METRICS
    # ========================================================

    y_true = results_df[
        "expected_job"
    ]

    y_pred = results_df[
        "predicted_job"
    ]

    accuracy = accuracy_score(
        y_true,
        y_pred
    )

    precision = precision_score(
        y_true,
        y_pred,
        average="weighted",
        zero_division=0
    )

    recall = recall_score(
        y_true,
        y_pred,
        average="weighted",
        zero_division=0
    )

    f1 = f1_score(
        y_true,
        y_pred,
        average="weighted",
        zero_division=0
    )

    # ========================================================
    # PRINT SUMMARY
    # ========================================================

    print()
    print("-" * 70)
    print("                    EVALUATION RESULTS")
    print("-" * 70)

    print(
        f"Total resumes tested : "
        f"{len(results_df)}"
    )

    print(
        f"Top-1 Accuracy       : "
        f"{top_1_accuracy:.2f}%"
    )

    print(
        f"Top-3 Accuracy       : "
        f"{top_3_accuracy:.2f}%"
    )

    print(
        f"Top-5 Accuracy       : "
        f"{top_5_accuracy:.2f}%"
    )

    print(
        f"MRR                  : "
        f"{mean_reciprocal_rank:.4f}"
    )

    print(
        f"Precision            : "
        f"{precision:.4f}"
    )

    print(
        f"Recall               : "
        f"{recall:.4f}"
    )

    print(
        f"F1 Score             : "
        f"{f1:.4f}"
    )

    # ========================================================
    # PER-RESUME RESULTS
    # ========================================================

    print()
    print("-" * 70)
    print("                    PER-RESUME RESULTS")
    print("-" * 70)

    for _, row in results_df.iterrows():

        print()
        print(
            f"{row['resume_id']}"
        )

        print(
            f"Expected : "
            f"{row['expected_job']}"
        )

        print(
            f"Predicted: "
            f"{row['predicted_job']}"
        )

        if pd.isna(row["rank"]):

            print(
                "Expected job rank: Not found"
            )

        else:

            print(
                f"Expected job rank: "
                f"#{int(row['rank'])}"
            )

        print(
            f"Top-1: "
            f"{'PASS' if row['top_1'] else 'FAIL'}"
        )

        print(
            f"Top-3: "
            f"{'PASS' if row['top_3'] else 'FAIL'}"
        )

        print(
            f"Top-5: "
            f"{'PASS' if row['top_5'] else 'FAIL'}"
        )

    # ========================================================
    # CLASSIFICATION REPORT
    # ========================================================

    print()
    print("-" * 70)
    print("                  CLASSIFICATION REPORT")
    print("-" * 70)

    print()

    print(
        classification_report(
            y_true,
            y_pred,
            zero_division=0
        )
    )

    # ========================================================
    # TOP 5 RANKINGS
    # ========================================================

    print()
    print("-" * 70)
    print("                     TOP 5 RANKINGS")
    print("-" * 70)

    for _, row in results_df.iterrows():

        print()
        print(
            f"{row['resume_id']} "
            f"Expected: {row['expected_job']}"
        )

        for index, job in enumerate(
            row["ranked_jobs"][:5],
            start=1
        ):

            marker = ""

            if job == row["expected_job"]:
                marker = "  <-- EXPECTED"

            print(
                f"  {index}. "
                f"{job}"
                f"{marker}"
            )

    # ========================================================
    # SAVE RESULTS
    # ========================================================

    output_file = (
        "data/evaluation_results.csv"
    )

    results_df[
        [
            "resume_id",
            "expected_job",
            "predicted_job",
            "rank",
            "top_1",
            "top_3",
            "top_5",
            "reciprocal_rank",
            "predicted_score",
            "predicted_semantic",
            "predicted_skill"
        ]
    ].to_csv(
        output_file,
        index=False
    )

    print()
    print("=" * 70)
    print(
        f"Detailed results saved to: "
        f"{output_file}"
    )
    print("=" * 70)
    print()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()