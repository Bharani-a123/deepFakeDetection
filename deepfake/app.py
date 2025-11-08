from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from model import classify_image  # import model logic
import numpy as np
from PIL import Image
import io
import cv2
import tempfile

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/detect-image/")
async def detect_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image file type")
    image_bytes = await file.read()
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Could not read image file")
    image_np = np.array(image)
    prediction = classify_image(image_np)
    return JSONResponse(content=prediction)

@app.post("/detect-video/")
async def detect_video(file: UploadFile = File(...)):
    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Invalid video file type")
    video_bytes = await file.read()

    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp4") as temp_video:
        temp_video.write(video_bytes)
        temp_video.flush()
        cap = cv2.VideoCapture(temp_video.name)

        if not cap.isOpened():
            raise HTTPException(status_code=400, detail="Cannot open video file")

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        frame_count = 0
        predictions = []

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Sample every 30th frame for performance; adjust as needed
            if frame_count % 30 == 0:
                try:
                    pred = classify_image(frame)
                    predictions.append(pred)
                except Exception:
                    # Log or handle specific classification errors if needed
                    pass

            frame_count += 1

        cap.release()

    if not predictions:
        raise HTTPException(status_code=400, detail="No frames processed from video")

    avg_fake_prob = sum(p['fake'] for p in predictions) / len(predictions)
    verdict = "fake" if avg_fake_prob > 0.5 else "real"

    return JSONResponse(content={
        "video_verdict": verdict,
        "average_fake_prob": round(avg_fake_prob, 3),
        "total_frames": total_frames,
        "frames_processed": len(predictions)
    })

@app.post("/detect-webcam-frame/")
async def detect_webcam_frame(frame: UploadFile = File(...)):
    if not frame.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image file type")
    frame_bytes = await frame.read()
    try:
        image = Image.open(io.BytesIO(frame_bytes)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Could not read image file")
    image_np = np.array(image)
    prediction = classify_image(image_np)
    return JSONResponse(content=prediction)
