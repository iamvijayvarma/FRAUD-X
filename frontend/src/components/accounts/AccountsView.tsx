import React, { useState, useEffect } from 'react';
import { Users, Search, Laptop, MapPin, ShieldAlert, CheckCircle2, IndianRupee } from 'lucide-react';
import { Account } from '../../types/api';
import { api } from '../../services/api';
import { formatINR } from '../../utils/formatters';

export const AccountsView: React.FC = () => {
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [search, setSearch] = useState<string>('');
  const [selectedAccountId, setSelectedAccountId] = useState<string | null>(null);
  const [accountDetail, setAccountDetail] = useState<any | null>(null);
  const [loadingDetail, setLoadingDetail] = useState<boolean>(false);

  useEffect(() => {
    api.getAccounts(50).then(accs => {
      setAccounts(accs);
      if (accs.length > 0) setSelectedAccountId(accs[0].id);
    }).finally(() => setIsLoading(false));
  }, []);

  useEffect(() => {
    if (!selectedAccountId) return;
    setLoadingDetail(true);
    api.getAccountDetail(selectedAccountId)
      .then(setAccountDetail)
      .catch(console.error)
      .finally(() => setLoadingDetail(false));
  }, [selectedAccountId]);

  const filtered = accounts.filter(a => {
    const q = search.toLowerCase();
    return a.id.toLowerCase().includes(q) || 
           a.holder_name.toLowerCase().includes(q) ||
           a.email.toLowerCase().includes(q) ||
           a.typical_city.toLowerCase().includes(q);
  });

  return (
    <div className="space-y-3.5 font-mono">
      {/* Header */}
      <div className="surface-card p-3.5 rounded-lg flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="p-1.5 rounded bg-white/[0.05] border border-white/[0.08] text-slate-300">
            <Users className="w-4 h-4 text-sky-400" />
          </div>
          <div>
            <h2 className="text-sm font-semibold text-white tracking-tight uppercase">
              Account Entities & Behavioral Baselines
            </h2>
            <p className="text-[11px] text-slate-400 font-sans">
              Profiles with calibrated spending mean (µ), deviation tolerances (σ), and authenticated device bonds.
            </p>
          </div>
        </div>

        <div className="relative">
          <Search className="w-3.5 h-3.5 absolute left-2.5 top-1/2 -translate-y-1/2 text-slate-500" />
          <input
            type="text"
            value={search}
            onChange={e => setSearch(e.target.value)}
            placeholder="Search account name, ID, city..."
            className="pl-8 pr-3 py-1 w-64 bg-[#171a23] border border-white/[0.08] rounded text-xs text-slate-200 placeholder:text-slate-500 focus:outline-none focus:border-sky-500"
          />
        </div>
      </div>

      {/* Split View */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-3.5">
        {/* Accounts Table List */}
        <div className="lg:col-span-7 surface-card rounded-lg overflow-hidden">
          <div className="overflow-x-auto max-h-[600px] overflow-y-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead className="sticky top-0 bg-[#141720] border-b border-white/[0.08] text-slate-400 text-[10px] uppercase font-mono tracking-wider">
                <tr>
                  <th className="py-2.5 px-3">Account ID</th>
                  <th className="py-2.5 px-3">Holder Name</th>
                  <th className="py-2.5 px-3 text-right">Avg Baseline (₹)</th>
                  <th className="py-2.5 px-3">Home Jurisdiction</th>
                  <th className="py-2.5 px-3">Risk Tier</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/[0.04]">
                {isLoading ? (
                  <tr><td colSpan={5} className="py-8 text-center text-slate-500 font-mono text-xs">Loading accounts...</td></tr>
                ) : filtered.map(acc => {
                  const isSelected = selectedAccountId === acc.id;
                  return (
                    <tr
                      key={acc.id}
                      onClick={() => setSelectedAccountId(acc.id)}
                      className={`cursor-pointer transition-colors ${
                        isSelected ? 'bg-sky-500/[0.08] border-l-2 border-l-sky-400' : 'hover:bg-white/[0.03]'
                      }`}
                    >
                      <td className="py-2.5 px-3 font-mono font-semibold text-sky-400 text-[11px]">{acc.id}</td>
                      <td className="py-2.5 px-3 text-slate-200 text-xs">{acc.holder_name}</td>
                      <td className="py-2.5 px-3 text-right font-mono font-semibold text-white text-xs">
                        {formatINR(acc.avg_amount)} <span className="text-[10px] text-slate-500 font-normal">±{formatINR(acc.std_amount)}</span>
                      </td>
                      <td className="py-2.5 px-3 text-slate-400 text-[11px]">{acc.typical_city}, {acc.typical_country}</td>
                      <td className="py-2.5 px-3">
                        <span className={`px-1.5 py-0.5 text-[9px] font-mono font-semibold rounded uppercase border ${
                          acc.risk_rating === 'CRITICAL' ? 'bg-rose-950/80 text-rose-300 border-rose-800/60' :
                          acc.risk_rating === 'HIGH' ? 'bg-amber-950/80 text-amber-300 border-amber-800/60' :
                          'bg-emerald-950/80 text-emerald-300 border-emerald-800/60'
                        }`}>
                          {acc.risk_rating}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* Selected Account Profile Dossier */}
        <div className="lg:col-span-5 space-y-3.5">
          <div className="surface-card p-3.5 rounded-lg text-xs">
            <span className="text-[10px] font-mono tracking-wider text-slate-500 uppercase block mb-3">
              Behavioral Profile Dossier
            </span>

            {accountDetail ? (
              <div className="space-y-3.5">
                <div className="pb-3 border-b border-white/[0.08] flex items-center justify-between">
                  <div>
                    <h3 className="text-sm font-semibold text-white">{accountDetail.account.holder_name}</h3>
                    <p className="text-[11px] text-sky-400 font-mono">{accountDetail.account.id} • {accountDetail.account.email}</p>
                  </div>
                  <span className="px-1.5 py-0.5 text-[10px] surface-nested text-emerald-400 border border-white/[0.08] rounded font-mono">
                    {accountDetail.account.status}
                  </span>
                </div>

                {/* Metrics */}
                <div className="grid grid-cols-2 gap-2">
                  <div className="p-2.5 surface-nested rounded-md">
                    <span className="text-[10px] text-slate-500 block font-mono">EXPECTED SPEND (µ)</span>
                    <span className="text-sm font-bold text-white font-mono">{formatINR(accountDetail.account.avg_amount)}</span>
                  </div>
                  <div className="p-2.5 surface-nested rounded-md">
                    <span className="text-[10px] text-slate-500 block font-mono">STANDARD DEVIATION (σ)</span>
                    <span className="text-sm font-bold text-white font-mono">±{formatINR(accountDetail.account.std_amount)}</span>
                  </div>
                </div>

                {/* Primary Devices */}
                <div>
                  <span className="text-[10px] font-mono text-slate-500 uppercase block mb-1.5">
                    Authenticated Hardware ({accountDetail.devices.length})
                  </span>
                  <div className="space-y-1.5">
                    {accountDetail.devices.map((d: any) => (
                      <div key={d.id} className="p-2 rounded surface-nested text-[11px] flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <Laptop className="w-3 h-3 text-sky-400" />
                          <span className="text-slate-300">{d.browser_os}</span>
                        </div>
                        <span className="text-[10px] text-slate-500 font-mono">{d.id.slice(0, 10)}...</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Recent Transactions */}
                <div>
                  <span className="text-[10px] font-mono text-slate-500 uppercase block mb-1.5">
                    Recent Account Activity
                  </span>
                  <div className="space-y-1.5 max-h-40 overflow-y-auto">
                    {accountDetail.recent_transactions.map((t: any) => (
                      <div key={t.id} className="p-2 rounded surface-nested flex items-center justify-between text-[11px]">
                        <div>
                          <span className="text-white font-semibold font-mono block">{formatINR(t.amount, true)}</span>
                          <span className="text-[10px] text-slate-400">{t.merchant}</span>
                        </div>
                        <div className="text-right">
                          <span className={`text-[10px] font-mono font-bold block ${
                            t.risk_score >= 60 ? 'text-rose-400' : 'text-emerald-400'
                          }`}>
                            Score {t.risk_score.toFixed(0)}
                          </span>
                          <span className="text-[9px] text-slate-500 font-mono">{t.action}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className="py-8 text-center text-slate-500 font-mono text-xs">Select an account to view behavioral profile.</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
