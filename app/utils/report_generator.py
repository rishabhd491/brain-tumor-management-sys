"""
Report Generator Module
----------------------
This module provides functions to generate PDF reports for patient scans.
"""

import os
import io
import logging
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)

try:
    # Import reportlab for PDF generation
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    reportlab_available = True
except ImportError:
    logger.warning("ReportLab not installed. PDF reports will not be available.")
    reportlab_available = False

def generate_scan_report(patient, scan, tumor_info=None):
    """
    Generate a PDF report for a patient's scan.
    
    Args:
        patient: Dictionary containing patient information
        scan: Dictionary containing scan information
        tumor_info: Dictionary containing tumor information (optional)
        
    Returns:
        PDF data as bytes, or None if generation fails
    """
    if not reportlab_available:
        logger.error("ReportLab library not available. Cannot generate PDF report.")
        return None
    
    try:
        # Create a file-like buffer for the PDF
        buffer = io.BytesIO()
        
        # Create the PDF document
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                               rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=72)
        
        # Create the list of elements to build the PDF
        elements = []
        
        # Get styles
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='CenterTitle', 
                                  parent=styles['Heading1'], 
                                  alignment=1,
                                  spaceAfter=12))
        styles.add(ParagraphStyle(name='SectionHeader', 
                                  parent=styles['Heading2'], 
                                  fontSize=14, 
                                  spaceAfter=6))
        styles.add(ParagraphStyle(name='SubsectionHeader', 
                                  parent=styles['Heading3'], 
                                  fontSize=12, 
                                  spaceAfter=6))
        
        # Add title
        elements.append(Paragraph("Brain Tumor Analysis Report", styles['CenterTitle']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Add report date
        report_date = datetime.now().strftime("%B %d, %Y")
        elements.append(Paragraph(f"Report Date: {report_date}", styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Patient Information section
        elements.append(Paragraph("Patient Information", styles['SectionHeader']))
        patient_data = [
            ["Patient Name:", patient.get('name', 'N/A')],
            ["Patient ID:", str(patient.get('id', 'N/A'))],
            ["Age:", str(patient.get('age', 'N/A'))],
            ["Gender:", patient.get('gender', 'N/A')],
            ["Contact:", patient.get('contact', 'N/A')],
            ["Registration Date:", patient.get('registration_date', 'N/A')]
        ]
        patient_table = Table(patient_data, colWidths=[2*inch, 3*inch])
        patient_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('PADDING', (0, 0), (-1, -1), 6)
        ]))
        elements.append(patient_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Add medical history if available
        if patient.get('medical_history'):
            elements.append(Paragraph("Medical History:", styles['SubsectionHeader']))
            elements.append(Paragraph(patient.get('medical_history', 'None'), styles['Normal']))
            elements.append(Spacer(1, 0.2*inch))
        
        # Scan Information section
        elements.append(Paragraph("Scan Information", styles['SectionHeader']))
        scan_data = [
            ["Scan ID:", str(scan.get('id', 'N/A'))],
            ["Scan Date:", scan.get('scan_date', 'N/A')],
            ["Detected Tumor Type:", scan.get('tumor_type', 'N/A')],
            ["Confidence:", f"{scan.get('confidence', 0):.2%}" if scan.get('confidence') is not None else 'N/A']
        ]
        scan_table = Table(scan_data, colWidths=[2*inch, 3*inch])
        scan_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('PADDING', (0, 0), (-1, -1), 6)
        ]))
        elements.append(scan_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Add scan image if available
        image_path = scan.get('image_path', '')
        if image_path and os.path.exists(image_path):
            try:
                elements.append(Paragraph("MRI Scan Image:", styles['SubsectionHeader']))
                
                # Add the image, scaled to fit the page width
                img = Image(image_path, width=5*inch, height=4*inch)
                elements.append(img)
                elements.append(Spacer(1, 0.2*inch))
            except Exception as e:
                logger.error(f"Error adding image to report: {e}")
        
        # Add doctor's notes if available
        if scan.get('doctor_notes'):
            elements.append(Paragraph("Doctor's Notes:", styles['SubsectionHeader']))
            elements.append(Paragraph(scan.get('doctor_notes', 'None'), styles['Normal']))
            elements.append(Spacer(1, 0.2*inch))
        
        # Add tumor information if available
        if tumor_info:
            elements.append(Paragraph("Tumor Information", styles['SectionHeader']))
            
            # Add tumor description
            elements.append(Paragraph("Description:", styles['SubsectionHeader']))
            elements.append(Paragraph(tumor_info.get('description', 'N/A'), styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
            
            # Add origin information
            elements.append(Paragraph("Origin:", styles['SubsectionHeader']))
            elements.append(Paragraph(tumor_info.get('origin', 'N/A'), styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
            
            # Add common symptoms
            elements.append(Paragraph("Common Symptoms:", styles['SubsectionHeader']))
            symptoms = tumor_info.get('common_symptoms', [])
            if symptoms:
                symptom_text = "<br/>• ".join([''] + symptoms)
                elements.append(Paragraph(f"• {symptom_text}", styles['Normal']))
            else:
                elements.append(Paragraph("No information available", styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
            
            # Add treatment options
            elements.append(Paragraph("Treatment Options:", styles['SubsectionHeader']))
            treatments = tumor_info.get('treatment_options', [])
            if treatments:
                treatment_text = "<br/>• ".join([''] + treatments)
                elements.append(Paragraph(f"• {treatment_text}", styles['Normal']))
            else:
                elements.append(Paragraph("No information available", styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
            
            # Add prognosis information
            if tumor_info.get('prognosis'):
                elements.append(Paragraph("Prognosis:", styles['SubsectionHeader']))
                elements.append(Paragraph(tumor_info.get('prognosis', 'N/A'), styles['Normal']))
                elements.append(Spacer(1, 0.1*inch))
        
        # Add disclaimer
        elements.append(Spacer(1, 0.3*inch))
        disclaimer = """<i>Disclaimer: This report is generated based on machine learning analysis and should be reviewed by a qualified medical professional. The information provided is not a substitute for professional medical advice, diagnosis, or treatment.</i>"""
        elements.append(Paragraph(disclaimer, styles['Normal']))
        
        # Build the PDF
        doc.build(elements)
        
        # Get the PDF data
        pdf_data = buffer.getvalue()
        buffer.close()
        
        return pdf_data
    
    except Exception as e:
        logger.error(f"Error generating PDF report: {e}")
        return None 