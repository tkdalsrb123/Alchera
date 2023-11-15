import os, sys, logging
import pandas as pd
import shutil
import random
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

def make_path(x):
    path = '\\'.join(x.iloc[:7])
    count = x.iloc[7]
    info.append((path, count))

if __name__ == '__main__':
    _, excel_dir, input_dir, output_dir = sys.argv

    info = []
    df = pd.read_excel(excel_dir)
    df.apply(make_path, axis=1)
    
    for i in tqdm(info):
        path = i[0]
        count = i[1]
        
        root = os.path.join(input_dir, path)
        file_list = os.listdir(root)
        
        select_files = random.sample(file_list, count)

        new_root = os.path.join(output_dir, path)
        os.makedirs(new_root, exist_ok=True)

        select_files = [(os.path.join(root, file), os.path.join(new_root, file)) for file in select_files]

        [shutil.copy2(file[0], file[1] ) for file in select_files]