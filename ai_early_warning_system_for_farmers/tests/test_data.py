import json
from pathlib import Path
import pytest
import scan_history
import utils

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def test_i18n_json_validity_and_completeness():
    """Verify that i18n.json exists, is valid UTF-8, and has non-empty en and ta strings."""
    i18n_path = DATA_DIR / "i18n.json"
    assert i18n_path.exists(), "i18n.json must exist"

    data = utils.load_json_file(i18n_path)
    assert isinstance(data, dict), "i18n.json must contain a dictionary of keys"
    assert len(data) >= 25, "i18n.json must contain comprehensive UI keys"

    required_keys = [
        "app_title", "nav_home", "nav_check_crop", "nav_weather_alerts",
        "nav_advice", "nav_schemes", "nav_identify_plant", "nav_plant_care",
        "nav_pests_symptoms", "low_confidence_message",
        "field_photo_limitation", "model_missing_title"
    ]

    for key in required_keys:
        assert key in data, f"Missing critical translation key: {key}"
        entry = data[key]
        assert "en" in entry and len(entry["en"].strip()) > 0, f"English text missing for {key}"
        assert "ta" in entry and len(entry["ta"].strip()) > 0, f"Tamil text missing for {key}"


def test_plants_json_structure():
    """Verify that plants.json contains structured entries with required botanical and care fields."""
    p_path = DATA_DIR / "plants.json"
    assert p_path.exists(), "plants.json must exist"

    plants = utils.load_json_file(p_path)
    assert isinstance(plants, dict), "plants.json must be a dict"
    assert len(plants) >= 7, "Must contain profiles across multiple plant categories"

    required_fields = [
        "plant_id", "common_name", "scientific_name", "family", "category",
        "description", "identifying_characteristics", "growing_conditions",
        "common_pests", "prevention_care", "safety_notes", "support_status",
        "verification_status"
    ]

    for p_id, entry in plants.items():
        assert entry["plant_id"] == p_id
        for field in required_fields:
            assert field in entry, f"Field '{field}' missing in plant '{p_id}'"


def test_species_registry_structure():
    """Verify species_registry.json separates plant identification and disease model classes."""
    reg_path = DATA_DIR / "species_registry.json"
    assert reg_path.exists(), "species_registry.json must exist"

    registry = utils.load_json_file(reg_path)
    assert "supported_species" in registry
    species = registry["supported_species"]

    # Verify Tomato has disease model mapping
    assert "tomato" in species
    assert "Tomato___Bacterial_spot" in species["tomato"]["disease_model_classes"]

    # Verify Paddy specifies dataset requirement honestly
    assert "paddy" in species
    assert species["paddy"]["disease_training_status"] == "awaiting_dataset"


def test_symptoms_json_structure():
    """Verify symptoms.json contains valid visual diagnostic guidance."""
    symp_path = DATA_DIR / "symptoms.json"
    assert symp_path.exists(), "symptoms.json must exist"

    symptoms = utils.load_json_file(symp_path)
    assert len(symptoms) >= 5

    for s_id, s_data in symptoms.items():
        assert "possible_causes" in s_data
        assert "field_action" in s_data
        assert len(s_data["possible_causes"]) > 0


def test_scan_history_and_report_generation():
    """Verify SQLite scan history lifecycle: saving, retrieval, report generation, and deletion."""
    test_uuid = "test_scan_123"
    scan_id = scan_history.save_scan(
        scan_uuid=test_uuid,
        selected_plant="Tomato",
        scan_type="Disease Screening",
        predicted_class="Tomato Early Blight",
        confidence=0.88,
        model_version="MobileNetV2-1.0",
        is_uncertain=False,
        weather_summary="Coimbatore, 28°C"
    )

    saved_scan = scan_history.get_scan_by_uuid(test_uuid)
    assert saved_scan is not None
    assert saved_scan["confidence"] == 0.88
    assert saved_scan["is_uncertain"] == 0

    # Test report text generation
    report = scan_history.generate_scan_report_text(saved_scan)
    assert "AI PLANT DOCTOR - AGRICULTURAL SCAN REPORT" in report
    assert test_uuid in report
    assert "Tomato Early Blight" in report
    assert "88.0%" in report

    # Test deletion
    deleted = scan_history.delete_scan(saved_scan["id"])
    assert deleted is True
    assert scan_history.get_scan_by_uuid(test_uuid) is None
