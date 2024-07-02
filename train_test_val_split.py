import os
import random
import shutil

def create_directories(base_dir):
    dirs = ['images/train', 'images/val', 'images/test', 'labels/train', 'labels/val', 'labels/test']
    for d in dirs:
        os.makedirs(os.path.join(base_dir, d), exist_ok=True)

def split_data(images_dir, labels_dir, output_dir, train_ratio=0.7, val_ratio=0.2, test_ratio=0.1):
    images = [f for f in os.listdir(images_dir) if f.endswith('.jpg')]
    random.shuffle(images)

    train_split = int(train_ratio * len(images))
    val_split = int(val_ratio * len(images)) + train_split

    train_images = images[:train_split]
    val_images = images[train_split:val_split]
    test_images = images[val_split:]

    def copy_files(image_list, split):
        for img in image_list:
            img_path = os.path.join(images_dir, img)
            label_path = os.path.join(labels_dir, img.replace('.jpg', '.txt'))

            if os.path.exists(label_path):
                shutil.copy(img_path, os.path.join(output_dir, f'images/{split}', img))
                shutil.copy(label_path, os.path.join(output_dir, f'labels/{split}', img.replace('.jpg', '.txt')))

    copy_files(train_images, 'train')
    copy_files(val_images, 'val')
    copy_files(test_images, 'test')

# Paths
images_dir = 'corr_images'
labels_dir = 'data_1/labels_yolo_1'
output_dir = 'data'

# Create directories for train, val, and test splits
create_directories(output_dir)

# Split the data
split_data(images_dir, labels_dir, output_dir, train_ratio=0.3, val_ratio=0.2, test_ratio=0.7)
