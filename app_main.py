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
model = YOLO('models/bestv2.pt')
model_numbers = torch.hub.load('ultralytics/yolov5', 'custom', path='models/best-11.pt') 

@app.post("/img")
async def processing_img(file: UploadFile = File(...)):
    os.makedirs("cashe", exist_ok=True)
    os.makedirs("cashe/results", exist_ok=True)
    
    file_path = f'cashe/{file.filename}'
    with open(file_path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    img = cv2.imread(file_path)
    # byte_image = cv2.imencode(".jpg", im)

    result = main(model, model_numbers, img, file_path)
    # shutil.rmtree('cashe')  
    os.remove(file_path)
    return result

@app.get("/get_res_img/{filename}", responses={200: {"description": "A picture of a vector image.", "content" : {"image/jpeg" : {"example" : "No example available. Just imagine a picture of a vector image."}}}})
def image_endpoint(filename: str):
    file_path = f'cashe/results/{filename}'
    if os.path.exists(file_path):
        os.rename(file_path, 'cashe/results/temp.jpg')
        return FileResponse('cashe/results/temp.jpg', media_type="image/jpeg", filename=filename)
    
    return {"error" : "File not found!"}