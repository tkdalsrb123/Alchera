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
                if os.path.split(root)[-1] == 'CMR_GT_ALL':
                    folder = root.split('\\')[-5]
                    file_path = os.path.join(root, file)
                
                    file_dict[folder].append(file_path)
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

if __name__ == "__main__":
    _, input_dir, output_dir = sys.argv
    
    json_dict = readfiles(input_dir, '.json')

    df2list = []
    for foldername, json_list in tqdm(json_dict.items(), desc='json_dict', position=0):
        count = 0
        for json_path in tqdm(json_list, desc='json_list', position=1):
            data = readJson(json_path)

            cuboid = data['object'][0]['cuboid']
            if cuboid:
                count += 1
        
        df2list.append([foldername, count])
    
    df = pd.DataFrame(df2list, columns=['filename', 'count'])
    df.to_excel(f"{output_dir}/count_json.xlsx", index=False)