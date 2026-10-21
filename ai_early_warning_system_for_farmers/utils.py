import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from PIL import Image
import numpy as np

logger = logging.getLogger(__name__)

# Constants
MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB limit
MIN_IMAGE_DIMENSION = 64
SUPPORTED_IMAGE_FORMATS = {"JPEG", "JPG", "PNG"}

# Supported Crops and their mapping to trained disease classes
# PlantVillage contains Tomato classes. Paddy and Groundnut are supported agricultural crops
# but require specific datasets to be trained before inference can run.
CROP_SUPPORT_MAP: Dict[str, Dict[str, Any]] = {
    "Tomato": {
        "supported_in_model": True,
        "classes": [
            "Tomato___Bacterial_spot",
            "Tomato___Early_blight",
            "Tomato___Late_blight",
            "Tomato___healthy"
        ],
        "class_to_disease_id": {
            "Tomato___Bacterial_spot": "tomato_bacterial_spot",
            "Tomato___Early_blight": "tomato_early_blight",
            "Tomato___Late_blight": "tomato_late_blight",
            "Tomato___healthy": "tomato_healthy"
        }
    },
    "Paddy (rice)": {
        "supported_in_model": False,
        "classes": [
            "Paddy___Blast"
        ],
        "class_to_disease_id": {
            "Paddy___Blast": "paddy_blast"
        }
    },
    "Groundnut": {
        "supported_in_model": False,
        "classes": [
            "Groundnut___Tikka"
        ],
        "class_to_disease_id": {
            "Groundnut___Tikka": "groundnut_tikka"
        }
    }
}


def load_json_file(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Safely load a JSON file with UTF-8 encoding.
    Returns an empty dict or raises informative ValueError if parsing fails.
    """
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"Required data file not found: {path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON from {path}: {e}")
        raise ValueError(f"Invalid JSON format in {path.name}: {e}")
    except Exception as e:
        logger.error(f"Error reading file {path}: {e}")
        raise


def get_text(i18n_dict: Dict[str, Any], key: str, lang: str = "en") -> str:
    """
    Retrieve translated text for a given key and language.
    Falls back to English if the key exists but Tamil is missing.
    Falls back to key name if completely missing.
    """
    if not isinstance(i18n_dict, dict):
        return key

    entry = i18n_dict.get(key)
    if not entry or not isinstance(entry, dict):
        return key

    val = entry.get(lang)
    if val and isinstance(val, str) and val.strip():
        return val

    # Fallback to English
    val_en = entry.get("en")
    if val_en and isinstance(val_en, str) and val_en.strip():
        return val_en

    return key


def validate_image_file(image_bytes: bytes) -> Tuple[bool, Optional[str], Optional[Image.Image]]:
    """
    Validate uploaded image bytes against size, corruption, format, and dimension limits.
    Returns: (is_valid, error_key_or_none, PIL_Image_or_none)
    """
    if not image_bytes or len(image_bytes) == 0:
        return False, "err_empty_upload", None

    if len(image_bytes) > MAX_IMAGE_SIZE_BYTES:
        return False, "err_image_too_large", None

    try:
        from io import BytesIO
        stream = BytesIO(image_bytes)
        img = Image.open(stream)
        img.verify()  # Verify structural integrity
        
        # Re-open after verify() as Pillow documentation specifies
        stream.seek(0)
        img = Image.open(stream)
        img.load()  # Force load pixel data
    except Exception as e:
        logger.warning(f"Image validation corruption error: {e}")
        return False, "err_corrupted_image", None

    fmt = (img.format or "").upper()
    if fmt not in SUPPORTED_IMAGE_FORMATS:
        return False, "err_unsupported_format", None

    width, height = img.size
    if width < MIN_IMAGE_DIMENSION or height < MIN_IMAGE_DIMENSION:
        return False, "err_invalid_dimensions", None

    # Convert to RGB if RGBA/Grayscale
    if img.mode != "RGB":
        img = img.convert("RGB")

    return True, None, img


def preprocess_image_for_model(img: Image.Image, target_size: Tuple[int, int] = (224, 224)) -> np.ndarray:
    """
    Preprocess a PIL Image for MobileNetV2 inference:
    - Resize to target_size (default 224x224)
    - Convert to float32 NumPy array
    - Scale inputs: MobileNetV2 uses [-1, 1] scaling (tf.keras.applications.mobilenet_v2.preprocess_input formula: (x / 127.5) - 1.0)
    - Add batch dimension: shape (1, 224, 224, 3)
    """
    resized = img.resize(target_size, Image.Resampling.BILINEAR)
    arr = np.array(resized, dtype=np.float32)
    # MobileNetV2 normalization: scale to [-1, 1]
    arr = (arr / 127.5) - 1.0
    # Add batch axis
    batched = np.expand_dims(arr, axis=0)
    return batched


def check_crop_compatibility(crop_name: str, trained_classes: List[str]) -> Tuple[bool, Optional[str]]:
    """
    Verify whether the selected crop is supported by the trained model classes.
    Never allows cross-crop disease diagnosis.
    """
    crop_info = CROP_SUPPORT_MAP.get(crop_name)
    if not crop_info:
        return False, f"Crop '{crop_name}' is not recognized in the system database."

    if not crop_info.get("supported_in_model", False):
        return False, f"Crop '{crop_name}' requires specific training data not present in the current model."

    expected_classes = crop_info.get("classes", [])
    # Check if any expected class is in trained_classes
    matching = [c for c in expected_classes if c in trained_classes]
    if not matching:
        return False, f"The loaded model does not contain classification heads for '{crop_name}'."

    return True, None


def evaluate_prediction_result(
    probabilities: np.ndarray,
    trained_classes: List[str],
    selected_crop: str,
    confidence_threshold: float = 0.60
) -> Dict[str, Any]:
    """
    Evaluate raw model probabilities against crop compatibility and confidence threshold.
    Strictly enforces:
    - 60% threshold
    - Crop alignment
    - No fabricated confidence or diagnoses
    """
    if len(probabilities) == 0 or len(trained_classes) == 0:
        return {
            "status": "error",
            "message": "Empty prediction array or class list."
        }

    best_idx = int(np.argmax(probabilities))
    raw_confidence = float(probabilities[best_idx])
    predicted_class = trained_classes[best_idx] if best_idx < len(trained_classes) else "Unknown"

    crop_info = CROP_SUPPORT_MAP.get(selected_crop, {})
    expected_classes = crop_info.get("classes", [])
    class_to_disease_id = crop_info.get("class_to_disease_id", {})

    # Check crop compatibility
    if predicted_class not in expected_classes:
        return {
            "status": "crop_mismatch",
            "selected_crop": selected_crop,
            "predicted_class": predicted_class,
            "confidence": raw_confidence,
            "message": f"Predicted condition '{predicted_class}' does not belong to selected crop '{selected_crop}'."
        }

    # Check 60% threshold
    if raw_confidence < confidence_threshold:
        return {
            "status": "low_confidence",
            "selected_crop": selected_crop,
            "confidence": raw_confidence,
            "threshold": confidence_threshold,
            "message": "Not sure, please consult your agriculture officer or KVK"
        }

    disease_id = class_to_disease_id.get(predicted_class, "unknown")

    return {
        "status": "confident_diagnosis",
        "selected_crop": selected_crop,
        "predicted_class": predicted_class,
        "disease_id": disease_id,
        "confidence": raw_confidence,
        "is_healthy": "healthy" in predicted_class.lower()
    }


def evaluate_plant_identification_result(
    probabilities: np.ndarray,
    trained_species_classes: List[str],
    confidence_threshold: float = 0.60
) -> Dict[str, Any]:
    """
    Evaluate raw model probabilities for Plant Identification:
    Enforces minimum 60% confidence threshold.
    """
    if len(probabilities) == 0 or len(trained_species_classes) == 0:
        return {
            "status": "error",
            "message": "Empty prediction array or species class list."
        }

    best_idx = int(np.argmax(probabilities))
    raw_confidence = float(probabilities[best_idx])
    predicted_species = trained_species_classes[best_idx] if best_idx < len(trained_species_classes) else "Unknown"

    if raw_confidence < confidence_threshold:
        return {
            "status": "low_confidence",
            "predicted_species": predicted_species,
            "confidence": raw_confidence,
            "threshold": confidence_threshold,
            "message": "Plant could not be identified with sufficient certainty. Please consult a botanical expert or provide a clearer close-up photograph."
        }

    return {
        "status": "identified",
        "predicted_species": predicted_species,
        "confidence": raw_confidence
    }
