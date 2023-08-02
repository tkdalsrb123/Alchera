import os, sys
import pandas as pd
import shutil

def make_df(dir):
    file_info = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext == '.jpg':
                file_path = os.path.join(root, file)
                filename_split = filename.split('_')
                category = '_'.join(filename_split[:4])
                file_idx = int(filename_split[-1])
                file_info.append([file_path, category, file_idx])
    df = pd.DataFrame(file_info, columns=['filepath', 'category', 'num'])

    return df

def file_extract(df, Category, minidx, maxidx):
    df = df[df['category'] == Category]

    for i in range(minidx, maxidx, 3):
        if minidx%3 == 0:
            extract_num = ((((i//3)-1) * 30) + 2) - 1
        else:
            extract_num = ((((i//3)) * 30) + (minidx%3)) - 1
        extract_num1 = extract_num + 10
        extract_num2 = extract_num + 20
        copyfile(df, extract_num)
        copyfile(df, extract_num1)
        copyfile(df, extract_num2)

def copyfile(df, num):
    extract_file = df.loc[df['num'] == num, 'filepath']
    extract_file = extract_file.values[0]
    root, file = os.path.split(extract_file)
    folder_name = '_'.join(file.split('_')[:3])
    folder = os.path.join(output_dir, folder_name)
    output_path = os.path.join(folder, file)
    os.makedirs(folder, exist_ok=True)
    shutil.copy2(extract_file, output_path)
    print(output_path)
    
_, old_db_dir, new_db_dir, output_dir, mode_num = sys.argv

old_db_df = make_df(old_db_dir)
new_db_df = make_df(new_db_dir)

category_list = old_db_df['category'].unique()
if mode_num == '0':
    for category in category_list:
        min_idx = old_db_df.loc[old_db_df['category'] == category, 'num'].min()
        max_idx = old_db_df.loc[old_db_df['category'] == category, 'num'].max()
        
        if min_idx%3 == 1:
            file_extract(new_db_df, category, min_idx, max_idx)
        elif min_idx%3 == 2:
            file_extract(new_db_df, category, min_idx, max_idx)
        elif min_idx%3 == 0:
            file_extract(new_db_df, category, min_idx, max_idx)

elif mode_num == '1': 
    for category in category_list:
        min_idx = old_db_df.loc[old_db_df['category'] == category, 'num'].min()
        max_idx = old_db_df.loc[old_db_df['category'] == category, 'num'].max()
        
        if min_idx%3 == 1:
            file_extract(new_db_df, category, min_idx, max_idx)
        elif min_idx%3 == 2:
            min_idx = min_idx + 2
            file_extract(new_db_df, category, min_idx, max_idx)
        elif min_idx%3 == 0:
            min_idx = min_idx + 1
            file_extract(new_db_df, category, min_idx, max_idx)