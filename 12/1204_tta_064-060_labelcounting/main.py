import os, sys, json, logging
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

def readfiles(dir, Ext):
    file_dict = defaultdict(list)

    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            ext = ext.lower()
            if ext == Ext:
                file_path = os.path.join(root, file)
            
                file_dict[filename] = file_path
    return file_dict

def readJson(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

if __name__ == "__main__":
    _, input_dir, output_dir = sys.argv
    
    json_dict = readfiles(input_dir, '.json')

    list2df = []
    for filename, json_path in json_dict.items():
        
        data = readJson(json_path)
        ann_len = len(data['annotations'])

        list2df.append(filename, ann_len)
        
    df = pd.DataFrame(list2df, columns=['filename', 'label'])
    df.to_excel(f'{output_dir}/label.xlsx', index=False)
    