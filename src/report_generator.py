


import markdown
from datetime import datetime
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import re

def generate_markdown_report(query, papers, total_cost, synthesis="", fact_check=""):
    """Generate Markdown formatted report"""
    
    report = f"# Research Report\n\n"
    report += f"**Query:** {query}\n\n"
    report += f"**Date:** {datetime.now().strftime('%Y-%m-%d')}\n\n"
    report += "---\n\n"
    
    if synthesis:
        report += "## Synthesis of Findings\n\n"
        report += synthesis + "\n\n"
        report += "---\n\n"
        
    if fact_check:
        report += "## Fact-Checking Analysis\n\n"
        report += fact_check + "\n\n"
        report += "---\n\n"
        
    report += "## Individual Paper Summaries\n\n"
    
    for i, paper in enumerate(papers, 1):
        report += f"### {i}. [{paper.get('source', 'UNKNOWN').upper()}] {paper['title']}\n\n"
        report += f"**Authors:** {', '.join(paper['authors'][:3])}"
        if len(paper['authors']) > 3:
            report += " et al."
        report += "\n\n"
        
        if 'citations' in paper:
            report += f"**Citations:** {paper['citations']}\n\n"
        
        if 'ai_summary' in paper:
            report += f"{paper['ai_summary']}\n\n"
        
        if 'pdf_url' in paper and paper['pdf_url']:
            report += f"**Link:** [{paper['pdf_url']}]({paper['pdf_url']})\n\n"
        
        report += "---\n\n"
    
    report += f"\n**Total API Cost:** ${total_cost:.4f}\n"
    
    return report

def generate_pdf_report(query, papers, total_cost, synthesis="", fact_check="", output_path=None):
    """Generate PDF report"""
    
    if output_path is None:
        from config import OUTPUT_DIR
        output_path = OUTPUT_DIR / f"research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    # Create PDF
    doc = SimpleDocTemplate(str(output_path), pagesize=letter,
                           topMargin=0.75*inch, bottomMargin=0.75*inch)
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor='#2C3E50',
        spaceAfter=12,
        alignment=TA_CENTER
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor='#34495E',
        spaceAfter=10
    )
    body_style = styles['BodyText']
    
    # Build content
    story = []
    
    # Title
    story.append(Paragraph("Research Report", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Query and date
    story.append(Paragraph(f"<b>Query:</b> {query}", body_style))
    story.append(Paragraph(f"<b>Date:</b> {datetime.now().strftime('%Y-%m-%d')}", body_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Synthesis
    if synthesis:
        story.append(Paragraph("Synthesis of Findings", heading_style))
        # Clean synthesis text for PDF
        synthesis_cleaned = synthesis.replace('#', '').replace('*', '')
        for line in synthesis_cleaned.split('\n'):
            if line.strip():
                story.append(Paragraph(line.strip(), body_style))
        story.append(PageBreak())
    
    if fact_check:
        story.append(Paragraph("Fact-Checking Analysis", heading_style))
        fact_check_cleaned = fact_check.replace('#', '').replace('*', '')
        for line in fact_check_cleaned.split('\n'):
            if line.strip():
                story.append(Paragraph(line.strip(), body_style))
        story.append(PageBreak())
        
        
    # Papers
    story.append(Paragraph("Individual Paper Summaries", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    for i, paper in enumerate(papers, 1):
        # Paper title
        title_text = f"{i}. [{paper.get('source', 'UNKNOWN').upper()}] {paper['title']}"
        story.append(Paragraph(title_text, heading_style))
        
        # Authors
        authors = ', '.join(paper['authors'][:3])
        if len(paper['authors']) > 3:
            authors += " et al."
        story.append(Paragraph(f"<b>Authors:</b> {authors}", body_style))
        
        # Citations
        if 'citations' in paper:
            story.append(Paragraph(f"<b>Citations:</b> {paper['citations']}", body_style))
        
        story.append(Spacer(1, 0.1*inch))
        
        # Summary
        if 'ai_summary' in paper:
            summary = paper['ai_summary'].replace('\n', '<br/>')
            story.append(Paragraph(summary, body_style))
        
        story.append(Spacer(1, 0.3*inch))
    
    # Cost
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(f"<b>Total API Cost:</b> ${total_cost:.4f}", body_style))
    
    # Build PDF
    doc.build(story)
    
    return output_path