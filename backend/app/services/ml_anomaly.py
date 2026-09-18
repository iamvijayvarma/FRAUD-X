import numpy as np
from sklearn.ensemble import IsolationForest
from typing import List, Tuple
from app.schemas.risk import SignalEvidence

class MLAnomalyEngine:
    """Lightweight Unsupervised Machine Learning Anomaly Detection using Isolation Forest."""

    def __init__(self):
        self.model = IsolationForest(
            n_estimators=100,
            contamination=0.08,
            random_state=42
        )
        self._fit_initial_baseline()

    def _fit_initial_baseline(self):
        """Fits the model on synthetic standard transaction distributions."""
        np.random.seed(42)
        n_samples = 1500
        
        # Features: [amount, z_score, vel_1m, vel_5m, speed_kmh, dev_share_count, hour]
        amounts = np.random.exponential(scale=75.0, size=n_samples) + 10.0
        z_scores = np.random.normal(loc=0.0, scale=1.0, size=n_samples)
        vel_1m = np.random.poisson(lam=0.2, size=n_samples)
        vel_5m = np.random.poisson(lam=0.8, size=n_samples)
        speeds = np.random.exponential(scale=25.0, size=n_samples) # normal ground travel
        dev_shares = np.random.choice([1, 1, 1, 1, 2], size=n_samples)
        hours = np.random.choice(np.arange(6, 23), size=n_samples)

        X_train = np.column_stack([amounts, z_scores, vel_1m, vel_5m, speeds, dev_shares, hours])
        self.model.fit(X_train)

    def score_transaction(
        self,
        amount: float,
        z_score: float,
        vel_1m: int,
        vel_5m: int,
        speed_kmh: float,
        dev_share_count: int,
        hour: int
    ) -> Tuple[float, List[SignalEvidence]]:
        """
        Returns normalized anomaly score (0.0 to 100.0) and any ML-specific signals.
        """
        features = np.array([[
            amount,
            z_score,
            vel_1m,
            vel_5m,
            max(0.0, speed_kmh),
            dev_share_count,
            hour
        ]])

        # decision_function returns negative values for anomalies, positive for normal
        raw_score = float(self.model.decision_function(features)[0])
        
        # Normalize: raw_score typically ranges from -0.35 (severe anomaly) to +0.25 (very normal)
        # We invert so higher = more anomalous
        normalized_score = float(np.clip(50.0 - (raw_score * 120.0), 0.0, 100.0))

        signals: List[SignalEvidence] = []
        if normalized_score >= 70.0:
            signals.append(SignalEvidence(
                code="UNSUPERVISED_ML_OUTLIER",
                name="Multi-Vector Anomaly (Isolation Forest)",
                category="ML",
                points=25.0,
                observed_value=f"ML Anomaly Index: {normalized_score:.1f}/100",
                baseline_value="Standard Distribution (< 50.0)",
                severity="WARNING",
                description=f"Isolation Forest identified non-linear multidimensional divergence across velocity, geo-velocity, and spending vectors."
            ))

        return round(normalized_score, 1), signals

ml_engine = MLAnomalyEngine()
