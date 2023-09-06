import os, sys, json
import pandas as pd
from tqdm import tqdm
import logging
import time

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

_, input_dir, output_dir = sys.argv

logger = make_logger('log.log')

json_list = []
for root, dirs, files in os.walk(input_dir):
    for file in files:
        filename, ext = os.path.splitext(file)
        if ext == '.json':
            json_path = os.path.join(root, file)

            json_list.append(json_path)

df_list = []
No = 1
for json_path in tqdm(json_list):
    logger.info(json_path)
    
    root, file = os.path.split(json_path)

    with open(json_path, encoding='utf-8') as f:
        json_file = json.load(f)
    
    어절 = json_file['docu_info']['TagCount']['T_TagCount']
    개체 = json_file['docu_info']['TagCount']['O_TagCount'] 
    속성 = json_file['docu_info']['TagCount']['A_TagCount']
    감성 = json_file['docu_info']['TagCount']['E_TagCount']
    
    df_list.append([No, file, 어절, 개체, 속성, 감성])

    No += 1
timestamp = time.time()
now = time.localtime(timestamp)
now_formated = time.strftime("%d일%H시%M분", now)
df = pd.DataFrame(df_list, columns=['No.1', '파일명', '어절 총 개수', '개체명 개수', '속성명 개수', '감성명 개수'])
df.to_excel(f'{output_dir}/TagCount_{now_formated}.xlsx', index=False)