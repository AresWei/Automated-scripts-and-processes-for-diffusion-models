import os
import re
import pandas as pd
from tqdm import tqdm

def find_images(directory, recursive):
    """
    遍历指定目录，查找所有图片文件。
    """
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}
    images = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in image_extensions):
                images.append(os.path.join(root, file))

        if not recursive:
            break

    return images

def process_filename(filename):
    """
    处理文件名：删除特定部分并替换字符。
    """
    name, ext = os.path.splitext(filename)
    new_name = re.sub(r'^[^_]*_', '', name)
    new_name = re.sub(r'(_[^_]*){2}$', '', new_name)
    new_name = new_name.replace('_', ' ')
    return new_name + ext

def add_sequence_if_exists(new_path):
    """
    如果文件已存在，则在文件名后添加一个序号 (1), (2), (3), ...
    """
    base, extension = os.path.splitext(new_path)
    counter = 1
    while os.path.exists(new_path):
        new_path = f"{base} ({counter}){extension}"
        counter += 1
    return new_path

def rename_files_with_sequence(directory, original_names, new_names):
    """
    重命名文件，并在遇到重名时添加序号。
    """
    for original_name, new_name in zip(original_names, new_names):
        old_path = os.path.join(directory, original_name)
        new_path = os.path.join(directory, new_name)
        if os.path.exists(old_path):
            new_path = add_sequence_if_exists(new_path)
            os.rename(old_path, new_path)

def main():
    try:
        directory_to_search = input("请输入要搜索的目录路径: ").strip()
        directory_to_search = directory_to_search.replace('\\', '/')

        if not os.path.isdir(directory_to_search):
            print("输入的路径不是有效的目录，请重新输入。")
            return

        recursive_search = input("是否递归搜索子目录? (y/n): ").lower() == 'y'
        user_prefix = input("请输入要添加到文件名前面的词（可留空）: ")

        image_paths = find_images(directory_to_search, recursive_search)
        original_names = [os.path.basename(path) for path in image_paths]
        processed_names = [process_filename(name) for name in original_names]
        names_without_extension = [os.path.splitext(name)[0] for name in processed_names]

        df = pd.DataFrame({'Original Name': names_without_extension, 'New Name': names_without_extension})
        excel_path = os.path.join(directory_to_search, 'rename_images.xlsx')
        df.to_excel(excel_path, index=False)
        print(f"已创建Excel文件：{excel_path}。请编辑'New Name'列，然后保存并关闭Excel文件。")

        input("编辑完毕后请按Enter继续...")

        df = pd.read_excel(excel_path)
        new_names = [name + os.path.splitext(original_name)[1] for name, original_name in
                     zip(df['New Name'].tolist(), original_names)]

        if user_prefix:
            new_names = [f"{user_prefix} {name}" for name in new_names]

        for i in tqdm(range(len(image_paths)), desc="重命名进度"):
            rename_files_with_sequence(os.path.dirname(image_paths[i]), [original_names[i]], [new_names[i]])

        print("文件重命名完成。")
    except Exception as e:
        print(f"程序运行中发生错误: {e}")

if __name__ == "__main__":
    main()
