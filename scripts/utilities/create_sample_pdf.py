#!/usr/bin/env python3
"""
Generate a sample financial PDF for NFRA testing.
Includes balance sheet, P&L, compliance notes, and tables.
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from datetime import datetime

def create_sample_pdf(filename="sample_financial_report.pdf"):
    """Create a comprehensive sample financial report PDF"""
    
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Define custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=30,
        alignment=1
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2f5aa8'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # ===== TITLE PAGE =====
    story.append(Paragraph("ANNUAL FINANCIAL REPORT 2025-2026", title_style))
    story.append(Paragraph("TechCorp Financial Solutions Limited", styles['Heading2']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"As of March 31, 2026", styles['Normal']))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
    story.append(Spacer(1, 0.5*inch))
    
    # Company info
    story.append(Paragraph("<b>Company Information:</b>", heading_style))
    company_data = [
        ['Company Name', 'TechCorp Financial Solutions Limited'],
        ['Registration Number', 'CIN: U72900DL2015PLC292345'],
        ['Financial Year', 'April 1, 2025 - March 31, 2026'],
        ['Auditor', 'Deloitte Haskins & Sells LLP'],
        ['Audit Status', 'Completed - Unqualified Opinion'],
    ]
    company_table = Table(company_data, colWidths=[2*inch, 3.5*inch])
    company_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f0f8')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    story.append(company_table)
    story.append(Spacer(1, 0.5*inch))
    
    # ===== PAGE 1: EXECUTIVE SUMMARY =====
    story.append(PageBreak())
    story.append(Paragraph("EXECUTIVE SUMMARY", heading_style))
    story.append(Paragraph(
        "TechCorp Financial Solutions Limited is a leading financial technology company "
        "providing digital payment and compliance solutions across India. This annual report "
        "presents the consolidated financial statements for FY2025-2026 prepared in accordance "
        "with Indian Accounting Standards (IndAS), RBI guidelines, and SEBI regulations.",
        styles['Normal']
    ))
    story.append(Spacer(1, 12))
    
    # Key Metrics
    story.append(Paragraph("<b>Key Financial Metrics (in INR Crores):</b>", heading_style))
    metrics_data = [
        ['Metric', 'FY2025-26', 'FY2024-25', 'Growth %'],
        ['Total Revenue', '₹450.50', '₹380.25', '+18.5%'],
        ['Operating Profit', '₹112.30', '₹87.15', '+28.9%'],
        ['Net Profit', '₹78.45', '₹61.20', '+28.1%'],
        ['Total Assets', '₹1,245.80', '₹1,087.50', '+14.6%'],
        ['Shareholders Equity', '₹650.30', '₹580.50', '+12.0%'],
    ]
    metrics_table = Table(metrics_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 1*inch])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2f5aa8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f4f8')]),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 12))
    
    # ===== PAGE 2: BALANCE SHEET =====
    story.append(PageBreak())
    story.append(Paragraph("BALANCE SHEET AS AT MARCH 31, 2026", heading_style))
    story.append(Paragraph("(Amount in INR Crores)", styles['Normal']))
    story.append(Spacer(1, 12))
    
    balance_sheet_data = [
        ['Particulars', 'March 31, 2026', 'March 31, 2025'],
        ['<b>ASSETS</b>', '', ''],
        ['Non-Current Assets', '', ''],
        ['  Property, Plant & Equipment', '₹185.50', '₹165.30'],
        ['  Intangible Assets', '₹95.20', '₹78.45'],
        ['  Right-of-use Assets', '₹120.40', '₹135.60'],
        ['  Long-term Investments', '₹230.80', '₹195.20'],
        ['  Deferred Tax Assets', '₹45.30', '₹38.90'],
        ['Total Non-Current Assets', '₹677.20', '₹613.45'],
        ['', '', ''],
        ['Current Assets', '', ''],
        ['  Inventories', '₹50.40', '₹45.80'],
        ['  Trade Receivables', '₹185.30', '₹168.50'],
        ['  Cash and Bank Balances', '₹98.60', '₹125.40'],
        ['  Other Current Assets', '₹134.30', '₹134.35'],
        ['Total Current Assets', '₹568.60', '₹474.05'],
        ['', '', ''],
        ['<b>TOTAL ASSETS</b>', '<b>₹1,245.80</b>', '<b>₹1,087.50</b>'],
        ['', '', ''],
        ['<b>LIABILITIES & EQUITY</b>', '', ''],
        ['Non-Current Liabilities', '', ''],
        ['  Borrowings', '₹280.50', '₹245.30'],
        ['  Other Long-term Liabilities', '₹60.40', '₹52.80'],
        ['  Provisions', '₹34.60', '₹28.90'],
        ['Total Non-Current Liabilities', '₹375.50', '₹327.00'],
        ['', '', ''],
        ['Current Liabilities', '', ''],
        ['  Trade Payables', '₹120.80', '₹115.30'],
        ['  Short-term Borrowings', '₹99.40', '₹64.70'],
        ['  Other Current Liabilities', '₹95.30', '₹87.40'],
        ['  Provisions', '₹22.50', '₹18.30'],
        ['Total Current Liabilities', '₹338.00', '₹285.70'],
        ['', '', ''],
        ['Equity', '', ''],
        ['  Share Capital', '₹100.00', '₹100.00'],
        ['  Reserves and Surplus', '₹550.30', '₹480.50'],
        ['<b>TOTAL EQUITY</b>', '<b>₹650.30</b>', '<b>₹580.50</b>'],
        ['', '', ''],
        ['<b>TOTAL LIABILITIES & EQUITY</b>', '<b>₹1,245.80</b>', '<b>₹1,087.50</b>'],
    ]
    
    bs_table = Table(balance_sheet_data, colWidths=[3.5*inch, 1.5*inch, 1.5*inch])
    bs_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2f5aa8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7f7f7')]),
    ]))
    story.append(bs_table)
    story.append(Spacer(1, 12))
    
    # ===== PAGE 3: P&L STATEMENT =====
    story.append(PageBreak())
    story.append(Paragraph("STATEMENT OF PROFIT AND LOSS FOR THE YEAR ENDED MARCH 31, 2026", heading_style))
    story.append(Paragraph("(Amount in INR Crores)", styles['Normal']))
    story.append(Spacer(1, 12))
    
    pl_data = [
        ['Particulars', 'FY 2025-26', 'FY 2024-25'],
        ['Revenue from Operations', '₹420.30', '₹355.80'],
        ['  - Service Revenue', '₹280.50', '₹248.30'],
        ['  - Product Revenue', '₹115.20', '₹92.50'],
        ['  - Other Operating Revenue', '₹24.60', '₹15.00'],
        ['Other Income', '₹30.20', '₹24.45'],
        ['<b>TOTAL INCOME</b>', '<b>₹450.50</b>', '<b>₹380.25</b>'],
        ['', '', ''],
        ['EXPENSES', '', ''],
        ['Cost of Materials Consumed', '₹85.40', '₹76.20'],
        ['Employee Benefits Expense', '₹165.80', '₹145.60'],
        ['Finance Costs', '₹28.50', '₹22.80'],
        ['Depreciation & Amortization', '₹42.30', '₹38.90'],
        ['Other Expenses', '₹16.20', '₹8.80'],
        ['<b>TOTAL EXPENSES</b>', '<b>₹338.20</b>', '<b>₹292.30</b>'],
        ['', '', ''],
        ['<b>PROFIT BEFORE TAX</b>', '<b>₹112.30</b>', '<b>₹87.95</b>'],
        ['Tax Expense', '₹33.85', '₹26.75'],
        ['<b>PROFIT AFTER TAX</b>', '<b>₹78.45</b>', '<b>₹61.20</b>'],
        ['', '', ''],
        ['Earnings Per Share (Basic)', '₹7.85', '₹6.12'],
        ['Earnings Per Share (Diluted)', '₹7.78', '₹6.08'],
    ]
    
    pl_table = Table(pl_data, colWidths=[3.5*inch, 1.5*inch, 1.5*inch])
    pl_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2f5aa8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7f7f7')]),
    ]))
    story.append(pl_table)
    story.append(Spacer(1, 12))
    
    # ===== PAGE 4: COMPLIANCE NOTES =====
    story.append(PageBreak())
    story.append(Paragraph("REGULATORY COMPLIANCE & GOVERNANCE", heading_style))
    
    story.append(Paragraph("<b>1. Accounting Standards Compliance</b>", styles['Heading3']))
    story.append(Paragraph(
        "These financial statements have been prepared in compliance with "
        "Indian Accounting Standards (IndAS) as notified under the Companies Act 2013. "
        "All applicable IndAS standards including IndAS 101 (First-time Adoption), "
        "IndAS 8 (Accounting Policies), and IndAS 10 (Events after Reporting Period) "
        "have been followed.",
        styles['Normal']
    ))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("<b>2. RBI Guidelines Adherence</b>", styles['Heading3']))
    compliance_rbi = [
        ['Guideline', 'Status', 'Details'],
        ['Capital Adequacy Ratio', '✓ Compliant', 'CAR: 15.2% (Required: 10.5%)'],
        ['Provisioning Norms', '✓ Compliant', 'General Provision: 0.4% of Standard Assets'],
        ['KYC Requirements', '✓ Compliant', '100% customer KYC compliance maintained'],
        ['AML/CFT Norms', '✓ Compliant', 'Annual compliance audit passed'],
        ['Data Security', '✓ Compliant', 'ISO 27001 certified, Regular penetration testing'],
    ]
    rbi_table = Table(compliance_rbi, colWidths=[2*inch, 1.2*inch, 2.3*inch])
    rbi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2f5aa8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f4f8')]),
    ]))
    story.append(rbi_table)
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("<b>3. SEBI Compliance</b>", styles['Heading3']))
    story.append(Paragraph(
        "As a listed entity, the company maintains full compliance with "
        "Securities and Exchange Board of India (SEBI) regulations including "
        "LODR (Listing Obligations and Disclosure Requirements), "
        "continuous disclosure of material events, and insider trading prevention.",
        styles['Normal']
    ))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("<b>4. BRSR (Business Responsibility & Sustainability Reporting)</b>", styles['Heading3']))
    brsr_data = [
        ['Principle', 'Actions Taken', 'Status'],
        ['P1: Governance', 'Board Diversity: 40% women, Regular Board evaluation', '✓ On Track'],
        ['P2: Product Responsibility', 'Customer complaint resolution: 98% within 7 days', '✓ Completed'],
        ['P3: Employee Wellbeing', 'Employee retention: 92%, Training hours: 40/emp/year', '✓ Exceeded'],
        ['P4: Community Development', 'CSR spending: 2.1% of profits, 5 villages adopted', '✓ On Track'],
        ['P5: Environmental', 'Carbon offset: 150% of emissions, Waste recycling: 78%', '✓ Exceeded'],
    ]
    brsr_table = Table(brsr_data, colWidths=[1.5*inch, 2.5*inch, 1.2*inch])
    brsr_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2f5aa8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f4f8')]),
    ]))
    story.append(brsr_table)
    story.append(Spacer(1, 12))
    
    # ===== PAGE 5: AUDITOR REPORT =====
    story.append(PageBreak())
    story.append(Paragraph("INDEPENDENT AUDITOR'S REPORT", heading_style))
    
    story.append(Paragraph("<b>To the Members of TechCorp Financial Solutions Limited</b>", styles['Heading3']))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("<b>Report on the Audit of Financial Statements</b>", styles['Heading3']))
    story.append(Paragraph(
        "We have audited the accompanying financial statements of TechCorp Financial Solutions Limited "
        "(the 'Company'), which comprise the Balance Sheet as at March 31, 2026, the Statement of "
        "Profit and Loss, the Statement of Cash Flows, and the Statement of Changes in Equity for "
        "the year ended on that date, and a summary of the significant accounting policies and other "
        "explanatory information.<br/><br/>"
        "<b>Opinion</b><br/>"
        "In our opinion and to the best of our information and according to the explanations given to us, "
        "the aforesaid financial statements give the information required by the Companies Act, 2013 "
        "('the Act') in the manner so required and give a true and fair view in conformity with the "
        "accounting principles generally accepted in India, of the state of affairs of the Company as "
        "at March 31, 2026, of the profit and the cash flows for the year ended on that date.",
        styles['Normal']
    ))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("<b>Auditor Details</b>", styles['Heading3']))
    auditor_data = [
        ['Particulars', 'Details'],
        ['Auditor Name', 'Deloitte Haskins & Sells LLP'],
        ['Registration Number', 'LLP ID AAB-8437'],
        ['Audit Period', 'April 1, 2025 - March 31, 2026'],
        ['Audit Opinion', 'UNQUALIFIED'],
        ['Audit Completion Date', 'April 15, 2026'],
        ['Key Audit Matters', '3 matters identified and addressed'],
    ]
    auditor_table = Table(auditor_data, colWidths=[2.5*inch, 3*inch])
    auditor_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f0f8')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    story.append(auditor_table)
    
    # Build PDF
    doc.build(story)
    return filename

if __name__ == "__main__":
    pdf_file = create_sample_pdf()
    print(f"✓ Sample PDF created: {pdf_file}")
    print(f"  Size: {pdf_file} (~150KB)")
    print(f"  Contents: Balance Sheet, P&L, Compliance Notes, Auditor Report")
