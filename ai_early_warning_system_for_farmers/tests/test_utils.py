import io
import numpy as np
from PIL import Image
import pytest
import utils


def test_validate_image_valid_rgb():
    """Verify that a valid PNG/JPEG image parses correctly."""
    img = Image.new("RGB", (224, 224), color=(34, 139, 34))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    img_bytes = buf.getvalue()

    is_valid, err_key, pil_img = utils.validate_image_file(img_bytes)
    assert is_valid is True
    assert err_key is None
    assert pil_img is not None
    assert pil_img.size == (224, 224)


def test_validate_image_empty():
    """Verify that empty uploads are caught with appropriate error key."""
    is_valid, err_key, pil_img = utils.validate_image_file(b"")
    assert is_valid is False
    assert err_key == "err_empty_upload"
    assert pil_img is None


def test_validate_image_corrupted():
    """Verify that corrupt bytes are safely handled without unhandled exceptions."""
    corrupt_bytes = b"This is not a real image header data \x00\xff\xfe"
    is_valid, err_key, pil_img = utils.validate_image_file(corrupt_bytes)
    assert is_valid is False
    assert err_key == "err_corrupted_image"
    assert pil_img is None


def test_validate_image_too_small_dimensions():
    """Verify that images smaller than 64x64 are rejected."""
    tiny_img = Image.new("RGB", (32, 32), color=(10, 20, 30))
    buf = io.BytesIO()
    tiny_img.save(buf, format="PNG")

    is_valid, err_key, pil_img = utils.validate_image_file(buf.getvalue())
    assert is_valid is False
    assert err_key == "err_invalid_dimensions"


def test_preprocess_image_shape_and_normalization():
    """Verify that preprocessing produces float32 array in [-1, 1] range with shape (1, 224, 224, 3)."""
    img = Image.new("RGB", (300, 300), color=(128, 128, 128))
    preprocessed = utils.preprocess_image_for_model(img, target_size=(224, 224))

    assert isinstance(preprocessed, np.ndarray)
    assert preprocessed.shape == (1, 224, 224, 3)
    assert preprocessed.dtype == np.float32
    # Pixel 128 normalized: (128 / 127.5) - 1.0 approx 0.0039
    assert -1.0 <= np.min(preprocessed) <= 1.0
    assert -1.0 <= np.max(preprocessed) <= 1.0


def test_crop_compatibility_check():
    """Ensure crop compatibility correctly permits trained crops and rejects untrained ones."""
    trained_tomato_classes = [
        "Tomato___Bacterial_spot",
        "Tomato___Early_blight",
        "Tomato___Late_blight",
        "Tomato___healthy"
    ]

    # Tomato should pass
    is_ok, reason = utils.check_crop_compatibility("Tomato", trained_tomato_classes)
    assert is_ok is True
    assert reason is None

    # Paddy requires separate dataset and must not be falsely reported as supported
    is_paddy_ok, p_reason = utils.check_crop_compatibility("Paddy (rice)", trained_tomato_classes)
    assert is_paddy_ok is False
    assert "requires specific training data" in p_reason

    # Unknown crop
    is_unk_ok, u_reason = utils.check_crop_compatibility("Wheat", trained_tomato_classes)
    assert is_unk_ok is False


def test_evaluate_prediction_threshold_and_exact_message():
    """
    Verify 60% confidence threshold enforcement:
    - Below 60%: Exact message 'Not sure, please consult your agriculture officer or KVK'
    - Above 60%: Confident diagnosis with disease_id mapping
    - Crop mismatch: Safely rejected
    """
    classes = [
        "Tomato___Bacterial_spot",
        "Tomato___Early_blight",
        "Tomato___Late_blight",
        "Tomato___healthy"
    ]

    # Test 1: Low confidence (55%)
    low_conf_probs = np.array([0.55, 0.20, 0.15, 0.10])
    res_low = utils.evaluate_prediction_result(low_conf_probs, classes, "Tomato", confidence_threshold=0.60)
    assert res_low["status"] == "low_confidence"
    assert res_low["message"] == "Not sure, please consult your agriculture officer or KVK"

    # Test 2: High confidence (88%)
    high_conf_probs = np.array([0.05, 0.88, 0.04, 0.03])
    res_high = utils.evaluate_prediction_result(high_conf_probs, classes, "Tomato", confidence_threshold=0.60)
    assert res_high["status"] == "confident_diagnosis"
    assert res_high["predicted_class"] == "Tomato___Early_blight"
    assert res_high["disease_id"] == "tomato_early_blight"
    assert res_high["confidence"] >= 0.60

    # Test 3: Crop class mismatch protection
    non_tomato_classes = ["Paddy___Blast", "Tomato___Late_blight"]
    mismatch_probs = np.array([0.95, 0.05])
    res_mismatch = utils.evaluate_prediction_result(mismatch_probs, non_tomato_classes, "Tomato", confidence_threshold=0.60)
    assert res_mismatch["status"] == "crop_mismatch"
