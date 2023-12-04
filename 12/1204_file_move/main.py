import os, sys, shutil
import pandas as pd
from collections import defaultdict
from tqdm import tqdm

def readfiles(dir):
    file_dict = defaultdict(list)

    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            
            file_path = os.path.join(root, file)
        
            file_dict[file] = file_path
    return file_dict

def makeOutputPath(file_path, file_dir, output_dir, Ext):
    root, file = os.path.split(file_path)
    filename, ext = os.path.splitext(file)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, f"{filename}{Ext}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path

if __name__ == "__main__":
    _, input_dir, csv_dir, output_dir = sys.argv
    
    file_dict = readfiles(input_dir)
    df = pd.read_csv(csv_dir, encoding='utf-8')
    
    file_list = df['filename'].values
    
    for filename in tqdm(file_list):
        file_path = file_dict[filename]
        ext = os.path.splitext(file_path)[-1]
        output_file_path = makeOutputPath(file_path, input_dir, output_dir, ext)
        shutil.move(file_path, output_file_path)