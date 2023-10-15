import os
from main import main

from fastapi import FastAPI, UploadFile, File
from starlette.responses import FileResponse, StreamingResponse
import cv2
import numpy as np
import base64
import shutil
import torch
from ultralytics import YOLO

app = FastAPI()
model = YOLO('models/best.pt')
model_numbers = torch.hub.load('ultralytics/yolov5', 'custom', path='models/best-11.pt') 

@app.post("/img")

async def processing_img(file: UploadFile = File(...)):
    os.mkdir("cashe")
    os.mkdir("cashe/boxes")
    os.mkdir("cashe/results")
    
    file_path = f'cashe/{file.filename}'
    with open(file_path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    img = cv2.imread(file_path)
    # byte_image = cv2.imencode(".jpg", im)

    result = main(model, model_numbers, img, file_path)
    # shutil.rmtree('cashe')  

    return result