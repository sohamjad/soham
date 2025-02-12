# Import opencv
import cv2 

# Import uuid
import uuid

# Import Operating System
import os

# Import time
import time

labels = ['office']
number_imgs = 15

IMAGES_PATH = os.path.join('Data', 'images', 'collectedimages')


if not os.path.exists(IMAGES_PATH):
    if os.name == 'posix':
        os.makedirs(IMAGES_PATH, exist_ok=True)
    if os.name == 'nt':
        os.makedirs(IMAGES_PATH, exist_ok=True)
for label in labels:
    path = os.path.join(IMAGES_PATH, label)
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

# Add a delay of 10 seconds before starting the image collection
print("Starting image collection in 5 seconds...")
time.sleep(5)        

for label in labels:
    cap = cv2.VideoCapture(0)
    print('Collecting images for {}'.format(label))
    time.sleep(5)
    for imgnum in range(number_imgs):
        print('Collecting image {}'.format(imgnum))
        ret, frame = cap.read()
        imgname = os.path.join(IMAGES_PATH,label,label+'.'+'{}.jpg'.format(str(uuid.uuid1())))
        cv2.imwrite(imgname, frame)
        cv2.imshow('frame', frame)
        time.sleep(2)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()        
