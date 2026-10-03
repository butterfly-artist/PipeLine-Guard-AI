import React, { useState } from "react";

export function UploadPanel({ onUpload, onDemo, loading }) {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [logFile, setLogFile] = useState(null);

  const handleFileChange = (e) => {
    setSelectedFiles(Array.from(e.target.files));
  };

  const handleLogChange = (e) => {
    if (e.target.files.length > 0) {
      setLogFile(e.target.files[0]);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (selectedFiles.length > 0) {
      onUpload(selectedFiles, logFile);
    }
  };

  return (
    <div className="glass-card p-6 rounded-2xl mb-8">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <span className="p-2 rounded-lg bg-indigo-500/20 text-indigo-400">📁</span>
            Data & Pipeline Context Ingestion
          </h2>
          <p className="text-sm text-slate-400 mt-1">
            Upload CSV, JSON, or Parquet datasets along with pipeline logs for instant intelligence.
          </p>
        </div>
        <button
          type="button"
          onClick={onDemo}
          disabled={loading}
          className="btn-demo px-5 py-2.5 rounded-xl text-sm font-semibold text-white shadow-lg transition-all transform active:scale-95"
        >
          {loading ? "Analyzing CartFlow..." : "⚡ Run CartFlow Demo"}
        </button>
      </div>

      <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="border-2 border-dashed border-slate-700 hover:border-indigo-500/50 transition-colors rounded-xl p-4 text-center bg-slate-900/50">
          <label className="cursor-pointer block">
            <span className="text-sm font-medium text-slate-300 block mb-1">
              Select Dataset Files (.csv, .json, .parquet)
            </span>
            <input
              type="file"
              multiple
              accept=".csv,.json,.jsonl,.parquet"
              onChange={handleFileChange}
              className="hidden"
            />
            <span className="text-xs text-indigo-400 font-semibold underline">
              {selectedFiles.length > 0
                ? `${selectedFiles.length} file(s) selected`
                : "Click to browse files"}
            </span>
          </label>
        </div>

        <div className="border-2 border-dashed border-slate-700 hover:border-indigo-500/50 transition-colors rounded-xl p-4 text-center bg-slate-900/50">
          <label className="cursor-pointer block">
            <span className="text-sm font-medium text-slate-300 block mb-1">
              Optional Pipeline Logs (.log)
            </span>
            <input
              type="file"
              accept=".log,.txt"
              onChange={handleLogChange}
              className="hidden"
            />
            <span className="text-xs text-indigo-400 font-semibold underline">
              {logFile ? logFile.name : "Click to select log file"}
            </span>
          </label>
        </div>

        <div className="md:col-span-2 flex justify-end">
          <button
            type="submit"
            disabled={loading || selectedFiles.length === 0}
            className="px-6 py-2.5 rounded-xl text-sm font-semibold text-white bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 disabled:opacity-50 transition-all shadow-md"
          >
            {loading ? "Processing..." : "Analyze Uploaded Data"}
          </button>
        </div>
      </form>
    </div>
  );
}
