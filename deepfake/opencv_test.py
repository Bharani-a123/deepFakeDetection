import cv2

cap = cv2.VideoCapture(r'C:\DeepFakeDetection\DFDC_Dataset\Fake\aaagqkcdis.mp4')
if not cap.isOpened():
    print("Cannot open video file")
else:
    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        count += 1
    cap.release()
    print(f"Total frames read: {count}")
