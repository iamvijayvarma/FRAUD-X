import React from 'react';
import { Shield, Activity, AlertTriangle, Sparkles, Terminal } from 'lucide-react';
import { ConnectionStatus } from '../../services/websocket';

interface HeaderProps {
  wsStatus: ConnectionStatus;
  latencyMs?: number;
  openAlertsCount: number;
  onOpenSimulator: () => void;
  onSelectAlerts: () => void;
  onOpenEvolution?: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  wsStatus,
  latencyMs = 7.4,
  openAlertsCount,
  onOpenSimulator,
  onSelectAlerts,
  onOpenEvolution
}) => {
  return (
    <header className="h-14 border-b border-white/[0.08] bg-[#0d1016] px-5 flex items-center justify-between sticky top-0 z-30 shrink-0 select-none">
      {/* Brand & System Tag */}
      <div className="flex items-center gap-3">
        <div className="h-8 w-8 rounded-md bg-white/[0.04] border border-white/[0.1] flex items-center justify-center text-slate-200">
          <Shield className="w-4 h-4 text-sky-400" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <span className="font-semibold tracking-tight text-sm text-white">
              FRAUD<span className="text-sky-400">-X</span>
            </span>
            <span className="px-1.5 py-0.5 text-[9px] font-mono tracking-wide bg-white/[0.05] text-slate-400 border border-white/[0.08] rounded">
              FC-05
            </span>
          </div>
          <p className="text-[11px] text-slate-400 tracking-normal hidden sm:block">
            Context-Aware Fraud Intelligence
          </p>
        </div>
      </div>

      {/* Telemetry Status Bar & Primary Controls */}
      <div className="flex items-center gap-2.5">
        {/* Stream Status */}
        <div className="flex items-center gap-2 px-2.5 py-1 rounded border border-white/[0.08] bg-white/[0.02] text-xs font-mono">
          <span className={`w-2 h-2 rounded-full ${
            wsStatus === 'LIVE' ? 'bg-emerald-400' :
            wsStatus === 'RECONNECTING' ? 'bg-amber-400' : 'bg-rose-400'
          }`} />
          <span className="text-[11px] text-slate-300 font-medium">
            {wsStatus === 'LIVE' ? 'LIVE' : wsStatus}
          </span>
        </div>

        {/* Pipeline Latency */}
        <div className="hidden md:flex items-center gap-1.5 px-2.5 py-1 rounded border border-white/[0.08] bg-white/[0.02] text-xs font-mono text-slate-400">
          <Activity className="w-3.5 h-3.5 text-slate-500" />
          <span className="text-[11px] text-slate-300 font-semibold">{latencyMs} ms</span>
        </div>

        {/* Priority Alerts Pill */}
        <button
          onClick={onSelectAlerts}
          className="flex items-center gap-1.5 px-2.5 py-1 rounded border border-rose-900/40 bg-rose-950/20 hover:bg-rose-900/30 text-xs font-mono text-rose-300 transition-colors"
        >
          <AlertTriangle className="w-3.5 h-3.5 text-rose-400" />
          <span className="text-[11px] font-medium">ALERTS</span>
          <span className="px-1.5 py-0.2 text-[10px] font-bold bg-rose-900/60 rounded text-rose-200">
            {openAlertsCount}
          </span>
        </button>

        {/* Judge Demo Shortcut */}
        {onOpenEvolution && (
          <button
            id="btn-header-judge-demo"
            onClick={onOpenEvolution}
            className="flex items-center gap-1.5 px-3 py-1 rounded bg-sky-500 hover:bg-sky-400 text-slate-950 text-xs font-semibold tracking-normal transition-colors cursor-pointer"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Judge Demo</span>
          </button>
        )}

        {/* Threat Attack Simulator Trigger Button */}
        <button
          id="btn-header-simulator"
          onClick={onOpenSimulator}
          className="flex items-center gap-1.5 px-3 py-1 rounded border border-white/[0.12] bg-white/[0.04] hover:bg-white/[0.08] text-slate-200 text-xs font-medium transition-colors cursor-pointer"
        >
          <Terminal className="w-3.5 h-3.5 text-slate-400" />
          <span>Simulator</span>
        </button>
      </div>
    </header>
  );
};
