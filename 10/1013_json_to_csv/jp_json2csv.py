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

def readJson(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

_, input_dir, output_dir = sys.argv

json_dict = readfiles(input_dir, '.json')

data_list = []
for filename, json_path in tqdm(json_dict.items()):
    json_file = readJson(json_path)

    for obj in json_file['object']:
        id = obj['id']
        gender = obj['gender']
        age = obj['age']
        accent = obj['accent']

    sentiment = json_file['annotation']['sentiment']
    inputscript = json_file['annotation']['inputscript']
    outputscript = json_file['annotation']['outputscript']

    data_list.append([filename, id, gender, age, accent, sentiment, inputscript, outputscript])
    
df = pd.DataFrame(data_list, columns=['filename', 'id', 'gender', 'age', 'accent', 'sentiment', 'inputscript', 'outputscript'])
df.to_csv(f'{output_dir}/jp_json2csv.csv', index=False)