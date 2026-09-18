import React, { useState } from 'react';
import { Header } from './components/layout/Header';
import { Sidebar, ActiveTab } from './components/layout/Sidebar';
import { KpiCards } from './components/dashboard/KpiCards';
import { RiskCharts } from './components/dashboard/RiskCharts';
import { LiveTransactionFeed } from './components/transactions/LiveTransactionFeed';
import { ActiveAlertsPanel } from './components/dashboard/ActiveAlertsPanel';
import { InvestigationDrawer } from './components/investigation/InvestigationDrawer';
import { NetworkIntelligenceView } from './components/network/NetworkIntelligenceView';
import { SimulatorControlDeck } from './components/simulator/SimulatorControlDeck';
import { AccountsView } from './components/accounts/AccountsView';
import { InvestigationIntelligenceView } from './components/investigation/InvestigationIntelligenceView';

import { useWebSocket } from './hooks/useWebSocket';
import { useTransactions } from './hooks/useTransactions';
import { useAnalytics } from './hooks/useAnalytics';
import { Transaction } from './types/api';

export function App() {
  const [activeTab, setActiveTab] = useState<ActiveTab>('dashboard');
  const [evolutionAccountId, setEvolutionAccountId] = useState<string>('ACC-IN-1043');
  
  // Real-time hooks
  const { status: wsStatus } = useWebSocket();
  const {
    transactions,
    isLoading: isTxLoading,
    isPaused,
    pausedBufferCount,
    togglePause,
    searchQuery,
    setSearchQuery,
    minRiskFilter,
    setMinRiskFilter,
    selectedRiskTier,
    setSelectedRiskTier,
    selectedTransaction,
    setSelectedTransaction
  } = useTransactions();

  const {
    overview,
    distribution,
    isLoading: isAnalyticsLoading
  } = useAnalytics();

  const openAlertsCount = overview?.open_alerts_count || 0;

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-[#070b12] text-slate-100 font-sans">
      {/* Persistent Left Sidebar */}
      <Sidebar
        activeTab={activeTab}
        onSelectTab={setActiveTab}
        openAlertsCount={openAlertsCount}
      />

      {/* Main Workspace Area */}
      <div className="flex-1 flex flex-col h-full overflow-hidden">
        {/* Top Telemetry Header */}
        <Header
          wsStatus={wsStatus}
          latencyMs={overview?.latency_ms || 7.4}
          openAlertsCount={openAlertsCount}
          onOpenSimulator={() => setActiveTab('simulator')}
          onSelectAlerts={() => setActiveTab('alerts')}
          onOpenEvolution={() => setActiveTab('evolution')}
        />

        {/* Dynamic View Workspace */}
        <main className={`flex-1 overflow-y-auto ${activeTab === 'evolution' ? 'p-0 flex flex-col' : 'p-5 space-y-5'}`}>
          {activeTab === 'evolution' && (
            <InvestigationIntelligenceView
              initialAccountId={evolutionAccountId}
              onOpenTransaction={(txId) => {
                const found = transactions.find(t => t.id === txId);
                if (found) setSelectedTransaction(found);
              }}
            />
          )}

          {activeTab === 'dashboard' && (
            <div className="space-y-5 max-w-[1600px] mx-auto">
              {/* Top Row: Executive KPI Cards */}
              <KpiCards metrics={overview} isLoading={isAnalyticsLoading} />

              {/* Middle Row: Risk Distribution & Activity Timeline */}
              <RiskCharts distributionData={distribution} isLoading={isAnalyticsLoading} />

              {/* Lower Split: Live Stream & Priority Alerts */}
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
                <div className="lg:col-span-8 h-[520px]">
                  <LiveTransactionFeed
                    transactions={transactions}
                    isPaused={isPaused}
                    pausedBufferCount={pausedBufferCount}
                    onTogglePause={togglePause}
                    searchQuery={searchQuery}
                    onSearchChange={setSearchQuery}
                    minRiskFilter={minRiskFilter}
                    onMinRiskChange={setMinRiskFilter}
                    selectedRiskTier={selectedRiskTier}
                    onSelectRiskTier={setSelectedRiskTier}
                    onSelectTransaction={setSelectedTransaction}
                    selectedTxId={selectedTransaction?.id}
                  />
                </div>

                <div className="lg:col-span-4 h-[520px] overflow-y-auto">
                  <ActiveAlertsPanel
                    transactions={transactions}
                    onSelectTransaction={setSelectedTransaction}
                  />
                </div>
              </div>
            </div>
          )}

          {activeTab === 'transactions' && (
            <div className="h-[calc(100vh-100px)] max-w-[1600px] mx-auto">
              <LiveTransactionFeed
                transactions={transactions}
                isPaused={isPaused}
                pausedBufferCount={pausedBufferCount}
                onTogglePause={togglePause}
                searchQuery={searchQuery}
                onSearchChange={setSearchQuery}
                minRiskFilter={minRiskFilter}
                onMinRiskChange={setMinRiskFilter}
                selectedRiskTier={selectedRiskTier}
                onSelectRiskTier={setSelectedRiskTier}
                onSelectTransaction={setSelectedTransaction}
                selectedTxId={selectedTransaction?.id}
              />
            </div>
          )}

          {activeTab === 'alerts' && (
            <div className="max-w-[1400px] mx-auto space-y-4">
              <div className="surface-card p-3.5 rounded-lg">
                <h2 className="text-sm font-semibold font-mono text-white uppercase tracking-tight">Priority Fraud Investigation Alerts</h2>
                <p className="text-[11px] font-mono text-slate-400 mt-0.5">Transactions with Critical/High risk scores requiring immediate operational verdict.</p>
              </div>
              <ActiveAlertsPanel
                transactions={transactions}
                onSelectTransaction={setSelectedTransaction}
              />
            </div>
          )}

          {activeTab === 'accounts' && (
            <div className="max-w-[1600px] mx-auto">
              <AccountsView />
            </div>
          )}

          {activeTab === 'network' && (
            <div className="max-w-[1600px] mx-auto">
              <NetworkIntelligenceView />
            </div>
          )}

          {activeTab === 'simulator' && (
            <div className="max-w-[1600px] mx-auto">
              <SimulatorControlDeck
                onScenarioTriggered={(scenario, results) => {
                  console.log(`Triggered ${scenario}:`, results);
                }}
              />
            </div>
          )}
        </main>
      </div>

      {/* Slide-Out Forensic Investigation Drawer */}
      <InvestigationDrawer
        transaction={selectedTransaction}
        onClose={() => setSelectedTransaction(null)}
        onActionComplete={(txId, action) => {
          console.log(`Action ${action} taken on ${txId}`);
        }}
        onInspectEvolution={(accId) => {
          setEvolutionAccountId(accId);
          setActiveTab('evolution');
        }}
      />
    </div>
  );
}

export default App;
