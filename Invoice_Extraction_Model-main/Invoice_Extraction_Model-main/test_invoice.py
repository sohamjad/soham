import cv2
import yaml
from ultralytics import YOLO
import os
import pytesseract
import numpy as np
from pdf2image import convert_from_path  # Use pdf2image for PDF processing
import matplotlib.pyplot as plt
import csv
import time  # For generating unique CSV filenames

# Function to load class names from data.yaml
def load_class_names(data_yaml):
    with open(data_yaml) as f:
        data = yaml.safe_load(f)
    return data['names']

# Extract images from PDF using pdf2image
def extract_images_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)  # Convert PDF pages to images
    return [cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR) for img in images]  # Convert to OpenCV BGR format

# Detect objects and perform OCR on an image
def detect_image(img, data_yaml, model, ocr_results, image_name):
    class_names = load_class_names(data_yaml)
    results = model(img)

    for result in results:
        boxes = result.boxes
        for box in boxes:
            conf = box.conf[0].item()  # Confidence score
            label_idx = box.cls[0].item()  # Class index
            label_name = class_names[label_idx]  # Map index to class name
            
            # Get bounding box coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            
            # Draw bounding box and label on the image
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, f"{label_name} {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Crop the bounding box area for OCR
            cropped_img = img[y1:y2, x1:x2]

            # Perform OCR on the cropped area
            try:
                ocr_text = pytesseract.image_to_string(cropped_img, config='--psm 6')
                ocr_text = ocr_text.replace('\n', ' ')
                ocr_results.append([image_name, label_name, ocr_text])
            except Exception as e:
                print(f"OCR failed for {label_name}: {e}")

    return img

# Save OCR results to a uniquely named CSV file
def save_ocr_results_to_csv(ocr_results, input_name):
    # Ensure the directory exists
    ocr_results_dir = "ocr_results"
    if not os.path.exists(ocr_results_dir):
        try:
            os.makedirs(ocr_results_dir)
        except Exception as e:
            print(f"Error creating directory: {e}")
            return

    # Generate a unique CSV file name based on input name and timestamp
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    csv_file = os.path.join(ocr_results_dir, f"ocr_results_{input_name}_{timestamp}.csv")
    
    try:
        with open(csv_file, mode="w", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            # Write header
            writer.writerow(["Image Name", "Class Name", "OCR Text"])  # CSV header

            # Write OCR results to the CSV file
            for row in ocr_results:
                writer.writerow(row)

        print(f"OCR results saved to {csv_file}")
    except PermissionError as e:
        print(f"Permission error: {e}")
    except Exception as e:
        print(f"Error writing to CSV: {e}")

# Process single image
def process_single_image(image_path, data_yaml, model):
    img = cv2.imread(image_path)
    ocr_results = []
    img_with_detections = detect_image(img, data_yaml, model, ocr_results, os.path.basename(image_path))
    save_ocr_results_to_csv(ocr_results, os.path.basename(image_path).split('.')[0])
    display_image(img_with_detections)

# Process multiple images
def process_multiple_images(image_paths, data_yaml, model):
    ocr_results = []
    for image_path in image_paths:
        img = cv2.imread(image_path)
        img_with_detections = detect_image(img, data_yaml, model, ocr_results, os.path.basename(image_path))
        display_image(img_with_detections)
    save_ocr_results_to_csv(ocr_results, "multiple_images")

# Display image with bounding boxes and OCR results
def display_image(img):
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

# Process PDF input
def process_pdf(pdf_path, data_yaml, model):
    images = extract_images_from_pdf(pdf_path)
    ocr_results = []

    for i, img in enumerate(images):
        img_with_detections = detect_image(img, data_yaml, model, ocr_results, f"{os.path.basename(pdf_path)}_page_{i+1}")
        display_image(img_with_detections)

    save_ocr_results_to_csv(ocr_results, os.path.basename(pdf_path).split('.')[0])

# Main function to handle different input types
def main():
    # Get input type from user
    input_type = input("Enter input type (image, images, pdf): ").strip().lower()

    # Get input path from user
    input_path = input("Enter the file path: ").strip()

    data_yaml = r'dataset\data.yaml'  # Path to your data.yaml file
    model_path = r'runs\detect\train\weights\best.pt'  # Path to the YOLOv8 model weights
    model = YOLO(model_path)

    if input_type == "image":
        process_single_image(input_path, data_yaml, model)
    elif input_type == "images":
        image_paths = input_path.split(",")  # Multiple image paths separated by commas
        process_multiple_images(image_paths, data_yaml, model)
    elif input_type == "pdf":
        process_pdf(input_path, data_yaml, model)
    else:
        print("Unsupported input type. Please choose from 'image', 'images', or 'pdf'.")

if __name__ == "__main__":
    main()
