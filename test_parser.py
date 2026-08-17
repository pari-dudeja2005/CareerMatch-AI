from src.parser import extract_text_from_pdf


class TestPDF:
    def read(self):
        with open("test_resume.pdf", "rb") as f:
            return f.read()


pdf = TestPDF()

text = extract_text_from_pdf(pdf)

print("\n========== EXTRACTED TEXT ==========\n")
print(text)
print("\n====================================")