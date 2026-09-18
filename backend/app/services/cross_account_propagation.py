from typing import List, Set
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_

from app.models.device import AccountDevice, Device
from app.models.account import Account
from app.models.transaction import Transaction
from app.schemas.investigation import CrossAccountPropagation, NetworkLink

class CrossAccountPropagationEngine:
    """
    Innovation 3: Cross-Account Context Propagation
    Propagates and grades entity relationships across shared hardware, counterparties, and merchants.
    """

    @staticmethod
    async def analyze(account_id: str, db: AsyncSession) -> CrossAccountPropagation:
        # 1. Fetch all devices associated with this account
        dev_stmt = select(AccountDevice.device_id).where(AccountDevice.account_id == account_id)
        dev_res = await db.execute(dev_stmt)
        device_ids: List[str] = list(dev_res.scalars().all())

        network_links: List[NetworkLink] = []
        correlated_accounts: Set[str] = set()
        shared_devices: List[str] = []
        max_link_severity = 0

        # Grade weighting
        GRADE_WEIGHTS = {
            "NORMAL": 0,
            "SUSPICIOUS_CONNECTION": 1,
            "HIGH_RISK_CLUSTER": 2,
            "POTENTIAL_COORDINATED_ACTIVITY": 3
        }

        # 2. For each device, find other linked accounts
        for dev_id in device_ids:
            other_accs_stmt = select(
                AccountDevice.account_id,
                Account.holder_name,
                Account.risk_rating
            ).join(
                Account, Account.id == AccountDevice.account_id
            ).where(
                AccountDevice.device_id == dev_id,
                AccountDevice.account_id != account_id
            )
            other_accs_res = await db.execute(other_accs_stmt)
            other_accs = other_accs_res.all()

            if other_accs:
                shared_devices.append(dev_id)

            for other_id, other_name, other_risk in other_accs:
                correlated_accounts.add(other_id)
                
                # Determine grade
                if other_risk in ["CRITICAL", "HIGH"] or len(other_accs) >= 2:
                    link_grade = "POTENTIAL_COORDINATED_ACTIVITY"
                    explanation = f"Hardware fingerprint '{dev_id[:14]}...' is actively shared with high-risk account {other_id} ({other_name}). Indicative of syndicate mule operation."
                elif other_risk == "MEDIUM":
                    link_grade = "HIGH_RISK_CLUSTER"
                    explanation = f"Shared hardware linkage with elevated-risk account {other_id} ({other_name})."
                else:
                    link_grade = "SUSPICIOUS_CONNECTION"
                    explanation = f"Hardware fingerprint shared across distinct account entities ({other_id})."

                weight = GRADE_WEIGHTS.get(link_grade, 0)
                if weight > max_link_severity:
                    max_link_severity = weight

                network_links.append(NetworkLink(
                    connected_account_id=other_id,
                    relationship_type="Shared Hardware Fingerprint",
                    shared_entity=dev_id,
                    link_grade=link_grade,
                    explanation=explanation
                ))

        # 3. Check direct P2P transaction counterparties
        p2p_stmt = select(Transaction).where(
            or_(
                Transaction.account_id == account_id,
                Transaction.target_account_id == account_id
            )
        ).where(Transaction.target_account_id.isnot(None)).limit(15)
        p2p_res = await db.execute(p2p_stmt)
        p2p_txs = p2p_res.scalars().all()

        for p_tx in p2p_txs:
            peer_id = p_tx.target_account_id if p_tx.account_id == account_id else p_tx.account_id
            if peer_id and peer_id != account_id and peer_id not in correlated_accounts:
                correlated_accounts.add(peer_id)
                grade = "HIGH_RISK_CLUSTER" if p_tx.risk_level in ["HIGH", "CRITICAL"] else "NORMAL"
                network_links.append(NetworkLink(
                    connected_account_id=peer_id,
                    relationship_type="Direct Fund Flow Counterparty",
                    shared_entity=f"TXN-{p_tx.id}",
                    link_grade=grade,
                    explanation=f"Direct counterparty transfer of ₹{p_tx.amount:,.2f} recorded on {p_tx.timestamp.strftime('%Y-%m-%d %H:%M')}."
                ))

        # Classify overall cluster
        if max_link_severity >= 3 or len(correlated_accounts) >= 3:
            cluster_classification = "POTENTIAL_COORDINATED_ACTIVITY"
            exposure_score = min(100.0, 70.0 + len(correlated_accounts) * 10.0)
        elif max_link_severity == 2 or len(correlated_accounts) >= 2:
            cluster_classification = "HIGH_RISK_CLUSTER"
            exposure_score = 65.0
        elif len(correlated_accounts) == 1:
            cluster_classification = "SUSPICIOUS_CONNECTION"
            exposure_score = 40.0
        else:
            cluster_classification = "NORMAL"
            exposure_score = 10.0

        return CrossAccountPropagation(
            account_id=account_id,
            network_exposure_score=exposure_score,
            cluster_classification=cluster_classification,
            correlated_accounts_count=len(correlated_accounts),
            shared_devices=shared_devices,
            network_links=network_links
        )

cross_account_propagation_engine = CrossAccountPropagationEngine()
