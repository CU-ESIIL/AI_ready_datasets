"""Render the compact AMBER planning draft; no acquisition or inference."""
from pathlib import Path
from html import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
source = ROOT / 'reports/data_management/amber_dense_plan.md'
target = ROOT / 'output/pdf/AMBER_dense_data_management_plan.pdf'
styles = {
    'title': ParagraphStyle('title', fontName='Times-Bold', fontSize=12, leading=13, spaceAfter=3),
    'sub': ParagraphStyle('sub', fontName='Times-Roman', fontSize=11, leading=12, spaceAfter=5),
    'head': ParagraphStyle('head', fontName='Times-Bold', fontSize=11, leading=12, spaceBefore=5, spaceAfter=3, keepWithNext=True),
    'body': ParagraphStyle('body', fontName='Times-Roman', fontSize=11, leading=12, spaceAfter=4),
}
flow = []
for i, block in enumerate(source.read_text().strip().split('\n\n')):
    kind = 'title' if block.startswith('# ') else 'head' if block.startswith('## ') else 'sub' if i == 1 else 'body'
    paragraph = Paragraph(escape(block.removeprefix('## ').removeprefix('# ')), styles[kind])
    flow.append(KeepTogether([paragraph]) if kind == 'body' else paragraph)

def footer(canvas, doc):
    canvas.setFont('Times-Roman', 9)
    canvas.drawRightString(558, 28, str(doc.page))

SimpleDocTemplate(str(target), pagesize=(612, 792), leftMargin=54, rightMargin=54,
                  topMargin=40, bottomMargin=42,
                  title='AMBER Data Management and Sharing Plan', author='AMBER').build(
                      flow, onFirstPage=footer, onLaterPages=footer)
reader = PdfReader(target)
assert not reader.is_encrypted and len(reader.pages) == 2
assert all(page.extract_text().strip() for page in reader.pages)
print('Verified two-page PDF:', target)
