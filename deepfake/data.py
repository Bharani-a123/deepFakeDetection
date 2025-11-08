import cv2
import os
from mtcnn import MTCNN

def process_folder(input_folder, output_folder, max_frames=70):
    detector = MTCNN()
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for video_name in os.listdir(input_folder):
        if not video_name.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            continue
        video_path = os.path.join(input_folder, video_name)
        cap = cv2.VideoCapture(video_path)
        frame_count = 0
        saved_count = 0
        while cap.isOpened() and saved_count < max_frames:
            ret, frame = cap.read()
            if not ret:
                break
            frame_count += 1
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faces = detector.detect_faces(rgb_frame)
            for i, face in enumerate(faces):
                x, y, width, height = face['box']
                x, y = max(0, x), max(0, y)
                face_crop = frame[y:y+height, x:x+width]
                face_crop = cv2.resize(face_crop, (224, 224))
                save_path = os.path.join(output_folder, f"{video_name}_frame{frame_count}_face{i}.jpg")
                cv2.imwrite(save_path, face_crop)
                saved_count += 1
            if saved_count >= max_frames:
                break
        cap.release()
        print(f"Processed {video_name}: saved {saved_count} faces from {frame_count} frames.")

base_dir = "DFDC_Dataset"
folders = ["Fake", "Real"]
for label in folders:
    process_folder(
        input_folder=os.path.join(base_dir, label),
        output_folder=os.path.join(base_dir, f"{label}_faces"),
        max_frames=20
    )
