from ultralytics import YOLO
import os

# Define the absolute paths
model_path = os.path.abspath('yolov8n.pt')
data_yaml_path = os.path.abspath('dataset/data.yaml')

# Load the YOLOv8 model
model = YOLO(model_path)

# Train the model using the data.yaml from the 'dataset' folder
model.train(data=data_yaml_path, epochs=100, imgsz=640)
