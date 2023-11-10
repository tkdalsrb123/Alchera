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
            if ext == Ext and 'Property' in filename:
                file_path = os.path.join(root, file)
            
                file_dict[filename] = file_path
    return file_dict

def readJson(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def saveJson(file, path):
    with open(path, 'w') as f:
        json.dump(file, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    _, json_dir, excel_dir = sys.argv

    logger = make_logger('log.log')

    json_dict = readfiles(json_dir, '.json')
    xlsx_dict = readfiles(excel_dir, '.xlsx')

    for filename, json_path in tqdm(json_dict.items()):
        xlsx_path = xlsx_dict[filename]

        logger.info(json_path)
                
        df = pd.read_excel(xlsx_path)
        info_list = []
        df.apply(lambda x: info_list.append({"location":x['Location'], "roadtype":x['RoadType'], "ill":x['IlluminationCondition']}), axis=1)

        data = readJson(json_path)

        for idx, d in enumerate(data):
            d['Location'] = info_list[idx]['location']
            d['RoadType'] = info_list[idx]['roadtype']
            d['IlluminationCondition'] = info_list[idx]['ill']
            
        saveJson(data, json_path)
        logger.info(json_path)

        
        
        