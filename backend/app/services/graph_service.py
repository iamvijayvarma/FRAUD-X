import networkx as nx
from typing import List, Dict, Any, Tuple, Optional, Set
from app.schemas.risk import SignalEvidence
from app.schemas.graph import GraphNode, GraphEdge, GraphNetworkResponse
import logging

logger = logging.getLogger("fraud_x.graph")

class GraphIntelligenceService:
    """Maintains a dynamic in-memory graph of accounts, devices, and merchants using NetworkX."""

    def __init__(self):
        self.graph = nx.MultiDiGraph()
        self.transfer_graph = nx.DiGraph() # Directed graph for cycle detection

    def add_account(self, account_id: str, label: str, risk_level: str = "LOW", properties: Dict[str, Any] = None):
        self.graph.add_node(account_id, label=label, type="ACCOUNT", risk_level=risk_level, properties=properties or {})
        self.transfer_graph.add_node(account_id)

    def add_device(self, device_id: str, label: str, properties: Dict[str, Any] = None):
        self.graph.add_node(device_id, label=label, type="DEVICE", risk_level="LOW", properties=properties or {})

    def add_merchant(self, merchant_id: str, label: str, category: str):
        self.graph.add_node(merchant_id, label=label, type="MERCHANT", risk_level="LOW", properties={"category": category})

    def record_device_usage(self, account_id: str, device_id: str, timestamp: str):
        if not self.graph.has_node(device_id):
            self.add_device(device_id, f"Device {device_id[:8]}")
        if not self.graph.has_node(account_id):
            self.add_account(account_id, account_id)
        
        self.graph.add_edge(account_id, device_id, type="USED_DEVICE", timestamp=timestamp)

    def record_transaction(
        self,
        account_id: str,
        target_account_id: Optional[str],
        merchant_name: str,
        amount: float,
        timestamp: str,
        device_id: str,
        risk_level: str
    ):
        # 1. Update Account & Device
        if not self.graph.has_node(account_id):
            self.add_account(account_id, account_id, risk_level=risk_level)
        else:
            self.graph.nodes[account_id]["risk_level"] = risk_level

        self.record_device_usage(account_id, device_id, timestamp)

        # 2. Add Merchant edge if applicable
        if merchant_name:
            merchant_node = f"MCH-{merchant_name.replace(' ', '_').upper()}"
            if not self.graph.has_node(merchant_node):
                self.add_merchant(merchant_node, merchant_name, "GENERAL")
            self.graph.add_edge(account_id, merchant_node, type="TRANSACTED_AT", amount=amount, timestamp=timestamp)

        # 3. Add Transfer edge if P2P
        if target_account_id:
            if not self.graph.has_node(target_account_id):
                self.add_account(target_account_id, target_account_id)
            self.graph.add_edge(account_id, target_account_id, type="TRANSFERRED_TO", amount=amount, timestamp=timestamp)
            self.transfer_graph.add_edge(account_id, target_account_id, amount=amount)

    def detect_circular_layering(self, account_id: str) -> Tuple[bool, List[List[str]]]:
        """Detects if account participates in a closed circular money routing cycle (A -> B -> C -> A)."""
        if not self.transfer_graph.has_node(account_id):
            return False, []
        
        try:
            # Look for simple cycles
            cycles = list(nx.simple_cycles(self.transfer_graph))
            relevant_cycles = [c for c in cycles if account_id in c and 2 <= len(c) <= 6]
            return len(relevant_cycles) > 0, relevant_cycles
        except Exception as e:
            logger.warning(f"Cycle detection error: {e}")
            return False, []

    def get_accounts_sharing_device(self, device_id: str) -> Set[str]:
        """Returns set of all account nodes connected to this device."""
        if not self.graph.has_node(device_id):
            return set()
        
        accounts = set()
        for u, v, data in self.graph.in_edges(device_id, data=True):
            if data.get("type") == "USED_DEVICE":
                accounts.add(u)
        return accounts

    def evaluate(
        self,
        account_id: str,
        target_account_id: Optional[str],
        device_id: str
    ) -> Tuple[List[SignalEvidence], bool, int]:
        signals: List[SignalEvidence] = []
        is_circular = False

        # 1. Device Sharing across Accounts
        accounts_sharing = self.get_accounts_sharing_device(device_id)
        accounts_sharing.add(account_id)
        share_count = len(accounts_sharing)

        # 2. Circular Fund Routing Loop Detection
        if target_account_id:
            # Temporarily test if adding this edge closes a cycle
            temp_graph = self.transfer_graph.copy()
            temp_graph.add_edge(account_id, target_account_id)
            try:
                cycles = list(nx.simple_cycles(temp_graph))
                relevant = [c for c in cycles if account_id in c]
                if relevant:
                    is_circular = True
                    cycle_str = " → ".join(relevant[0] + [relevant[0][0]])
                    signals.append(SignalEvidence(
                        code="CIRCULAR_TRANSFER_RING",
                        name="Circular Money Laundering Cycle",
                        category="GRAPH",
                        points=35.0,
                        observed_value=f"Cycle: {cycle_str}",
                        baseline_value="Acyclic transaction DAG",
                        severity="CRITICAL",
                        description=f"Transaction creates or completes a closed circular transfer ring ({cycle_str}) characteristic of layered money laundering."
                    ))
            except Exception:
                pass

        return signals, is_circular, share_count

    def export_subgraph(self, center_id: Optional[str] = None, max_nodes: int = 40) -> GraphNetworkResponse:
        """Exports subgraph formatted for the React force-directed visualizer."""
        if not self.graph.nodes:
            return GraphNetworkResponse(nodes=[], edges=[])

        selected_nodes: Set[str] = set()

        if center_id and self.graph.has_node(center_id):
            selected_nodes.add(center_id)
            # 1-hop and 2-hop neighbors
            for neighbor in self.graph.neighbors(center_id):
                selected_nodes.add(neighbor)
                if len(selected_nodes) >= max_nodes:
                    break
        else:
            # Export most connected nodes
            degrees = sorted(self.graph.degree, key=lambda x: x[1], reverse=True)
            for node, deg in degrees[:max_nodes]:
                selected_nodes.add(node)

        # Build response nodes
        nodes_out: List[GraphNode] = []
        for n in selected_nodes:
            attrs = self.graph.nodes[n]
            deg = self.graph.degree(n)
            nodes_out.append(GraphNode(
                id=n,
                label=attrs.get("label", n),
                type=attrs.get("type", "ACCOUNT"),
                risk_level=attrs.get("risk_level", "LOW"),
                degree=deg,
                properties=attrs.get("properties", {})
            ))

        # Build response edges
        edges_out: List[GraphEdge] = []
        for u, v, data in self.graph.edges(data=True):
            if u in selected_nodes and v in selected_nodes:
                edges_out.append(GraphEdge(
                    source=u,
                    target=v,
                    type=data.get("type", "TRANSACTED_AT"),
                    amount=data.get("amount"),
                    timestamp=str(data.get("timestamp", "")),
                    is_circular=False
                ))

        # Check for any cycles in entire graph
        try:
            cycles = list(nx.simple_cycles(self.transfer_graph))
            cycles_detected = [c for c in cycles if len(c) <= 6][:5]
        except Exception:
            cycles_detected = []

        return GraphNetworkResponse(
            nodes=nodes_out,
            edges=edges_out,
            cycles_detected=cycles_detected,
            suspicious_clusters_count=len(cycles_detected)
        )

graph_service = GraphIntelligenceService()
