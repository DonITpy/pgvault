import { useEffect, useState } from "react";

type ScanResponse = {
  config: any[];
  pii: any[];
};

function App() {
  const [data, setData] = useState<ScanResponse | null>(null);

  useEffect(() => {
    fetch(import.meta.env.VITE_API_URL + "/scan")
      .then((res) => res.json())
      .then((json) => setData(json))
      .catch((err) => console.error(err));
  }, []);

  if (!data) {
    return <p>Cargando hallazgos...</p>;
  }

  return (
    <div>
      <h1>PgVault Dashboard</h1>
      <p>Hallazgos de configuración: {data.config.length}</p>
      <p>Hallazgos de PII: {data.pii.length}</p>
    </div>
  );
}

export default App; 