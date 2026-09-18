import { 
  OverviewMetrics, 
  RiskDistributionResponse, 
  Transaction, 
  Account, 
  GraphNetworkResponse, 
  SimulatorStatus, 
  AINarrativeReport 
} from '../types/api';
import {
  InvestigationSummary,
  InvestigationDossier
} from '../types/investigation';

const API_BASE = '/api';

export const api = {
  // Analytics
  async getOverview(): Promise<OverviewMetrics> {
    const res = await fetch(`${API_BASE}/analytics/overview`);
    if (!res.ok) throw new Error(`Failed to fetch overview metrics: ${res.statusText}`);
    return res.json();
  },

  async getRiskDistribution(): Promise<RiskDistributionResponse> {
    const res = await fetch(`${API_BASE}/analytics/risk-distribution`);
    if (!res.ok) throw new Error(`Failed to fetch risk distribution: ${res.statusText}`);
    return res.json();
  },

  // Transactions
  async getTransactions(params?: { limit?: number; offset?: number; min_risk?: number; risk_level?: string; account_id?: string }): Promise<{ total: number; transactions: Transaction[] }> {
    const searchParams = new URLSearchParams();
    if (params?.limit) searchParams.append('limit', params.limit.toString());
    if (params?.offset) searchParams.append('offset', params.offset.toString());
    if (params?.min_risk !== undefined) searchParams.append('min_risk', params.min_risk.toString());
    if (params?.risk_level) searchParams.append('risk_level', params.risk_level);
    if (params?.account_id) searchParams.append('account_id', params.account_id);

    const res = await fetch(`${API_BASE}/transactions?${searchParams.toString()}`);
    if (!res.ok) throw new Error(`Failed to fetch transactions: ${res.statusText}`);
    return res.json();
  },

  async getTransaction(id: string): Promise<Transaction> {
    const res = await fetch(`${API_BASE}/transactions/${id}`);
    if (!res.ok) throw new Error(`Failed to fetch transaction ${id}: ${res.statusText}`);
    return res.json();
  },

  async ingestTransaction(payload: any): Promise<Transaction> {
    const res = await fetch(`${API_BASE}/transactions/ingest`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error(`Failed to ingest transaction: ${res.statusText}`);
    return res.json();
  },

  // Accounts
  async getAccounts(limit: number = 50): Promise<Account[]> {
    const res = await fetch(`${API_BASE}/accounts?limit=${limit}`);
    if (!res.ok) throw new Error(`Failed to fetch accounts: ${res.statusText}`);
    return res.json();
  },

  async getAccountDetail(id: string): Promise<any> {
    const res = await fetch(`${API_BASE}/accounts/${id}`);
    if (!res.ok) throw new Error(`Failed to fetch account detail ${id}: ${res.statusText}`);
    return res.json();
  },

  // Graph
  async getNetworkGraph(centerId?: string, maxNodes: number = 45): Promise<GraphNetworkResponse> {
    const searchParams = new URLSearchParams();
    if (centerId) searchParams.append('center_id', centerId);
    searchParams.append('max_nodes', maxNodes.toString());

    const res = await fetch(`${API_BASE}/graph/network?${searchParams.toString()}`);
    if (!res.ok) throw new Error(`Failed to fetch network graph: ${res.statusText}`);
    return res.json();
  },

  // Simulator
  async getSimulatorStatus(): Promise<SimulatorStatus> {
    const res = await fetch(`${API_BASE}/simulator/status`);
    if (!res.ok) throw new Error(`Failed to fetch simulator status: ${res.statusText}`);
    return res.json();
  },

  async triggerScenario(scenario: string, targetAccountId?: string): Promise<any> {
    const res = await fetch(`${API_BASE}/simulator/scenario`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ scenario, target_account_id: targetAccountId })
    });
    if (!res.ok) throw new Error(`Failed to trigger scenario ${scenario}: ${res.statusText}`);
    return res.json();
  },

  async controlSimulator(action: 'START' | 'STOP', tps?: number): Promise<SimulatorStatus> {
    const res = await fetch(`${API_BASE}/simulator/control`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action, tps })
    });
    if (!res.ok) throw new Error(`Failed to ${action} simulator: ${res.statusText}`);
    return res.json();
  },

  async resetSimulator(): Promise<any> {
    const res = await fetch(`${API_BASE}/simulator/reset`, {
      method: 'POST'
    });
    if (!res.ok) throw new Error(`Failed to reset simulator: ${res.statusText}`);
    return res.json();
  },

  // AI Analyst
  async investigateAI(txId: string): Promise<AINarrativeReport> {
    const res = await fetch(`${API_BASE}/ai/investigate/${txId}`, {
      method: 'POST'
    });
    if (!res.ok) throw new Error(`Failed to generate AI investigation: ${res.statusText}`);
    return res.json();
  },

  // Contextual Fraud Evolution & Investigations (Phase 3 Innovation Layer)
  async getInvestigations(limit: number = 50): Promise<InvestigationSummary[]> {
    const res = await fetch(`${API_BASE}/investigations?limit=${limit}`);
    if (!res.ok) throw new Error(`Failed to fetch investigations: ${res.statusText}`);
    return res.json();
  },

  async getInvestigationDossier(accountId: string): Promise<InvestigationDossier> {
    const res = await fetch(`${API_BASE}/investigations/${accountId}`);
    if (!res.ok) throw new Error(`Failed to fetch dossier for ${accountId}: ${res.statusText}`);
    return res.json();
  },

  async triggerJudgeDemo(): Promise<InvestigationDossier> {
    const res = await fetch(`${API_BASE}/investigations/judge-demo`, {
      method: 'POST'
    });
    if (!res.ok) throw new Error(`Failed to execute Judge Demo scenario: ${res.statusText}`);
    return res.json();
  },

  async resetJudgeDemo(): Promise<InvestigationDossier> {
    const res = await fetch(`${API_BASE}/investigations/judge-demo/reset`, {
      method: 'POST'
    });
    if (!res.ok) throw new Error(`Failed to reset Judge Demo scenario: ${res.statusText}`);
    return res.json();
  }
};


