import React from 'react';
import { 
  LayoutDashboard, 
  Layers, 
  AlertOctagon, 
  Users, 
  Share2, 
  Terminal, 
  GitBranch,
  CheckCircle,
  Shield
} from 'lucide-react';

export type ActiveTab = 'dashboard' | 'evolution' | 'transactions' | 'alerts' | 'accounts' | 'network' | 'simulator';

interface SidebarProps {
  activeTab: ActiveTab;
  onSelectTab: (tab: ActiveTab) => void;
  openAlertsCount: number;
}

export const Sidebar: React.FC<SidebarProps> = ({
  activeTab,
  onSelectTab,
  openAlertsCount
}) => {
  const navItems = [
    { id: 'dashboard', label: 'Command Center', icon: LayoutDashboard, badge: null },
    { id: 'evolution', label: 'Investigations', icon: GitBranch, badge: 'EVOLUTION' },
    { id: 'transactions', label: 'Live Transactions', icon: Layers, badge: null },
    { id: 'alerts', label: 'Active Alerts', icon: AlertOctagon, badge: openAlertsCount > 0 ? openAlertsCount : null },
    { id: 'accounts', label: 'Accounts', icon: Users, badge: null },
    { id: 'network', label: 'Network Intelligence', icon: Share2, badge: null },
    { id: 'simulator', label: 'Attack Simulator', icon: Terminal, badge: null },
  ];

  return (
    <aside className="w-60 border-r border-white/[0.08] bg-[#0e1117] flex flex-col justify-between shrink-0 select-none">
      <div className="p-3 space-y-5">
        {/* Navigation Group */}
        <div>
          <div className="px-2.5 mb-2 text-[10px] font-mono tracking-wider uppercase text-slate-500 font-medium">
            Platform Navigation
          </div>
          <nav className="space-y-0.5">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  id={`nav-${item.id}`}
                  onClick={() => onSelectTab(item.id as ActiveTab)}
                  className={`w-full flex items-center justify-between px-2.5 py-2 rounded-md text-xs font-medium cursor-pointer transition-colors ${
                    isActive
                      ? 'bg-white/[0.08] text-white border border-white/[0.1]'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-white/[0.03] border border-transparent'
                  }`}
                >
                  <div className="flex items-center gap-2.5">
                    <Icon className={`w-4 h-4 ${isActive ? 'text-sky-400' : 'text-slate-500'}`} />
                    <span>{item.label}</span>
                  </div>

                  {item.badge !== null && (
                    <span className={`px-1.5 py-0.5 text-[9px] font-mono rounded ${
                      item.id === 'alerts'
                        ? 'bg-rose-950/60 text-rose-300 border border-rose-900/60 font-semibold'
                        : 'bg-white/[0.05] text-slate-400 border border-white/[0.08]'
                    }`}>
                      {item.badge}
                    </span>
                  )}
                </button>
              );
            })}
          </nav>
        </div>

        {/* Six Core Contextual Engines */}
        <div className="pt-4 border-t border-white/[0.06]">
          <div className="px-2.5 mb-2 text-[10px] font-mono tracking-wider uppercase text-slate-500 font-medium">
            Active Signal Engines
          </div>
          <div className="px-2.5 space-y-1.5 text-[11px] font-mono">
            <div className="flex items-center justify-between text-slate-400">
              <span className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                01. Behaviour
              </span>
              <span className="text-[10px] text-slate-500 font-medium">Z-Score</span>
            </div>
            <div className="flex items-center justify-between text-slate-400">
              <span className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                02. Account History
              </span>
              <span className="text-[10px] text-slate-500 font-medium">Baselines</span>
            </div>
            <div className="flex items-center justify-between text-slate-400">
              <span className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                03. Device Identity
              </span>
              <span className="text-[10px] text-slate-500 font-medium">Hardware</span>
            </div>
            <div className="flex items-center justify-between text-slate-400">
              <span className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                04. Location Geo
              </span>
              <span className="text-[10px] text-slate-500 font-medium">Haversine</span>
            </div>
            <div className="flex items-center justify-between text-slate-400">
              <span className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                05. Velocity Sliding
              </span>
              <span className="text-[10px] text-slate-500 font-medium">Burst</span>
            </div>
            <div className="flex items-center justify-between text-slate-400">
              <span className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                06. Network Graph
              </span>
              <span className="text-[10px] text-slate-500 font-medium">NetworkX</span>
            </div>
          </div>
        </div>
      </div>

      {/* Operator Credentials Footer */}
      <div className="p-3 border-t border-white/[0.08] bg-[#0b0e14]">
        <div className="flex items-center gap-2.5">
          <div className="w-7 h-7 rounded bg-white/[0.04] border border-white/[0.08] flex items-center justify-center text-slate-300 font-mono text-[11px]">
            FX
          </div>
          <div className="min-w-0">
            <div className="text-xs font-medium text-slate-200 truncate">Forensic Analyst</div>
            <div className="text-[10px] text-slate-500 font-mono flex items-center gap-1">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
              Secured Session
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
};
