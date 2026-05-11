from typing import List, Dict


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
