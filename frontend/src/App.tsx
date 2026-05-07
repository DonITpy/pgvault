import { useEffect, useState } from "react";

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

function App() {
  const [findings, setFindings] = useState<Finding[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(import.meta.env.VITE_API_URL + "/scan/flat")
      .then((res) => res.json())
      .then((json) => {
        setFindings(json.findings || []);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <p>Cargando hallazgos...</p>;
  }

  return (
    <div style={{ padding: "1rem" }}>
      <h1>PgVault Dashboard</h1>
      <p>Total de hallazgos: {findings.length}</p>
      <table border={1} cellPadding={4} cellSpacing={0}>
        <thead>
          <tr>
            <th>Módulo</th>
            <th>Regla</th>
            <th>Riesgo</th>
            <th>Confianza</th>
            <th>Tabla</th>
            <th>Columna</th>
            <th>Detalle</th>
          </tr>
        </thead>
        <tbody>
          {findings.map((f, idx) => (
            <tr key={idx}>
              <td>{f.module}</td>
              <td>{f.rule_id}</td>
              <td>{f.risk}</td>
              <td>{f.confidence}</td>
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