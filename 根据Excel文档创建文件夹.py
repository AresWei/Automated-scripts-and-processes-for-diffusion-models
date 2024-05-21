import pandas as pd
import os
import shutil
from tqdm import tqdm

def create_folders_from_excel(excel_file_path, base_path):
    # Read the Excel file
    excel_data = pd.read_excel(excel_file_path, sheet_name=None)

    # Function to create directories
    def create_directories(base, sheet_name, categories):
        sheet_path = os.path.join(base, f"{sheet_name}")
        if not os.path.exists(sheet_path):
            os.makedirs(sheet_path)

        for category in tqdm(categories, desc=f"Creating folders in {sheet_name}"):
            # Check if the category has at least 2 elements (Chinese and English names)
            if len(category) > 1 and pd.notna(category[1]):
                # Folder name format: ChineseEnglish
                folder_name = f"{category[0]}{category[1]}"
            else:
                # If English name is missing, use Chinese name
                folder_name = category[0]

            folder_path = os.path.join(sheet_path, folder_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
        return sheet_path

    # Iterate through each sheet and create directories
    for sheet_name, data in tqdm(excel_data.items(), desc="Processing sheets"):
        categories = data.values.tolist()
        create_directories(base_path, sheet_name, categories)

    print("Folder creation process completed.")

def rename_folders_to_english_only(base_path):
    # Rename second-level directories to English only
    all_dirs = []
    for root, dirs, files in os.walk(base_path):
        for dir in dirs:
            all_dirs.append((root, dir))

    for root, dir in tqdm(all_dirs, desc="Renaming folders"):
        if '_' in dir:  # Checking for our 'ChineseEnglish' format
            new_name = dir.split('_')[-1]  # Taking only the English part
            os.rename(os.path.join(root, dir), os.path.join(root, new_name))

    print("Folder renaming process completed.")

# Example usage
excel_file_path = r"C:\Users\A\Desktop\AAA.xlsx"  # Replace with your Excel file path
base_path = r"C:\Users\A\Desktop\AAAAA"  # Replace with your desired base path

create_folders_from_excel(excel_file_path, base_path)
rename_folders_to_english_only(base_path)
