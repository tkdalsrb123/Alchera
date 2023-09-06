import os, sys
import pandas as pd
import shutil
import logging
from tqdm import tqdm

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

def readfiles(x, dir):
    file_list = []
    for root, dirs, files in os.walk(dir):
        if x in root:
            for file in files:    
                filename, ext = os.path.splitext(file)
                if 'ccan' in filename:
                    if ext == '.bin' or ext == '.timestamp':
                        file_path = os.path.join(root, file)
                        file_list.append(file_path)
    return file_list
          
_, input_dir, csv_dir, output_dir = sys.argv

logger = make_logger('log.log')

df = pd.read_csv(csv_dir, encoding='UTF-8')
file_series = df['filename'].apply(readfiles, args=(input_dir,))
file_lists = file_series.values

for file_list in tqdm(file_lists, desc='시퀀스', position=0):
    for file_path in tqdm(file_list, desc='파일', position=1):
        logger.info(file_path)
        root, file = os.path.split(file_path)
        mid = '\\'.join(root.split('\\')[len(input_dir.split('\\')):])
        folder = os.path.join(output_dir, mid)
        os.makedirs(folder, exist_ok=True)

        output_file_path = os.path.join(folder, file)
        logger.info(f"{output_file_path} 복사 !!")
        shutil.copy2(file_path, output_file_path)