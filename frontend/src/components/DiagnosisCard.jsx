import React from "react";

export function DiagnosisCard({ diagnosis }) {
  if (!diagnosis) return null;

  const severityColors = {
    CRITICAL: "bg-rose-500/20 text-rose-400 border-rose-500/40",
    HIGH: "bg-orange-500/20 text-orange-400 border-orange-500/40",
    MEDIUM: "bg-amber-500/20 text-amber-400 border-amber-500/40",
    LOW: "bg-emerald-500/20 text-emerald-400 border-emerald-500/40",
  };

  const badgeClass = severityColors[diagnosis.severity] || severityColors.MEDIUM;

  return (
    <div className="glass-card p-6 rounded-2xl mb-8 border-l-4 border-indigo-500">
      <div className="flex justify-between items-start gap-4 mb-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs font-bold px-2.5 py-0.5 rounded bg-indigo-500/20 text-indigo-400 border border-indigo-500/30 uppercase tracking-wide">
              Gemma 4 Open-Weight AI
            </span>
            <span className={`text-xs font-bold px-2.5 py-0.5 rounded border ${badgeClass}`}>
              {diagnosis.severity} SEVERITY
            </span>
          </div>
          <h3 className="text-xl font-extrabold text-white mt-2">
            AI Diagnosis & Incident Root Cause
          </h3>
        </div>
      </div>

      <div className="bg-slate-900/80 p-4 rounded-xl border border-slate-800 mb-4">
        <p className="text-slate-200 text-sm leading-relaxed font-medium">
          {diagnosis.root_cause}
        </p>
      </div>

      {diagnosis.affected_entities && diagnosis.affected_entities.length > 0 && (
        <div className="flex flex-wrap gap-2 items-center text-xs text-slate-400">
          <span className="font-semibold text-slate-300">Affected Entities:</span>
          {diagnosis.affected_entities.map((e, idx) => (
            <span key={idx} className="px-2 py-1 rounded bg-slate-800 text-indigo-300 font-mono">
              {e}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}
