import os
from fpdf import FPDF

def md_to_pdf(md_file, pdf_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        text = f.read()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)

    # Simple replacement to avoid encoding issues
    text = text.replace('**', '').replace('$', '')

    lines = text.split('\n')
    for line in lines:
        clean_line = line.strip()
        if not clean_line:
            pdf.ln(5)
            continue

        try:
            clean_line.encode('latin-1')
        except UnicodeEncodeError:
            clean_line = clean_line.encode('latin-1', 'replace').decode('latin-1')

        # Using a fixed width to avoid "Not enough horizontal space" error
        pdf.multi_cell(190, 10, clean_line)

    pdf.output(pdf_file)

def main():
    md_dir = 'meta_analysis_neuroscience'
    pdf_dir = 'pdfs'
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
    for filename in os.listdir(md_dir):
        if filename.endswith('.md'):
            md_path = os.path.join(md_dir, filename)
            pdf_path = os.path.join(pdf_dir, filename.replace('.md', '.pdf'))
            print(f"Converting {md_path}...")
            md_to_pdf(md_path, pdf_path)

if __name__ == "__main__":
    main()
