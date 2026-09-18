import React, { useState, useEffect } from 'react';
import { 
  Sparkles, 
  TrendingUp, 
  Layers, 
  Network, 
  History, 
  FileText, 
  AlertTriangle, 
  ShieldAlert, 
  CheckCircle2, 
  Cpu, 
  Zap, 
  Smartphone, 
  Search, 
  RefreshCw,
  ShieldCheck,
  Info
} from 'lucide-react';
import { 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  Tooltip, 
  ResponsiveContainer, 
  ReferenceLine 
} from 'recharts';
import { api } from '../../services/api';
import { 
  InvestigationSummary, 
  InvestigationDossier 
} from '../../types/investigation';
import { formatCurrency } from '../../utils/formatters';

interface InvestigationIntelligenceViewProps {
  initialAccountId?: string;
  onOpenTransaction?: (txId: string) => void;
}

export const InvestigationIntelligenceView: React.FC<InvestigationIntelligenceViewProps> = ({
  initialAccountId,
  onOpenTransaction
}) => {
  const [investigations, setInvestigations] = useState<InvestigationSummary[]>([]);
  const [selectedAccountId, setSelectedAccountId] = useState<string>(initialAccountId || 'ACC-IN-1043');
  const [dossier, setDossier] = useState<InvestigationDossier | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [demoRunning, setDemoRunning] = useState<boolean>(false);
  const [resetRunning, setResetRunning] = useState<boolean>(false);
  const [actionNotification, setActionNotification] = useState<string | null>(null);
  const [activeStoryStage, setActiveStoryStage] = useState<number>(0);
  const [searchQuery, setSearchQuery] = useState<string>('');

  // Fetch list of investigations
  const loadInvestigations = async () => {
    try {
      const data = await api.getInvestigations(50);
      setInvestigations(data);
      if (!selectedAccountId && data.length > 0) {
        setSelectedAccountId(data[0].account_id);
      }
    } catch (err) {
      console.error('Failed to load investigations list:', err);
    }
  };

  // Fetch dossier for selected account
  const loadDossier = async (accountId: string) => {
    setLoading(true);
    try {
      const data = await api.getInvestigationDossier(accountId);
      setDossier(data);
    } catch (err) {
      console.error(`Failed to load dossier for ${accountId}:`, err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadInvestigations();
  }, []);

  useEffect(() => {
    if (selectedAccountId) {
      loadDossier(selectedAccountId);
    }
  }, [selectedAccountId]);

  // Execute Judge Demo Scenario
  const handleRunJudgeDemo = async () => {
    setDemoRunning(true);
    try {
      const demoResult = await api.triggerJudgeDemo();
      setDossier(demoResult);
      setSelectedAccountId(demoResult.summary.account_id);
      await loadInvestigations();
      setActionNotification('Judge Demo scenario executed: 4 progressive transactions + cross-account syndicate link active.');
      setTimeout(() => setActionNotification(null), 5000);
    } catch (err) {
      console.error('Failed to run Judge Demo scenario:', err);
    } finally {
      setDemoRunning(false);
    }
  };

  // Reset Judge Demo Scenario
  const handleResetJudgeDemo = async () => {
    setResetRunning(true);
    try {
      const resetResult = await api.resetJudgeDemo();
      setDossier(resetResult);
      setSelectedAccountId(resetResult.summary.account_id);
      await loadInvestigations();
      setActionNotification('Demo scenario reset to baseline: 1 legitimate transaction on ACC-IN-1043 (Coimbatore, ₹2,500, LOW).');
      setTimeout(() => setActionNotification(null), 5000);
    } catch (err) {
      console.error('Failed to reset Judge Demo scenario:', err);
    } finally {
      setResetRunning(false);
    }
  };

  const handleSimulateAction = (actionName: string, protocolName: string) => {
    setActionNotification(`Simulated Action Recorded: ${actionName} recommendation logged under protocol [${protocolName}].`);
    setTimeout(() => setActionNotification(null), 5000);
  };

  const getPriorityBadgeClass = (level: string) => {
    switch (level) {
      case 'URGENT':
        return 'bg-rose-950/80 text-rose-300 border border-rose-800/80';
      case 'INVESTIGATE':
        return 'bg-amber-950/80 text-amber-300 border border-amber-800/70';
      case 'WATCH':
        return 'bg-sky-950/80 text-sky-300 border border-sky-800/60';
      default:
        return 'bg-white/[0.04] text-slate-400 border border-white/[0.08]';
    }
  };

  const getRiskLevelBadge = (level: string) => {
    switch (level) {
      case 'CRITICAL':
        return 'bg-rose-950 text-rose-300 border border-rose-800';
      case 'HIGH':
        return 'bg-orange-950 text-orange-300 border border-orange-800';
      case 'MEDIUM':
        return 'bg-amber-950 text-amber-300 border border-amber-800';
      default:
        return 'bg-emerald-950 text-emerald-300 border border-emerald-800';
    }
  };

  const filteredInvestigations = investigations.filter(inv => 
    inv.account_id.toLowerCase().includes(searchQuery.toLowerCase()) ||
    inv.holder_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    inv.primary_bank.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const storyStages = dossier ? [
    { title: '1. Chronological Timeline', content: dossier.fraud_story.timeline, icon: History },
    { title: '2. Behaviour Regime Shift', content: dossier.fraud_story.behaviour_change, icon: TrendingUp },
    { title: '3. Signal Confluence', content: dossier.fraud_story.signal_confluence, icon: Sparkles },
    { title: '4. Syndicate Propagation', content: dossier.fraud_story.network_relationship, icon: Network },
    { title: '5. Risk Escalation Curve', content: dossier.fraud_story.risk_escalation, icon: AlertTriangle },
    { title: '6. Current Diagnostic', content: dossier.fraud_story.current_assessment, icon: ShieldAlert },
    { title: '7. Recommended Action', content: dossier.fraud_story.recommended_action, icon: CheckCircle2 }
  ] : [];

  const isDemoAccount = selectedAccountId === 'ACC-IN-1043';

  return (
    <div className="flex-1 flex flex-col h-full bg-[#0b0d11] text-slate-100 overflow-hidden">
      {/* INNOVATION DEMO HEADER BAR */}
      <div className="bg-[#12151c] border-b border-white/[0.08] px-5 py-3 flex flex-col md:flex-row items-start md:items-center justify-between gap-3 shrink-0">
        <div className="flex items-center gap-3">
          <div className="p-1.5 rounded bg-white/[0.05] border border-white/[0.08] text-sky-400">
            <Cpu className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-sm font-semibold tracking-tight text-white uppercase font-mono">
                Contextual Fraud Evolution Engine
              </h1>
              <span className="px-1.5 py-0.5 text-[9px] font-mono tracking-wide rounded bg-white/[0.06] text-slate-300 border border-white/[0.08]">
                TEMPORAL TRAJECTORY
              </span>
            </div>
            <p className="text-[11px] text-slate-400 font-sans">
              Multi-temporal risk velocity, orthogonal signal confluence, and causal narrative synthesis.
            </p>
          </div>
        </div>

        {/* Action Controls: Run Demo + Reset Demo */}
        <div className="flex items-center gap-2">
          <button
            id="btn-run-judge-demo"
            onClick={handleRunJudgeDemo}
            disabled={demoRunning || resetRunning}
            className="flex items-center gap-2 px-3.5 py-1.5 rounded font-mono font-medium text-xs tracking-tight bg-sky-500 hover:bg-sky-400 text-slate-950 transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {demoRunning ? (
              <>
                <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                <span>Simulating...</span>
              </>
            ) : (
              <>
                <Zap className="w-3.5 h-3.5" />
                <span>Run Judge Demo</span>
              </>
            )}
          </button>

          <button
            id="btn-reset-judge-demo"
            onClick={handleResetJudgeDemo}
            disabled={demoRunning || resetRunning}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded font-mono text-xs border border-white/[0.1] bg-white/[0.04] hover:bg-white/[0.08] text-slate-300 hover:text-white transition-colors cursor-pointer disabled:opacity-50"
            title="Reset Scenario to Clean Baseline State"
          >
            {resetRunning ? (
              <RefreshCw className="w-3.5 h-3.5 animate-spin" />
            ) : (
              <History className="w-3.5 h-3.5 text-slate-400" />
            )}
            <span>Reset</span>
          </button>

          <button
            onClick={() => loadDossier(selectedAccountId)}
            className="p-1.5 rounded border border-white/[0.1] bg-white/[0.04] hover:bg-white/[0.08] text-slate-300 hover:text-white transition-colors cursor-pointer"
            title="Refresh Account Dossier"
          >
            <RefreshCw className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* WORKBENCH BODY */}
      <div className="flex-1 flex overflow-hidden">
        {/* LEFT COLUMN: Triage Queue */}
        <div className="w-72 border-r border-white/[0.08] bg-[#0e1117] flex flex-col shrink-0">
          <div className="p-3 border-b border-white/[0.08] bg-[#12151c]">
            <div className="flex items-center justify-between mb-2">
              <span className="text-[10px] font-mono uppercase text-slate-400 font-medium tracking-wider">
                Investigative Triage
              </span>
              <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-white/[0.05] text-slate-400 border border-white/[0.08]">
                {investigations.length} Cases
              </span>
            </div>
            <div className="relative">
              <Search className="w-3.5 h-3.5 absolute left-2.5 top-2.5 text-slate-500" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search account or name..."
                className="w-full bg-[#171a23] border border-white/[0.08] rounded pl-8 pr-2.5 py-1 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-sky-500 font-mono"
              />
            </div>
          </div>

          {/* List of Accounts */}
          <div className="flex-1 overflow-y-auto divide-y divide-white/[0.04]">
            {filteredInvestigations.map((inv) => {
              const isSelected = selectedAccountId === inv.account_id;
              return (
                <div
                  key={inv.account_id}
                  onClick={() => setSelectedAccountId(inv.account_id)}
                  className={`p-3 cursor-pointer transition-colors ${
                    isSelected
                      ? 'bg-sky-500/[0.08] border-l-2 border-l-sky-400'
                      : 'hover:bg-white/[0.03]'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-mono text-xs font-semibold text-slate-200">
                      {inv.account_id}
                    </span>
                    <span className={`px-1.5 py-0.2 text-[9px] font-mono font-medium rounded uppercase ${getPriorityBadgeClass(inv.investigation_priority)}`}>
                      {inv.investigation_priority}
                    </span>
                  </div>

                  <div className="text-xs text-slate-300 truncate">
                    {inv.holder_name}
                  </div>

                  <div className="flex items-center justify-between text-[11px] text-slate-500 font-mono mt-1">
                    <span>{inv.primary_bank}</span>
                    <div className="flex items-center gap-2">
                      <span>{inv.total_transactions_analyzed} txs</span>
                      <span className={`font-semibold ${
                        inv.current_risk_score >= 80 ? 'text-rose-400' :
                        inv.current_risk_score >= 50 ? 'text-amber-400' : 'text-emerald-400'
                      }`}>
                        {inv.current_risk_score}
                      </span>
                    </div>
                  </div>

                  {inv.is_escalating && (
                    <div className="mt-1 flex items-center gap-1 text-[10px] text-rose-400 font-mono">
                      <TrendingUp className="w-3 h-3" />
                      <span>ESCALATING VELOCITY</span>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* RIGHT COLUMN: Innovation Dossier & Evolution Story */}
        <div className="flex-1 overflow-y-auto p-5 space-y-4">
          {/* Notification Toast */}
          {actionNotification && (
            <div className="p-2.5 bg-sky-950/60 border border-sky-800 text-sky-200 rounded flex items-center gap-2 font-mono text-xs">
              <Info className="w-3.5 h-3.5 text-sky-400 shrink-0" />
              <span>{actionNotification}</span>
            </div>
          )}

          {/* System Architecture Bar */}
          <div className="surface-card rounded-lg p-3.5">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-2 mb-2.5 border-b border-white/[0.06]">
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-sky-400"></span>
                <span className="text-xs font-semibold uppercase font-mono tracking-tight text-white">
                  Contextual Fraud Evolution Architecture
                </span>
              </div>
              <span className="text-[10px] font-mono text-slate-500">
                Temporal Risk Multiplier Engine
              </span>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2 text-center font-mono text-[11px]">
              <div className="surface-nested p-2 rounded">
                <div className="text-slate-200 font-medium">1. Temporal Trajectory</div>
                <div className="text-[9px] text-slate-500 mt-0.5">ΔRisk / Δt Velocity</div>
              </div>
              <div className="surface-nested p-2 rounded">
                <div className="text-slate-200 font-medium">2. Signal Confluence</div>
                <div className="text-[9px] text-slate-500 mt-0.5">Compounding Multiplier</div>
              </div>
              <div className="surface-nested p-2 rounded">
                <div className="text-slate-200 font-medium">3. Syndicate Link</div>
                <div className="text-[9px] text-slate-500 mt-0.5">Network Entanglement</div>
              </div>
              <div className="surface-nested p-2 rounded">
                <div className="text-slate-200 font-medium">4. Change Detection</div>
                <div className="text-[9px] text-slate-500 mt-0.5">Statistical Shift</div>
              </div>
              <div className="surface-nested p-2 rounded">
                <div className="text-slate-200 font-medium">5. Causal Narrative</div>
                <div className="text-[9px] text-slate-500 mt-0.5">7-Stage Story</div>
              </div>
              <div className="surface-nested p-2 rounded border border-sky-500/30 text-sky-300 font-semibold">
                = Fraud Intelligence
              </div>
            </div>
          </div>

          {loading ? (
            <div className="h-64 flex flex-col items-center justify-center space-y-2 font-mono text-xs text-slate-400">
              <RefreshCw className="w-6 h-6 text-sky-400 animate-spin" />
              <span>Synthesizing Contextual Dossier...</span>
            </div>
          ) : !dossier ? (
            <div className="h-64 flex items-center justify-center text-slate-500 font-mono text-xs">
              Select an account from the triage queue to inspect evolutionary intelligence.
            </div>
          ) : (
            <>
              {/* DOSSIER HEADER SUMMARY & ADAPTIVE PRIORITY */}
              <div className="surface-card rounded-lg p-4">
                <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-3 pb-3 border-b border-white/[0.06]">
                  <div>
                    <div className="flex items-center gap-2.5">
                      <span className="text-lg font-bold font-mono text-white">
                        {dossier.summary.account_id}
                      </span>
                      <span className="text-xs text-slate-300 font-medium">
                        — {dossier.summary.holder_name}
                      </span>
                      <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-white/[0.05] text-slate-400 border border-white/[0.08]">
                        {dossier.summary.primary_bank}
                      </span>
                    </div>
                    <div className="text-[11px] text-slate-400 font-mono mt-1 flex items-center gap-2.5 flex-wrap">
                      <span>Baseline City: <strong className="text-slate-200">{dossier.change_point.historical_typical_city}</strong></span>
                      <span>•</span>
                      <span>Historical Baseline: <strong className="text-slate-200">{formatCurrency(dossier.change_point.historical_avg_amount)}</strong></span>
                      <span>•</span>
                      <span>Active Regime: <strong className="text-rose-400">{formatCurrency(dossier.change_point.recent_avg_amount)}</strong> ({dossier.change_point.deviation_magnitude}x)</span>
                    </div>
                  </div>

                  {/* Adaptive Priority Indicators */}
                  <div className="flex items-center gap-4">
                    <div className="text-right">
                      <div className="text-[10px] font-mono uppercase text-slate-500">Triage Level</div>
                      <div className={`px-2.5 py-0.5 mt-0.5 text-xs font-mono font-semibold rounded ${getPriorityBadgeClass(dossier.summary.investigation_priority)}`}>
                        {dossier.summary.investigation_priority}
                      </div>
                    </div>

                    <div className="text-right pl-3 border-l border-white/[0.08]">
                      <div className="text-[10px] font-mono uppercase text-slate-500">Priority Score</div>
                      <div className="text-xl font-bold font-mono text-slate-200">
                        {dossier.summary.priority_score}
                        <span className="text-xs text-slate-500 font-normal"> / 100</span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* 4 CORE INNOVATION METRICS */}
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 mt-3 text-xs font-mono">
                  <div className="surface-nested p-2.5 rounded">
                    <div className="text-[10px] uppercase text-slate-500">Risk Growth Rate</div>
                    <div className="text-sm font-bold text-rose-400 mt-0.5">
                      +{dossier.evolution.risk_growth_rate} pts/step
                    </div>
                    <div className="text-[10px] text-slate-400 mt-0.5">
                      {dossier.evolution.escalation_points_count} escalation events
                    </div>
                  </div>

                  <div className="surface-nested p-2.5 rounded">
                    <div className="text-[10px] uppercase text-slate-500">Signal Confluence</div>
                    <div className="text-sm font-bold text-amber-400 mt-0.5">
                      {dossier.confluence.compounding_multiplier}x Multiplier
                    </div>
                    <div className="text-[10px] text-slate-400 mt-0.5">
                      +{dossier.confluence.combined_risk_boost} pts boost
                    </div>
                  </div>

                  <div className="surface-nested p-2.5 rounded">
                    <div className="text-[10px] uppercase text-slate-500">Regime Shift</div>
                    <div className="text-sm font-bold text-orange-400 mt-0.5">
                      {dossier.change_point.deviation_magnitude}x Shift
                    </div>
                    <div className="text-[10px] text-slate-400 mt-0.5">
                      {dossier.change_point.affected_dimensions.length} affected vectors
                    </div>
                  </div>

                  <div className="surface-nested p-2.5 rounded">
                    <div className="text-[10px] uppercase text-slate-500">Syndicate Exposure</div>
                    <div className="text-sm font-bold text-sky-400 mt-0.5">
                      {dossier.network_propagation.network_exposure_score} / 100
                    </div>
                    <div className="text-[10px] text-slate-400 mt-0.5">
                      {dossier.network_propagation.correlated_accounts_count} linked accounts
                    </div>
                  </div>
                </div>
              </div>

              {/* 5-STEP JUDGE DEMO TIMELINE */}
              {isDemoAccount && (
                <div className="surface-card rounded-lg p-4">
                  <div className="flex items-center justify-between mb-3 pb-2 border-b border-white/[0.06]">
                    <div>
                      <h2 className="text-xs font-semibold uppercase font-mono tracking-wider text-slate-200">
                        30-Second Judge Demo: 5-Step Escalation Sequence
                      </h2>
                      <p className="text-[11px] text-slate-400">
                        Progressive multi-transaction escalation on ACC-IN-1043 concluding in cross-account syndicate linkage.
                      </p>
                    </div>
                    <span className="text-[9px] font-mono px-2 py-0.5 rounded bg-white/[0.06] text-slate-400 border border-white/[0.08]">
                      DEMO FLOW
                    </span>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-2 font-mono">
                    <div className="surface-nested p-2.5 rounded">
                      <div className="text-[10px] text-slate-500 uppercase font-medium">Step 1 • Baseline</div>
                      <div className="text-xs font-bold text-white mt-0.5">₹2,500</div>
                      <div className="text-[11px] text-slate-300">Coimbatore (UPI)</div>
                      <div className="text-[10px] text-slate-500 mt-0.5">Known Device</div>
                      <div className="mt-1.5 text-[9px] font-semibold px-1.5 py-0.2 rounded bg-emerald-950 text-emerald-300 border border-emerald-800 inline-block">
                        LOW (18)
                      </div>
                    </div>

                    <div className="surface-nested p-2.5 rounded">
                      <div className="text-[10px] text-amber-500 uppercase font-medium">Step 2 • Device Shift</div>
                      <div className="text-xs font-bold text-white mt-0.5">₹35,000</div>
                      <div className="text-[11px] text-slate-300">Coimbatore (UPI)</div>
                      <div className="text-[10px] text-amber-400 mt-0.5">New Device Introduced</div>
                      <div className="mt-1.5 text-[9px] font-semibold px-1.5 py-0.2 rounded bg-amber-950 text-amber-300 border border-amber-800 inline-block">
                        ESCALATION (85)
                      </div>
                    </div>

                    <div className="surface-nested p-2.5 rounded">
                      <div className="text-[10px] text-orange-500 uppercase font-medium">Step 3 • Geo Anomaly</div>
                      <div className="text-xs font-bold text-white mt-0.5">₹85,000</div>
                      <div className="text-[11px] text-slate-300">Mumbai (Net Banking)</div>
                      <div className="text-[10px] text-orange-400 mt-0.5">Impossible Velocity</div>
                      <div className="mt-1.5 text-[9px] font-semibold px-1.5 py-0.2 rounded bg-orange-950 text-orange-300 border border-orange-800 inline-block">
                        HIGH (80)
                      </div>
                    </div>

                    <div className="surface-nested p-2.5 rounded">
                      <div className="text-[10px] text-rose-500 uppercase font-medium">Step 4 • Rapid Drain</div>
                      <div className="text-xs font-bold text-white mt-0.5">₹1,20,000</div>
                      <div className="text-[11px] text-slate-300">New Delhi (IMPS)</div>
                      <div className="text-[10px] text-rose-400 mt-0.5">Volume Spike</div>
                      <div className="mt-1.5 text-[9px] font-semibold px-1.5 py-0.2 rounded bg-rose-950 text-rose-300 border border-rose-800 inline-block">
                        CRITICAL (100)
                      </div>
                    </div>

                    <div className="surface-nested p-2.5 rounded">
                      <div className="text-[10px] text-sky-400 uppercase font-medium">Step 5 • Syndicate Link</div>
                      <div className="text-[11px] font-bold text-slate-200 mt-0.5">↔ ACC-IN-1002</div>
                      <div className="text-[11px] text-slate-300 mt-0.5">Shared Hardware</div>
                      <div className="text-[10px] text-slate-400 mt-0.5">Mule Ring Detected</div>
                      <div className="mt-1.5 text-[9px] font-semibold px-1.5 py-0.2 rounded bg-white/[0.08] text-slate-200 border border-white/[0.1] inline-block">
                        COORDINATED
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* TEMPORAL RISK EVOLUTION TRAJECTORY */}
              <div className="surface-card rounded-lg p-4">
                <div className="flex items-center justify-between mb-3 pb-2 border-b border-white/[0.06]">
                  <div>
                    <h2 className="text-xs font-semibold uppercase font-mono tracking-wider text-slate-200">
                      Temporal Risk Evolution Trajectory
                    </h2>
                    <p className="text-[11px] text-slate-400">
                      Tracking continuous multi-transaction risk escalation rate across recent account history.
                    </p>
                  </div>

                  <div className="flex items-center gap-2 font-mono text-xs">
                    <span className="text-slate-500 text-[10px]">Trajectory:</span>
                    <span className="px-1.5 py-0.5 rounded bg-white/[0.05] text-slate-300 border border-white/[0.08] text-[10px]">
                      {dossier.evolution.trajectory_levels.join(' → ')}
                    </span>
                  </div>
                </div>

                {/* Step-by-Step Chronological Cards */}
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-2.5 mb-4">
                  {dossier.evolution.timeline_points.map((pt, idx) => (
                    <div 
                      key={pt.transaction_id || idx}
                      className="surface-nested p-2.5 rounded flex flex-col justify-between"
                    >
                      <div className="flex items-center justify-between text-[10px] font-mono mb-1">
                        <span className="text-slate-500">Step {idx + 1}</span>
                        <span className={`px-1 py-0.2 text-[9px] font-medium rounded ${getRiskLevelBadge(pt.risk_level)}`}>
                          {pt.risk_level} ({pt.risk_score})
                        </span>
                      </div>

                      <div className="text-sm font-bold font-mono text-white mb-0.5">
                        {formatCurrency(pt.amount)}
                      </div>

                      <div className="text-[11px] text-slate-300 truncate">
                        {pt.city}
                      </div>

                      <div className="text-[10px] text-slate-500 font-mono truncate mt-0.5">
                        Device: {pt.device_id.slice(0, 14)}...
                      </div>

                      {pt.signals.length > 0 && (
                        <div className="mt-2 flex flex-wrap gap-1">
                          {pt.signals.map(s => (
                            <span key={s} className="px-1 py-0.2 text-[9px] font-mono rounded bg-white/[0.04] text-slate-400 border border-white/[0.06]">
                              {s}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>

                {/* Trajectory Trend Area Chart */}
                {dossier.evolution.timeline_points.length > 1 && (
                  <div className="h-36 w-full pt-2">
                    <ResponsiveContainer width="100%" height="100%">
                      <AreaChart data={dossier.evolution.timeline_points.map((p, i) => ({
                        step: `Step ${i + 1} (${p.city})`,
                        score: p.risk_score,
                        amount: p.amount
                      }))}>
                        <defs>
                          <linearGradient id="riskGrad" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#0284c7" stopOpacity={0.25}/>
                            <stop offset="95%" stopColor="#0284c7" stopOpacity={0.0}/>
                          </linearGradient>
                        </defs>
                        <XAxis dataKey="step" stroke="#64748b" fontSize={10} axisLine={false} tickLine={false} />
                        <YAxis stroke="#64748b" fontSize={10} domain={[0, 100]} axisLine={false} tickLine={false} />
                        <Tooltip 
                          contentStyle={{ backgroundColor: '#171a23', borderColor: 'rgba(255,255,255,0.1)', borderRadius: '6px', fontSize: '11px', fontFamily: 'monospace' }}
                        />
                        <ReferenceLine y={85} stroke="#ef4444" strokeDasharray="3 3" />
                        <ReferenceLine y={60} stroke="#f59e0b" strokeDasharray="3 3" />
                        <Area type="monotone" dataKey="score" stroke="#0284c7" strokeWidth={1.5} fillOpacity={1} fill="url(#riskGrad)" />
                      </AreaChart>
                    </ResponsiveContainer>
                  </div>
                )}
              </div>

              {/* CONFLUENCE & CHANGE-POINT DUAL CARDS */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-3.5">
                {/* Signal Confluence Engine */}
                <div className="surface-card rounded-lg p-4 flex flex-col justify-between">
                  <div>
                    <div className="flex items-center justify-between mb-2.5 pb-2 border-b border-white/[0.06]">
                      <div>
                        <h2 className="text-xs font-semibold uppercase font-mono tracking-wider text-slate-200">
                          Signal Confluence
                        </h2>
                        <div className="text-[11px] text-slate-400">Orthogonal compounding & non-linear synergy</div>
                      </div>

                      <span className="px-2 py-0.5 text-xs font-mono font-medium rounded bg-white/[0.05] text-slate-300 border border-white/[0.08]">
                        {dossier.confluence.compounding_multiplier}x Multiplier
                      </span>
                    </div>

                    <div className="surface-nested p-2.5 rounded my-2">
                      <div className="text-xs font-mono font-semibold text-slate-200 mb-0.5">
                        {dossier.confluence.confluence_name}
                      </div>
                      <p className="text-xs text-slate-300 leading-relaxed font-sans">
                        {dossier.confluence.description}
                      </p>
                    </div>

                    <div className="text-[10px] font-mono text-slate-500 uppercase mb-1.5">
                      Contributing Signals ({dossier.confluence.contributing_signals.length}):
                    </div>
                    <div className="flex flex-wrap gap-1">
                      {dossier.confluence.contributing_signals.map(s => (
                        <span key={s} className="px-1.5 py-0.5 text-[10px] font-mono rounded bg-white/[0.04] text-slate-300 border border-white/[0.06]">
                          {s}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div className="mt-3 pt-2 border-t border-white/[0.06] flex items-center justify-between text-xs font-mono">
                    <span className="text-slate-500 text-[11px]">Synergy Fit:</span>
                    <span className="font-medium text-slate-300">{(dossier.confluence.confidence_score * 100).toFixed(0)}% Mathematical Fit</span>
                  </div>
                </div>

                {/* Behavioural Change-Point Detection */}
                <div className="surface-card rounded-lg p-4 flex flex-col justify-between">
                  <div>
                    <div className="flex items-center justify-between mb-2.5 pb-2 border-b border-white/[0.06]">
                      <div>
                        <h2 className="text-xs font-semibold uppercase font-mono tracking-wider text-slate-200">
                          Behaviour Change-Point
                        </h2>
                        <div className="text-[11px] text-slate-400">Statistical baseline vs active regime divergence</div>
                      </div>

                      <span className={`px-2 py-0.5 text-xs font-mono font-medium rounded ${
                        dossier.change_point.regime_shift_detected 
                          ? 'bg-amber-950 text-amber-300 border border-amber-800' 
                          : 'bg-emerald-950 text-emerald-300 border border-emerald-800'
                      }`}>
                        {dossier.change_point.regime_shift_detected ? 'REGIME SHIFT' : 'NORMAL VARIANCE'}
                      </span>
                    </div>

                    <div className="grid grid-cols-2 gap-2 my-2 font-mono">
                      <div className="surface-nested p-2 rounded">
                        <div className="text-[10px] text-slate-500 uppercase">Calibrated Mean (µ)</div>
                        <div className="text-xs font-bold text-slate-200 mt-0.5">
                          {formatCurrency(dossier.change_point.historical_avg_amount)}
                        </div>
                        <div className="text-[10px] text-slate-500 mt-0.5">
                          {dossier.change_point.historical_typical_city}
                        </div>
                      </div>

                      <div className="surface-nested p-2 rounded">
                        <div className="text-[10px] text-slate-500 uppercase">Active Regime Mean</div>
                        <div className="text-xs font-bold text-rose-400 mt-0.5">
                          {formatCurrency(dossier.change_point.recent_avg_amount)}
                        </div>
                        <div className="text-[10px] text-amber-400 mt-0.5">
                          {dossier.change_point.deviation_magnitude}x Outlier Shift
                        </div>
                      </div>
                    </div>

                    <p className="text-xs text-slate-300 leading-relaxed surface-nested p-2.5 rounded font-sans">
                      {dossier.change_point.narrative}
                    </p>
                  </div>

                  <div className="mt-3 pt-2 border-t border-white/[0.06] flex items-center gap-2 text-[11px] font-mono">
                    <span className="text-slate-500">Affected Vectors:</span>
                    <span className="text-slate-300">[{dossier.change_point.affected_dimensions.join(', ')}]</span>
                  </div>
                </div>
              </div>

              {/* CROSS-ACCOUNT NETWORK PROPAGATION & PATTERNS */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-3.5">
                {/* Cross-Account Context Propagation */}
                <div className="surface-card rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2.5 pb-2 border-b border-white/[0.06]">
                    <div>
                      <h2 className="text-xs font-semibold uppercase font-mono tracking-wider text-slate-200">
                        Cross-Account Syndicate Links
                      </h2>
                      <div className="text-[11px] text-slate-400">Shared hardware & mule ring entity grading</div>
                    </div>

                    <span className="px-2 py-0.5 text-xs font-mono font-medium rounded bg-white/[0.05] text-slate-300 border border-white/[0.08]">
                      {dossier.network_propagation.cluster_classification}
                    </span>
                  </div>

                  <div className="space-y-2 mt-2.5">
                    {dossier.network_propagation.network_links.length === 0 ? (
                      <div className="p-4 rounded surface-nested text-xs text-slate-500 font-mono text-center">
                        No cross-account hardware entanglement detected for this entity.
                      </div>
                    ) : (
                      dossier.network_propagation.network_links.map((link, idx) => (
                        <div key={idx} className="surface-nested p-2.5 rounded font-mono text-xs">
                          <div className="flex items-center justify-between mb-1">
                            <span className="font-bold text-slate-200 flex items-center gap-1.5">
                              <Smartphone className="w-3.5 h-3.5 text-slate-500" />
                              {link.connected_account_id}
                            </span>
                            <span className="px-1.5 py-0.2 text-[9px] rounded bg-rose-950 text-rose-300 border border-rose-800">
                              {link.link_grade}
                            </span>
                          </div>
                          <div className="text-[10px] text-slate-400 mb-1">
                            Shared Entity: <span className="text-slate-200">{link.shared_entity}</span>
                          </div>
                          <p className="text-slate-300 text-[11px] leading-relaxed font-sans">
                            {link.explanation}
                          </p>
                        </div>
                      ))
                    )}
                  </div>
                </div>

                {/* Fraud Pattern Formation */}
                <div className="surface-card rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2.5 pb-2 border-b border-white/[0.06]">
                    <div>
                      <h2 className="text-xs font-semibold uppercase font-mono tracking-wider text-slate-200">
                        Fraud Pattern Hypotheses
                      </h2>
                      <div className="text-[11px] text-slate-400">Synthesized human-readable attack narratives</div>
                    </div>
                  </div>

                  <div className="space-y-2 mt-2.5">
                    {dossier.patterns.map((pat) => (
                      <div key={pat.pattern_id} className="surface-nested p-2.5 rounded">
                        <div className="flex items-center justify-between mb-1">
                          <span className="font-mono text-xs font-semibold text-slate-200">
                            {pat.pattern_name}
                          </span>
                          <span className="text-xs font-mono font-medium text-emerald-400">
                            {(pat.confidence_score * 100).toFixed(0)}% Fit
                          </span>
                        </div>

                        <div className="text-[10px] font-mono text-slate-400 mb-1">
                          {pat.pattern_type}
                        </div>

                        <p className="text-xs text-slate-300 mb-2 leading-relaxed font-sans">
                          {pat.investigative_hypothesis}
                        </p>

                        <div className="space-y-1">
                          {pat.primary_evidence.map((ev, eIdx) => (
                            <div key={eIdx} className="flex items-start gap-1.5 text-[11px] text-slate-400 font-mono">
                              <CheckCircle2 className="w-3 h-3 text-emerald-400 shrink-0 mt-0.5" />
                              <span>{ev}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* EXPLAINABLE FRAUD STORY (7-STAGE CAUSAL FRAMEWORK) */}
              <div className="surface-card rounded-lg p-4">
                <div className="flex items-center justify-between mb-3 pb-2 border-b border-white/[0.06]">
                  <div>
                    <h2 className="text-xs font-semibold uppercase font-mono tracking-wider text-slate-200">
                      Explainable Fraud Narrative (7-Stage Causal Framework)
                    </h2>
                    <p className="text-[11px] text-slate-400">
                      Step-by-step causal progression of fraud synthesized for financial analysts and compliance.
                    </p>
                  </div>
                </div>

                {/* 7-Stage Tabs */}
                <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-1.5 mb-3">
                  {storyStages.map((stage, sIdx) => {
                    const Icon = stage.icon;
                    const isActive = activeStoryStage === sIdx;
                    return (
                      <button
                        key={sIdx}
                        onClick={() => setActiveStoryStage(sIdx)}
                        className={`p-2 rounded text-left transition-colors cursor-pointer border ${
                          isActive 
                            ? 'bg-white/[0.08] border-white/[0.12] text-white'
                            : 'surface-nested text-slate-400 hover:text-slate-200'
                        }`}
                      >
                        <div className="flex items-center gap-1.5 mb-0.5">
                          <Icon className="w-3 h-3 text-sky-400" />
                          <span className="text-[9px] font-mono font-medium">Stage {sIdx + 1}</span>
                        </div>
                        <div className="text-[10px] font-medium truncate">
                          {stage.title.split('. ')[1]}
                        </div>
                      </button>
                    );
                  })}
                </div>

                {/* Active Stage Detailed Card */}
                <div className="surface-nested p-3 rounded">
                  <div className="flex items-center gap-1.5 text-xs font-mono font-semibold text-sky-400 mb-1.5">
                    {React.createElement(storyStages[activeStoryStage].icon, { className: 'w-3.5 h-3.5' })}
                    <span>{storyStages[activeStoryStage].title}</span>
                  </div>
                  <p className="text-xs text-slate-200 leading-relaxed font-sans">
                    {storyStages[activeStoryStage].content}
                  </p>
                </div>

                {/* Complete Unfolded Narrative */}
                <div className="mt-3 pt-3 border-t border-white/[0.06]">
                  <div className="text-[10px] font-mono uppercase text-slate-500 font-medium mb-1.5">
                    Consolidated Forensic Story
                  </div>
                  <div className="surface-nested p-3 rounded text-xs text-slate-300 leading-relaxed font-mono whitespace-pre-wrap">
                    {dossier.fraud_story.full_narrative}
                  </div>
                </div>

                {/* Immediate Mitigation Triggers */}
                <div className="mt-3 p-2.5 surface-nested rounded flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2.5">
                  <div className="flex items-center gap-2 text-xs text-slate-300">
                    <ShieldCheck className="w-4 h-4 text-sky-400 shrink-0" />
                    <span><strong>System Recommendation:</strong> {dossier.fraud_story.recommended_action}</span>
                  </div>
                  <div className="flex items-center gap-2 shrink-0">
                    <button 
                      onClick={() => handleSimulateAction('Step-Up Auth Triggered', 'Risk Mitigation Policy')}
                      className="px-2.5 py-1 rounded bg-white/[0.06] hover:bg-white/[0.1] border border-white/[0.08] text-slate-200 text-xs font-mono transition cursor-pointer"
                    >
                      Step-Up Auth
                    </button>
                    <button 
                      onClick={() => handleSimulateAction('Account Quarantine Enforced', 'Account Security Policy')}
                      className="px-2.5 py-1 rounded bg-rose-900/80 hover:bg-rose-800 text-rose-100 text-xs font-mono font-medium uppercase transition cursor-pointer"
                    >
                      Freeze Account
                    </button>
                  </div>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};
