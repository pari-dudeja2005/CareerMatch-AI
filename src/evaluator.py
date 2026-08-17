import pandas as pd

from src.scoring import calculate_job_match


def evaluate_model(
    evaluation_csv="data/evaluation.csv"
):

    df = pd.read_csv(
        evaluation_csv
    )

    total = len(df)

    correct_top1 = 0
    correct_top3 = 0

    results = []


    for resume_id in df[
        "resume_id"
    ].unique():

        resume_rows = df[
            df["resume_id"]
            == resume_id
        ]


        resume_text = resume_rows.iloc[0][
            "resume_text"
        ]


        expected_job = resume_rows.iloc[0][
            "expected_job"
        ]


        ranked = []


        for _, row in resume_rows.iterrows():

            score = calculate_job_match(
                resume_text,
                row["job_description"]
            )


            ranked.append({

                "job_title":
                    row["job_title"],

                "score":
                    score[
                        "overall_match"
                    ]
            })


        ranked.sort(
            key=lambda x:
            x["score"],
            reverse=True
        )


        top1 = ranked[0][
            "job_title"
        ]


        top3 = [
            item["job_title"]
            for item in ranked[:3]
        ]


        if top1 == expected_job:

            correct_top1 += 1


        if expected_job in top3:

            correct_top3 += 1


        results.append({

            "resume_id":
                resume_id,

            "expected_job":
                expected_job,

            "predicted_job":
                top1,

            "top3":
                ", ".join(top3)
        })


    if total == 0:

        return {
            "top1_accuracy": 0,
            "top3_accuracy": 0,
            "results": []
        }


    return {

        "top1_accuracy":
            round(
                correct_top1 /
                total *
                100,
                2
            ),

        "top3_accuracy":
            round(
                correct_top3 /
                total *
                100,
                2
            ),

        "results":
            results
    }