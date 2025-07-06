# detect_review2.py

import cv2
import numpy as np
import os
import shutil
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.xception import preprocess_input

# Constants
IMG_SIZE = 299

# Load the trained model
model = load_model(os.path.join(os.path.dirname(__file__), 'model.h5'))


def extract_sampled_frames(video_path, output_folder, max_frames=10):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    interval = max(1, total_frames // max_frames)
    count = 0
    saved = 0

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if count % interval == 0:
            resized = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))
            cv2.imwrite(os.path.join(output_folder, f"frame_{saved}.jpg"), resized)
            saved += 1

        count += 1
    cap.release()
    print(f"✅ Extracted {saved} frames to '{output_folder}'")


def clean_up_folder(folder_path):
    shutil.rmtree(folder_path, ignore_errors=True)
    print(f"🧹 Deleted temporary folder: '{folder_path}'")


def predict_video(video_path):
    temp_folder = "temp_frames"
    extract_sampled_frames(video_path, temp_folder)

    predictions = []
    for fname in os.listdir(temp_folder):
        path = os.path.join(temp_folder, fname)
        img = cv2.imread(path)
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        img = np.expand_dims(img, axis=0)
        img = preprocess_input(img.astype(np.float32))
        pred = model.predict(img)[0][0]
        predictions.append(pred)

    if not predictions:
        clean_up_folder(temp_folder)
        return "❌ No frames could be analyzed."

    avg_pred = np.mean(predictions)
    label = "FAKE" if avg_pred > 0.5 else "REAL"

    # Optional: cleanup dataset folder if used
    dataset_path = "C:/Users/vasav/OneDrive/Desktop/walmart2025/dataset"
    if os.path.exists(dataset_path):
        clean_up_folder(dataset_path)

    clean_up_folder(temp_folder)

    return f"🎯 Prediction: {label} (Confidence: {avg_pred:.2f})"


def predict_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return "❌ Failed to load image."
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img.astype(np.float32))

    pred = model.predict(img)[0][0]
    label = "FAKE" if pred > 0.5 else "REAL"
    return f"🎯 Prediction: {label} (Confidence: {pred:.2f})"


# Debug: Example usage (disable or delete during production)
if __name__ == "__main__":
    print(predict_video("C:/Users/vasav/OneDrive/Desktop/walmart2025/videos/real/WhatsApp Video 2025-06-21 at 16.27.02.mp4"))
    # print(predict_image("path_to_some_image.jpg"))
