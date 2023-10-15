import cv2
import numpy as np
import torch
import os

from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator 

def main(model: YOLO, model_numbers: YOLO, image: np.array, image_path: str) -> str:
    results = model.predict(image)
    file_name = ""
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
                if len(number_name) > 6:
                    file_name = number_name
                try:
                    cv2.imwrite(f'cashe/boxes/{number_name}.jpg', number)  
                except:
                    cv2.imwrite(f'cashe/boxes/no_number.jpg', number) 
                # number_name = number_name.replace("[", "").replace("]", "").replace(" ", "").replace(",", "")
                annotator.box_label(b, number_name)
            
        image = annotator.result() 
        try:
            cv2.imwrite(f'cashe/results/{file_name}.jpg', image)    
        except:
            file_name = 'no_number'
            cv2.imwrite('cashe/results/no_number.jpg', image)

    # return file_name

    return {
        "image": f"{file_name}.jpg",
		"verified": 'false',  
		"annotations": [
			{
				"label": file_name,
				"coordinates": {   
					"x": 879.5,             
					"y": 239.43883792048929,        
					"width": 305.0,
					"height": 59.0
				}
			}
		]
    }
        
        
        

if __name__ == "__main__":
    DATASET_PATH = "./dataset_test"
    model = YOLO('bestv2.pt')
    model_numbers = torch.hub.load('ultralytics/yolov5', 'custom', path='best-11.pt') 
    image_paths = os.listdir(DATASET_PATH)
    for image_path in image_paths:
        image = cv2.imread(f"{DATASET_PATH}/{image_path}")
        main(model, model_numbers, image, image_path)