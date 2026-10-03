import React from "react";

export function QualityRules({ dqResults }) {
  if (!dqResults || dqResults.length === 0) return null;

  const passedCount = dqResults.filter((r) => r.status === "PASS").length;
  const failedCount = dqResults.filter((r) => r.status === "FAIL").length;

  return (
    <div className="glass-card p-6 rounded-2xl mb-8">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
          <span className="p-1.5 rounded-lg bg-purple-500/20 text-purple-400">🛡️</span>
          Deterministic Data Quality Execution
        </h3>
        <div className="flex gap-2">
          <span className="px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
            {passedCount} Passed
          </span>
          <span className="px-3 py-1 rounded-full text-xs font-semibold bg-rose-500/20 text-rose-400 border border-rose-500/30">
            {failedCount} Failed
          </span>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm text-slate-300">
          <thead className="bg-slate-900/60 text-slate-400 uppercase text-xs">
            <tr>
              <th className="py-3 px-4 rounded-l-lg">Rule ID</th>
              <th className="py-3 px-4">Status</th>
              <th className="py-3 px-4">Checked Rows</th>
              <th className="py-3 px-4">Failed Rows</th>
              <th className="py-3 px-4">Failure Rate</th>
              <th className="py-3 px-4 rounded-r-lg">Details</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
            {dqResults.map((r, idx) => (
              <tr key={idx} className="hover:bg-slate-800/40 transition-colors">
                <td className="py-3 px-4 font-mono text-xs text-indigo-300">{r.rule_id}</td>
                <td className="py-3 px-4">
                  <span
                    className={`inline-block px-2.5 py-0.5 rounded-full text-xs font-bold ${
                      r.status === "PASS"
                        ? "bg-emerald-500/20 text-emerald-400"
                        : "bg-rose-500/20 text-rose-400 animate-pulse"
                    }`}
                  >
                    {r.status}
                  </span>
                </td>
                <td className="py-3 px-4 font-mono">{r.checked_rows.toLocaleString()}</td>
                <td className="py-3 px-4 font-mono font-semibold text-rose-400">
                  {r.failed_rows.toLocaleString()}
                </td>
                <td className="py-3 px-4 font-mono">{r.failure_rate}%</td>
                <td className="py-3 px-4 text-xs text-slate-400 max-w-xs truncate">
                  {r.details || "Clean execution"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
