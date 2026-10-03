import React from "react";

export function ImpactGraph({ impact }) {
  if (!impact || impact.length === 0) return null;

  return (
    <div className="glass-card p-6 rounded-2xl mb-8">
      <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
        <span className="p-1.5 rounded-lg bg-orange-500/20 text-orange-400">🌊</span>
        Downstream Pipeline & Asset Impact Analysis
      </h3>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {impact.map((item, idx) => (
          <div key={idx} className="p-4 rounded-xl bg-slate-900/60 border border-slate-800">
            <div className="flex justify-between items-center mb-2">
              <span className="font-mono text-sm font-bold text-indigo-300">{item.asset}</span>
              <span className="px-2 py-0.5 rounded text-xs font-bold bg-orange-500/20 text-orange-400 uppercase">
                {item.severity}
              </span>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              {item.reason}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
