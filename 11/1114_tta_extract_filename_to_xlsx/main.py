import os, sys, logging
import pandas as pd
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

def readfiles(dir):
    file_list = []

    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)

            file_path = os.path.join(root, file)

            path_split = file_path.split('\\')
            file_list.append(path_split)
                
    return file_list

def makeOutputPath(file_path, file_dir, output_dir, Ext):
    root, file = os.path.split(file_path)
    filename, ext = os.path.splitext(file)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, f"{filename}.{Ext}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path

if __name__ == '__main__':
    _, input_dir, output_dir = sys.argv
    
    file_list = readfiles(input_dir)

    df = pd.DataFrame(file_list)
    df.to_excel(f"{output_dir}/file_path.xlsx", header=False, index=False)
        