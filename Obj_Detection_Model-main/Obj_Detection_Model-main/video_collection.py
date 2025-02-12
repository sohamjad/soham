# Import OpenCV
import cv2

# Import uuid
import uuid

# Import Operating System
import os

# Import time
import time

labels = ['office']
number_imgs = 15

IMAGES_PATH = os.path.join('Data', 'videos', 'collectedvideos')

if not os.path.exists(IMAGES_PATH):
    os.makedirs(IMAGES_PATH, exist_ok=True)

for label in labels:
    path = os.path.join(IMAGES_PATH, label)
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

# Add a delay of 10 seconds before starting the video collection
print("Starting video collection in 5 seconds...")
time.sleep(5)

def record_video(output_path, codec='XVID', fps=20.0, frame_size=(640, 480), duration=100):
    # Open a connection to the webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*codec)
    out = cv2.VideoWriter(output_path, fourcc, fps, frame_size)

    print("Recording started. Press 'q' to stop recording.")

    start_time = cv2.getTickCount()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Could not read frame.")
            break

        # Write the frame to the output file
        out.write(frame)

        # Display the resulting frame
        cv2.imshow('Webcam', frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Stop recording after the specified duration
        elapsed_time = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()
        if elapsed_time > duration:
            break

    # When everything is done, release the capture and writer
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("Recording finished.")

# Example usage
output_video_path = os.path.join(IMAGES_PATH, 'output.avi')
record_video(output_path=output_video_path, duration=100)
