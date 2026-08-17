from src.parser import extract_text_from_pdf
from src.skill_extractor import find_similar_skills


PDF_PATH = "test_resume.pdf"


with open(PDF_PATH, "rb") as pdf_file:

    text = extract_text_from_pdf(
        pdf_file
    )


results = find_similar_skills(
    text,
    threshold=0.55
)


print(
    "\n========== EXTRACTED RESUME SKILLS ==========\n"
)


for result in results:

    print(
        f"{result['skill']:<35}"
        f" | {result['category']:<20}"
        f" | similarity={result['similarity']}"
        f" | source='{result['source_phrase']}'"
    )


print(
    "\n=============================================="
)
