import cv2
from ultralytics import YOLO
import yaml
import time

# Function to load class names from data.yaml
def load_class_names(data_yaml):
    with open(data_yaml) as f:
        data = yaml.safe_load(f)
    return data['names']

# Function to perform object detection on webcam feed and display annotations
def detect_web(model_path, data_yaml):
    # Load the trained YOLOv8 model
    model = YOLO(model_path)

    # Load class names
    class_names = load_class_names(data_yaml)

    # Open a connection to the webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to capture image.")
            break

        # Perform object detection
        results = model(frame)

        # Draw bounding boxes and labels on the frame
        for result in results:
            boxes = result.boxes
            for box in boxes:
                conf = box.conf[0].item()  # Confidence score
                label_idx = box.cls[0].item()  # Class index
                label_name = class_names[label_idx]  # Map index to class name from data.yaml
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates

                # Draw the bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Put the label and confidence score
                label = f"{label_name} {conf:.2f}"
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the frame with annotations
        cv2.imshow('Webcam - Object Detection', frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

# Example usage
if __name__ == "__main__":
    model_path = r'runs\detect\train\weights\best.pt'  # Path to the YOLOv8 model weights
    data_yaml = r'dataset\data.yaml'  # Path to your data.yaml file
    detect_web(model_path, data_yaml)
