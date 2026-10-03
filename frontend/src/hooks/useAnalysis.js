import { useState } from "react";
import { runDemoAnalysis, analyzeDatasets } from "../services/api";

export function useAnalysis() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const executeDemo = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await runDemoAnalysis();
      setData(res);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const executeUpload = async (files, logFile) => {
    setLoading(true);
    setError(null);
    try {
      const res = await analyzeDatasets(files, logFile);
      setData(res);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return {
    data,
    loading,
    error,
    executeDemo,
    executeUpload,
  };
}
