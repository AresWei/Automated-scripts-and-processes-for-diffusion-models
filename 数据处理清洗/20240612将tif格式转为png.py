from PIL import Image
import os
from tqdm import tqdm

def convert_tiff_to_png(source_folder, target_folder):
    """
    将指定文件夹中的所有TIF或TIFF格式图片转换为PNG格式，并保存在目标文件夹。
    """
    # 检查目标文件夹是否存在，如果不存在则创建
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # 获取所有TIF或TIFF文件
    files = [f for f in os.listdir(source_folder) if f.lower().endswith(('.tif', '.tiff'))]

    # 用tqdm显示进度条
    for filename in tqdm(files, desc="转换进度"):
        file_path = os.path.join(source_folder, filename)
        # 防止文件重名，添加序号
        target_filename = os.path.splitext(filename)[0] + '.png'
        target_file_path = os.path.join(target_folder, target_filename)
        counter = 1
        # 如果文件已存在，则修改文件名
        while os.path.exists(target_file_path):
            target_filename = f"{os.path.splitext(filename)[0]}({counter}).png"
            target_file_path = os.path.join(target_folder, target_filename)
            counter += 1

        # 打开并转换图像
        with Image.open(file_path) as img:
            img.save(target_file_path, "PNG")

    print("所有文件转换完毕！")


# 用户输入源文件夹和目标文件夹的路径
source_folder = input("请输入源文件夹的路径：")
target_folder = input("请输入目标文件夹的路径：")

# 调用函数
convert_tiff_to_png(source_folder, target_folder)
