### Simple script to count the photos in various subfolders of a directory
### and copy a selection of photos to a new directory, 
### based on a CSV file with selected photo names

import os
import csv
import shutil
import pandas as pd

def count_photos(directory, max_depth=3):
    photo_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
    photo_count = 0

    for root, dirs, files in os.walk(directory):
        # Calculate the current depth
        depth = root[len(directory):].count(os.sep)
        if depth < max_depth:
            for file in files:
                if any(file.lower().endswith(ext) for ext in photo_extensions):
                    photo_count += 1

    return photo_count

def read_photo_selection(csv_file):
    df = pd.read_csv(csv_file, encoding='utf-8').dropna(axis=1, how='all')
    day1_photos = df['Day 1'].dropna().tolist()
    day2_photos = df['Day 2'].dropna().tolist()
    day3_photos = df['Day 3'].dropna().tolist()

    return day1_photos, day2_photos, day3_photos

def copy_photos(photo_list, source_directory, destination_directory):
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    for photo in photo_list:
        for root, dirs, files in os.walk(source_directory):
            for file in files:
                file_name, file_ext = os.path.splitext(file)
                if photo == file_name:
                    source_path = os.path.join(root, file)
                    destination_path = os.path.join(destination_directory, file)
                    shutil.copy2(source_path, destination_path)
                    break

if __name__ == "__main__":
    directory = "./Foto Cybo_"
    total_photos = count_photos(directory)
    print(f"Total number of photos in '{directory}': {total_photos}")

    csv_file = "Selezione foto.csv"
    day1_photos, day2_photos, day3_photos = read_photo_selection(csv_file)

    copy_photos(day1_photos, directory, "./Foto Cybo_/Day1_choice")
    copy_photos(day2_photos, directory, "./Foto Cybo_/Day2_choice")
    copy_photos(day3_photos, directory, "./Foto Cybo_/Day3_choice")