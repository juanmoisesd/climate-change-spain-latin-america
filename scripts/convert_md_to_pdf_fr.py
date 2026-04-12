import os
from fpdf import FPDF

class AcademicPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Meta-analyse Scientifique - Juan Moises de la Serna', 0, 0, 'R')
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

    # Aggressive character replacement to ensure compatibility with standard fonts
    replacements = {
        '—': '-',
        'œ': 'oe',
        '’': "'",
        '“': '"',
        '”': '"',
        '«': '"',
        '»': '"',
        '\u2013': '-',
        '\u2014': '-',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    text = text.replace('**', '').replace('$', '')

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
            # Try to encode as latin-1 to catch any other odd characters
            try:
                line_encoded = line.encode('latin-1', 'replace').decode('latin-1')
            except Exception:
                line_encoded = line
            pdf.multi_cell(170, 7, line_encoded, align='J')

    pdf.output(pdf_file)

def main():
    md_dir = 'meta_analysis_neuroscience_fr'
    pdf_dir = 'pdfs_fr'
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
