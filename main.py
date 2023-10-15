import cv2
import numpy as np
import torch
import os

from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator 
import pandas as pd

def validate_number(num: str) -> bool:
    num_list = list(num)
    if len(num_list) != 8: return False
    try:
        main_sum = int(num_list[-1])
        num_list.pop(-1)
        print(num_list)
        num_list = [int(i) for i in num_list]
        mult = [2, 1, 2, 1, 2, 1, 2]
        print(num_list)
        print(mult)
        num_list = [a*b for a,b in zip(num_list, mult)]

        print(num_list)

        sum = 0
        for elem in num_list:
            if elem > 9:
                sum = sum + int(str(elem)[0]) + int(str(elem)[1])
            else:
                sum = sum + elem
        print(main_sum)
        print(sum)
        if main_sum == (10 - sum % 10):
            return True
    except:
       return False

    return False

def prepare_arr(arr, n):
  arr.append(arr[-1][:-2] + [arr[-1][-2] + arr[-1][-1]] if len(arr) else [1] * n)

  if len(arr[-1]) != 1:
    prepare_arr(arr, n)

  return arr

def try_to_return_one_number(num: str) -> str:
  num_list = list(num)
  if len(num_list) != 8: return False, False
  main_sum = int(num_list[-1])
  num_list.pop(-1)
  nan_index = -1
  for i in range(len(num_list)):
    if num_list[i] == "_":
      nan_index = i
  if nan_index == -1: return False
  
  sum = 0
  mult = [2, 1, 2, 1, 2, 1, 2]
  for index, elem in enumerate(num_list):
    if elem != "_":
        elem = int(elem) * mult[index]
        # print(elem)
        if elem > 9:
            sum = sum + int(str(elem)[0]) + int(str(elem)[1])
        else:
            sum = sum + (int(elem) * mult[index])
  
  # print(nan_index + 1)
  print(sum)
  print(main_sum)
  if nan_index // 2 == 0:
    our = 10 - sum % 10
    their = 10 - ((((sum // 10) + 1) * 10 - main_sum)) % 10
    return mult[nan_index] * our - their
  else:
    num = 10 - (sum + main_sum) % 10
    (num)
    if num == 10:
      return 0
    else:
      return int((10 + int(str(num)) - 1) / 2)

def return_most_strange(arr):
  distances = []
  if len(arr) > 7:
     return False, False
  for a in arr:
    distances.append(np.abs(a - arr.mean()))
  for index, a in enumerate(arr):
    if np.abs(np.abs(a - arr.mean()) > (np.array(distances).mean() * 2)):
      return index, a
  return False, False
    
def get_dists(arr):
  dists = []
  for i in range(len(arr) - 1):
    dists.append(arr[i+1] - arr[i])
  return dists



def main(model: YOLO, model_numbers: YOLO, image: np.array, image_path: str) -> str:
    results = model.predict(image)
    file_name = ""
    x = 0
    y = 0
    w = 0
    h = 0
    number_labels = []
    for r in results:
        
        annotator = Annotator(image)
        
        boxes = r.boxes
        for box in boxes:
            if box.conf[0] > 0.65:
                b = box.xyxy[0]  # get box coordinates in (top, left, bottom, right) format
                c = box.cls
                x, y, w, h = box.xywhn[0]
                print(x, y, w, h)
                number = image[int(b[1]) - 3:int(b[3]) + 3, int(b[0]):int(b[2])]
                imgray = cv2.cvtColor(number, cv2.COLOR_BGR2GRAY)
                # For retangle bboxes
                if ((b[3]-b[1]) / (b[2]-b[0])) < 1.5:
                    print("++++++++++++++++++++++++++++++++++++++++++++++")
                    # imgray = cv2.cvtColor(number, cv2.COLOR_BGR2GRAY)
                    # #cv2.threshold(src, thresh1, thresh2, threshold_type)
                    # ret, thresh = cv2.threshold(imgray, 160, 255, cv2.THRESH_BINARY_INV)
                    # for x in range(len(thresh)):
                    #     for y in range(len(thresh[x])):
                    #         if thresh[x][y] == 0:
                    #             nb = number[x][y][0]
                    #             ng = number[x][y][1]
                    #             nr = number[x][y][2]

                    #             if nb + 15 > 255:
                    #                 nb = 255
                    #             else:
                    #                 nb = nb + 15
                    #             if ng + 15 > 255:
                    #                 ng = 255
                    #             else:
                    #                 ng = ng + 15
                    #             if nr + 15 > 255:
                    #                 nr = 255
                    #             else:
                    #                 nr = nr + 15
                    #             number[x][y] = (nb, ng, nr)
                    number = cv2.cvtColor(imgray, cv2.COLOR_GRAY2BGR)
                    number = cv2.resize(number, (60, 20))
                    top = bottom = 20
                    left = right = 0
                    number = cv2.copyMakeBorder(number, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(200, 255, 128))
                    

                results_numbers = model_numbers(number).xyxy[0]
                results_numbers = sorted(results_numbers,key=lambda l:l[0])
                number_name = ""
                
                arr = []
                for result_number in results_numbers:
                   if result_number[4] > 0.1:
                    print(result_number)
                    number_labels.append({"label": result_number[5], "coordinates": {"x": float(result_number[0] + result_number[2]) / 2, "y": float(result_number[1] + result_number[3]) / 2, "w": float(result_number[2] - result_number[0]), "h": float(result_number[3] - result_number[1]), "conf": float(result_number[4])}})
                    arr.append(result_number[0])

                dists = get_dists(arr)
                print(return_most_strange(np.array(dists)))
                indx_strange, strange_dist = return_most_strange(np.array(dists))
                tmban = ""
                # mean_cord = (arr[indx_strange] + arr[indx_strange + 1]) / 2
                
                for index, num_res in enumerate(results_numbers):
                    # number = cv2.rectangle(number, (int(num_res[1]), int(num_res[3])), (int(num_res[0]), int(num_res[2])), (128, 255, 128), 2)
                    number_name = number_name + str(int(num_res[-1]))

                if strange_dist != False:
                    s = "_" * (8 - len(number_name))
                    number_name = number_name[:indx_strange + 1] + s + number_name[indx_strange + 1:]
                number_name = number_name + tmban
                if len(number_name) < 8:
                    if x < image.shape[1] / 2:
                        print("LEFT")
                        s = "_" * (8 - len(number_name))
                        number_name = s + number_name
                    elif x > image.shape[1] / 2:
                        print("RIGHT")
                        s = "_" * (8 - len(number_name))
                        number_name = number_name + s
                if len(number_name) > 6:
                    file_name = number_name
                try:
                    cv2.imwrite(f'./boxes/{number_name}.jpg', number)  
                except:
                    cv2.imwrite(f'./boxes/no_number.jpg', number) 
                number_name = number_name.replace("[", "").replace("]", "").replace(" ", "").replace(",", "")
               
                    
                annotator.box_label(b, number_name)
        # print("IMAGE_PATH: ", image_path)
        image = annotator.result() 
        try:
            cv2.imwrite(f'./results/{file_name}.jpg', image)    
        except:
            file_name = 'no_number'
            cv2.imwrite('./results/no_number.jpg', image)
    label = 0
    try:
        label = int(file_name.replace("_", ""))
    except:
        label = 0
    # return file_name
    return {
        "image": f"{image_path}",
		"verified": str(validate_number(file_name)),  
		"annotations": [
			{
				"label": int(label),
				"coordinates": {   
					"x": float(x),             
					"y": float(y),        
					"width": float(w),
					"height": float(h)
				},
                "numbers": number_labels
			}
		]
    }
        
        
        

if __name__ == "__main__":
    DATASET_PATH = "./test_dataset/dataset"
    accuricy = []
    model = YOLO('bestv2.pt')
    model_numbers = torch.hub.load('ultralytics/yolov5', 'custom', path='best-11.pt') 
    image_paths = os.listdir(DATASET_PATH)
    image_counter = 0
    for image_path in image_paths:
        image = cv2.imread(f"{DATASET_PATH}/{image_path}")
        labels = main(model, model_numbers, image, image_path)
        print(labels)
        print("THEIR: ", image_path)
        print("OUR: ", labels["image"])
        if image_path == labels["image"]:
           accuricy.append(1)
        else:
           accuricy.append(0)
        
        print("acc: ", np.array(accuricy).mean())