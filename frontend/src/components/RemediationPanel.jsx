import React from "react";

export function RemediationPanel({ remediation, qualityRules }) {
  if ((!remediation || remediation.length === 0) && (!qualityRules || qualityRules.length === 0)) {
    return null;
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
      {remediation && remediation.length > 0 && (
        <div className="glass-card p-6 rounded-2xl">
          <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <span className="p-1.5 rounded-lg bg-emerald-500/20 text-emerald-400">🔧</span>
            Actionable Remediation Steps
          </h3>
          <ul className="space-y-3">
            {remediation.map((r, idx) => (
              <li key={idx} className="flex items-start gap-3 p-3 rounded-xl bg-slate-900/60 border border-slate-800 text-sm text-slate-200">
                <span className="text-emerald-400 font-bold mt-0.5">✓</span>
                <div>
                  <span className="text-xs font-bold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 uppercase mr-2">
                    {r.priority}
                  </span>
                  <span>{r.action}</span>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}

      {qualityRules && qualityRules.length > 0 && (
        <div className="glass-card p-6 rounded-2xl">
          <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <span className="p-1.5 rounded-lg bg-indigo-500/20 text-indigo-400">⚡</span>
            Generated Reusable Quality Rules
          </h3>
          <div className="space-y-3">
            {qualityRules.map((rule, idx) => (
              <div key={idx} className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 text-xs font-mono">
                <div className="flex justify-between items-center mb-1">
                  <span className="font-bold text-indigo-300">{rule.name}</span>
                  <span className="px-1.5 py-0.5 rounded bg-indigo-500/20 text-indigo-400">{rule.type}</span>
                </div>
                <div className="text-slate-400">
                  Target Column: <span className="text-slate-200">{rule.column}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
