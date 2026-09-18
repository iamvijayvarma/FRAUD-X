import { useState, useEffect, useCallback } from 'react';
import { OverviewMetrics, RiskDistributionResponse } from '../types/api';
import { api } from '../services/api';
import { wsService } from '../services/websocket';

export function useAnalytics() {
  const [overview, setOverview] = useState<OverviewMetrics | null>(null);
  const [distribution, setDistribution] = useState<RiskDistributionResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchAnalytics = useCallback(async () => {
    try {
      setError(null);
      const [ovData, distData] = await Promise.all([
        api.getOverview(),
        api.getRiskDistribution()
      ]);
      setOverview(ovData);
      setDistribution(distData);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch analytics data');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchAnalytics();

    // Listen for WebSocket live transaction to increment totals locally
    const unsub = wsService.on('TX_PROCESSED', (data: any) => {
      setOverview(prev => {
        if (!prev) return prev;
        const isHigh = data.risk_level === 'HIGH' || data.risk_level === 'CRITICAL';
        const isBlocked = data.action_taken === 'BLOCK' || data.action_taken === 'HOLD';
        return {
          ...prev,
          total_transactions: prev.total_transactions + 1,
          fraud_blocked_amount: isBlocked ? prev.fraud_blocked_amount + data.amount : prev.fraud_blocked_amount,
          high_risk_transactions_count: isHigh ? prev.high_risk_transactions_count + 1 : prev.high_risk_transactions_count
        };
      });
    });

    // Background sync every 15s
    const interval = setInterval(fetchAnalytics, 15000);

    return () => {
      unsub();
      clearInterval(interval);
    };
  }, [fetchAnalytics]);

  return {
    overview,
    distribution,
    isLoading,
    error,
    refresh: fetchAnalytics
  };
}
