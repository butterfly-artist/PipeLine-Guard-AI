import React from "react";

export function ProfileSummary({ profile }) {
  if (!profile) return null;

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
      <div className="glass-card p-4 rounded-xl">
        <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block">Dataset</span>
        <span className="text-lg font-bold text-white truncate block mt-1">{profile.dataset_name}</span>
      </div>

      <div className="glass-card p-4 rounded-xl">
        <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block">Row Count</span>
        <span className="text-2xl font-extrabold text-indigo-400 mt-1 block">
          {profile.row_count.toLocaleString()}
        </span>
      </div>

      <div className="glass-card p-4 rounded-xl">
        <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block">Column Count</span>
        <span className="text-2xl font-extrabold text-purple-400 mt-1 block">
          {profile.column_count}
        </span>
      </div>

      <div className="glass-card p-4 rounded-xl">
        <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block">Duplicates</span>
        <span className="text-2xl font-extrabold text-amber-400 mt-1 block">
          {profile.duplicate_rows}
        </span>
      </div>
    </div>
  );
}
