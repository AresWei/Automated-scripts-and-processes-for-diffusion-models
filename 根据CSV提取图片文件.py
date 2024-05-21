import pandas as pd
import xlsxwriter
import os
from tqdm import tqdm
from PIL import Image

# 支持的图像格式
SUPPORTED_FORMATS = ('BMP', 'DIB', 'EPS', 'GIF', 'ICNS', 'ICO', 'IM', 'JPEG', 'JPG', 'MSP', 'PCX', 'PNG', 'PPM', 'SGI', 'SPIDER', 'TGA', 'TIFF', 'WebP', 'XBM')

# 从用户输入获取CSV文件路径
csv_file_path = input("请输入CSV文件的路径：")

# 检查路径是否存在
if not os.path.exists(csv_file_path) or not os.path.isfile(csv_file_path):
    raise Exception(f"无法找到文件: {csv_file_path}")

# 尝试读取CSV文件，指定不同的编码尝试解决可能的编码问题
try:
    image_paths = pd.read_csv(csv_file_path, encoding='utf-8', header=None).iloc[:, 0]
except UnicodeDecodeError:
    try:
        image_paths = pd.read_csv(csv_file_path, encoding='gbk', header=None).iloc[:, 0]
    except Exception as e:
        raise Exception(f"读取CSV文件时遇到错误: {e}")

# 创建一个新的Excel工作簿和工作表，启用ZIP64扩展，excel_output_path参数可修改
excel_output_path = '测试文档.xlsx'
workbook = xlsxwriter.Workbook(excel_output_path, {'use_zip64': True})
worksheet = workbook.add_worksheet()

# 初始化进度条
total_images = len(image_paths)
pbar = tqdm(total=total_images, unit='row', desc='Inserting images')

# 创建日志文件
log_file = open('image_load_errors.log', 'w', encoding='utf-8')

# 遍历图片路径并插入图片
for idx, image_path in enumerate(image_paths):
    try:
        # 尝试打开图像
        with Image.open(image_path) as im:
            # 检查图像格式是否受支持
            if im.format not in SUPPORTED_FORMATS:
                log_file.write(f"Unsupported image format: {image_path}\n")
                pbar.update(1)
                continue
    except Exception as e:
        log_file.write(f"Error opening image: {image_path}, {e}\n")
        pbar.update(1)
        continue

    # 将图片插入到工作表
    worksheet.insert_image(idx, 0, image_path, {'x_scale': 0.5, 'y_scale': 0.5})
    pbar.update(1)

# 关闭进度条、日志文件和工作簿
pbar.close()
log_file.close()
workbook.close()

print(f"完成! 图片已被添加到 {excel_output_path}")
print(f"日志文件 image_load_errors.log 包含无法正常读取的图像文件路径。")
