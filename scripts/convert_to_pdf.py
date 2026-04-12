import os
import glob
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 12)
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')

def convert_md_to_pdf(md_file, pdf_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            pdf.ln(2)
            continue

        if line.startswith('# '):
            pdf.set_font("Helvetica", 'B', 16)
            pdf.multi_cell(0, 10, line[2:])
            pdf.ln(5)
        elif line.startswith('## '):
            pdf.set_font("Helvetica", 'B', 14)
            pdf.multi_cell(0, 10, line[3:])
            pdf.ln(2)
        elif line.startswith('### '):
            pdf.set_font("Helvetica", 'B', 12)
            pdf.multi_cell(0, 10, line[4:])
            pdf.ln(2)
        elif line.startswith('**'):
             pdf.set_font("Helvetica", 'B', 11)
             clean_line = line.replace('**', '')
             pdf.multi_cell(0, 8, clean_line)
             pdf.ln(1)
        else:
            pdf.set_font("Helvetica", size=11)
            # Handle UTF-8 safely for multilingual content
            text = line.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 8, text)
            pdf.ln(1)

    pdf.output(pdf_file)

if __name__ == "__main__":
    folders = ["manuscripts", "manuscripts/en", "manuscripts/fr"]
    for folder in folders:
        if not os.path.exists(folder): continue
        md_files = glob.glob(os.path.join(folder, "*.md"))
        for md_file in sorted(md_files):
            pdf_file = md_file.replace(".md", ".pdf")
            print(f"Converting {md_file} to {pdf_file}...")
            convert_md_to_pdf(md_file, pdf_file)
    print("Conversion complete.")
