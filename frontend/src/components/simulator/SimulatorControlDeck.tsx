import React, { useState, useEffect } from 'react';
import { 
  Zap, 
  Play, 
  Square, 
  RotateCcw, 
  AlertTriangle, 
  CheckCircle2, 
  ShieldAlert, 
  Layers, 
  Globe, 
  Radio, 
  TrendingUp, 
  Users 
} from 'lucide-react';
import { SimulatorStatus } from '../../types/api';
import { api } from '../../services/api';
import { wsService } from '../../services/websocket';

interface SimulatorControlDeckProps {
  onScenarioTriggered?: (scenario: string, results: any) => void;
}

export const SimulatorControlDeck: React.FC<SimulatorControlDeckProps> = ({
  onScenarioTriggered
}) => {
  const [status, setStatus] = useState<SimulatorStatus>({
    is_running: false,
    current_tps: 1.0,
    total_injected: 0,
    active_scenario: null,
    status_message: 'Simulator idle'
  });
  const [isTriggering, setIsTriggering] = useState<string | null>(null);
  const [feedbackMsg, setFeedbackMsg] = useState<{ text: string; type: 'success' | 'info' | 'error' } | null>(null);
  const [targetTps, setTargetTps] = useState<number>(1.0);

  // Load simulator status on mount
  useEffect(() => {
    api.getSimulatorStatus().then(setStatus).catch(() => {});

    const unsub = wsService.on('SIMULATOR_STATE', (newStatus: SimulatorStatus) => {
      setStatus(newStatus);
    });

    return () => {
      unsub();
    };
  }, []);

  const scenarios = [
    {
      id: 'ATO',
      name: 'Account Takeover (ATO)',
      tag: 'CRITICAL',
      icon: ShieldAlert,
      desc: 'Injects credential theft login from unrecognized hardware profile in Mumbai & rapid high-value ₹1,25,000 electronics orders.',
      color: 'border-rose-500/40 hover:border-rose-500 bg-rose-950/20'
    },
    {
      id: 'IMPOSSIBLE_TRAVEL',
      name: 'Impossible Travel',
      tag: 'HIGH',
      icon: Globe,
      desc: 'Simulates instantaneous transaction teleportation between Coimbatore and Mumbai within 15 minutes (> 3,900 km/h).',
      color: 'border-orange-500/40 hover:border-orange-500 bg-orange-950/20'
    },
    {
      id: 'CARD_TESTING',
      name: 'UPI / Card Testing Burst',
      tag: 'CRITICAL',
      icon: Layers,
      desc: 'Fires an automated bot sequence of 7 rapid consecutive micro-authorizations testing UPI/card validity.',
      color: 'border-amber-500/40 hover:border-amber-500 bg-amber-950/20'
    },
    {
      id: 'WHALE_OUTLIER',
      name: 'Whale Spend Anomaly',
      tag: 'HIGH',
      icon: TrendingUp,
      desc: 'Submits a single ₹4,80,000 luxury jewellery order at Tanishq for a student persona with ₹2,200 average baseline.',
      color: 'border-cyan-500/40 hover:border-cyan-500 bg-cyan-950/20'
    },
    {
      id: 'MULE_RING',
      name: 'Mule Syndicate Ring',
      tag: 'CRITICAL',
      icon: Users,
      desc: 'Coordinates 4 distinct accounts utilizing 1 shared physical device fingerprint in a closed circular IMPS transfer loop.',
      color: 'border-purple-500/40 hover:border-purple-500 bg-purple-950/20'
    },
    {
      id: 'NORMAL_FLOW',
      name: 'Legitimate Traffic',
      tag: 'SAFE',
      icon: CheckCircle2,
      desc: 'Injects standard Swiggy, DMart, and UPI purchases conforming with registered devices and Indian city baselines.',
      color: 'border-emerald-500/40 hover:border-emerald-500 bg-emerald-950/20'
    }
  ];

  const handleTrigger = async (scenarioId: string) => {
    try {
      setIsTriggering(scenarioId);
      setFeedbackMsg({ text: `Injecting ${scenarioId} scenario into real-time pipeline...`, type: 'info' });
      const res = await api.triggerScenario(scenarioId);
      setFeedbackMsg({ 
        text: `Scenario ${scenarioId} executed: Injected ${res.injected_count} transactions. Detection engine reacted live.`, 
        type: 'success' 
      });
      if (onScenarioTriggered) onScenarioTriggered(scenarioId, res);
      // Refresh status
      const updated = await api.getSimulatorStatus();
      setStatus(updated);
    } catch (err: any) {
      setFeedbackMsg({ text: `Failed to trigger scenario: ${err.message}`, type: 'error' });
    } finally {
      setIsTriggering(null);
    }
  };

  const handleToggleStream = async () => {
    try {
      if (status.is_running) {
        const updated = await api.controlSimulator('STOP');
        setStatus(updated);
        setFeedbackMsg({ text: 'Continuous simulator stream halted.', type: 'info' });
      } else {
        const updated = await api.controlSimulator('START', targetTps);
        setStatus(updated);
        setFeedbackMsg({ text: `Continuous simulator stream initiated at ${targetTps} TPS.`, type: 'success' });
      }
    } catch (err: any) {
      setFeedbackMsg({ text: `Stream control error: ${err.message}`, type: 'error' });
    }
  };

  const handleReset = async () => {
    if (!window.confirm('Reset simulator state and reload clean baseline data?')) return;
    try {
      setFeedbackMsg({ text: 'Resetting simulation environment...', type: 'info' });
      await api.resetSimulator();
      const updated = await api.getSimulatorStatus();
      setStatus(updated);
      setFeedbackMsg({ text: 'Simulation environment restored to baseline.', type: 'success' });
    } catch (err: any) {
      setFeedbackMsg({ text: `Reset error: ${err.message}`, type: 'error' });
    }
  };

  return (
    <div className="space-y-4 font-mono">
      {/* Simulator Control Header */}
      <div className="surface-card p-3.5 rounded-lg flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <div className="p-1.5 rounded bg-white/[0.05] border border-white/[0.08]">
              <Zap className="w-4 h-4 text-sky-400" />
            </div>
            <h2 className="text-sm font-semibold text-white tracking-tight uppercase">
              Attack Simulator Deck
            </h2>
            <span className="px-1.5 py-0.5 text-[9px] font-mono rounded bg-white/[0.05] text-slate-400 border border-white/[0.08] uppercase">
              DEMO ENGINE
            </span>
          </div>
          <p className="text-[11px] text-slate-400 mt-1 font-sans">
            Inject synthetic threats into the active ingestion stream to demonstrate multi-engine risk fusion live.
          </p>
        </div>

        {/* Continuous Stream Controller */}
        <div className="flex items-center gap-3 surface-nested p-2 rounded-lg">
          <div className="flex items-center gap-2 text-xs">
            <span className="text-slate-500 font-mono text-[11px]">TPS:</span>
            <input
              type="range"
              min={0.5}
              max={5.0}
              step={0.5}
              value={targetTps}
              onChange={(e) => setTargetTps(Number(e.target.value))}
              disabled={status.is_running}
              className="w-20 accent-sky-500 cursor-pointer disabled:opacity-50"
            />
            <span className="text-sky-400 font-bold font-mono text-[11px] w-6">{targetTps}</span>
          </div>

          <button
            onClick={handleToggleStream}
            className={`flex items-center gap-1.5 px-3 py-1 rounded text-xs font-semibold font-mono transition-colors ${
              status.is_running
                ? 'bg-rose-950/60 border border-rose-800/60 text-rose-300 hover:bg-rose-900/40'
                : 'bg-emerald-950/60 border border-emerald-800/60 text-emerald-300 hover:bg-emerald-900/40'
            }`}
          >
            {status.is_running ? <Square className="w-3 h-3 fill-current" /> : <Play className="w-3 h-3 fill-current" />}
            <span>{status.is_running ? 'HALT STREAM' : 'START STREAM'}</span>
          </button>

          <button
            onClick={handleReset}
            title="Reset simulation environment"
            className="p-1.5 text-slate-400 hover:text-slate-200 rounded hover:bg-white/[0.05] transition-colors"
          >
            <RotateCcw className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* Real-time Status Feedback Bar */}
      {feedbackMsg && (
        <div className={`p-2.5 rounded border flex items-center gap-2 text-xs font-mono ${
          feedbackMsg.type === 'success' ? 'bg-emerald-950/60 border-emerald-900/60 text-emerald-300' :
          feedbackMsg.type === 'error' ? 'bg-rose-950/60 border-rose-900/60 text-rose-300' :
          'surface-nested text-slate-300 border-white/[0.08]'
        }`}>
          {feedbackMsg.type === 'success' ? <CheckCircle2 className="w-3.5 h-3.5 shrink-0" /> : <Radio className="w-3.5 h-3.5 shrink-0 animate-spin" />}
          <span>{feedbackMsg.text}</span>
        </div>
      )}

      {/* Scenario Trigger Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3.5">
        {scenarios.map((scen) => {
          const Icon = scen.icon;
          const isCurrentTrigger = isTriggering === scen.id;
          const tagColor =
            scen.tag === 'CRITICAL' ? 'bg-rose-950/80 text-rose-300 border-rose-800/60' :
            scen.tag === 'HIGH' ? 'bg-amber-950/80 text-amber-300 border-amber-800/60' :
            'bg-emerald-950/80 text-emerald-300 border-emerald-800/60';

          return (
            <div
              key={scen.id}
              className="surface-card surface-card-hover p-3.5 rounded-lg flex flex-col justify-between border border-white/[0.08] transition-all"
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <div className="p-1.5 rounded bg-white/[0.05] border border-white/[0.08]">
                      <Icon className="w-3.5 h-3.5 text-slate-300" />
                    </div>
                    <span className="font-semibold text-xs text-slate-200">{scen.name}</span>
                  </div>
                  <span className={`px-1.5 py-0.5 text-[9px] font-mono font-semibold rounded uppercase border ${tagColor}`}>
                    {scen.tag}
                  </span>
                </div>

                <p className="text-[11px] text-slate-400 leading-relaxed mb-3.5 font-sans">
                  {scen.desc}
                </p>
              </div>

              <button
                onClick={() => handleTrigger(scen.id)}
                disabled={isCurrentTrigger !== null}
                className="w-full py-1.5 px-3 rounded bg-white/[0.05] hover:bg-white/[0.1] border border-white/[0.1] text-slate-200 font-mono text-xs flex items-center justify-center gap-2 transition-colors cursor-pointer disabled:opacity-40"
              >
                <Zap className="w-3 h-3 text-sky-400" />
                <span>{isCurrentTrigger ? 'Injecting scenario...' : 'Inject Threat'}</span>
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
};
