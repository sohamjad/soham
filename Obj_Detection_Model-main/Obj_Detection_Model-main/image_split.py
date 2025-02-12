import os
import shutil
import random

def remove_directory(directory):
    """Remove the directory and all its contents."""
    if os.path.exists(directory):
        shutil.rmtree(directory)
        print(f"Removed {directory}")

def clean_directories(directory, keep_folders):
    """Remove all files and directories in 'directory' except for those in 'keep_folders'."""
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if item not in keep_folders:
            if os.path.isdir(item_path):
                remove_directory(item_path)
            else:
                os.remove(item_path)

# Set the paths to the original images and labels folders
images_folder = 'dataset/images'
labels_folder = 'dataset/labels'

# Set the paths to the output folders
train_images_folder = os.path.join(images_folder, 'train')
val_images_folder = os.path.join(images_folder, 'val')
test_images_folder = os.path.join(images_folder, 'test')
train_labels_folder = os.path.join(labels_folder, 'train')
val_labels_folder = os.path.join(labels_folder, 'val')
test_labels_folder = os.path.join(labels_folder, 'test')

# Create the output folders if they don't exist
os.makedirs(train_images_folder, exist_ok=True)
os.makedirs(val_images_folder, exist_ok=True)
os.makedirs(test_images_folder, exist_ok=True)
os.makedirs(train_labels_folder, exist_ok=True)
os.makedirs(val_labels_folder, exist_ok=True)
os.makedirs(test_labels_folder, exist_ok=True)

# Get the list of image files and their corresponding label files
image_files = [f for f in os.listdir(images_folder) if f.endswith('.jpg') or f.endswith('.png')]
label_files = [f for f in os.listdir(labels_folder) if f.endswith('.txt')]

# Ensure every image has a corresponding label
image_files.sort()
label_files.sort()
assert len(image_files) == len(label_files), "Mismatch between number of images and labels"

# Create a dictionary for fast lookup of labels
label_dict = {os.path.splitext(label)[0]: label for label in label_files}

# Filter out images that do not have corresponding labels
filtered_image_files = [img for img in image_files if os.path.splitext(img)[0] in label_dict]

# Shuffle the images to randomize the split
random.shuffle(filtered_image_files)

# Calculate the indices for train, val, and test splits
total_images = len(filtered_image_files)
train_idx = int(0.9 * total_images)
val_idx = int(0.95 * total_images)

# Split the data into train, val, and test sets
train_images = filtered_image_files[:train_idx]
val_images = filtered_image_files[train_idx:val_idx]
test_images = filtered_image_files[val_idx:]

# Debug print statements
print(f"Total images: {total_images}")
print(f"Train images: {len(train_images)}")
print(f"Val images: {len(val_images)}")
print(f"Test images: {len(test_images)}")

# Copy the files to their corresponding folders
def copy_files(image_list, src_img_folder, src_label_folder, dst_img_folder, dst_label_folder):
    for img in image_list:
        label = label_dict[os.path.splitext(img)[0]]
        src_img_path = os.path.join(src_img_folder, img)
        dst_img_path = os.path.join(dst_img_folder, img)
        src_label_path = os.path.join(src_label_folder, label)
        dst_label_path = os.path.join(dst_label_folder, label)
        
        # Debug print statements
        print(f"Copying {src_img_path} to {dst_img_path}")
        print(f"Copying {src_label_path} to {dst_label_path}")
        
        shutil.copy(src_img_path, dst_img_path)
        shutil.copy(src_label_path, dst_label_path)

# Copy files to train, val, and test folders
copy_files(train_images, images_folder, labels_folder, train_images_folder, train_labels_folder)
copy_files(val_images, images_folder, labels_folder, val_images_folder, val_labels_folder)
copy_files(test_images, images_folder, labels_folder, test_images_folder, test_labels_folder)

print("Dataset split complete!")

# Clean up the images and labels folders, keeping only train, val, and test directories
clean_directories(images_folder, ['train', 'val', 'test'])
clean_directories(labels_folder, ['train', 'val', 'test'])
