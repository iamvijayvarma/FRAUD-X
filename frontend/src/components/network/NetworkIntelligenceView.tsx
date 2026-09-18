import React, { useState, useEffect, useMemo } from 'react';
import { 
  Share2, 
  RotateCw, 
  AlertTriangle, 
  ShieldAlert, 
  Info,
  CheckCircle2 
} from 'lucide-react';
import { GraphNetworkResponse, GraphNode } from '../../types/api';
import { api } from '../../services/api';

export const NetworkIntelligenceView: React.FC = () => {
  const [graphData, setGraphData] = useState<GraphNetworkResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);

  const fetchGraph = async () => {
    try {
      setIsLoading(true);
      const data = await api.getNetworkGraph(undefined, 50);
      setGraphData(data);
      if (data.nodes.length > 0) {
        const highRisk = data.nodes.find(n => n.risk_level === 'CRITICAL' || n.risk_level === 'HIGH');
        setSelectedNode(highRisk || data.nodes[0]);
      }
    } catch (err) {
      console.error('Failed to load network graph:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchGraph();
  }, []);

  // Compute 2D node positions in an aesthetically balanced organic cluster
  const positionedNodes = useMemo(() => {
    if (!graphData?.nodes) return [];
    const count = graphData.nodes.length;
    const width = 800;
    const height = 520;
    const centerX = width / 2;
    const centerY = height / 2;
    const radius = Math.min(width, height) * 0.38;

    return graphData.nodes.map((node, i) => {
      const angle = i * (Math.PI * (3 - Math.sqrt(5)));
      const r = Math.sqrt(i / count) * radius + 40;
      const x = centerX + r * Math.cos(angle);
      const y = centerY + r * Math.sin(angle);
      return { ...node, x, y };
    });
  }, [graphData]);

  const nodeMap = useMemo(() => {
    const map = new Map<string, { x: number; y: number; node: GraphNode }>();
    positionedNodes.forEach(pn => map.set(pn.id, { x: pn.x, y: pn.y, node: pn }));
    return map;
  }, [positionedNodes]);

  const connectedNodeIds = useMemo(() => {
    if (!selectedNode || !graphData?.edges) return new Set<string>();
    const ids = new Set<string>();
    ids.add(selectedNode.id);
    graphData.edges.forEach(e => {
      if (e.source === selectedNode.id) ids.add(e.target);
      if (e.target === selectedNode.id) ids.add(e.source);
    });
    return ids;
  }, [selectedNode, graphData]);

  const getNodeColor = (node: GraphNode) => {
    if (node.risk_level === 'CRITICAL') return '#ef4444';
    if (node.risk_level === 'HIGH') return '#f97316';
    if (node.type === 'DEVICE') return '#a78bfa';
    if (node.type === 'MERCHANT') return '#06b6d4';
    return '#38bdf8';
  };

  return (
    <div className="space-y-3.5 font-mono">
      {/* Header Bar */}
      <div className="surface-card p-3.5 rounded-lg flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="p-1.5 rounded bg-white/[0.05] border border-white/[0.08] text-slate-300">
            <Share2 className="w-4 h-4 text-sky-400" />
          </div>
          <div>
            <h2 className="text-sm font-semibold text-white tracking-tight uppercase">
              Network Graph & Syndicate Topology
            </h2>
            <p className="text-[11px] text-slate-400 font-sans">
              Shared hardware profiles, merchant hubs, and circular fund routing rings (NetworkX Engine).
            </p>
          </div>
        </div>

        <button
          onClick={fetchGraph}
          disabled={isLoading}
          className="flex items-center gap-1.5 px-3 py-1.5 bg-white/[0.05] hover:bg-white/[0.08] text-slate-200 border border-white/[0.1] rounded text-xs transition-colors cursor-pointer"
        >
          <RotateCw className={`w-3.5 h-3.5 ${isLoading ? 'animate-spin' : ''}`} />
          <span>Sync Topology</span>
        </button>
      </div>

      {/* Main Workspace Split */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-3.5">
        {/* Graph Canvas Container */}
        <div className="lg:col-span-8 surface-card rounded-lg p-3.5 relative overflow-hidden bg-[#0d1016]">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-3 text-xs text-slate-400 font-mono">
              <span>Nodes: <strong className="text-slate-200">{graphData?.nodes.length || 0}</strong></span>
              <span>Edges: <strong className="text-slate-200">{graphData?.edges.length || 0}</strong></span>
              {graphData?.cycles_detected && graphData.cycles_detected.length > 0 && (
                <span className="px-1.5 py-0.2 rounded text-[10px] font-semibold bg-rose-950 text-rose-300 border border-rose-800">
                  {graphData.cycles_detected.length} Cycles Detected
                </span>
              )}
            </div>

            {/* Legend */}
            <div className="flex items-center gap-3 text-[10px] text-slate-400 font-mono">
              <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-sky-400"></span>Account</span>
              <span className="flex items-center gap-1"><span className="w-2 h-2 rounded bg-violet-400"></span>Device</span>
              <span className="flex items-center gap-1"><span className="w-2 h-2 rotate-45 bg-cyan-400"></span>Merchant</span>
              <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-rose-500"></span>Critical</span>
            </div>
          </div>

          {/* SVG Topology Visualizer */}
          <div className="w-full h-[500px] flex items-center justify-center relative select-none">
            {isLoading && !graphData ? (
              <div className="text-xs text-slate-500">Synthesizing network topology...</div>
            ) : (
              <svg viewBox="0 0 800 520" className="w-full h-full">
                {/* Edges */}
                <g className="edges">
                  {graphData?.edges.map((edge, idx) => {
                    const src = nodeMap.get(edge.source);
                    const dst = nodeMap.get(edge.target);
                    if (!src || !dst) return null;

                    const isHighlighted = selectedNode && (edge.source === selectedNode.id || edge.target === selectedNode.id);
                    const isCycle = edge.is_circular || (graphData.cycles_detected && graphData.cycles_detected.some(c => c.includes(edge.source) && c.includes(edge.target)));

                    return (
                      <line
                        key={idx}
                        x1={src.x}
                        y1={src.y}
                        x2={dst.x}
                        y2={dst.y}
                        stroke={isCycle ? '#ef4444' : isHighlighted ? '#38bdf8' : 'rgba(255,255,255,0.08)'}
                        strokeWidth={isCycle ? 2 : isHighlighted ? 1.5 : 1}
                        strokeDasharray={edge.type === 'USED_DEVICE' ? '3 3' : undefined}
                        opacity={isHighlighted || isCycle ? 1 : 0.4}
                      />
                    );
                  })}
                </g>

                {/* Nodes */}
                <g className="nodes">
                  {positionedNodes.map((node) => {
                    const isSelected = selectedNode?.id === node.id;
                    const isConnected = connectedNodeIds.has(node.id);
                    const color = getNodeColor(node);

                    return (
                      <g
                        key={node.id}
                        onClick={() => setSelectedNode(node)}
                        className="cursor-pointer transition-transform hover:scale-110"
                      >
                        {/* Selection Halo */}
                        {isSelected && (
                          <circle
                            cx={node.x}
                            cy={node.y}
                            r={15}
                            fill="none"
                            stroke="#ffffff"
                            strokeWidth={1.5}
                            opacity={0.8}
                          />
                        )}

                        {/* Node Shape based on type */}
                        {node.type === 'DEVICE' ? (
                          <rect
                            x={(node.x || 0) - 6}
                            y={(node.y || 0) - 6}
                            width={12}
                            height={12}
                            rx={2}
                            fill={color}
                            stroke="#0f172a"
                            strokeWidth={1.5}
                            opacity={!selectedNode || isConnected ? 1 : 0.25}
                          />
                        ) : node.type === 'MERCHANT' ? (
                          <polygon
                            points={`${node.x},${(node.y || 0) - 7} ${(node.x || 0) + 7},${node.y} ${node.x},${(node.y || 0) + 7} ${(node.x || 0) - 7},${node.y}`}
                            fill={color}
                            stroke="#0f172a"
                            strokeWidth={1.5}
                            opacity={!selectedNode || isConnected ? 1 : 0.25}
                          />
                        ) : (
                          <circle
                            cx={node.x}
                            cy={node.y}
                            r={node.risk_level === 'CRITICAL' ? 8 : 6}
                            fill={color}
                            stroke="#0f172a"
                            strokeWidth={1.5}
                            opacity={!selectedNode || isConnected ? 1 : 0.25}
                          />
                        )}

                        {/* Label */}
                        <text
                          x={node.x}
                          y={(node.y || 0) + 14}
                          textAnchor="middle"
                          fill={isSelected ? '#ffffff' : isConnected ? '#cbd5e1' : '#64748b'}
                          fontSize={9}
                          fontFamily="monospace"
                          fontWeight={isSelected ? 'bold' : 'normal'}
                        >
                          {node.label.length > 12 ? `${node.label.slice(0, 10)}...` : node.label}
                        </text>
                      </g>
                    );
                  })}
                </g>
              </svg>
            )}
          </div>
        </div>

        {/* Selected Entity Inspector Panel */}
        <div className="lg:col-span-4 space-y-3">
          <div className="surface-card p-3.5 rounded-lg space-y-3">
            <span className="text-[10px] font-semibold tracking-wider text-slate-500 uppercase block">
              Selected Entity Dossier
            </span>

            {selectedNode ? (
              <div className="space-y-3 text-xs">
                <div className="flex items-center justify-between pb-2.5 border-b border-white/[0.06]">
                  <div>
                    <span className="text-white font-semibold text-sm block">{selectedNode.label}</span>
                    <span className="text-slate-500 text-[10px]">{selectedNode.id}</span>
                  </div>
                  <span className={`px-1.5 py-0.5 text-[9px] font-semibold rounded uppercase ${
                    selectedNode.risk_level === 'CRITICAL' ? 'bg-rose-950 text-rose-300 border border-rose-800' :
                    selectedNode.risk_level === 'HIGH' ? 'bg-orange-950 text-orange-300 border border-orange-800' :
                    'bg-white/[0.06] text-slate-300 border border-white/[0.08]'
                  }`}>
                    {selectedNode.risk_level}
                  </span>
                </div>

                <div className="grid grid-cols-2 gap-2 text-[11px]">
                  <div className="surface-nested p-2 rounded">
                    <span className="text-slate-500 block text-[9px]">TYPE</span>
                    <span className="font-semibold text-slate-200">{selectedNode.type}</span>
                  </div>
                  <div className="surface-nested p-2 rounded">
                    <span className="text-slate-500 block text-[9px]">CENTRALITY</span>
                    <span className="font-semibold text-sky-400">{selectedNode.degree} links</span>
                  </div>
                </div>

                {/* Connected relationships */}
                <div>
                  <span className="text-[10px] font-semibold text-slate-400 uppercase block mb-1.5">
                    Active Links ({connectedNodeIds.size - 1})
                  </span>
                  <div className="space-y-1 max-h-40 overflow-y-auto">
                    {graphData?.edges
                      .filter(e => e.source === selectedNode.id || e.target === selectedNode.id)
                      .map((edge, i) => {
                        const otherId = edge.source === selectedNode.id ? edge.target : edge.source;
                        return (
                          <div key={i} className="surface-nested p-1.5 rounded flex items-center justify-between text-[10px]">
                            <span className="text-slate-400">{edge.type}</span>
                            <span className="text-sky-300 font-mono">{otherId}</span>
                          </div>
                        );
                      })}
                  </div>
                </div>
              </div>
            ) : (
              <div className="py-8 text-center text-slate-500 text-xs">
                Click any node in the topology visualizer to inspect entity connections.
              </div>
            )}
          </div>

          {/* Detected Rings */}
          {graphData?.cycles_detected && graphData.cycles_detected.length > 0 && (
            <div className="surface-card p-3 rounded-lg border-rose-900/40 text-xs space-y-2">
              <div className="flex items-center gap-1.5 text-rose-400 font-semibold text-xs">
                <AlertTriangle className="w-3.5 h-3.5" />
                <span>CIRCULAR LAYERING RINGS</span>
              </div>
              <p className="text-[11px] text-slate-400 font-sans">
                Closed circular transfer loops indicative of layered money mule transactions:
              </p>
              <div className="space-y-1 font-mono text-[10px]">
                {graphData.cycles_detected.map((cycle, i) => (
                  <div key={i} className="surface-nested p-1.5 rounded text-rose-300">
                    {cycle.join(' → ')} → {cycle[0]}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
