import os, sys, logging, shutil
import pandas as pd
from collections import defaultdict
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

def readfiles(dir):
    file_dict = defaultdict(list)

    for root, dirs, files in os.walk(dir):
        for file in files:
            path = os.path.join(root, file)
            file_dict[os.path.split(root)[-1]].append(path)
    return file_dict

def makeOutputPath(file_path, file_dir, output_dir):
    root, file = os.path.split(file_path)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, file)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path

def file_copy(path):
    copy_path = makeOutputPath(path, input_dir, output_dir)
    shutil.copy2(path, copy_path)
    
        
if __name__ == "__main__":
    _, csv_dir, input_dir, output_dir = sys.argv

    
    df = pd.read_csv(csv_dir, header=None)
    seq_list = df[0].values
    
    parent_dir = os.listdir(input_dir)
    file_dict = {}
    for dir in tqdm(parent_dir, desc='read files'):
        
        path = os.path.join(input_dir, dir)
        if '001_OG_DB' in os.listdir(path):
            path = os.path.join(path, '001_OG_DB')
        

        file_dict.update(readfiles(path))
    
    for seq in tqdm(seq_list, desc='copy files'):
        file_list = file_dict.get(seq)
        if file_list:
            [file_copy(file) for file in file_list ]
        else:
            print(seq, "없습니다")

    
    