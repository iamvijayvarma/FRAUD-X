import React from 'react';
import { AlertOctagon, ArrowRight, ShieldAlert } from 'lucide-react';
import { Transaction } from '../../types/api';
import { formatINR } from '../../utils/formatters';

interface ActiveAlertsPanelProps {
  transactions: Transaction[];
  onSelectTransaction: (tx: Transaction) => void;
}

export const ActiveAlertsPanel: React.FC<ActiveAlertsPanelProps> = ({
  transactions,
  onSelectTransaction
}) => {
  // Filter for high and critical alerts
  const highRiskTxs = transactions
    .filter(t => t.risk_level === 'HIGH' || t.risk_level === 'CRITICAL')
    .slice(0, 5);

  return (
    <div className="surface-card p-3.5 rounded-lg space-y-2.5 flex flex-col h-full">
      <div className="flex items-center justify-between pb-2 border-b border-white/[0.06]">
        <div className="flex items-center gap-2">
          <AlertOctagon className="w-4 h-4 text-rose-400" />
          <span className="text-xs font-semibold text-slate-200 uppercase tracking-tight">
            Priority Fraud Alerts
          </span>
        </div>
        <span className="text-[10px] font-mono text-slate-500">TRIAGE QUEUE</span>
      </div>

      {highRiskTxs.length === 0 ? (
        <div className="p-8 text-center text-slate-500 text-xs font-mono">
          No critical alerts pending review in current ingestion window.
        </div>
      ) : (
        <div className="space-y-2 overflow-y-auto pr-0.5">
          {highRiskTxs.map((tx) => {
            const primaryDriver = tx.assessment?.primary_reasons?.[0] || 'Multi-vector contextual anomaly';
            const isCritical = tx.risk_level === 'CRITICAL';
            return (
              <div
                key={tx.id}
                onClick={() => onSelectTransaction(tx)}
                className="surface-nested p-2.5 rounded-md surface-card-hover cursor-pointer flex flex-col gap-1.5"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className={`px-1.5 py-0.2 text-[9px] font-mono font-semibold rounded uppercase ${
                      isCritical
                        ? 'bg-rose-950/80 text-rose-300 border border-rose-800/60'
                        : 'bg-amber-950/80 text-amber-300 border border-amber-800/60'
                    }`}>
                      {tx.risk_level} • {tx.risk_score}
                    </span>
                    <span className="text-xs font-mono font-medium text-slate-300">{tx.account_id}</span>
                  </div>
                  <span className="text-xs font-mono font-bold text-white">
                    {formatINR(tx.amount, true)}
                  </span>
                </div>

                <p className="text-[11px] text-slate-300 leading-snug line-clamp-2">
                  {primaryDriver}
                </p>

                <div className="flex items-center justify-between pt-1 border-t border-white/[0.04] text-[10px] font-mono text-slate-400">
                  <span>{tx.location_city} • {tx.transaction_type || 'UPI'}</span>
                  <div className="flex items-center gap-1 text-sky-400 font-medium hover:text-sky-300">
                    <span>Investigate</span>
                    <ArrowRight className="w-3 h-3" />
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
