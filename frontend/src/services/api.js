const API_BASE_URL = "http://localhost:8000/api";

export async function runDemoAnalysis() {
  const response = await fetch(`${API_BASE_URL}/demo`);
  if (!response.ok) {
    throw new Error(`Demo analysis failed: ${response.statusText}`);
  }
  return response.json();
}

export async function analyzeDatasets(files, logFile = null) {
  const formData = new FormData();
  for (let i = 0; i < files.length; i++) {
    formData.append("files", files[i]);
  }
  if (logFile) {
    formData.append("log_file", logFile);
  }

  const response = await fetch(`${API_BASE_URL}/analyze`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({ detail: "Analysis request failed" }));
    throw new Error(err.detail || "Analysis failed");
  }

  return response.json();
}
