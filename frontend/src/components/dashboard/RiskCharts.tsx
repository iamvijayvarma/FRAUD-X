import React from 'react';
import { 
  ResponsiveContainer, 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  Tooltip, 
  Cell, 
  AreaChart, 
  Area 
} from 'recharts';
import { RiskDistributionResponse } from '../../types/api';
import { formatINR } from '../../utils/formatters';

interface RiskChartsProps {
  distributionData: RiskDistributionResponse | null;
  isLoading: boolean;
}

export const RiskCharts: React.FC<RiskChartsProps> = ({ distributionData, isLoading }) => {
  const distribution = distributionData?.distribution || [
    { level: 'LOW', count: 0, color: '#10b981' },
    { level: 'MEDIUM', count: 0, color: '#f59e0b' },
    { level: 'HIGH', count: 0, color: '#f97316' },
    { level: 'CRITICAL', count: 0, color: '#ef4444' }
  ];

  const timeline = distributionData?.timeline || [];

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-3.5">
      {/* Risk Distribution Breakdown */}
      <div className="lg:col-span-4 surface-card rounded-lg p-3.5 flex flex-col justify-between">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-semibold tracking-tight text-slate-200 uppercase">
            Risk Tier Distribution
          </span>
          <span className="text-[10px] font-mono text-slate-500">Calibrated Fusion</span>
        </div>

        <div className="h-40 w-full">
          {isLoading && !distributionData ? (
            <div className="h-full flex items-center justify-center text-xs font-mono text-slate-500">
              Loading distribution telemetry...
            </div>
          ) : (
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={distribution} layout="vertical" margin={{ top: 5, right: 15, left: 0, bottom: 5 }}>
                <XAxis type="number" hide />
                <YAxis 
                  dataKey="level" 
                  type="category" 
                  tick={{ fill: '#94a3b8', fontSize: 10, fontFamily: 'monospace' }} 
                  width={60} 
                  axisLine={false} 
                  tickLine={false} 
                />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#171a23', borderColor: 'rgba(255,255,255,0.1)', borderRadius: '6px', fontSize: '11px', fontFamily: 'monospace' }}
                  formatter={(value: any) => [`${value} transactions`, 'Volume']}
                />
                <Bar dataKey="count" radius={[0, 3, 3, 0]} barSize={14}>
                  {distribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>

        {/* Legend Summary */}
        <div className="grid grid-cols-4 gap-1 pt-2 border-t border-white/[0.06] text-center font-mono">
          {distribution.map((item) => (
            <div key={item.level} className="text-[10px]">
              <div className="text-slate-500">{item.level}</div>
              <div className="font-semibold text-xs mt-0.5" style={{ color: item.color }}>
                {item.count}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Real-Time Risk Activity Timeline */}
      <div className="lg:col-span-8 surface-card rounded-lg p-3.5 flex flex-col justify-between">
        <div className="flex items-center justify-between mb-2">
          <div>
            <span className="text-xs font-semibold tracking-tight text-slate-200 uppercase">
              Transaction Risk Trajectory
            </span>
            <p className="text-[11px] text-slate-400">Chronological risk score evaluations</p>
          </div>
          <div className="flex items-center gap-3 text-[10px] font-mono text-slate-400">
            <span className="flex items-center gap-1.5"><span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>&lt;30 Low</span>
            <span className="flex items-center gap-1.5"><span className="w-1.5 h-1.5 rounded-full bg-amber-400"></span>30-60 Med</span>
            <span className="flex items-center gap-1.5"><span className="w-1.5 h-1.5 rounded-full bg-rose-400"></span>&gt;60 Critical</span>
          </div>
        </div>

        <div className="h-40 w-full">
          {timeline.length === 0 ? (
            <div className="h-full flex items-center justify-center text-xs font-mono text-slate-500">
              Awaiting streaming transactions...
            </div>
          ) : (
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={timeline} margin={{ top: 5, right: 10, left: -25, bottom: 0 }}>
                <defs>
                  <linearGradient id="riskScoreGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#0284c7" stopOpacity={0.25}/>
                    <stop offset="95%" stopColor="#0284c7" stopOpacity={0.0}/>
                  </linearGradient>
                </defs>
                <XAxis 
                  dataKey="time" 
                  tick={{ fill: '#64748b', fontSize: 10, fontFamily: 'monospace' }} 
                  axisLine={{ stroke: 'rgba(255,255,255,0.08)' }} 
                  tickLine={false} 
                />
                <YAxis 
                  domain={[0, 100]} 
                  tick={{ fill: '#64748b', fontSize: 10, fontFamily: 'monospace' }} 
                  axisLine={{ stroke: 'rgba(255,255,255,0.08)' }} 
                  tickLine={false} 
                />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#171a23', borderColor: 'rgba(255,255,255,0.1)', borderRadius: '6px', fontSize: '11px', fontFamily: 'monospace' }}
                  formatter={(val: any, name: any, props: any) => [
                    `${val}/100 (${props.payload.risk_level}) • ${formatINR(props.payload.amount, true)}`,
                    'Risk Score'
                  ]}
                />
                <Area 
                  type="monotone" 
                  dataKey="risk_score" 
                  stroke="#0284c7" 
                  strokeWidth={1.5} 
                  fillOpacity={1} 
                  fill="url(#riskScoreGrad)" 
                />
              </AreaChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>
    </div>
  );
};
