import cv2
import yaml
from ultralytics import YOLO
import os
import pytesseract
import numpy as np
from pdf2image import convert_from_path  # Use pdf2image for PDF processing
import matplotlib.pyplot as plt

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
def detect_image(img, data_yaml, model, ocr_results):
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

            # Save OCR results
            try:
                ocr_text = pytesseract.image_to_string(cropped_img, config='--psm 6')
                ocr_text = ocr_text.replace('\n', ' ')
                if label_name not in ocr_results:
                    ocr_results[label_name] = []
                ocr_results[label_name].append(ocr_text)
            except Exception as e:
                print(f"OCR failed for {label_name}: {e}")

    return img

# Save OCR results to text files
def save_ocr_results(ocr_results):
    if not os.path.exists("ocr_results"):
        os.makedirs("ocr_results")
    
    for class_name, texts in ocr_results.items():
        with open(f"ocr_results/{class_name}.txt", "w", encoding="utf-8") as f:
            for text in texts:
                f.write(text + "\n")

# Process single image
def process_single_image(image_path, data_yaml, model):
    img = cv2.imread(image_path)
    ocr_results = {}
    img_with_detections = detect_image(img, data_yaml, model, ocr_results)
    save_ocr_results(ocr_results)
    display_image(img_with_detections)

# Process multiple images
def process_multiple_images(image_paths, data_yaml, model):
    ocr_results = {}
    for image_path in image_paths:
        img = cv2.imread(image_path)
        img_with_detections = detect_image(img, data_yaml, model, ocr_results)
        display_image(img_with_detections)
    save_ocr_results(ocr_results)

# Display image with bounding boxes and OCR results
def display_image(img):
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

# Detect objects in a video and display frames with bounding boxes (from provided video code)
def detect_video(video_path, model_path, data_yaml):
    # Load the trained model
    model = YOLO(model_path)  # Path to the best weights after training

    # Load class names
    class_names = load_class_names(data_yaml)

    # Initialize the video capture
    cap = cv2.VideoCapture(video_path)

    # Define the size of the output window
    window_name = 'Video'
    window_width, window_height = 640, 480
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, window_width, window_height)

    while True:
        ret, img = cap.read()
        if not ret:
            break

        # Perform inference
        results = model(img)

        # Draw bounding boxes and labels on the image
        for result in results:
            boxes = result.boxes
            for box in boxes:
                conf = box.conf[0].item()  # Confidence score
                label_idx = box.cls[0].item()  # Class index
                label_name = class_names[label_idx]  # Map index to class name from data.yaml
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates

                # Draw the bounding box
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Put the label and confidence score
                label = f"{label_name} {conf:.2f}"
                cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Resize the frame to fit the window
        img_resized = cv2.resize(img, (window_width, window_height))

        # Display the frame
        cv2.imshow(window_name, img_resized)

        # Check if 'q' key is pressed to stop the video
        if cv2.waitKey(500) & 0xFF == ord('q'):  # 500 ms delay
            break

    # Release the video capture object and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

    # Return a message for successful processing
    return "Video processed successfully"

# Process video input
def process_video(video_path, model_path, data_yaml):
    return detect_video(video_path, model_path, data_yaml)

# Process PDF input
def process_pdf(pdf_path, data_yaml, model):
    images = extract_images_from_pdf(pdf_path)
    ocr_results = {}

    for img in images:
        img_with_detections = detect_image(img, data_yaml, model, ocr_results)
        display_image(img_with_detections)

    save_ocr_results(ocr_results)

# Main function to handle different input types
def main():
    # Get input type from user
    input_type = input("Enter input type (image, images, video, pdf): ").strip().lower()

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
    elif input_type == "video":
        print(process_video(input_path, model_path, data_yaml))
    elif input_type == "pdf":
        process_pdf(input_path, data_yaml, model)
    else:
        print("Unsupported input type. Please choose from 'image', 'images', 'video', or 'pdf'.")

if __name__ == "__main__":
    main()
