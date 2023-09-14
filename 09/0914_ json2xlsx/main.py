import os, sys, json
import logging
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

def readfiles(dir, Ext):
    file_dict = defaultdict(list)
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            if Ext == 'json':
                if ext == '.json':
                    filename = '_'.join(filename.split('_')[:-1])
                    file_path = os.path.join(root, file)

                    file_dict[filename].append(file_path)
                    
    return file_dict

_, input_dir, output_dir = sys.argv

logger = make_logger('log.log')

json_dict = readfiles(input_dir, 'json')

json_info_dict = defaultdict(lambda: defaultdict(str))
for filename, json_path_list in tqdm(json_dict.items()):
    for json_path in json_path_list:
        logger.info(json_path)
        with open(json_path, encoding='utf-8') as f:
            json_file = json.load(f)
        
        facepart = json_file['images']['facepart']
        for key, val in json_file['annotations'].items():
            col = f'{facepart}_{key}'
            json_info_dict[filename][col] = val

df = pd.DataFrame.from_dict(json_info_dict).T
df.reset_index(names=['filename'], inplace=True)
df.to_excel(f'{output_dir}/annotatinos2xlsx.xlsx', index=False)

