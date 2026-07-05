import os
from datetime import datetime
from typing import Dict, Any, List
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generate_txt_report(record_data: Dict[str, Any], detections: List[Dict[str, Any]]) -> str:
    """
    Generates a plain text report of the image analysis.
    """
    timestamp_str = record_data.get('timestamp', datetime.now().isoformat())
    try:
        dt = datetime.fromisoformat(timestamp_str)
        formatted_date = dt.strftime("%B %d, %Y - %I:%M %p")
    except:
        formatted_date = timestamp_str

    report = []
    report.append("=" * 80)
    report.append("                 AI VISUAL ACCESSIBILITY ASSISTANT REPORT")
    report.append("=" * 80)
    report.append(f"Generated On: {formatted_date}")
    report.append(f"File Name:    {record_data.get('filename', 'Unknown')}")
    report.append(f"Resolution:   {record_data.get('resolution', 'Unknown')}")
    report.append(f"File Size:    {record_data.get('file_size_kb', 0.0):.2f} KB")
    report.append("-" * 80)
    report.append("")
    
    report.append("1. AI IMAGE CAPTION")
    report.append(f"   {record_data.get('caption', 'N/A')}")
    report.append(f"   Confidence: {record_data.get('caption_confidence', 0.0) * 100:.1f}%" if record_data.get('caption_confidence') else "   Confidence: N/A")
    report.append("")
    
    report.append("2. SCENE UNDERSTANDING")
    report.append(f"   Category:    {record_data.get('scene_category', 'N/A')}")
    report.append(f"   Description: {record_data.get('scene_explanation', 'N/A')}")
    report.append("")
    
    report.append("3. DETECTED OBJECTS")
    if detections:
        report.append(f"   {'Object Name':<25} {'Confidence':<15}")
        report.append(f"   {'-' * 25} {'-' * 15}")
        for det in detections:
            report.append(f"   {det['name']:<25} {det['confidence'] * 100:.1f}%")
    else:
        report.append("   No objects detected.")
    report.append("")
    
    report.append("4. AI SUMMARY")
    report.append(f"   {record_data.get('summary', 'N/A')}")
    report.append("")
    
    report.append("5. DETAILED ACCESSIBILITY DESCRIPTION")
    report.append(f"   {record_data.get('accessibility_description', 'N/A')}")
    report.append("")
    
    report.append("6. AI INSIGHTS")
    report.append(f"   Main Subject: {record_data.get('main_subject', 'N/A')}")
    report.append(f"   Activity:     {record_data.get('activity', 'N/A')}")
    report.append(f"   Environment:  {record_data.get('environment', 'N/A')}")
    report.append(f"   Context:      {record_data.get('context', 'N/A')}")
    report.append(f"   Use Case:     {record_data.get('use_case', 'N/A')}")
    report.append("")
    report.append("=" * 80)
    
    return "\n".join(report)

def generate_pdf_report(record_data: Dict[str, Any], detections: List[Dict[str, Any]], output_path: str) -> bool:
    """
    Generates a beautifully formatted PDF report using ReportLab.
    """
    try:
        # Ensure output folder exists
        dir_name = os.path.dirname(output_path)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
            
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=54,
            leftMargin=54,
            topMargin=54,
            bottomMargin=54
        )
        
        styles = getSampleStyleSheet()
        
        # Define Custom Styles for Startup look
        # Primary Color: Slate Blue (#2D3748), Secondary: Teal (#319795)
        primary_color = colors.HexColor("#1A365D")
        secondary_color = colors.HexColor("#2B6CB0")
        dark_neutral = colors.HexColor("#2D3748")
        light_neutral = colors.HexColor("#F7FAFC")
        
        title_style = ParagraphStyle(
            name='ReportTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=22,
            textColor=primary_color,
            spaceAfter=15
        )
        
        subtitle_style = ParagraphStyle(
            name='ReportSubtitle',
            parent=styles['Normal'],
            fontName='Helvetica-Oblique',
            fontSize=10,
            textColor=colors.HexColor("#718096"),
            spaceAfter=20
        )
        
        heading_style = ParagraphStyle(
            name='SectionHeading',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=14,
            textColor=secondary_color,
            spaceBefore=12,
            spaceAfter=6,
            keepWithNext=True
        )
        
        body_style = ParagraphStyle(
            name='ReportBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            textColor=dark_neutral,
            leading=14,
            spaceAfter=10
        )
        
        body_bold_style = ParagraphStyle(
            name='ReportBodyBold',
            parent=body_style,
            fontName='Helvetica-Bold'
        )

        story = []
        
        # 1. Header Title
        story.append(Paragraph("AI Visual Accessibility Assistant Report", title_style))
        
        timestamp_str = record_data.get('timestamp', datetime.now().isoformat())
        try:
            dt = datetime.fromisoformat(timestamp_str)
            formatted_date = dt.strftime("%B %d, %Y - %I:%M %p")
        except:
            formatted_date = timestamp_str
            
        story.append(Paragraph(f"Analysis Report Generated on {formatted_date}", subtitle_style))
        story.append(Spacer(1, 10))
        
        # 2. Metadata Table
        metadata_data = [
            [Paragraph("<b>File Name</b>", body_style), Paragraph(record_data.get('filename', 'Unknown'), body_style)],
            [Paragraph("<b>Resolution</b>", body_style), Paragraph(record_data.get('resolution', 'Unknown'), body_style)],
            [Paragraph("<b>File Size</b>", body_style), Paragraph(f"{record_data.get('file_size_kb', 0.0):.2f} KB", body_style)]
        ]
        t = Table(metadata_data, colWidths=[150, 350])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), light_neutral),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
            ('PADDING', (0,0), (-1,-1), 8),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(t)
        story.append(Spacer(1, 20))
        
        # 3. Caption
        story.append(Paragraph("1. Image Captioning", heading_style))
        caption_text = record_data.get('caption', 'N/A')
        confidence = record_data.get('caption_confidence')
        if confidence:
            caption_text += f" (Confidence: {confidence * 100:.1f}%)"
        story.append(Paragraph(caption_text, body_style))
        
        # 4. Scene Understanding
        story.append(Paragraph("2. Scene Understanding", heading_style))
        scene_category = record_data.get('scene_category', 'N/A')
        scene_explanation = record_data.get('scene_explanation', 'N/A')
        scene_text = f"<b>Category:</b> {scene_category}<br/><b>Analysis:</b> {scene_explanation}"
        story.append(Paragraph(scene_text, body_style))
        
        # 5. Detected Objects
        story.append(Paragraph("3. Detected Objects", heading_style))
        if detections:
            objects_table_data = [[Paragraph("<b>Object</b>", body_bold_style), Paragraph("<b>Confidence</b>", body_bold_style)]]
            for det in detections:
                objects_table_data.append([
                    Paragraph(det['name'], body_style),
                    Paragraph(f"{det['confidence'] * 100:.1f}%", body_style)
                ])
            ot = Table(objects_table_data, colWidths=[250, 250])
            ot.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EDF2F7")),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
                ('PADDING', (0,0), (-1,-1), 6),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ]))
            story.append(ot)
        else:
            story.append(Paragraph("No objects detected in the image.", body_style))
            
        story.append(Spacer(1, 15))
        
        # Page break for structured multi-page layout
        story.append(PageBreak())
        
        # 6. AI Summary
        story.append(Paragraph("4. AI Summary", heading_style))
        story.append(Paragraph(record_data.get('summary', 'N/A'), body_style))
        
        # 7. Accessibility Description (The core feature)
        story.append(Paragraph("5. Detailed Accessibility Description", heading_style))
        # Highlight this in a box
        desc_table_data = [[Paragraph(record_data.get('accessibility_description', 'N/A'), body_style)]]
        dt = Table(desc_table_data, colWidths=[500])
        dt.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EBF8FF")), # Soft blue tint
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#90CDF4")),
            ('PADDING', (0,0), (-1,-1), 12),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        story.append(dt)
        story.append(Spacer(1, 15))
        
        # 8. AI Insights
        story.append(Paragraph("6. AI Insights", heading_style))
        insights_data = [
            [Paragraph("<b>Main Subject</b>", body_style), Paragraph(record_data.get('main_subject', 'N/A'), body_style)],
            [Paragraph("<b>Activity</b>", body_style), Paragraph(record_data.get('activity', 'N/A'), body_style)],
            [Paragraph("<b>Environment</b>", body_style), Paragraph(record_data.get('environment', 'N/A'), body_style)],
            [Paragraph("<b>Context</b>", body_style), Paragraph(record_data.get('context', 'N/A'), body_style)],
            [Paragraph("<b>Possible Use Case</b>", body_style), Paragraph(record_data.get('use_case', 'N/A'), body_style)]
        ]
        it = Table(insights_data, colWidths=[150, 350])
        it.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
            ('PADDING', (0,0), (-1,-1), 8),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(it)
        
        doc.build(story)
        return True
    except Exception as e:
        import traceback
        print(f"Error during PDF generation: {e}")
        traceback.print_exc()
        return False
