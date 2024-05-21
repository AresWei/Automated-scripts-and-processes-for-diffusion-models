# Function: Ensured that the number of images in each subdirectory was at least 15, achieving this goal by copying existing images, and logging any errors encountered during processing

import os
import shutil
import logging
from tqdm import tqdm

# 设置日志记录
def setup_logging():
    logging.basicConfig(filename='buglogs.log', level=logging.ERROR,
                        format='%(asctime)s:%(levelname)s:%(message)s')

# 判断文件是否为图片
def is_image_file(filename):
    return any(filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff'])

# 获取新的文件名，如果文件名重复则在后面加上序号
def get_new_filename(directory, filename):
    name, ext = os.path.splitext(filename)
    counter = 1
    new_filename = f"{name}({counter}){ext}"
    while os.path.exists(os.path.join(directory, new_filename)):
        counter += 1
        new_filename = f"{name}({counter}){ext}"
    return new_filename

# 复制图片使其数量达到15张
def duplicate_images(directory):
    images = [f for f in os.listdir(directory) if is_image_file(f)]
    count = len(images)
    if count < 15: # You can set this parameter according to the actual situation
        target_count = 15 # You can set this parameter according to the actual situation
        for i in range(target_count - count):
            for img in images:
                if len(os.listdir(directory)) >= target_count:
                    break
                new_img_name = get_new_filename(directory, img)
                shutil.copy(os.path.join(directory, img), os.path.join(directory, new_img_name))

# 遍历和处理图片文件夹
def traverse_and_process_images(root_directory):
    setup_logging()
    try:
        for root, dirs, files in os.walk(root_directory):
            image_files = [f for f in files if is_image_file(f)]
            image_count = len(image_files)
            print(f"目录: {root}, 图片数量: {image_count}")
            if image_count < 15: # You can set this parameter according to the actual situation, and ensure that this parameter is consistent with the quantity parameter above
                duplicate_images(root)
    except Exception as e:
        logging.error(f"处理目录 {root} 时出错: {str(e)}")

# 主函数
def main():
    root_directory = input("请输入要处理的目录路径: ")
    if not os.path.exists(root_directory):
        print("提供的目录路径不存在.")
        return

    total_directories = sum([len(dirs) for _, dirs, _ in os.walk(root_directory)])
    with tqdm(total=total_directories, desc="处理目录") as pbar:
        for root, dirs, _ in os.walk(root_directory):
            for d in dirs:
                traverse_and_process_images(os.path.join(root, d))
                pbar.update(1)

if __name__ == "__main__":
    main()
