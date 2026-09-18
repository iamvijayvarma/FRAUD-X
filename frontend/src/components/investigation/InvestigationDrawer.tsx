import React, { useState } from 'react';
import { 
  X, 
  ShieldAlert, 
  MapPin, 
  Laptop, 
  Activity, 
  CheckCircle2, 
  ChevronRight,
  TrendingUp,
  RotateCcw,
  Bot,
  AlertTriangle
} from 'lucide-react';
import { Transaction, AINarrativeReport } from '../../types/api';
import { api } from '../../services/api';
import { formatINR } from '../../utils/formatters';

interface InvestigationDrawerProps {
  transaction: Transaction | null;
  onClose: () => void;
  onActionComplete?: (txId: string, action: string) => void;
  onInspectEvolution?: (accountId: string) => void;
}

export const InvestigationDrawer: React.FC<InvestigationDrawerProps> = ({
  transaction,
  onClose,
  onActionComplete,
  onInspectEvolution
}) => {
  const [aiReport, setAiReport] = useState<AINarrativeReport | null>(
    transaction?.ai_narrative && typeof transaction.ai_narrative !== 'string'
      ? transaction.ai_narrative
      : null
  );
  const [isGeneratingAi, setIsGeneratingAi] = useState(false);
  const [actionSuccessMsg, setActionSuccessMsg] = useState<string | null>(null);

  if (!transaction) return null;

  const assessment = transaction.assessment;
  const signals = assessment?.signals || [];

  const handleGenerateAI = async () => {
    try {
      setIsGeneratingAi(true);
      const report = await api.investigateAI(transaction.id);
      setAiReport(report);
    } catch (err) {
      console.error('Failed to generate AI narrative:', err);
    } finally {
      setIsGeneratingAi(false);
    }
  };

  const handleExecuteAction = (action: string) => {
    setActionSuccessMsg(`Operational verdict recorded: ${action}`);
    if (onActionComplete) onActionComplete(transaction.id, action);
    setTimeout(() => setActionSuccessMsg(null), 3000);
  };

  // Group signals into the Six Required Contextual Categories
  const sigCodes = new Set(signals.map(s => s.code));

  // 01. Transaction Behaviour
  const behaviorSignals = signals.filter(s => s.category === 'BEHAVIORAL' || s.category === 'ML');
  // 02. Account History
  const historySignals = signals.filter(s => s.code === 'AMOUNT_ABOVE_BASELINE' || s.code === 'BEHAVIORAL_ANOMALY');
  // 03. Device Characteristics
  const deviceSignals = signals.filter(s => s.category === 'DEVICE');
  // 04. Location Patterns
  const locationSignals = signals.filter(s => s.category === 'LOCATION');
  // 05. Transaction Velocity
  const velocitySignals = signals.filter(s => s.category === 'VELOCITY');
  // 06. Network Relationships
  const networkSignals = signals.filter(s => s.category === 'GRAPH');

  const sixSignals = [
    {
      num: '01',
      title: 'Transaction Behaviour',
      signals: behaviorSignals,
      fallbackText: behaviorSignals.length > 0 ? null : `Amount ₹${transaction.amount.toLocaleString('en-IN')} conforms with calibrated standard spending deviations.`,
      metricBadge: assessment?.ml_score ? `ML Anomaly: ${(assessment.ml_score * 100).toFixed(0)}%` : null
    },
    {
      num: '02',
      title: 'Account History',
      signals: historySignals,
      fallbackText: historySignals.length > 0 ? null : 'Activity reflects established historical baseline and frequency profile.',
      metricBadge: transaction.bank_name ? `Bank: ${transaction.bank_name}` : null
    },
    {
      num: '03',
      title: 'Device Characteristics',
      signals: deviceSignals,
      fallbackText: deviceSignals.length > 0 ? null : 'Originating hardware fingerprint matches authenticated device bond.',
      metricBadge: assessment ? `Linked: ${assessment.device_account_count} Accts` : null
    },
    {
      num: '04',
      title: 'Location Patterns',
      signals: locationSignals,
      fallbackText: locationSignals.length > 0 ? null : `Domestic geographic transit conforms to plausible physical travel limits.`,
      metricBadge: assessment?.speed_kmh ? `Transit: ${assessment.speed_kmh.toFixed(0)} km/h` : null
    },
    {
      num: '05',
      title: 'Transaction Velocity',
      signals: velocitySignals,
      fallbackText: velocitySignals.length > 0 ? null : 'Normal transaction pacing; no sliding-window burst pattern detected.',
      metricBadge: assessment ? `1m: ${assessment.velocity_count_1m} | 5m: ${assessment.velocity_count_5m}` : null
    },
    {
      num: '06',
      title: 'Network Relationships',
      signals: networkSignals,
      fallbackText: networkSignals.length > 0 ? null : 'Zero circular fund routing rings or money mule cluster links observed.',
      metricBadge: assessment?.is_circular_loop ? 'Circular Loop Flagged' : 'No Mule Ring'
    }
  ];

  return (
    <div className="fixed inset-y-0 right-0 w-full sm:w-[560px] lg:w-[620px] bg-[#0f121a] border-l border-white/[0.08] shadow-2xl z-50 flex flex-col overflow-hidden">
      {/* Drawer Header */}
      <div className="p-3.5 border-b border-white/[0.08] bg-[#121622] flex items-center justify-between shrink-0">
        <div className="flex items-center gap-3">
          <div className="p-1.5 rounded bg-white/[0.05] border border-white/[0.08] text-slate-200">
            <ShieldAlert className="w-4 h-4 text-sky-400" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-mono font-bold text-white text-sm">{transaction.id}</span>
              <span className="px-1.5 py-0.2 text-[9px] font-mono font-medium rounded uppercase bg-white/[0.06] text-slate-300 border border-white/[0.08]">
                {transaction.action_taken}
              </span>
            </div>
            <p className="text-[11px] text-slate-400 font-mono">
              Account: <span className="text-slate-200 font-semibold">{transaction.account_id}</span> • {new Date(transaction.timestamp).toLocaleString()}
            </p>
          </div>
        </div>

        <button
          onClick={onClose}
          className="p-1.5 rounded text-slate-400 hover:text-white hover:bg-white/[0.06] transition-colors cursor-pointer"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Drawer Scrollable Content */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 text-xs">
        {/* Action Feedback Banner */}
        {actionSuccessMsg && (
          <div className="p-2.5 bg-emerald-950/60 border border-emerald-800 text-emerald-300 rounded flex items-center gap-2 font-mono text-xs">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
            <span>{actionSuccessMsg}</span>
          </div>
        )}

        {/* Executive Verdict Score Card */}
        <div className="p-3.5 rounded-lg surface-nested flex items-center justify-between">
          <div>
            <span className="text-[10px] font-mono text-slate-500 uppercase tracking-wider block">
              COMPOSITE RISK FUSION INDEX
            </span>
            <div className="flex items-baseline gap-2 mt-1">
              <span className="text-2xl font-bold font-mono tracking-tight text-white">
                {transaction.risk_score}
              </span>
              <span className="text-slate-500 font-mono text-xs">/ 100</span>
              <span className={`ml-2 px-1.5 py-0.5 text-[10px] font-semibold font-mono rounded uppercase ${
                transaction.risk_level === 'CRITICAL' ? 'bg-rose-950 text-rose-300 border border-rose-800' :
                transaction.risk_level === 'HIGH' ? 'bg-orange-950 text-orange-300 border border-orange-800' :
                transaction.risk_level === 'MEDIUM' ? 'bg-amber-950 text-amber-300 border border-amber-800' :
                'bg-emerald-950 text-emerald-300 border border-emerald-800'
              }`}>
                {transaction.risk_level} RISK
              </span>
            </div>
          </div>

          <div className="text-right">
            <span className="text-[10px] font-mono text-slate-500 uppercase tracking-wider block">
              RECOMMENDED ACTION
            </span>
            <span className={`text-sm font-bold font-mono mt-1 block ${
              transaction.action_taken === 'BLOCK' ? 'text-rose-400' :
              transaction.action_taken === 'HOLD' ? 'text-orange-400' :
              transaction.action_taken === 'CHALLENGE' ? 'text-amber-400' :
              'text-emerald-400'
            }`}>
              {transaction.action_taken}
            </span>
          </div>
        </div>

        {/* Transaction Telemetry Snapshot */}
        <div className="grid grid-cols-2 gap-2 surface-nested p-3 rounded-lg text-[11px] font-mono">
          <div>
            <span className="text-slate-500 text-[10px] block uppercase">AMOUNT (INR)</span>
            <span className="text-white font-bold text-xs">{formatINR(transaction.amount, true)}</span>
            <span className="text-slate-400 text-[10px] block mt-0.5">{transaction.transaction_type || 'UPI'} {transaction.bank_name ? `• ${transaction.bank_name}` : ''}</span>
          </div>
          <div>
            <span className="text-slate-500 text-[10px] block uppercase">MERCHANT / RECIPIENT</span>
            <span className="text-slate-200 font-medium truncate block">{transaction.merchant_name}</span>
            <span className="text-slate-400 text-[10px] block mt-0.5">({transaction.merchant_category})</span>
          </div>
          <div>
            <span className="text-slate-500 text-[10px] block uppercase">ORIGIN LOCATION</span>
            <span className="text-slate-300 flex items-center gap-1 mt-0.5">
              <MapPin className="w-3 h-3 text-slate-500" />
              {transaction.location_city}, {transaction.location_country}
            </span>
          </div>
          <div>
            <span className="text-slate-500 text-[10px] block uppercase">HARDWARE FINGERPRINT</span>
            <span className="text-slate-300 flex items-center gap-1 mt-0.5">
              <Laptop className="w-3 h-3 text-slate-500" />
              {transaction.device_id.slice(0, 14)}...
            </span>
          </div>
        </div>

        {/* Shortcut to Contextual Evolution Dossier */}
        {onInspectEvolution && (
          <button
            onClick={() => {
              onClose();
              onInspectEvolution(transaction.account_id);
            }}
            className="w-full flex items-center justify-between p-2.5 rounded-lg border border-white/[0.08] bg-white/[0.02] hover:bg-white/[0.05] transition-colors cursor-pointer text-xs font-mono text-slate-300 group"
          >
            <div className="flex items-center gap-2">
              <TrendingUp className="w-3.5 h-3.5 text-sky-400" />
              <span>Inspect Account Evolution Dossier ({transaction.account_id})</span>
            </div>
            <ChevronRight className="w-3.5 h-3.5 text-slate-500 group-hover:text-slate-300" />
          </button>
        )}

        {/* EVIDENCE GROUPED UNDER THE SIX REQUIRED SIGNALS */}
        <div className="space-y-2.5">
          <div className="flex items-center justify-between pb-1 border-b border-white/[0.06]">
            <span className="text-xs font-semibold text-slate-200 uppercase tracking-tight">
              EVIDENCE UNDER SIX CONTEXTUAL SIGNALS
            </span>
            <span className="text-[10px] font-mono text-slate-500">Forensic Decomposition</span>
          </div>

          <div className="space-y-2">
            {sixSignals.map((item) => {
              const hasSignals = item.signals.length > 0;
              return (
                <div
                  key={item.num}
                  className="surface-nested p-2.5 rounded-md flex flex-col gap-1.5"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-[10px] font-semibold text-sky-400">
                        {item.num}
                      </span>
                      <span className="font-medium text-slate-200 text-xs">
                        {item.title}
                      </span>
                    </div>

                    <div className="flex items-center gap-2">
                      {item.metricBadge && (
                        <span className="text-[9px] font-mono text-slate-400 bg-white/[0.04] px-1.5 py-0.2 rounded border border-white/[0.06]">
                          {item.metricBadge}
                        </span>
                      )}
                      <span className={`w-1.5 h-1.5 rounded-full ${hasSignals ? 'bg-rose-400' : 'bg-emerald-400'}`} />
                    </div>
                  </div>

                  {hasSignals ? (
                    <div className="space-y-1.5 mt-0.5">
                      {item.signals.map((sig, sIdx) => (
                        <div key={sIdx} className="bg-black/30 p-2 rounded border border-white/[0.05] space-y-1">
                          <div className="flex items-center justify-between">
                            <span className="font-mono text-[10px] font-semibold text-rose-300">
                              {sig.name}
                            </span>
                            <span className="font-mono text-[10px] font-bold text-sky-400">
                              +{sig.points} pts
                            </span>
                          </div>
                          <p className="text-[11px] text-slate-300 leading-normal font-sans">
                            {sig.description}
                          </p>
                          <div className="grid grid-cols-2 gap-2 text-[10px] font-mono pt-1 text-slate-400 border-t border-white/[0.04]">
                            <div>Observed: <span className="text-slate-200">{sig.observed_value}</span></div>
                            <div>Baseline: <span className="text-slate-400">{sig.baseline_value}</span></div>
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-[11px] text-slate-400 leading-normal font-sans">
                      {item.fallbackText}
                    </p>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* AI Forensic Intelligence Brief */}
        <div className="surface-nested p-3 rounded-lg space-y-2.5">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Bot className="w-4 h-4 text-sky-400" />
              <span className="text-xs font-semibold text-slate-200 uppercase tracking-tight">
                AI Forensic Analyst Brief
              </span>
            </div>
            {!aiReport && (
              <button
                onClick={handleGenerateAI}
                disabled={isGeneratingAi}
                className="px-2.5 py-1 rounded bg-white/[0.06] hover:bg-white/[0.1] border border-white/[0.1] text-xs font-mono text-slate-200 transition cursor-pointer disabled:opacity-50"
              >
                {isGeneratingAi ? 'Synthesizing...' : 'Generate Narrative'}
              </button>
            )}
          </div>

          {aiReport ? (
            <div className="space-y-2.5 text-[11px] text-slate-300 font-sans leading-relaxed">
              <div className="p-2 rounded bg-white/[0.02] border border-white/[0.05]">
                <span className="text-[10px] font-mono text-slate-500 uppercase block mb-1">Executive Summary</span>
                <p className="font-medium text-slate-200">{aiReport.executive_summary}</p>
              </div>

              <div className="p-2 rounded bg-white/[0.02] border border-white/[0.05]">
                <span className="text-[10px] font-mono text-slate-500 uppercase block mb-1">Forensic Narrative</span>
                <p className="whitespace-pre-line text-slate-300">{aiReport.forensic_narrative}</p>
              </div>

              {aiReport.immediate_mitigations && aiReport.immediate_mitigations.length > 0 && (
                <div className="p-2 rounded bg-white/[0.02] border border-white/[0.05]">
                  <span className="text-[10px] font-mono text-slate-500 uppercase block mb-1">Immediate Mitigations</span>
                  <ul className="list-disc list-inside space-y-0.5 text-slate-300">
                    {aiReport.immediate_mitigations.map((m, i) => (
                      <li key={i}>{m}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ) : (
            <p className="text-[11px] text-slate-500 font-mono">
              Deterministic synthesis available on demand. Click "Generate Narrative" for AI forensic evaluation.
            </p>
          )}
        </div>

        {/* Operational Verdict Enforcement Controls */}
        <div className="pt-2 border-t border-white/[0.08] space-y-2">
          <span className="text-[10px] font-mono uppercase text-slate-500 font-medium block">
            Enforce Operational Action
          </span>
          <div className="grid grid-cols-4 gap-2">
            <button
              onClick={() => handleExecuteAction('ALLOW')}
              className="py-1.5 px-2 rounded border border-emerald-900/40 bg-emerald-950/20 hover:bg-emerald-900/30 text-emerald-300 font-mono text-xs font-medium transition cursor-pointer"
            >
              ALLOW
            </button>
            <button
              onClick={() => handleExecuteAction('MONITOR')}
              className="py-1.5 px-2 rounded border border-sky-900/40 bg-sky-950/20 hover:bg-sky-900/30 text-sky-300 font-mono text-xs font-medium transition cursor-pointer"
            >
              MONITOR
            </button>
            <button
              onClick={() => handleExecuteAction('HOLD')}
              className="py-1.5 px-2 rounded border border-amber-900/40 bg-amber-950/20 hover:bg-amber-900/30 text-amber-300 font-mono text-xs font-medium transition cursor-pointer"
            >
              HOLD
            </button>
            <button
              onClick={() => handleExecuteAction('BLOCK')}
              className="py-1.5 px-2 rounded border border-rose-900/40 bg-rose-950/20 hover:bg-rose-900/30 text-rose-300 font-mono text-xs font-semibold transition cursor-pointer"
            >
              BLOCK
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
