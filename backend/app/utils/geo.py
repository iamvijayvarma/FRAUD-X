import math
from typing import Tuple, Dict

EARTH_RADIUS_KM = 6371.0

# Indian Financial Hubs & Major Cities: (lat, lon, state_and_country)
KNOWN_CITIES: Dict[str, Tuple[float, float, str]] = {
    "Chennai": (13.0827, 80.2707, "Tamil Nadu, India"),
    "Coimbatore": (11.0168, 76.9558, "Tamil Nadu, India"),
    "Bengaluru": (12.9716, 77.5946, "Karnataka, India"),
    "Hyderabad": (17.3850, 78.4867, "Telangana, India"),
    "Mumbai": (19.0760, 72.8777, "Maharashtra, India"),
    "Pune": (18.5204, 73.8567, "Maharashtra, India"),
    "New Delhi": (28.6139, 77.2090, "Delhi, India"),
    "Kolkata": (22.5726, 88.3639, "West Bengal, India"),
    "Ahmedabad": (23.0225, 72.5714, "Gujarat, India"),
    "Kochi": (9.9312, 76.2673, "Kerala, India"),
    "Madurai": (9.9252, 78.1198, "Tamil Nadu, India"),
    "Tiruchirappalli": (10.7905, 78.7047, "Tamil Nadu, India")
}

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the Great-Circle distance between two points on Earth
    in kilometers using the Haversine formula.
    """
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat / 2.0)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2.0)**2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

    return EARTH_RADIUS_KM * c

def calculate_speed_kmh(distance_km: float, time_diff_seconds: float) -> float:
    """
    Calculates speed in km/h given distance in km and elapsed time in seconds.
    Caps minimum time window at 1 second to prevent division by zero.
    """
    effective_seconds = max(1.0, time_diff_seconds)
    hours = effective_seconds / 3600.0
    return distance_km / hours
