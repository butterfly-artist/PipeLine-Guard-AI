import React from "react";

export function EvidencePanel({ evidence }) {
  if (!evidence || evidence.length === 0) return null;

  return (
    <div className="glass-card p-6 rounded-2xl mb-8">
      <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
        <span className="p-1.5 rounded-lg bg-indigo-500/20 text-indigo-400">🔍</span>
        Deterministic Evidence Grounding
      </h3>
      <p className="text-xs text-slate-400 mb-4">
        Every AI diagnostic conclusion is tied directly to measurable observations extracted by Python.
      </p>

      <div className="space-y-3">
        {evidence.map((item, idx) => (
          <div
            key={idx}
            className="flex flex-col md:flex-row md:items-center justify-between p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 gap-2"
          >
            <div className="flex items-center gap-3">
              <span className="px-2 py-0.5 rounded text-xs font-mono font-bold bg-indigo-500/20 text-indigo-400 uppercase">
                {item.source}
              </span>
              <span className="text-xs font-mono font-semibold text-slate-300">
                {item.reference}
              </span>
            </div>
            <p className="text-sm text-slate-200 font-medium">
              {item.observation}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
