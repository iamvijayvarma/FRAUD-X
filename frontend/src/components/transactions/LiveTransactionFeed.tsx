import React from 'react';
import { 
  Play, 
  Pause, 
  Search, 
  MapPin, 
  Laptop,
  ArrowUpRight
} from 'lucide-react';
import { Transaction, RiskLevel } from '../../types/api';
import { formatINR } from '../../utils/formatters';

interface LiveTransactionFeedProps {
  transactions: Transaction[];
  isPaused: boolean;
  pausedBufferCount: number;
  onTogglePause: () => void;
  searchQuery: string;
  onSearchChange: (q: string) => void;
  minRiskFilter: number;
  onMinRiskChange: (val: number) => void;
  selectedRiskTier: RiskLevel | 'ALL';
  onSelectRiskTier: (tier: RiskLevel | 'ALL') => void;
  onSelectTransaction: (tx: Transaction) => void;
  selectedTxId?: string;
}

export const LiveTransactionFeed: React.FC<LiveTransactionFeedProps> = ({
  transactions,
  isPaused,
  pausedBufferCount,
  onTogglePause,
  searchQuery,
  onSearchChange,
  minRiskFilter,
  onMinRiskChange,
  selectedRiskTier,
  onSelectRiskTier,
  onSelectTransaction,
  selectedTxId
}) => {
  const getRiskBadge = (level: RiskLevel, score: number) => {
    switch (level) {
      case 'CRITICAL':
        return (
          <span className="px-1.5 py-0.5 text-[9px] font-mono font-semibold bg-rose-950/80 text-rose-300 border border-rose-800/60 rounded">
            CRITICAL {score}
          </span>
        );
      case 'HIGH':
        return (
          <span className="px-1.5 py-0.5 text-[9px] font-mono font-semibold bg-orange-950/80 text-orange-300 border border-orange-800/60 rounded">
            HIGH {score}
          </span>
        );
      case 'MEDIUM':
        return (
          <span className="px-1.5 py-0.5 text-[9px] font-mono font-semibold bg-amber-950/80 text-amber-300 border border-amber-800/60 rounded">
            MED {score}
          </span>
        );
      default:
        return (
          <span className="px-1.5 py-0.5 text-[9px] font-mono font-medium bg-emerald-950/80 text-emerald-300 border border-emerald-800/50 rounded">
            LOW {score}
          </span>
        );
    }
  };

  const getActionBadge = (action: string) => {
    switch (action) {
      case 'BLOCK':
        return <span className="text-rose-400 font-semibold font-mono text-[10px]">BLOCK</span>;
      case 'HOLD':
        return <span className="text-orange-400 font-semibold font-mono text-[10px]">HOLD</span>;
      case 'CHALLENGE':
        return <span className="text-amber-400 font-medium font-mono text-[10px]">CHALLENGE</span>;
      case 'MONITOR':
        return <span className="text-sky-400 font-mono text-[10px]">MONITOR</span>;
      default:
        return <span className="text-emerald-400 font-mono text-[10px]">ALLOW</span>;
    }
  };

  return (
    <div className="surface-card rounded-lg flex flex-col h-full overflow-hidden">
      {/* Feed Control Toolbar */}
      <div className="p-3 border-b border-white/[0.08] bg-[#0e1117] flex flex-wrap items-center justify-between gap-2.5 shrink-0">
        <div className="flex items-center gap-2">
          <button
            onClick={onTogglePause}
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded text-xs font-mono transition-colors cursor-pointer ${
              isPaused
                ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40 hover:bg-amber-500/30'
                : 'bg-white/[0.05] text-slate-300 border border-white/[0.1] hover:bg-white/[0.08]'
            }`}
          >
            {isPaused ? <Play className="w-3 h-3 fill-current" /> : <Pause className="w-3 h-3 fill-current" />}
            <span className="text-[11px]">{isPaused ? 'Resume Stream' : 'Pause'}</span>
            {isPaused && pausedBufferCount > 0 && (
              <span className="px-1 py-0.2 text-[9px] bg-amber-500 text-black font-bold rounded">
                +{pausedBufferCount}
              </span>
            )}
          </button>

          {/* Search Bar */}
          <div className="relative">
            <Search className="w-3.5 h-3.5 absolute left-2.5 top-1/2 -translate-y-1/2 text-slate-500" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => onSearchChange(e.target.value)}
              placeholder="Search account, merchant, city..."
              className="pl-8 pr-2.5 py-1 w-56 bg-[#171a23] border border-white/[0.08] rounded text-xs text-slate-200 placeholder:text-slate-500 focus:outline-none focus:border-sky-500"
            />
          </div>
        </div>

        {/* Filters */}
        <div className="flex items-center gap-3">
          {/* Risk Tier Selectors */}
          <div className="flex items-center bg-[#171a23] border border-white/[0.08] rounded p-0.5 text-xs font-mono">
            {(['ALL', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'] as const).map((tier) => (
              <button
                key={tier}
                onClick={() => onSelectRiskTier(tier)}
                className={`px-2 py-0.5 rounded text-[10px] font-medium transition-colors cursor-pointer ${
                  selectedRiskTier === tier
                    ? 'bg-white/[0.1] text-white'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {tier}
              </button>
            ))}
          </div>

          {/* Min Score Range Slider */}
          <div className="hidden sm:flex items-center gap-2 text-[11px] font-mono text-slate-400">
            <span>Min:</span>
            <input
              type="range"
              min={0}
              max={90}
              step={10}
              value={minRiskFilter}
              onChange={(e) => onMinRiskChange(Number(e.target.value))}
              className="w-16 accent-sky-500 cursor-pointer"
            />
            <span className="w-5 text-slate-300 font-semibold">{minRiskFilter}</span>
          </div>
        </div>
      </div>

      {/* Transaction Table */}
      <div className="overflow-x-auto flex-1">
        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="border-b border-white/[0.08] bg-[#141720] text-slate-400 text-[10px] font-mono tracking-wider uppercase sticky top-0 z-10">
              <th className="py-2 px-3">Time</th>
              <th className="py-2 px-3">Transaction</th>
              <th className="py-2 px-3">Account</th>
              <th className="py-2 px-3 text-right">Amount</th>
              <th className="py-2 px-3">Method</th>
              <th className="py-2 px-3">Merchant / Beneficiary</th>
              <th className="py-2 px-3">Location</th>
              <th className="py-2 px-3">Risk Tier</th>
              <th className="py-2 px-3">Decision</th>
              <th className="py-2 px-3 text-center">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/[0.04]">
            {transactions.length === 0 ? (
              <tr>
                <td colSpan={10} className="py-12 text-center text-slate-500 font-mono text-xs">
                  No live transactions matching current filters.
                </td>
              </tr>
            ) : (
              transactions.map((tx) => {
                const isSelected = selectedTxId === tx.id;
                const formattedTime = new Date(tx.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
                
                return (
                  <tr
                    key={tx.id}
                    onClick={() => onSelectTransaction(tx)}
                    className={`cursor-pointer transition-colors ${
                      isSelected
                        ? 'bg-sky-500/[0.08] border-l-2 border-l-sky-400'
                        : 'hover:bg-white/[0.03]'
                    }`}
                  >
                    {/* Timestamp */}
                    <td className="py-2 px-3 text-slate-400 font-mono text-[11px] whitespace-nowrap">
                      {formattedTime}
                    </td>

                    {/* ID */}
                    <td className="py-2 px-3 font-mono text-slate-200 text-xs">
                      {tx.id}
                    </td>

                    {/* Account */}
                    <td className="py-2 px-3 text-slate-300 font-mono text-xs">
                      {tx.account_id}
                    </td>

                    {/* Amount */}
                    <td className="py-2 px-3 text-right font-mono font-semibold text-white whitespace-nowrap">
                      {formatINR(tx.amount, true)}
                    </td>

                    {/* Payment Method */}
                    <td className="py-2 px-3 font-mono text-[11px] text-slate-300 whitespace-nowrap">
                      <span className="px-1.5 py-0.5 rounded bg-white/[0.04] border border-white/[0.06] text-slate-300">
                        {tx.transaction_type || 'UPI'}
                      </span>
                    </td>

                    {/* Merchant & Category */}
                    <td className="py-2 px-3 max-w-[200px] truncate text-slate-300">
                      <span className="font-medium text-slate-200">{tx.merchant_name}</span>
                      <span className="text-[10px] text-slate-500 ml-1.5">({tx.merchant_category})</span>
                    </td>

                    {/* Location */}
                    <td className="py-2 px-3 text-slate-400 whitespace-nowrap text-[11px]">
                      {tx.location_city}, {tx.location_country}
                    </td>

                    {/* Risk */}
                    <td className="py-2 px-3 whitespace-nowrap">
                      {getRiskBadge(tx.risk_level, tx.risk_score)}
                    </td>

                    {/* Decision */}
                    <td className="py-2 px-3 whitespace-nowrap">
                      {getActionBadge(tx.action_taken)}
                    </td>

                    {/* Action */}
                    <td className="py-2 px-3 text-center whitespace-nowrap">
                      <span className="text-sky-400 hover:text-sky-300 text-[11px] font-medium inline-flex items-center gap-0.5">
                        Inspect <ArrowUpRight className="w-3 h-3" />
                      </span>
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
