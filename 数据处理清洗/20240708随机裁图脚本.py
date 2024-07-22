import os
import random
from PIL import Image
from tqdm import tqdm

def get_random_crop_box(image_width, image_height):
    min_size = 2400
    max_width = image_width - min_size
    max_height = image_height - min_size

    left = random.randint(0, max_width)
    upper = random.randint(0, max_height)
    right = random.randint(left + min_size, image_width)
    lower = random.randint(upper + min_size, image_height)

    return (left, upper, right, lower)

def get_unique_filename(output_dir, base_name):
    counter = 1
    new_name = base_name
    while os.path.exists(os.path.join(output_dir, new_name)):
        new_name = f"{os.path.splitext(base_name)[0]}({counter}){os.path.splitext(base_name)[1]}"
        counter += 1
    return new_name

def crop_image(input_path, output_dir):
    with Image.open(input_path) as img:
        image_width, image_height = img.size
        for i in range(4):
            crop_box = get_random_crop_box(image_width, image_height)
            cropped_img = img.crop(crop_box)
            base_name = f"{os.path.splitext(os.path.basename(input_path))[0]}_crop_{i+1}.png"
            unique_name = get_unique_filename(output_dir, base_name)
            output_path = os.path.join(output_dir, unique_name)
            cropped_img.save(output_path)

def batch_crop_images(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    image_files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    total_files = len(image_files)

    with tqdm(total=total_files, desc="Processing images", unit="file") as pbar:
        for file_name in image_files:
            input_path = os.path.join(input_dir, file_name)
            crop_image(input_path, output_dir)
            pbar.update(1)

if __name__ == "__main__":
    input_dir = input("请输入图像文件夹路径: ")
    output_dir = input("请输入保存文件夹路径: ")

    batch_crop_images(input_dir, output_dir)
