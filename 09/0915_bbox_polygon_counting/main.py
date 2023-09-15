import json, os, sys
import logging
from tqdm import tqdm
import pandas as pd

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
    file_list = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext == Ext:
                file_path = os.path.join(root, file)
                
                file_list.append(file_path)
                
    return file_list

_, input_dir = sys.argv

logger = make_logger('log.log')

json_list = readfiles(input_dir, '.json')

df2list = []
for json_path in json_list:
    root, file = os.path.split(json_path)
    logger.info(json_path)
    with open(json_path, encoding='utf-8') as f:
        json_file = json.load(f)

    bbox_count = 0
    seg_count = 0    
    for ann in json_file['annotations']:
        if len(ann['bbox']) > 1:
            bbox_count += 1
        
        if len(ann['segmentation']) > 1:
            seg_count += 1
            
    df2list.append([file, bbox_count, seg_count])
df = pd.DataFrame(df2list, columns=['파일명', 'bbox', 'segmentation'])
df.to_excel('./bbox_seg_count.xlsx', index=False)
