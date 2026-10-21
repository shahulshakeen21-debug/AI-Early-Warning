import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import requests

logger = logging.getLogger(__name__)

# Official Open-Meteo Endpoints
GEOCODING_API_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_API_URL = "https://api.open-meteo.com/v1/forecast"
REQUEST_TIMEOUT = 10  # Seconds

# Configurable preliminary agricultural advisory thresholds
# Note: These are documented decision-support thresholds, not validated epidemiology models.
DEFAULT_ALERT_THRESHOLDS = {
    "fungal_humidity_pct": 80.0,      # Relative humidity threshold (%)
    "fungal_rain_prob_pct": 50.0,     # Rain probability threshold (%)
    "fungal_rain_sum_mm": 5.0,        # Daily rainfall threshold (mm)
    "spray_rain_prob_pct": 60.0,      # Probability threshold where spray may be washed off
    "spray_rain_sum_mm": 5.0,         # Rainfall threshold (mm)
    "heat_stress_temp_c": 36.0        # High temperature threshold (°C)
}


class WeatherServiceError(Exception):
    """Custom exception raised when Open-Meteo geocoding or forecast fails."""
    pass


def validate_coordinates(latitude: float, longitude: float) -> Tuple[bool, Optional[str]]:
    """
    Validate that latitude is between -90 and 90, and longitude is between -180 and 180.
    """
    try:
        lat = float(latitude)
        lon = float(longitude)
    except (ValueError, TypeError):
        return False, "Coordinates must be numerical values."

    if not (-90.0 <= lat <= 90.0):
        return False, f"Latitude {lat} is outside the valid range [-90, 90]."
    if not (-180.0 <= lon <= 180.0):
        return False, f"Longitude {lon} is outside the valid range [-180, 180]."

    return True, None


def geocode_place_name(place_name: str, timeout: int = REQUEST_TIMEOUT) -> Dict[str, Any]:
    """
    Resolve a place name into latitude and longitude using Open-Meteo Geocoding API.
    Does NOT silently substitute a default location upon failure.
    """
    if not place_name or not place_name.strip():
        raise WeatherServiceError("Place name cannot be empty.")

    params = {
        "name": place_name.strip(),
        "count": 5,
        "language": "en",
        "format": "json"
    }

    try:
        response = requests.get(GEOCODING_API_URL, params=params, timeout=timeout)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout:
        logger.error(f"Geocoding request timed out for place: {place_name}")
        raise WeatherServiceError("Connection to Open-Meteo Geocoding API timed out. Please check your internet connection.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Geocoding network error: {e}")
        raise WeatherServiceError(f"Network error while searching location: {e}")
    except ValueError as e:
        logger.error(f"Invalid JSON returned from geocoding API: {e}")
        raise WeatherServiceError("Received an invalid response format from Open-Meteo Geocoding API.")

    results = data.get("results")
    if not results or len(results) == 0:
        raise WeatherServiceError(f"Could not find any location matching '{place_name}'.")

    # Select best match
    best = results[0]
    resolved_info = {
        "name": best.get("name", place_name),
        "latitude": float(best.get("latitude")),
        "longitude": float(best.get("longitude")),
        "country": best.get("country", ""),
        "admin1": best.get("admin1", ""),  # State / Province (e.g., Tamil Nadu)
        "elevation": best.get("elevation", 0)
    }

    return resolved_info


def fetch_weather_forecast(
    latitude: float,
    longitude: float,
    timeout: int = REQUEST_TIMEOUT
) -> Dict[str, Any]:
    """
    Fetch genuine 5-day weather forecast from Open-Meteo public API.
    Operates strictly on actual API responses; never returns fabricated data.
    """
    is_valid, err_msg = validate_coordinates(latitude, longitude)
    if not is_valid:
        raise WeatherServiceError(err_msg)

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "precipitation_probability_max"
        ],
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation"
        ],
        "timezone": "auto",
        "forecast_days": 5
    }

    try:
        response = requests.get(FORECAST_API_URL, params=params, timeout=timeout)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout:
        logger.error(f"Forecast request timed out for ({latitude}, {longitude})")
        raise WeatherServiceError("Connection to Open-Meteo Forecast API timed out. Please retry.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Forecast network error: {e}")
        raise WeatherServiceError(f"Network error while fetching weather forecast: {e}")
    except ValueError as e:
        logger.error(f"Invalid JSON returned from forecast API: {e}")
        raise WeatherServiceError("Received an invalid response format from Open-Meteo Forecast API.")

    # Validate essential top-level fields
    if "daily" not in data or "daily_units" not in data:
        raise WeatherServiceError("Forecast response missing required daily weather fields.")

    retrieval_iso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    parsed_data = {
        "source": "Open-Meteo Weather Forecast API (Live Model Data)",
        "retrieved_at": retrieval_iso,
        "latitude": data.get("latitude", latitude),
        "longitude": data.get("longitude", longitude),
        "timezone": data.get("timezone", "UTC"),
        "timezone_abbreviation": data.get("timezone_abbreviation", ""),
        "elevation": data.get("elevation", 0),
        "daily_units": data.get("daily_units", {}),
        "daily": data.get("daily", {}),
        "hourly_units": data.get("hourly_units", {}),
        "hourly": data.get("hourly", {})
    }

    return parsed_data


def generate_agricultural_weather_alerts(
    forecast_data: Dict[str, Any],
    thresholds: Optional[Dict[str, float]] = None
) -> List[Dict[str, Any]]:
    """
    Generate agricultural weather-risk alerts from genuine forecast data.
    Implements transparent documented rules:
    1. High humidity combined with rainfall or high rain probability -> fungal disease risk
    2. Heavy rainfall or high rain probability -> pesticide spraying wash-off risk
    3. Extreme high temperature -> crop heat stress alert

    Rules operate ONLY on available actual data. Does not invent zero or missing readings.
    """
    if not forecast_data or "daily" not in forecast_data:
        return []

    th = thresholds or DEFAULT_ALERT_THRESHOLDS
    alerts: List[Dict[str, Any]] = []

    daily = forecast_data.get("daily", {})
    hourly = forecast_data.get("hourly", {})

    dates = daily.get("time", [])
    max_temps = daily.get("temperature_2m_max", [])
    rain_sums = daily.get("precipitation_sum", [])
    rain_probs = daily.get("precipitation_probability_max", [])

    hourly_humidities = hourly.get("relative_humidity_2m", [])
    hourly_times = hourly.get("time", [])

    # Calculate average or peak daily humidity from hourly readings if available
    daily_peak_humidity: Dict[str, float] = {}
    if hourly_times and hourly_humidities and len(hourly_times) == len(hourly_humidities):
        for t_str, h_val in zip(hourly_times, hourly_humidities):
            if h_val is not None:
                day_key = t_str.split("T")[0]
                daily_peak_humidity[day_key] = max(daily_peak_humidity.get(day_key, 0.0), float(h_val))

    for i, date_str in enumerate(dates):
        t_max = max_temps[i] if i < len(max_temps) else None
        r_sum = rain_sums[i] if i < len(rain_sums) else None
        r_prob = rain_probs[i] if i < len(rain_probs) else None
        peak_hum = daily_peak_humidity.get(date_str)

        # Rule 1: Fungal Disease Warning
        # Requires high peak humidity AND (significant rainfall OR high rain probability)
        if peak_hum is not None and peak_hum >= th["fungal_humidity_pct"]:
            rain_trigger = (r_sum is not None and r_sum >= th["fungal_rain_sum_mm"]) or \
                           (r_prob is not None and r_prob >= th["fungal_rain_prob_pct"])
            if rain_trigger:
                alerts.append({
                    "rule_id": "fungal_disease_risk",
                    "title_key": "alert_fungal_risk_title",
                    "severity": "warning",
                    "date": date_str,
                    "metrics": {
                        "peak_humidity": peak_hum,
                        "precipitation_sum": r_sum,
                        "rain_probability": r_prob
                    },
                    "description": {
                        "en": f"High humidity ({peak_hum:.1f}%) combined with forecast precipitation ({r_sum if r_sum is not None else 'N/A'} mm, {r_prob if r_prob is not None else 'N/A'}% chance) creates conditions favourable for fungal sporulation (such as Blight, Blast, and Tikka). Inspect leaves regularly for water-soaked lesions.",
                        "ta": f"அதிக ஈரப்பதம் ({peak_hum:.1f}%) மற்றும் மழை வாய்ப்பு பூஞ்சை நோய் பரவலுக்கு உகந்த சூழலை உருவாக்குகிறது. இலைகளில் கருகல் மற்றும் புள்ளிகள் ஏற்படுகிறதா என கவனிக்கவும்."
                    },
                    "action_advice": {
                        "en": "Avoid overhead watering, maintain crop aeration, and keep drainage channels clear.",
                        "ta": "இலைகளில் நீர் தேங்குவதைத் தவிர்க்கவும், வடிகால் வசதியைச் சீரமைக்கவும்."
                    }
                })

        # Rule 2: Pesticide Spray Advisory
        # Rain may wash off spray deposits or make chemical handling unsafe
        if (r_sum is not None and r_sum >= th["spray_rain_sum_mm"]) or \
           (r_prob is not None and r_prob >= th["spray_rain_prob_pct"]):
            alerts.append({
                "rule_id": "spray_safety_risk",
                "title_key": "alert_spray_safety_title",
                "severity": "caution",
                "date": date_str,
                "metrics": {
                    "precipitation_sum": r_sum,
                    "rain_probability": r_prob
                },
                "description": {
                    "en": f"Forecast rainfall ({r_sum if r_sum is not None else 'N/A'} mm, {r_prob if r_prob is not None else 'N/A'}% rain probability) may wash off pesticide/fungicide sprays and reduce chemical efficacy.",
                    "ta": f"எதிர்பார்க்கப்படும் மழை ({r_sum if r_sum is not None else 'N/A'} மி.மீ, {r_prob if r_prob is not None else 'N/A'}%) தெளிக்கப்பட்ட பூச்சிக்கொல்லிகளை அடித்துச் செல்லக்கூடும்."
                },
                "action_advice": {
                    "en": "Postpone non-urgent foliar spraying until dry weather resumes. Check product label rainfastness guidelines.",
                    "ta": "மழை நிற்கும் வரை தெளிப்பதைத் தள்ளிவைக்கவும். உழவர் அலுவலர் வழிகாட்டுதலைப் பின்பற்றவும்."
                }
            })

        # Rule 3: Heat Stress Alert
        if t_max is not None and t_max >= th["heat_stress_temp_c"]:
            alerts.append({
                "rule_id": "heat_stress_risk",
                "title_key": "alert_heat_stress_title",
                "severity": "warning",
                "date": date_str,
                "metrics": {
                    "max_temperature": t_max
                },
                "description": {
                    "en": f"Maximum temperature forecast is {t_max:.1f}°C. Extreme temperatures can cause flower drop, leaf scorch, and wilting in sensitive crops.",
                    "ta": f"அதிகபட்ச வெப்பநிலை {t_max:.1f}°C ஆக எதிர்பார்க்கப்படுகிறது. இது பயிர்களில் பூ உதிர்தல் மற்றும் வாடலை ஏற்படுத்தக்கூடும்."
                },
                "action_advice": {
                    "en": "Provide light irrigation during early mornings or evenings. Apply mulching to retain root-zone soil moisture.",
                    "ta": "காலை அல்லது மாலை வேளையில் மிதமான பாசனம் அளிக்கவும். மண்ணில் ஈரப்பதம் காக்க மூடாக்கு இடவும்."
                }
            })

    return alerts
