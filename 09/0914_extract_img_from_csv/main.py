import os, sys
import logging
import pandas as pd
import numpy as np
import shutil
from tqdm import tqdm
from collections import defaultdict

def make_logger(log):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    # formatter
    file_formatter = logging.Formatter("%(asctime)s [%(levelname)s:%(lineno)d] -- %(message)s")
    # file_handler
    file_handler = logging.FileHandler(log, mode='w')
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)
    # logger.add
    logger.addHandler(file_handler)
    
    return logger

def readfiles(dir, Ext):
    file_dict = defaultdict(str)
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext == Ext:
                file_path = os.path.join(root, file)

                file_dict[filename] = file_path
    return file_dict

def make_output_folder(input_path, file_path, output_path):
    root, file = os.path.split(file_path)
    mid = '\\'.join(root.split('\\')[len(input_path.split('\\')):])
    folder= os.path.join(output_path, mid)
    os.makedirs(folder, exist_ok=True)
    return folder

def shutil_file(file_dict, filename, ext, num=None):
    if type(num) == int:
        for i in range(num):
            new_filename = f"{filename}_{i+1}"
            input_file_path = file_dict.get(new_filename)
            if input_file_path:
                folder = make_output_folder(img_dir, input_file_path, output_dir)
                output_file_path = os.path.join(folder, f"{new_filename}{ext}")
                shutil.copy2(input_file_path, output_file_path)
            
    elif num == None:
        new_filename = f"{filename}_{2}"
        input_file_path = file_dict.get(filename)
        if input_file_path:
            folder = make_output_folder(img_dir, input_file_path, output_dir)
            output_file_path = os.path.join(folder, f"{new_filename}{ext}")
            shutil.copy2(input_file_path, output_file_path)
        
def extract_file(x, img_dict):
    logger.info(x)
    filename = x.loc[1]
    if pd.isna(x.loc[3]) == True and x.loc[2] == 2:
        shutil_file(img_dict, filename, '.jpg', 2)
    elif pd.isna(x.loc[3]) == True and x.loc[2] == 1:
        shutil_file(img_dict, filename, '.jpg', 1)
    elif x.loc[3] == 'O' and pd.isna(x.loc[4]) == True and x.loc[2] == 2:
        shutil_file(img_dict, filename, '.jpg')
     
_, img_dir, csv_dir, output_dir = sys.argv

logger = make_logger('log.log')

img_dict = readfiles(img_dir, '.jpg')

tqdm.pandas()

df = pd.read_csv(csv_dir, encoding='utf-8', header=None)

df.progress_apply(extract_file, axis=1, args=(img_dict,))



