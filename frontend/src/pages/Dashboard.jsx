import React from "react";
import { UploadPanel } from "../components/UploadPanel";
import { ProfileSummary } from "../components/ProfileSummary";
import { QualityRules } from "../components/QualityRules";
import { DiagnosisCard } from "../components/DiagnosisCard";
import { EvidencePanel } from "../components/EvidencePanel";
import { ImpactGraph } from "../components/ImpactGraph";
import { RemediationPanel } from "../components/RemediationPanel";

export function Dashboard({ data, loading, error, executeDemo, executeUpload }) {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans p-6 md:p-10">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <header className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-10 pb-6 border-b border-slate-800">
          <div>
            <div className="flex items-center gap-3">
              <span className="p-2.5 rounded-xl bg-gradient-to-tr from-indigo-500 to-purple-600 text-white font-extrabold text-xl shadow-lg">
                🛡️
              </span>
              <h1 className="text-3xl font-black tracking-tight text-white">
                PipeGuard <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">AI</span>
              </h1>
            </div>
            <p className="text-sm text-slate-400 mt-1 font-medium">
              From raw data to evidence-backed data-quality intelligence.
            </p>
          </div>
          <div className="flex items-center gap-3">
            <span className="px-3 py-1.5 rounded-full text-xs font-semibold bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
              Model-Powered Tool
            </span>
            <span className="px-3 py-1.5 rounded-full text-xs font-semibold bg-purple-500/10 text-purple-400 border border-purple-500/20">
              Gemma 4
            </span>
          </div>
        </header>

        {/* Upload & Demo Panel */}
        <UploadPanel onUpload={executeUpload} onDemo={executeDemo} loading={loading} />

        {/* Error Alert */}
        {error && (
          <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-400 text-sm mb-8">
            <strong>Error:</strong> {error}
          </div>
        )}

        {/* Loading Skeleton */}
        {loading && (
          <div className="glass-card p-12 text-center rounded-2xl mb-8 animate-pulse">
            <div className="inline-block p-4 rounded-full bg-indigo-500/20 text-indigo-400 text-2xl mb-4">
              ⚙️
            </div>
            <h3 className="text-lg font-bold text-white mb-2">Analyzing Dataset & Pipeline Evidence...</h3>
            <p className="text-xs text-slate-400">
              Extracting facts, validating quality rules, and invoking Gemma 4 reasoning engine.
            </p>
          </div>
        )}

        {/* Results View */}
        {data && !loading && (
          <div>
            <ProfileSummary profile={data.profile} />
            <DiagnosisCard diagnosis={data.diagnosis} />
            <EvidencePanel evidence={data.diagnosis?.evidence} />
            <QualityRules dqResults={data.dq_results} />
            <ImpactGraph impact={data.diagnosis?.impact} />
            <RemediationPanel
              remediation={data.diagnosis?.remediation}
              qualityRules={data.diagnosis?.quality_rules}
            />
          </div>
        )}
      </div>
    </div>
  );
}
