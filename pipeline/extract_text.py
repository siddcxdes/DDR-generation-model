import pdfplumber
import os

def extract_inspection_report(pdf_path):
    extracted_text = {}

    with pdfplumber.open(pdf_path) as pdf:
        print(f"Total Pages : {len(pdf.pages)}")

        for i, page in enumerate(pdf.pages, start = 1):
            text = page.extract_text()
            extracted_text[f"page_{i}"] = text

            print(f"Page {i} : {len(text)} characters extracted")
    return extracted_text
pdf_path = "/Users/sidxcodes/DDR Report Generation/input/Sample Report.pdf"
extracted_data = extract_inspection_report(pdf_path)

output_path = "/Users/sidxcodes/DDR Report Generation/extracted/report_text.txt"
output_dir = os.path.dirname(output_path)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open("extracted/report_text.txt", "w", encoding="utf-8") as f:
    for page_num, text in extracted_data.items():
        f.write(f"{page_num.upper()}\n")
        f.write(text)
        f.write("\n\n")




