from typing import List, Tuple, Optional
from datetime import datetime
from app.models.account import Account
from app.models.transaction import Transaction
from app.schemas.risk import SignalEvidence
from app.utils.geo import haversine_distance, calculate_speed_kmh
from app.config import settings

class LocationEngine:
    """Evaluates geographic deviations, impossible travel velocity, and high-risk jurisdictions."""

    @staticmethod
    def evaluate(
        account: Account,
        current_lat: float,
        current_lon: float,
        current_city: str,
        current_time: datetime,
        last_transaction: Optional[Transaction] = None
    ) -> Tuple[List[SignalEvidence], Optional[float], Optional[float]]:
        signals: List[SignalEvidence] = []
        speed_kmh: Optional[float] = None
        dist_from_last_km: Optional[float] = None

        # 1. Sequential Geodesic Velocity / Impossible Travel
        if last_transaction and last_transaction.location_lat and last_transaction.location_lon:
            dist_from_last_km = haversine_distance(
                last_transaction.location_lat,
                last_transaction.location_lon,
                current_lat,
                current_lon
            )
            time_diff_seconds = abs((current_time - last_transaction.timestamp).total_seconds())
            
            # If transactions occurred within 24 hours
            if time_diff_seconds <= 86400 and dist_from_last_km >= settings.MIN_DISTANCE_FOR_TRAVEL_ALERT_KM:
                speed_kmh = calculate_speed_kmh(dist_from_last_km, time_diff_seconds)
                
                # Commercial flight max operational speed threshold is ~800-900 km/h
                if speed_kmh > settings.IMPOSSIBLE_TRAVEL_SPEED_KMH:
                    time_min = max(1, int(time_diff_seconds / 60))
                    signals.append(SignalEvidence(
                        code="IMPOSSIBLE_TRAVEL_VELOCITY",
                        name="Impossible Travel Velocity",
                        category="LOCATION",
                        points=45.0,
                        observed_value=f"{speed_kmh:,.0f} km/h ({dist_from_last_km:,.0f} km in {time_min}m)",
                        baseline_value=f"< {settings.IMPOSSIBLE_TRAVEL_SPEED_KMH:.0f} km/h (Commercial Air)",
                        severity="CRITICAL",
                        description=f"Sequential transactions separated by {dist_from_last_km:,.0f} km within {time_min} minutes require a physical velocity of {speed_kmh:,.0f} km/h, which is physically impossible without credential sharing or session hijacking."
                    ))

        # 2. Deviation from Account Historical Home Location
        if account.typical_location_lat and account.typical_location_lon:
            dist_from_home = haversine_distance(
                account.typical_location_lat,
                account.typical_location_lon,
                current_lat,
                current_lon
            )
            if dist_from_home > 3000.0:
                signals.append(SignalEvidence(
                    code="UNUSUAL_GEOGRAPHIC_LOCATION",
                    name="Extreme Geolocation Deviation",
                    category="LOCATION",
                    points=15.0,
                    observed_value=f"{current_city} ({dist_from_home:,.0f} km from home)",
                    baseline_value=f"{account.typical_city}, {account.typical_country}",
                    severity="WARNING",
                    description=f"Transaction originated from {current_city}, which is {dist_from_home:,.0f} km away from user's primary residence."
                ))

        return signals, speed_kmh, dist_from_last_km

location_engine = LocationEngine()
