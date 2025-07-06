import cv2
import os
import shutil

def extract_frames(video_path, label, output_dir, max_frames=30):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    interval = max(1, total_frames // max_frames)
    count, saved = 0, 0

    label_dir = os.path.join(output_dir, label)
    os.makedirs(label_dir, exist_ok=True)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if count % interval == 0:
            resized = cv2.resize(frame, (299, 299))
            frame_path = os.path.join(label_dir, f"{label}_{saved}.jpg")
            cv2.imwrite(frame_path, resized)
            saved += 1

        count += 1
    cap.release()
    print(f"✅ Extracted {saved} frames to {label_dir}")

# Example usage:
# Clear dataset first (optional)
shutil.rmtree("dataset", ignore_errors=True)

# Extract frames
extract_frames("C:/Users/vasav/OneDrive/Desktop/walmart2025/videos/real/WhatsApp Video 2025-06-21 at 16.27.02.mp4", "real", "dataset", max_frames=30)

#extract_frames("videos/fake1.mp4", "fake", "dataset", max_frames=30)
