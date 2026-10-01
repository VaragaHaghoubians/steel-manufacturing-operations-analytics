"""Management summary generated from calculated metrics, not preset findings."""
import html
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image

def management_findings(overall, machine, capacity, downtime, defects, shift):
    lowest = machine.sort_values('oee').iloc[0]
    candidate = capacity.iloc[0]
    top_loss = downtime.iloc[0]
    defect_share = defects.head(2)['share'].sum()
    return [
        f"Production attainment is {overall['production_attainment']:.1%}; aggregate quantities count process-stage completions, not shipped products.",
        f"{candidate['operation']} is the simulated capacity-constraint candidate at {candidate['mean_good_units_per_scheduled_hour']:.1f} good units per scheduled hour, with parallel machines pooled.",
        f"{lowest['machine_id']} has the lowest OEE ({lowest['oee']:.1%}). Check time losses, speed and scrap before deciding why.",
        f"{top_loss['downtime_reason']} accounts for {top_loss['share']:.1%} of attributed lost time; the top three categories account for {downtime.head(3)['share'].sum():.1%}.",
        f"The two largest defect categories account for {defect_share:.1%} of recorded scrap. Shift differences cannot prove a team effect because product mix changes and each team stays on one shift."
    ]

ACTIONS = [
    'Check the lowest-output operation: review cycle times, product mix and all parallel machines before suggesting more equipment.',
    'Review the largest downtime categories with maintenance; collect event-level start/end times and distinguish waiting from failures.',
    'Standardize defect reporting and separate inspection discoveries from the operation that caused the defect.',
    'Monitor weekly machine-level OEE and attainment with agreed metric definitions; validate proposed interventions using a baseline.'
]

def write_reports(root, overall, findings):
    root = Path(root)
    reports = root/'reports'
    summary = '# Management summary\n\nSynthetic steel fabrication demonstration; no real plant results or achieved savings.\n\n## Key findings\n\n'
    summary += '\n'.join(f'- {line}' for line in findings)
    summary += '\n\n## Recommended investigations\n\n' + '\n'.join(f'- {line}' for line in ACTIONS)
    summary += '\n\n## Limits\n\nIndependent machine-shift observations do not model transfers, WIP, part genealogy or flow conservation. Constraint ranking is a capacity-screening proxy, not a proven line bottleneck. See docs/methodology.md.\n'
    (reports/'manufacturing_summary.md').write_text(summary,encoding='utf-8')
    styles = getSampleStyleSheet()
    story = [Paragraph('Steel Manufacturing Operations Analytics',styles['Title']),
             Paragraph('Management briefing | synthetic six-month simulation',styles['Heading2']),
             Paragraph('Pressing - Spot Welding - Machining - Inspection - Packaging',styles['Normal']),Spacer(1,12)]
    table = Table([['Production attainment','Scrap rate','Pooled OEE'],
        [f"{overall['production_attainment']:.1%}",f"{overall['scrap_rate']:.1%}",f"{overall['oee']:.1%}"]],colWidths=[2.1*inch]*3)
    table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#0f172a')),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),('BOTTOMPADDING',(0,0),(-1,-1),9),
        ('TOPPADDING',(0,0),(-1,-1),9),('BACKGROUND',(0,1),(-1,1),colors.HexColor('#e0f2fe'))]))
    story.extend([table,Spacer(1,12),Paragraph('Key findings',styles['Heading2'])])
    for line in findings:
        story.extend([Paragraph(html.escape(line),styles['Normal']),Spacer(1,8)])
    story.extend([Paragraph('Recommended investigations',styles['Heading2'])])
    for line in ACTIONS:
        story.extend([Paragraph(html.escape(line),styles['Normal']),Spacer(1,8)])
    story.extend([Paragraph('Interpretation limits',styles['Heading2']),Paragraph(
        'All observations are synthetic. Machine-shift records are independent; there is no part genealogy, WIP or flow-conservation model. Stage counts must not be interpreted as shipped output. No causal or financial impact is claimed.',styles['Normal'])])
    def footer(canvas, doc):
        canvas.setFont('Helvetica',9)
        canvas.drawString(40,25,'Portfolio demonstration | synthetic data')
        canvas.drawRightString(555,25,f'Page {doc.page}')
    SimpleDocTemplate(str(reports/'manufacturing_summary.pdf'),topMargin=36,bottomMargin=45).build(story,onFirstPage=footer,onLaterPages=footer)
