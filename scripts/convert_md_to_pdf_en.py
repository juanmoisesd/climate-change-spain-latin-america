import os
from fpdf import FPDF

class AcademicPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Scientific Meta-Analysis - Juan Moises de la Serna', 0, 0, 'R')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def md_to_pdf(md_file, pdf_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        text = f.read()

    pdf = AcademicPDF()
    pdf.set_left_margin(20)
    pdf.set_right_margin(20)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)

    # Pre-process text to remove common problematic characters for latin-1
    text = text.replace('**', '').replace('$', '').replace('•', '*')

    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            pdf.ln(5)
            continue

        if line.startswith('# '):
            pdf.set_font("Helvetica", 'B', 18)
            pdf.set_text_color(0, 51, 102)
            pdf.multi_cell(170, 10, line[2:], align='C')
            pdf.set_text_color(0)
            pdf.ln(5)
        elif line.startswith('## '):
            pdf.set_font("Helvetica", 'B', 14)
            pdf.set_text_color(0, 102, 204)
            pdf.multi_cell(170, 10, line[3:])
            pdf.set_text_color(0)
        elif line.startswith('### '):
            pdf.set_font("Helvetica", 'B', 12)
            pdf.multi_cell(170, 8, line[4:])
        else:
            pdf.set_font("Helvetica", '', 11)
            try:
                line.encode('latin-1')
                clean_line = line
            except UnicodeEncodeError:
                clean_line = line.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(170, 7, clean_line, align='J')

    pdf.output(pdf_file)

def main():
    md_dir = 'meta_analysis_neuroscience_en'
    pdf_dir = 'pdfs_en'
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
    for filename in sorted(os.listdir(md_dir)):
        if filename.endswith('.md'):
            md_path = os.path.join(md_dir, filename)
            pdf_path = os.path.join(pdf_dir, filename.replace('.md', '.pdf'))
            print(f"Converting {md_path}...")
            md_to_pdf(md_path, pdf_path)

if __name__ == "__main__":
    main()
