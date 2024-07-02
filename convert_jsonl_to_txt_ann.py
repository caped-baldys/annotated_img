import os
import json
import shutil
import random

# Mapping of label strings to class indices
label_map = {
    'Scratch': 0,
    'Dirt': 1,
    'Bird Dropping': 2,
    'Rust': 3,
    'Dent': 4,
    'Broken': 5
}

def convert_bbox_to_yolo(size, bbox):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (bbox['x'] + bbox['width'] / 2.0) * dw
    y = (bbox['y'] + bbox['height'] / 2.0) * dh
    w = bbox['width'] * dw
    h = bbox['height'] * dh
    return (x, y, w, h)

def convert_jsonl_to_yolo(jsonl_file, output_dir, images_dir, img_size):
    os.makedirs(output_dir, exist_ok=True)

    with open(jsonl_file, 'r') as f:
        for line in f:
            data = json.loads(line)
            image_path = os.path.join(images_dir, data['filename'])
            image_size = img_size  # Assuming a fixed image size for simplicity

            yolo_annotations = []
            for ann in data['bbox']:
                if ann['label'] in label_map:
                    class_id = label_map[ann['label']]
                    bbox_yolo = convert_bbox_to_yolo(image_size, ann)
                    yolo_annotations.append(f"{class_id} {bbox_yolo[0]} {bbox_yolo[1]} {bbox_yolo[2]} {bbox_yolo[3]}")
            
            label_file = os.path.join(output_dir, data['filename'].replace('.jpg', '.txt'))
            with open(label_file, 'w') as out_f:
                out_f.write("\n".join(yolo_annotations))

jsonl_file = 'labels/all_corr.jsonl'
output_dir = 'data_1/labels_yolo_1'
images_dir = 'corr_images'
img_size = (640, 480)  # Replace with the actual size of your images

os.makedirs(output_dir, exist_ok=True)

convert_jsonl_to_yolo(jsonl_file, output_dir, images_dir, img_size)