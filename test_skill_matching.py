from src.skill_extractor import find_similar_skills


text = """
I developed predictive machine learning models
using Python and worked with large datasets.
"""


results = find_similar_skills(
    text,
    threshold=0.45
)


print(
    "\n========== SEMANTIC SKILL EXTRACTION ==========\n"
)


for result in results[:15]:

    print(
        f"{result['skill']:<30}"
        f" | similarity={result['similarity']}"
        f" | source='{result['source_phrase']}'"
    )


print(
    "\n================================================"
)