import { RiskLevel, ActionTaken } from './api';

export interface RiskTrajectoryPoint {
  transaction_id: string;
  timestamp: string;
  amount: number;
  currency: string;
  city: string;
  risk_score: number;
  risk_level: RiskLevel;
  action_taken: ActionTaken;
  signals: string[];
  device_id: string;
  is_new_device: boolean;
}

export interface RiskEvolutionTrajectory {
  account_id: string;
  trajectory_levels: RiskLevel[];
  score_history: number[];
  is_escalating: boolean;
  risk_growth_rate: number;
  accumulated_signals: string[];
  escalation_points_count: number;
  avg_interval_seconds?: number | null;
  timeline_points: RiskTrajectoryPoint[];
}

export interface SignalConfluence {
  has_confluence: boolean;
  confluence_name: string;
  compounding_multiplier: number;
  combined_risk_boost: number;
  contributing_signals: string[];
  confidence_score: number;
  description: string;
}

export interface ChangePointAnalysis {
  regime_shift_detected: boolean;
  change_point_timestamp?: string | null;
  change_point_tx_id?: string | null;
  historical_avg_amount: number;
  historical_typical_city: string;
  recent_avg_amount: number;
  deviation_magnitude: number;
  affected_dimensions: string[];
  narrative: string;
}

export interface NetworkLink {
  connected_account_id: string;
  relationship_type: string;
  shared_entity: string;
  link_grade: 'NORMAL' | 'SUSPICIOUS_CONNECTION' | 'HIGH_RISK_CLUSTER' | 'POTENTIAL_COORDINATED_ACTIVITY';
  explanation: string;
}

export interface CrossAccountPropagation {
  account_id: string;
  network_exposure_score: number;
  cluster_classification: 'NORMAL' | 'SUSPICIOUS_CONNECTION' | 'HIGH_RISK_CLUSTER' | 'POTENTIAL_COORDINATED_ACTIVITY';
  correlated_accounts_count: number;
  shared_devices: string[];
  network_links: NetworkLink[];
}

export interface FraudPatternHypothesis {
  pattern_id: string;
  pattern_name: string;
  pattern_type: string;
  confidence_score: number;
  primary_evidence: string[];
  investigative_hypothesis: string;
}

export interface ExplainableFraudStory {
  timeline: string;
  behaviour_change: string;
  signal_confluence: string;
  network_relationship: string;
  risk_escalation: string;
  current_assessment: string;
  recommended_action: string;
  full_narrative: string;
}

export interface InvestigationSummary {
  account_id: string;
  holder_name: string;
  primary_bank: string;
  current_risk_score: number;
  current_risk_level: RiskLevel;
  investigation_priority: 'NORMAL' | 'WATCH' | 'INVESTIGATE' | 'URGENT';
  priority_score: number;
  detected_pattern: string;
  is_escalating: boolean;
  last_active: string;
  total_transactions_analyzed: number;
}

export interface InvestigationDossier {
  summary: InvestigationSummary;
  evolution: RiskEvolutionTrajectory;
  confluence: SignalConfluence;
  change_point: ChangePointAnalysis;
  network_propagation: CrossAccountPropagation;
  patterns: FraudPatternHypothesis[];
  fraud_story: ExplainableFraudStory;
}
