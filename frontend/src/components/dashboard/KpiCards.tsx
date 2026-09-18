import React from 'react';
import { ShieldAlert, CheckCircle2, IndianRupee, Activity, AlertOctagon, ArrowRight } from 'lucide-react';
import { OverviewMetrics } from '../../types/api';
import { formatINR } from '../../utils/formatters';

interface KpiCardsProps {
  metrics: OverviewMetrics | null;
  isLoading: boolean;
}

export const KpiCards: React.FC<KpiCardsProps> = ({ metrics, isLoading }) => {
  const cards = [
    {
      title: 'TOTAL PROCESSED',
      value: metrics ? metrics.total_transactions.toLocaleString('en-IN') : '---',
      sub: 'Streaming transaction volume',
      statusColor: 'text-slate-200'
    },
    {
      title: 'ACTIVE ALERTS',
      value: metrics ? metrics.open_alerts_count.toString() : '---',
      sub: 'Requiring operational verdict',
      statusColor: metrics && metrics.open_alerts_count > 0 ? 'text-rose-400' : 'text-slate-200'
    },
    {
      title: 'HIGH / CRITICAL RISK',
      value: metrics ? metrics.high_risk_transactions_count.toString() : '---',
      sub: 'Confluent anomaly vectors',
      statusColor: metrics && metrics.high_risk_transactions_count > 0 ? 'text-amber-400' : 'text-slate-200'
    },
    {
      title: 'PROTECTED CAPITAL',
      value: metrics ? formatINR(metrics.fraud_blocked_amount, true) : '---',
      sub: 'Prevented malicious outflow',
      statusColor: 'text-emerald-400'
    },
    {
      title: 'PROCESSING PIPELINE',
      value: metrics ? `${metrics.latency_ms} ms` : '---',
      sub: 'Context extraction & fusion',
      statusColor: 'text-sky-400'
    }
  ];

  const signals = [
    { num: '01', name: 'Transaction Behaviour', metric: 'Amount Spikes & Z-Score' },
    { num: '02', name: 'Account History', metric: 'Calibrated Spending Means' },
    { num: '03', name: 'Device Characteristics', metric: 'Hardware Fingerprints' },
    { num: '04', name: 'Location Patterns', metric: 'Haversine Transit Velocity' },
    { num: '05', name: 'Transaction Velocity', metric: 'Sliding Temporal Windows' },
    { num: '06', name: 'Network Relationships', metric: 'Cross-Entity Graph Ring' },
  ];

  return (
    <div className="space-y-3.5">
      {/* KPI Cards Grid - Uniform & Compact */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
        {cards.map((card, idx) => (
          <div
            key={idx}
            className="surface-card rounded-lg p-3.5 flex flex-col justify-between"
          >
            <div className="text-[10px] font-mono tracking-wider font-medium text-slate-400 uppercase">
              {card.title}
            </div>

            <div className="my-1.5">
              {isLoading && !metrics ? (
                <div className="h-6 w-20 bg-white/[0.04] animate-pulse rounded"></div>
              ) : (
                <div className={`text-xl font-bold font-mono tracking-tight ${card.statusColor}`}>
                  {card.value}
                </div>
              )}
            </div>

            <div className="text-[11px] text-slate-500 font-mono truncate">
              {card.sub}
            </div>
          </div>
        ))}
      </div>

      {/* Six Contextual Signals Pipeline Bar */}
      <div className="surface-card rounded-lg p-3 border border-white/[0.08]">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-2.5 mb-2.5 border-b border-white/[0.06]">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-sky-400"></span>
            <span className="text-xs font-semibold text-slate-200 tracking-tight">
              SIX CONTEXTUAL FRAUD SIGNALS
            </span>
            <span className="text-[10px] font-mono text-slate-500">
              Core Intelligence Pipeline
            </span>
          </div>
          <div className="flex items-center gap-2 text-[10px] font-mono text-slate-400">
            <span>Transaction</span>
            <ArrowRight className="w-3 h-3 text-slate-600" />
            <span className="text-sky-400 font-medium">Context Retrieval</span>
            <ArrowRight className="w-3 h-3 text-slate-600" />
            <span className="text-amber-400 font-medium">Risk Fusion</span>
            <ArrowRight className="w-3 h-3 text-slate-600" />
            <span>Forensic Verdict</span>
          </div>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2">
          {signals.map((sig) => (
            <div
              key={sig.num}
              className="surface-nested rounded-md p-2 flex flex-col justify-between"
            >
              <div className="flex items-center justify-between text-[10px] font-mono text-slate-500 mb-1">
                <span className="text-sky-400 font-semibold">{sig.num}</span>
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
              </div>
              <div className="text-xs font-medium text-slate-200 leading-tight truncate">
                {sig.name}
              </div>
              <div className="text-[10px] text-slate-500 font-mono truncate mt-0.5">
                {sig.metric}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
