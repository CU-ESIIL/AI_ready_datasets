"""Build the NSF planning draft; no acquisition or model inference."""
from pathlib import Path
from html import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
source = ROOT / 'reports/data_management/nsf_plan.md'
target = ROOT / 'output/pdf/NSF_data_management_and_sharing_plan.pdf'
styles = {
 'title': ParagraphStyle('title', fontName='Times-Bold', fontSize=15, leading=17, spaceAfter=5),
 'sub': ParagraphStyle('sub', fontName='Times-Roman', fontSize=10, leading=12, spaceAfter=5),
 'head': ParagraphStyle('head', fontName='Times-Bold', fontSize=11, leading=13, spaceBefore=7, spaceAfter=4, keepWithNext=True),
 'body': ParagraphStyle('body', fontName='Times-Roman', fontSize=10.5, leading=12, spaceAfter=5),
}
blocks = source.read_text().strip().split('\n\n')
flow = []
for i, block in enumerate(blocks):
 kind = 'title' if block.startswith('# ') else 'head' if block.startswith('## ') else 'sub' if i < 3 else 'body'
 text = block.removeprefix('## ').removeprefix('# ')
 flow.append(Paragraph(escape(text), styles[kind]))
flow.append(Spacer(1, 3))
flow.append(Paragraph('Organization follows NSF\'s five general categories. Current submission uses the Research.gov DMSP tool under NSF 26-202. Check solicitation-specific requirements and finalize bracketed commitments before submission. Guidance: https://www.nsf.gov/funding/data-management-plan and https://www.nsf.gov/policies/document/pappg24-1-supplement-2', styles['sub']))
def footer(canvas, doc):
 canvas.setStrokeColor(colors.HexColor('#cccccc'))
 canvas.line(54, 39, 558, 39)
 canvas.setFont('Times-Roman', 9)
 canvas.drawString(54, 27, 'AI-ready environmental datasets | DMSP planning draft')
 canvas.drawRightString(558, 27, str(doc.page))
doc = SimpleDocTemplate(str(target), pagesize=(612,792), leftMargin=54, rightMargin=54, topMargin=43, bottomMargin=49, title='Data Management and Sharing Plan', author='AI-ready datasets project')
doc.build(flow, onFirstPage=footer, onLaterPages=footer)
reader = PdfReader(target)
assert not reader.is_encrypted
assert len(reader.pages) == 2, len(reader.pages)
assert all(page.extract_text().strip() for page in reader.pages)
print(f'Verified readable PDF: {len(reader.pages)} pages; {target.stat().st_size} bytes')
