from typing import List, Dict
from io import BytesIO
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from datetime import datetime


def build_html_report(db_name: str, score: int, summary: Dict, findings: List[Dict]) -> str:
    rows_html = ""
    for f in findings:
        rows_html += f"""
        <tr>
          <td>{f.get("module", "")}</td>
          <td>{f.get("rule_id", "")}</td>
          <td>{f.get("risk", "")}</td>
          <td>{f.get("confidence", "")}</td>
          <td>{f.get("match_type", "")}</td>
          <td>{f.get("table", "") or "-"}</td>
          <td>{f.get("column", "") or "-"}</td>
          <td>{f.get("details", "")}</td>
        </tr>
        """

    html = f"""
    <html>
    <head>
      <meta charset="utf-8" />
      <title>Reporte PgVault - {db_name}</title>
      <style>
        body {{
          font-family: Arial, sans-serif;
          padding: 16px;
        }}
        h1, h2 {{
          margin-bottom: 8px;
        }}
        table {{
          width: 100%;
          border-collapse: collapse;
          margin-top: 16px;
        }}
        th, td {{
          border: 1px solid #ccc;
          padding: 4px 6px;
          font-size: 12px;
        }}
        th {{
          background-color: #f0f0f0;
        }}
      </style>
    </head>
    <body>
      <h1>Reporte de seguridad PgVault</h1>
      <h2>Base de datos: {db_name}</h2>
      <p>Score de seguridad: <strong>{score}/100</strong></p>
      <p>Total de hallazgos: {summary.get("total_findings", 0)}</p>
      <ul>
        <li>Crítico: {summary.get("critical", 0)}</li>
        <li>Alto: {summary.get("high", 0)}</li>
        <li>Medio: {summary.get("medium", 0)}</li>
        <li>Bajo: {summary.get("low", 0)}</li>
      </ul>

      <h2>Detalle de hallazgos</h2>
      <table>
        <thead>
          <tr>
            <th>Módulo</th>
            <th>Regla</th>
            <th>Riesgo</th>
            <th>Confianza</th>
            <th>Tipo</th>
            <th>Tabla</th>
            <th>Columna</th>
            <th>Detalle</th>
          </tr>
        </thead>
        <tbody>
          {rows_html}
        </tbody>
      </table>
    </body>
    </html>
    """
    return html


def build_pdf_report(db_name: str, score: int, summary: Dict, findings: List[Dict]) -> bytes:
    """Genera un reporte en PDF."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), rightMargin=0.5*inch, leftMargin=0.5*inch)
    story = []
    styles = getSampleStyleSheet()
    
    # Título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f3a93'),
        spaceAfter=12,
    )
    story.append(Paragraph('Reporte de Seguridad PgVault', title_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Información de la BD
    db_style = ParagraphStyle(
        'DBInfo',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#333333'),
        spaceAfter=6,
    )
    story.append(Paragraph(f'<b>Base de datos:</b> {db_name}', db_style))
    story.append(Paragraph(f'<b>Fecha:</b> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', db_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Score
    score_color = '#27ae60' if score >= 70 else '#e67e22' if score >= 50 else '#e74c3c'
    story.append(Paragraph(f'<b>Score de seguridad:</b> <font color="{score_color}"><b>{score}/100</b></font>', db_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Resumen
    story.append(Paragraph('Resumen de Hallazgos', styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    summary_data = [
        ['Total', 'Crítico', 'Alto', 'Medio', 'Bajo'],
        [
            str(summary.get('total_findings', 0)),
            str(summary.get('critical', 0)),
            str(summary.get('high', 0)),
            str(summary.get('medium', 0)),
            str(summary.get('low', 0)),
        ]
    ]
    
    summary_table = Table(summary_data, colWidths=[1.5*inch]*5)
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f3a93')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Detalle de hallazgos
    story.append(Paragraph('Detalle de Hallazgos', styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    # Tabla de hallazgos - simplificada
    table_data = [['Módulo', 'Regla', 'Riesgo', 'Confianza', 'Tipo', 'Tabla', 'Columna', 'Detalle']]
    
    # Crear párrafos para envolver texto largo
    for f in findings:
        table_data.append([
            Paragraph(str(f.get('module', '')), ParagraphStyle('normal', parent=styles['Normal'], fontSize=9)),
            Paragraph(str(f.get('rule_id', '')), ParagraphStyle('normal', parent=styles['Normal'], fontSize=9)),
            Paragraph(str(f.get('risk', '')), ParagraphStyle('normal', parent=styles['Normal'], fontSize=9)),
            Paragraph(str(f.get('confidence', '')), ParagraphStyle('normal', parent=styles['Normal'], fontSize=9)),
            Paragraph(str(f.get('match_type', '')), ParagraphStyle('normal', parent=styles['Normal'], fontSize=9)),
            Paragraph(str(f.get('table', '') or '-'), ParagraphStyle('normal', parent=styles['Normal'], fontSize=9)),
            Paragraph(str(f.get('column', '') or '-'), ParagraphStyle('normal', parent=styles['Normal'], fontSize=9)),
            Paragraph(str(f.get('details', ''))[:80], ParagraphStyle('normal', parent=styles['Normal'], fontSize=9)),
        ])
    
    # Ancho total disponible en landscape A4 es ~9.5 pulgadas
    findings_table = Table(table_data, colWidths=[0.9*inch, 1.2*inch, 0.8*inch, 0.8*inch, 1.0*inch, 0.9*inch, 0.9*inch, 2.0*inch])
    findings_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f3a93')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (2, 0), (4, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(findings_table)
    
    # Generar PDF
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
