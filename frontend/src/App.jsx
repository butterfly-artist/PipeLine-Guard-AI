import React from "react";
import { useAnalysis } from "./hooks/useAnalysis";
import { Dashboard } from "./pages/Dashboard";

export default function App() {
  const { data, loading, error, executeDemo, executeUpload } = useAnalysis();

  return (
    <Dashboard
      data={data}
      loading={loading}
      error={error}
      executeDemo={executeDemo}
      executeUpload={executeUpload}
    />
  );
}
