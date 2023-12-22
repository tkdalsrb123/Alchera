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
                file_path = os.path.join(root, file)
            
                file_dict[filename] = file_path
    return file_dict

def makeOutputPath(file_path, file_dir, output_dir, Ext):
    root, file = os.path.split(file_path)
    filename, ext = os.path.splitext(file)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, f"{filename}.{Ext}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path  

def readJson(path):
    with open(path, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    return data 

def saveJson(file, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(file, f, indent=2, ensure_ascii=False)
        
if __name__ == "__main__":
    _, input_json_dir, revise_json_dir = sys.argv
    
    logger = make_logger('log.log')
    
    json_dict = readfiles(input_json_dir, '.json')
    revise_dict = readfiles(revise_json_dir, '.json')

    for filename, json_path in tqdm(json_dict.items()):
        revise_path = revise_dict.get(filename)
        if revise_path:
            logger.info(revise_path)
            data = readJson(json_path)
            revise_data = readJson(revise_path)
            
            backgrounds = data['backgrounds']
            
            std_obj = {}
            for obj in data['object']:
                std_obj[obj['id']] = obj['segmentation']

            revise_data['backgrounds'] = backgrounds
            
            for idx, obj in enumerate(revise_data['object']):
                std_seg = std_obj.get(obj['id'])
                if std_seg:
                    revise_data['object'][idx]['segmentation'] = std_seg
                
            saveJson(revise_data, revise_path)