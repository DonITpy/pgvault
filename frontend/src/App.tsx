import { useEffect, useMemo, useState } from "react";

type Finding = {
  module: string;
  rule_id: string;
  risk: string;
  confidence: number;
  match_type: string;
  table?: string;
  column?: string;
  details: string;
};

type ScanResponse = {
  score: number;
  summary: {
    total_findings: number;
    critical: number;
    high: number;
    medium: number;
    low: number;
  };
  findings: Finding[];
};

function App() {
  const [data, setData] = useState<ScanResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [riskFilter, setRiskFilter] = useState("Todos");
  const [moduleFilter, setModuleFilter] = useState("Todos");

  useEffect(() => {
    fetch(import.meta.env.VITE_API_URL + "/scan/flat")
      .then((res) => res.json())
      .then((json) => {
        setData(json);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  const filteredFindings = useMemo(() => {
    if (!data) return [];

    return data.findings.filter((f) => {
      const riskOk = riskFilter === "Todos" || f.risk === riskFilter;
      const moduleOk = moduleFilter === "Todos" || f.module === moduleFilter;
      return riskOk && moduleOk;
    });
  }, [data, riskFilter, moduleFilter]);

  const handleDownloadReport = async () => {
    try {
      const response = await fetch(import.meta.env.VITE_API_URL + "/report/pdf");
      if (!response.ok) throw new Error("Error descargando el reporte");
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `pgvault-report-${new Date().toISOString().split('T')[0]}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Error al descargar el reporte:", error);
      alert("No se pudo descargar el reporte");
    }
  };

  if (loading) {
    return <p>Cargando hallazgos...</p>;
  }

  if (!data) {
    return <p>No se pudo cargar el dashboard.</p>;
  }

  return (
    <div style={{ padding: "1rem", fontFamily: "Arial, sans-serif" }}>
      <h1>PgVault Dashboard</h1>

      <div style={{ marginBottom: "1rem" }}>
        <h2>Score general: {data.score}/100</h2>
        <p>Total hallazgos: {data.summary.total_findings}</p>
        <p>Crítico: {data.summary.critical}</p>
        <p>Alto: {data.summary.high}</p>
        <p>Medio: {data.summary.medium}</p>
        <p>Bajo: {data.summary.low}</p>
      </div>

      <div style={{ display: "flex", gap: "1rem", marginBottom: "1rem" }}>
        <div>
          <label>Filtrar por riesgo: </label>
          <select value={riskFilter} onChange={(e) => setRiskFilter(e.target.value)}>
            <option>Todos</option>
            <option>Crítico</option>
            <option>Alto</option>
            <option>Medio</option>
            <option>Bajo</option>
          </select>
        </div>

        <div>
          <label>Filtrar por módulo: </label>
          <select value={moduleFilter} onChange={(e) => setModuleFilter(e.target.value)}>
            <option>Todos</option>
            <option>config</option>
            <option>pii</option>
          </select>
        </div>

        <button onClick={handleDownloadReport}>
          Ver reporte
        </button>
      </div>

      <table border={1} cellPadding={6} cellSpacing={0} style={{ width: "100%" }}>
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
          {filteredFindings.map((f, idx) => (
            <tr key={idx}>
              <td>{f.module}</td>
              <td>{f.rule_id}</td>
              <td>{f.risk}</td>
              <td>{f.confidence}</td>
              <td>{f.match_type}</td>
              <td>{f.table || "-"}</td>
              <td>{f.column || "-"}</td>
              <td>{f.details}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;