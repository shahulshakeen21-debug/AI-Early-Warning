import argparse
import json
import logging
import os
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("TrainModel")

# Fixed random seed for reproducibility
RANDOM_SEED = 42

# Target crops and classes from PlantVillage
# Tomato classes present in PlantVillage
TARGET_CLASSES = [
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___healthy"
]


def print_instructions_and_exit(dataset_dir: str):
    """
    Print clear instructions on how to download and arrange the PlantVillage dataset
    without crashing unexpectedly.
    """
    print("\n" + "=" * 70)
    print("PLANTVILLAGE DATASET REQUIRED FOR TRAINING")
    print("=" * 70)
    print(f"The training script checked for dataset folder at:\n  {os.path.abspath(dataset_dir)}")
    print("\nTo train the model with genuine PlantVillage data:")
    print("1. Download the PlantVillage dataset from Kaggle:")
    print("   https://www.kaggle.com/datasets/emmarex/plantdisease")
    print("   or Kaggle's 'plantvillage-dataset' repository.")
    print("2. Extract the dataset into the project folder under:")
    print(f"   ai_early_warning_system_for_farmers/{dataset_dir}/")
    print("3. Ensure the folder contains subdirectories for target tomato classes:")
    for cls_name in TARGET_CLASSES:
        print(f"   - {dataset_dir}/{cls_name}/")
    print("4. Re-run training:")
    print("   python train_model.py")
    print("=" * 70 + "\n")
    sys.exit(0)


def check_tensorflow_support():
    """
    Verify TensorFlow / Keras installation on the current Python environment.
    Provides clear diagnostics if TF is missing or incompatible.
    """
    try:
        import tensorflow as tf
        import keras
        return tf, keras
    except ImportError as e:
        logger.error(f"TensorFlow or Keras import failed: {e}")
        print("\n" + "!" * 70)
        print("TENSORFLOW COMPATIBILITY NOTICE")
        print("!" * 70)
        print(f"Current Python runtime: {sys.version.split()[0]}")
        print("TensorFlow wheels on Windows officially support Python 3.9, 3.10, and 3.11.")
        print("If you are running Python 3.12 or 3.13, please install Python 3.10 or 3.11:")
        print("  py -3.10 -m venv venv")
        print("  .\\venv\\Scripts\\activate")
        print("  pip install tensorflow==2.15.0 scikit-learn pillow numpy\n")
        print("The main Streamlit decision-support application (weather, advice, schemes,")
        print("image validation, and bilingual UI) runs independently on all Python versions.")
        print("!" * 70 + "\n")
        sys.exit(0)


def build_mobilenet_model(num_classes: int, input_shape=(224, 224, 3)):
    """
    Build transfer learning model using MobileNetV2 with ImageNet weights.
    Appends GlobalAveragePooling2D, Dropout(0.2), and Softmax Dense head.
    """
    tf, keras = check_tensorflow_support()
    from keras import layers, models

    base_model = tf.keras.applications.MobileNetV2(
        input_shape=input_shape,
        include_top=False,
        weights="imagenet"
    )
    base_model.trainable = False  # Freeze base feature extractor

    inputs = layers.Input(shape=input_shape)
    # Data augmentation pipeline
    x = layers.RandomFlip("horizontal")(inputs)
    x = layers.RandomRotation(0.1)(x)
    x = layers.RandomZoom(0.1)(x)
    # Preprocessing for MobileNetV2: [-1, 1]
    x = layers.Rescaling(scale=1.0 / 127.5, offset=-1.0)(x)
    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.2, seed=RANDOM_SEED)(x)
    outputs = layers.Dense(num_classes, activation="softmax")(x)

    model = models.Model(inputs, outputs, name="MobileNetV2_CropClassifier")
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )
    return model, tf, keras


def train(data_dir: str = "dataset", epochs: int = 10, batch_size: int = 32):
    """
    Train MobileNetV2 on local PlantVillage dataset.
    Reports actual training & validation loss/accuracy, confusion matrix, and classification report.
    Saves model.h5 and class_names.json only upon actual successful training.
    """
    p_data = Path(data_dir)
    if not p_data.exists() or not p_data.is_dir():
        print_instructions_and_exit(data_dir)

    # Check for subdirectories
    subdirs = [d.name for d in p_data.iterdir() if d.is_dir()]
    valid_classes = [c for c in TARGET_CLASSES if c in subdirs]

    if len(valid_classes) < 2:
        logger.warning(f"Found {len(valid_classes)} classes in {data_dir}. At least 2 target classes required.")
        print_instructions_and_exit(data_dir)

    tf, keras = check_tensorflow_support()
    import numpy as np
    from sklearn.metrics import classification_report, confusion_matrix

    logger.info(f"Target classes identified ({len(valid_classes)}): {valid_classes}")

    # Set seeds
    tf.random.set_seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

    logger.info("Loading training and validation datasets (80/20 split)...")
    train_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        labels="inferred",
        label_mode="categorical",
        class_names=valid_classes,
        image_size=(224, 224),
        batch_size=batch_size,
        shuffle=True,
        seed=RANDOM_SEED,
        validation_split=0.2,
        subset="training"
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        labels="inferred",
        label_mode="categorical",
        class_names=valid_classes,
        image_size=(224, 224),
        batch_size=batch_size,
        shuffle=False,
        seed=RANDOM_SEED,
        validation_split=0.2,
        subset="validation"
    )

    class_names = train_ds.class_names
    logger.info(f"Output layer class mapping: {class_names}")

    model, tf, keras = build_mobilenet_model(num_classes=len(class_names))
    model.summary()

    callbacks = [
        keras.callbacks.EarlyStopping(monitor="val_loss", patience=3, restore_best_weights=True)
    ]

    logger.info("Starting model training...")
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=callbacks
    )

    # Evaluate validation metrics
    logger.info("Computing validation evaluation metrics...")
    y_true = []
    y_pred = []

    for images, labels in val_ds:
        preds = model.predict(images, verbose=0)
        y_true.extend(np.argmax(labels.numpy(), axis=1))
        y_pred.extend(np.argmax(preds, axis=1))

    cm = confusion_matrix(y_true, y_pred)
    cr = classification_report(y_true, y_pred, target_names=class_names)

    print("\n" + "=" * 60)
    print("ACTUAL VALIDATION EVALUATION RESULTS")
    print("=" * 60)
    print("Note: Evaluated strictly on the held-out validation split of the dataset.")
    print("PlantVillage dataset lab images do not guarantee equal field performance.")
    print("-" * 60)
    print(f"Final Validation Loss:     {history.history.get('val_loss', [-1])[-1]:.4f}")
    print(f"Final Validation Accuracy: {history.history.get('val_accuracy', [-1])[-1]:.4f}")
    print("\nConfusion Matrix:")
    print(cm)
    print("\nClassification Report:")
    print(cr)
    print("=" * 60 + "\n")

    # Save model and class mapping
    model_path = "model.h5"
    class_names_path = "class_names.json"

    logger.info(f"Saving model to {model_path}...")
    model.save(model_path)

    logger.info(f"Saving class names to {class_names_path}...")
    with open(class_names_path, "w", encoding="utf-8") as f:
        json.dump(class_names, f, indent=2)

    logger.info("Training and export complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train MobileNetV2 on PlantVillage dataset.")
    parser.add_argument("--data_dir", type=str, default="dataset", help="Path to PlantVillage tomato classes directory")
    parser.add_argument("--epochs", type=int, default=10, help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=32, help="Batch size")
    args = parser.parse_args()

    train(data_dir=args.data_dir, epochs=args.epochs, batch_size=args.batch_size)
