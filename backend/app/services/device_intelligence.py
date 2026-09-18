from typing import List, Set
from app.models.device import Device
from app.schemas.risk import SignalEvidence

class DeviceIntelligenceEngine:
    """Evaluates device identity, historical linkage, and cross-account device sharing."""

    @staticmethod
    def evaluate(
        device_id: str,
        known_account_device_ids: Set[str],
        total_accounts_linked_to_device: int,
        device_record: Device | None = None
    ) -> List[SignalEvidence]:
        signals: List[SignalEvidence] = []

        is_new_device = device_id not in known_account_device_ids

        # 1. New Unrecognized Device
        if is_new_device:
            signals.append(SignalEvidence(
                code="NEW_DEVICE_DETECTED",
                name="Unrecognized Device Fingerprint",
                category="DEVICE",
                points=20.0,
                observed_value=device_id[:16] + "...",
                baseline_value=f"{len(known_account_device_ids)} registered devices",
                severity="WARNING",
                description="Transaction originated from a hardware fingerprint never previously authenticated on this account."
            ))

        # 2. Suspicious Device Reuse Across Multiple Accounts (Credential Stuffing / Mule Farm)
        if total_accounts_linked_to_device >= 3:
            signals.append(SignalEvidence(
                code="SUSPICIOUS_DEVICE_REUSE",
                name="Syndicate Device Reuse",
                category="DEVICE",
                points=40.0,
                observed_value=f"{total_accounts_linked_to_device} distinct accounts",
                baseline_value="1 account per device",
                severity="CRITICAL",
                description=f"This hardware fingerprint has been utilized across {total_accounts_linked_to_device} distinct accounts, indicating an emulator farm or money mule syndicate."
            ))

        # 3. Known Anonymous Proxy / Tor / VPN
        if device_record and device_record.is_known_proxy:
            signals.append(SignalEvidence(
                code="PROXY_OR_VPN_DETECTED",
                name="Anonymizing Proxy / Tor Exit",
                category="DEVICE",
                points=25.0,
                observed_value="Proxy/VPN Detected",
                baseline_value="Direct ISP connection",
                severity="WARNING",
                description="Connection routed through known commercial VPN or anonymizing proxy network."
            ))

        return signals

device_intelligence = DeviceIntelligenceEngine()
