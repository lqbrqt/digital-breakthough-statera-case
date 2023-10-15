from ultralytics import YOLO
import wandb


 
wandb.init(entity="magika_dgtu")
# Load the model.
model = YOLO('yolov8m.pt')

# Training.
results = model.train(
   data='t.yaml',
   imgsz=640,
   epochs=80,
   batch=16,
   name='yolov8m_custom_v_0.4',
   workers=0,
   )