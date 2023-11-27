import os, sys, json, logging
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
            ext = ext.lower()
            if ext == Ext:
                f = os.path.split(root)[-1]
                file_path = os.path.join(root, file)
            
                file_dict[f].append(file_path)
    return file_dict

def readJson(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def save_csv(_list, category, output_path):
    df = pd.DataFrame(_list, columns=['file_name', category])
    df.to_csv(f'{output_path}/{category}_label_count.csv', index=False)

def counting_label(_data):
    count = 0
    for body in _data['annotations']['segmentation_body']:
        if type(body['points']) == list:
            count += 1
    return count

if __name__ == "__main__":
    _, input_dir, output_dir = sys.argv
    
    logger = make_logger('log.log')

    json_dict = readfiles(input_dir, '.json')

    body2df = []
    face2df = []
    for f, json_list in tqdm(json_dict.items()):
        for json_path in json_list:
            logger.info(json_path)
            
            filename = os.path.split(json_path)[-1]
            data = readJson(json_path)
            count = 0
            if f == 'body':
                count = counting_label(data)
                body2df.append([filename, count])
            
            elif f == 'face':
                count = counting_label(data)
                face2df.append([filename, count])
        
    save_csv(body2df, 'body', output_dir)
    save_csv(face2df, 'face', output_dir)
    