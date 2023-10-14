import cv2
import numpy as np
import torch
import os

from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator 

def main(model: YOLO, model_numbers: YOLO, image: np.array, image_path: str) -> str:
    results = model.predict(image)
    for r in results:
        
        annotator = Annotator(image)
        
        boxes = r.boxes
        for box in boxes:
            
            if box.conf[0] > 0.65:
                b = box.xyxy[0]  # get box coordinates in (top, left, bottom, right) format
                c = box.cls
                
                number = image[int(b[1]):int(b[3]), int(b[0]):int(b[2])]
                
                # For retangle bboxes
                if ((b[3]-b[1]) / (b[2]-b[0])) < 1.5:
                    print("++++++++++++++++++++++++++++++++++++++++++++++")
                    number = cv2.resize(number, (60, 20))
                    top = bottom = 20
                    left = right = 0
                    number = cv2.copyMakeBorder(number, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(200, 255, 128))

                results_numbers = model_numbers(number).xyxy[0]
                results_numbers = sorted(results_numbers,key=lambda l:l[0])
                number_name = ""
                
                for num_res in results_numbers:
                    # number = cv2.rectangle(number, (int(num_res[1]), int(num_res[3])), (int(num_res[0]), int(num_res[2])), (128, 255, 128), 2)
                    number_name = number_name + str(int(num_res[-1]))

                # width = (b[2] - b[0]) / 16 

                # number_first_half = image[int(b[1]):int(b[3]), int(b[0]):int(((b[0] + b[2]) / 2) + width)]
                # number_second_half = image[int(b[1]):int(b[3]), int(((b[0] + b[2]) / 2) - width):int(b[2])]
                # first = infer("D:/Projects/Python_Projects/Hackathons/AI-2/SVHNClassifier-PyTorch-master/model-54000.pth", number_first_half)
                # second = infer("D:/Projects/Python_Projects/Hackathons/AI-2/SVHNClassifier-PyTorch-master/model-54000.pth", number_second_half)
                # cv2.imwrite(f'./boxes/{first}_left.jpg', number_first_half)
                # cv2.imwrite(f'./boxes/{second}_right.jpg', number_second_half)
                # first = non_ten_list(first)
                # second = non_ten_list(second)
                # number_name = str(first + second)
                try:
                    cv2.imwrite(f'./boxes/{number_name}.jpg', number)  
                except:
                    cv2.imwrite(f'./boxes/no_number.jpg', number) 
                # number_name = number_name.replace("[", "").replace("]", "").replace(" ", "").replace(",", "")
                annotator.box_label(b, number_name)
            
        image = annotator.result() 
        try: 
            cv2.imwrite(f'./results/{number_name}.jpg', image)    
        except:
            cv2.imwrite('./results/no_number.jpb', image)
        
        
        

if __name__ == "__main__":
    DATASET_PATH = "./dataset_test"
    model = YOLO('bestv2.pt')
    model_numbers = torch.hub.load('ultralytics/yolov5', 'custom', path='best-11.pt') 
    image_paths = os.listdir(DATASET_PATH)
    for image_path in image_paths:
        image = cv2.imread(f"{DATASET_PATH}/{image_path}")
        main(model, model_numbers, image, image_path)