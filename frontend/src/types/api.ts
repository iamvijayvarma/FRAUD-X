export type RiskLevel = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
export type ActionTaken = 'ALLOW' | 'MONITOR' | 'CHALLENGE' | 'HOLD' | 'BLOCK';

export interface SignalEvidence {
  code: string;
  name: string;
  category: 'BEHAVIORAL' | 'DEVICE' | 'LOCATION' | 'VELOCITY' | 'GRAPH' | 'ML';
  points: number;
  observed_value: string;
  baseline_value: string;
  severity: 'INFO' | 'WARNING' | 'CRITICAL';
  description: string;
}

export interface RiskAssessment {
  transaction_id: string;
  risk_score: number;
  risk_level: RiskLevel;
  action_taken: ActionTaken;
  primary_reasons: string[];
  signals: SignalEvidence[];
  ml_score: number;
  velocity_count_1m: number;
  velocity_count_5m: number;
  speed_kmh?: number | null;
  distance_km?: number | null;
  device_account_count: number;
  is_circular_loop: boolean;
}

export interface AINarrativeReport {
  transaction_id: string;
  executive_summary: string;
  forensic_narrative: string;
  correlation_analysis: string;
  recommended_action: string;
  confidence_score: number;
  action_justification: string;
  immediate_mitigations: string[];
  timestamp: string;
}

export interface Transaction {
  id: string;
  timestamp: string;
  account_id: string;
  target_account_id?: string | null;
  amount: number;
  currency: string;
  merchant_name: string;
  merchant_category: string;
  transaction_type: string;
  bank_name?: string;
  device_id: string;
  ip_address: string;
  location_city: string;
  location_country: string;
  location_lat: number;
  location_lon: number;
  risk_score: number;
  risk_level: RiskLevel;
  action_taken: ActionTaken;
  assessment?: RiskAssessment;
  ai_narrative?: AINarrativeReport | string;
}

export interface Account {
  id: string;
  holder_name: string;
  email: string;
  avg_amount: number;
  std_amount: number;
  typical_city: string;
  typical_country: string;
  primary_bank?: string;
  status: string;
  risk_rating: RiskLevel;
}

export interface OverviewMetrics {
  total_transactions: number;
  fraud_blocked_amount: number;
  average_risk_score: number;
  open_alerts_count: number;
  high_risk_transactions_count: number;
  processing_engine_status: string;
  latency_ms: number;
}

export interface RiskDistributionItem {
  level: RiskLevel;
  count: number;
  color: string;
}

export interface TimelinePoint {
  id: string;
  time: string;
  risk_score: number;
  risk_level: RiskLevel;
  amount: number;
}

export interface RiskDistributionResponse {
  distribution: RiskDistributionItem[];
  timeline: TimelinePoint[];
}

export interface GraphNode {
  id: string;
  label: string;
  type: 'ACCOUNT' | 'DEVICE' | 'MERCHANT' | 'IP';
  risk_level: RiskLevel;
  degree: number;
  properties?: Record<string, any>;
  x?: number;
  y?: number;
}

export interface GraphEdge {
  source: string;
  target: string;
  type: string;
  amount?: number | null;
  timestamp?: string | null;
  is_circular?: boolean;
}

export interface GraphNetworkResponse {
  nodes: GraphNode[];
  edges: GraphEdge[];
  cycles_detected: string[][];
  suspicious_clusters_count: number;
}

export interface SimulatorStatus {
  is_running: boolean;
  current_tps: number;
  total_injected: number;
  active_scenario?: string | null;
  status_message: string;
}
