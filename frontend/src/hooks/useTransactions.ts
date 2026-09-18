import { useState, useEffect, useMemo, useCallback } from 'react';
import { Transaction, RiskLevel } from '../types/api';
import { api } from '../services/api';
import { wsService } from '../services/websocket';

export function useTransactions() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [isPaused, setIsPaused] = useState<boolean>(false);
  const [pausedBuffer, setPausedBuffer] = useState<Transaction[]>([]);
  
  // Filters
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [minRiskFilter, setMinRiskFilter] = useState<number>(0);
  const [selectedRiskTier, setSelectedRiskTier] = useState<RiskLevel | 'ALL'>('ALL');
  
  // Selected transaction for investigation drawer
  const [selectedTransaction, setSelectedTransaction] = useState<Transaction | null>(null);

  // Initial load from backend
  const loadTransactions = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      const res = await api.getTransactions({ limit: 40 });
      setTransactions(res.transactions);
    } catch (err: any) {
      setError(err.message || 'Failed to load transactions');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadTransactions();
  }, [loadTransactions]);

  // Real-time WebSocket listener
  useEffect(() => {
    const unsub = wsService.on('TX_PROCESSED', (newTx: Transaction) => {
      if (isPaused) {
        setPausedBuffer(prev => [newTx, ...prev].slice(0, 50));
      } else {
        setTransactions(prev => {
          // Avoid duplicate ID
          if (prev.some(t => t.id === newTx.id)) return prev;
          return [newTx, ...prev].slice(0, 80); // Bound at 80 items
        });
      }
    });

    return () => {
      unsub();
    };
  }, [isPaused]);

  // Resume stream and flush paused buffer
  const togglePause = useCallback(() => {
    setIsPaused(prev => {
      if (prev && pausedBuffer.length > 0) {
        setTransactions(current => {
          const combined = [...pausedBuffer, ...current];
          const unique = Array.from(new Map(combined.map(t => [t.id, t])).values());
          return unique.slice(0, 80);
        });
        setPausedBuffer([]);
      }
      return !prev;
    });
  }, [pausedBuffer]);

  // Filtered transactions
  const filteredTransactions = useMemo(() => {
    return transactions.filter(tx => {
      // Risk score threshold
      if (tx.risk_score < minRiskFilter) return false;
      
      // Risk tier
      if (selectedRiskTier !== 'ALL' && tx.risk_level !== selectedRiskTier) return false;

      // Text search (account_id, merchant_name, id, city, device_id)
      if (searchQuery.trim()) {
        const query = searchQuery.toLowerCase().trim();
        const matchId = tx.id.toLowerCase().includes(query);
        const matchAcc = tx.account_id.toLowerCase().includes(query);
        const matchMerch = (tx.merchant_name || '').toLowerCase().includes(query);
        const matchCity = (tx.location_city || '').toLowerCase().includes(query);
        const matchDev = (tx.device_id || '').toLowerCase().includes(query);
        if (!matchId && !matchAcc && !matchMerch && !matchCity && !matchDev) {
          return false;
        }
      }

      return true;
    });
  }, [transactions, minRiskFilter, selectedRiskTier, searchQuery]);

  return {
    transactions: filteredTransactions,
    rawCount: transactions.length,
    isLoading,
    error,
    isPaused,
    pausedBufferCount: pausedBuffer.length,
    togglePause,
    searchQuery,
    setSearchQuery,
    minRiskFilter,
    setMinRiskFilter,
    selectedRiskTier,
    setSelectedRiskTier,
    selectedTransaction,
    setSelectedTransaction,
    refresh: loadTransactions
  };
}
