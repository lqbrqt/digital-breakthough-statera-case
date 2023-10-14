from main import main

from fastapi import FastAPI, UploadFile, File
from starlette.responses import FileResponse, StreamingResponse
import cv2
import numpy as np
import base64
import shutil

app = FastAPI()


@app.post("/img")

async def processing_img(file: UploadFile = File(...)):
    file_path = f'cashe/{file.filename}'
    with open(file_path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    img = cv2.imread(file_path)
    # byte_image = cv2.imencode(".jpg", im)

    model = YOLO('bestv2.pt')
    model_numbers = torch.hub.load('ultralytics/yolov5', 'custom', path='best-11.pt') 
    
    main(model, model_numbers, img, file_path)

    return {"filename": file.filename}