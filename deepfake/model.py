import torch
from transformers import AutoImageProcessor, SiglipForImageClassification
from PIL import Image
import io
import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

model_name = "prithivMLmods/deepfake-detector-model-v1"
model = SiglipForImageClassification.from_pretrained(model_name)
processor = AutoImageProcessor.from_pretrained(model_name, use_fast=True)
model.eval()

id2label = {"1": "fake", "0": "real"}

def classify_image(image):
    image = Image.fromarray(image).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    probs = torch.nn.functional.softmax(logits, dim=1).squeeze().tolist()
    prediction = {id2label[str(i)]: round(probs[i], 3) for i in range(len(probs))}
    return prediction
