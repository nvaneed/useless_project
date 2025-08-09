# Suppress macOS warning
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

import cv2
import numpy as np
from PIL import Image
import os
import logging
from settings.settings import PATHS

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_images_and_labels(path: str):
    """
    Load face images and corresponding labels from the given directory path.

    Parameters:
        path (str): Directory path containing face images.

    Returns:
        tuple: (face_samples, ids) Lists of face samples and corresponding labels.
    """
    try:
        imagePaths = [os.path.join(path, f) for f in os.listdir(path) if f.lower().endswith((".jpg", ".png"))]
        faceSamples = []
        ids = []

        # Load Haar cascade
        detector = cv2.CascadeClassifier(PATHS['cascade_file'])
        if detector.empty():
            raise ValueError(f"Error loading cascade classifier from {PATHS['cascade_file']}")

        logger.info(f"Found {len(imagePaths)} images in {path}")

        for imagePath in imagePaths:
            try:
                # Convert image to grayscale
                PIL_img = Image.open(imagePath).convert('L')
                img_numpy = np.array(PIL_img, 'uint8')

                # Extract the user ID from filename -> "User-1.jpg"
                try:
                    id = int(os.path.split(imagePath)[-1].split("-")[1].split(".")[0])
                except Exception as e:
                    logger.warning(f"Filename format error: {imagePath} ({e})")
                    continue

                # Detect faces
                faces = detector.detectMultiScale(img_numpy, scaleFactor=1.2, minNeighbors=5)

                if len(faces) == 0:
                    logger.warning(f"No face detected in {imagePath}")
                    continue

                for (x, y, w, h) in faces:
                    faceSamples.append(img_numpy[y:y+h, x:x+w])
                    ids.append(id)

                logger.info(f"Processed {imagePath} → ID {id}, Faces found: {len(faces)}")

            except Exception as e:
                logger.error(f"Error processing {imagePath}: {e}")

        logger.info(f"Total faces collected: {len(faceSamples)}")
        logger.info(f"Unique IDs: {set(ids)}")

        return faceSamples, ids

    except Exception as e:
        logger.error(f"Error in get_images_and_labels: {e}")
        raise


if __name__ == "__main__":
    try:
        logger.info("Starting face recognition training...")

        # Initialize recognizer (requires opencv-contrib-python)
        recognizer = cv2.face.LBPHFaceRecognizer_create()

        # Load training data
        faces, ids = get_images_and_labels(PATHS['image_dir'])

        if not faces or not ids:
            raise ValueError("No valid training data found. Check your dataset and cascade file.")

        # Train model
        logger.info("Training model...")
        recognizer.train(faces, np.array(ids))

        # Save trained model
        recognizer.write(PATHS['trainer_file'])
        logger.info(f"✅ Model trained successfully with {len(np.unique(ids))} unique IDs and {len(faces)} face samples.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
