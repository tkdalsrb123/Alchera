import json, os, sys
import pandas as pd
from collections import defaultdict, OrderedDict
import logging
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


def readfiles(dir):
    file_dict = defaultdict(str)
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext == '.json':
                file_path = os.path.join(root, file)

                file_dict[filename] = file_path
    return file_dict

def jsonID(JsonPath, rename):
    root, file = os.path.split(JsonPath)
    mid = '\\'.join(root.split('\\')[len(input_dir.split('\\')):])
    folder = os.path.join(output_dir, mid)
    os.makedirs(folder, exist_ok=True)
    json_output_path = os.path.join(folder, f'{rename}.json')
    
    logger.info(JsonPath)
    with open(JsonPath, 'r', encoding='utf-8') as f:
        json_file = json.load(f)

    id = 1
    new_json = []
    for val in json_file:
        v = list(val.items())
        v.insert(0, ('ID', [f'{id}'.zfill(2)]))
        new_val = OrderedDict(v)
        new_json.append(new_val)
        id += 1

    logger.info(f"{json_output_path} 저장!!")
    with open(json_output_path , 'w', encoding='utf-8') as o:
        json.dump(new_json, o, indent=2, ensure_ascii=False)
    
_, input_dir, output_dir, xlsx_dir = sys.argv

logger = make_logger('log.log')

df = pd.read_excel(xlsx_dir)
rename_dict = dict(zip(df['file_name'], df['file_rename']))

json_dict = readfiles(input_dir)

for filename, filerename in tqdm(rename_dict.items()):
    have_json = json_dict.get(filename)
    if have_json != None:
        json_path = json_dict[filename]
        
        jsonID(json_path, filerename)

    