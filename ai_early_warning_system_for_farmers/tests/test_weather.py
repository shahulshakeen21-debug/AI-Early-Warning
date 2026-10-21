import pytest
import weather


def test_validate_coordinates():
    """Verify coordinate bounds validation."""
    # Valid coordinates
    ok, err = weather.validate_coordinates(11.0055, 76.9661)
    assert ok is True
    assert err is None

    # Invalid latitude
    ok, err = weather.validate_coordinates(95.0, 76.9661)
    assert ok is False
    assert "Latitude" in err

    # Invalid longitude
    ok, err = weather.validate_coordinates(11.0, 195.0)
    assert ok is False
    assert "Longitude" in err

    # Non-numeric
    ok, err = weather.validate_coordinates("abc", 76.0)
    assert ok is False


def test_generate_agricultural_weather_alerts_fungal_and_spray():
    """Verify rule-based alert triggering using a realistic forecast fixture."""
    forecast_fixture = {
        "daily": {
            "time": ["2026-10-22", "2026-10-23"],
            "temperature_2m_max": [31.5, 30.0],
            "precipitation_sum": [12.0, 0.0],
            "precipitation_probability_max": [85.0, 10.0]
        },
        "hourly": {
            "time": [
                "2026-10-22T06:00", "2026-10-22T12:00",
                "2026-10-23T06:00", "2026-10-23T12:00"
            ],
            "relative_humidity_2m": [88.0, 82.0, 60.0, 55.0]
        }
    }

    alerts = weather.generate_agricultural_weather_alerts(forecast_fixture)
    rule_ids = [a["rule_id"] for a in alerts]

    # Day 1 has high humidity (88%) and high rain (12mm, 85%) -> triggers fungal & spray safety
    assert "fungal_disease_risk" in rule_ids
    assert "spray_safety_risk" in rule_ids

    # Day 2 has moderate weather -> no false alerts
    day2_alerts = [a for a in alerts if a["date"] == "2026-10-23"]
    assert len(day2_alerts) == 0


def test_generate_agricultural_weather_alerts_heat_stress():
    """Verify heat stress alert triggers when forecast temperature exceeds 36°C."""
    forecast_fixture = {
        "daily": {
            "time": ["2026-10-24"],
            "temperature_2m_max": [38.5],
            "precipitation_sum": [0.0],
            "precipitation_probability_max": [5.0]
        },
        "hourly": {
            "time": ["2026-10-24T12:00"],
            "relative_humidity_2m": [45.0]
        }
    }

    alerts = weather.generate_agricultural_weather_alerts(forecast_fixture)
    assert len(alerts) == 1
    assert alerts[0]["rule_id"] == "heat_stress_risk"
    assert alerts[0]["metrics"]["max_temperature"] == 38.5


def test_no_alerts_when_conditions_mild():
    """Verify no spurious alerts are generated during calm, optimal weather."""
    forecast_fixture = {
        "daily": {
            "time": ["2026-10-25"],
            "temperature_2m_max": [28.0],
            "precipitation_sum": [0.0],
            "precipitation_probability_max": [10.0]
        },
        "hourly": {
            "time": ["2026-10-25T08:00"],
            "relative_humidity_2m": [65.0]
        }
    }

    alerts = weather.generate_agricultural_weather_alerts(forecast_fixture)
    assert len(alerts) == 0


def test_missing_weather_variables_do_not_fabricate_data():
    """Verify that when hourly humidity is missing, fungal alert does not fabricate zero or true."""
    forecast_fixture = {
        "daily": {
            "time": ["2026-10-26"],
            "temperature_2m_max": [30.0],
            "precipitation_sum": [2.0],
            "precipitation_probability_max": [30.0]
        },
        "hourly": {
            "time": [],
            "relative_humidity_2m": []
        }
    }

    alerts = weather.generate_agricultural_weather_alerts(forecast_fixture)
    # Without humidity data, fungal alert cannot be reliably evaluated and must be omitted
    assert "fungal_disease_risk" not in [a["rule_id"] for a in alerts]
