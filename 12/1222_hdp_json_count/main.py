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
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def make_csv(_list, col, output_path):
    df = pd.DataFrame(_list, columns=col)
    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    _, input_dir = sys.argv
    
    folder_list = [os.path.join(input_dir, dirs, '04_BBOX') for dirs in os.listdir(input_dir)]
    
    file_dict = {}
    for folder in tqdm(folder_list, desc='gather file'):
        seq = folder.split('\\')[-2]
        file_dict[seq] = [os.path.join(folder, file) for file in os.listdir(folder)]

    list2df = []
    for seq, json_path_list in tqdm(file_dict.items(), desc='create csv'):
        info_dict = {'RM_Arrow':0, 'RM_Character':0, 'RM_Figure':0, 'RM_Number':0}
        for json_path in json_path_list:
            data = readJson(json_path)
            for obj in data['objects']:
                info_dict[obj['name']] += 1 
        
        list2df.append([seq, info_dict['RM_Arrow'], info_dict['RM_Character'], info_dict['RM_Figure'], info_dict['RM_Number']])
    
    make_csv(list2df, ["sequence", "RM_Arrow", "RM_Character", "RM_Figure", "RM_Number"], f'./{os.path.split(input_dir)[-1]}.csv')
        