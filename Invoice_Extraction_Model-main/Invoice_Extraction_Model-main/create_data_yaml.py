import yaml
import os

def create_data_yaml():
    classes_txt_path = 'dataset/classes.txt'  # Path to the classes.txt file

    data_yaml = {
        'names': {},
        'path': 'dataset',
        'train': 'images/train',
        'val': 'images/val',
        'test': 'images/test'
    }

    # Check if classes.txt file exists
    if not os.path.exists(classes_txt_path):
        print(f"Error: classes.txt file not found at {classes_txt_path}")
        return

    # Read class names from the classes.txt file
    with open(classes_txt_path, 'r') as file:
        class_names = file.read().splitlines()

    # Check if class names were read correctly
    if not class_names:
        print("Error: No class names found in classes.txt")
        return

    for index, class_name in enumerate(class_names):
        data_yaml['names'][index] = class_name

    folder_path = 'dataset'
    file_path = os.path.join(folder_path, 'data.yaml')

    # Ensure the folder exists
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Write data to data.yaml file
    with open(file_path, 'w') as file:
        yaml.dump(data_yaml, file, default_flow_style=False)

    print(f"data.yaml file created successfully at {file_path}")
    return file_path  # Return the file path for further use

# Example usage
if __name__ == "__main__":
    create_data_yaml()
