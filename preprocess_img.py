from PIL import Image
import numpy as np
import os

def average_pixel(image):
    # Convert image to a numpy array
    pixels = np.array(image)
    # Calculate the average pixel value
    avg_pixel = np.mean(pixels, axis=(0, 1))
    return avg_pixel

def subtract_pixels(image, average_pixel):
    # Convert image to numpy array
    img_array = np.array(image, dtype=np.int16)  # Use int16 to prevent overflow
    # Subtract average pixel from all pixels
    result_array = img_array - average_pixel
    # Ensure no pixel values are negative
    result_array[result_array < 0] = 0
    return Image.fromarray(result_array.astype(np.uint8))

def process_image(input_path, output_path):
    # Open the image
    image = Image.open(input_path)
    # Find the average pixel
    avg_pixel = average_pixel(image)
    # Subtract the average pixel from all pixels
    result_image = subtract_pixels(image, avg_pixel)
    # Save the resulting image
    result_image.save(output_path)

def process_images_in_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            process_image(input_path, output_path)
            print(f'Processed {filename}')


if __name__ == "__main__":
    input_folder_path = r"data\images\train"  
    output_folder_path = r"train"  
    process_images_in_folder(input_folder_path, output_folder_path)
    print("DONE <3")
