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

def make_output_path(input_path, file_path, output_path):
    root, file = os.path.split(file_path)
    mid = '\\'.join(root.split('\\')[len(input_path.split('\\')):])
    folder= os.path.join(output_path, mid)
    os.makedirs(folder, exist_ok=True)
    output_file_path = os.path.join(folder, file)
    logger.info(f'{output_file_path} 저장!!')
    return output_file_path

_, input_dir, output_dir = sys.argv

logger = make_logger('log.log')

json_list = readfiles(input_dir, '.json')

error_file_list = []
for json_path in tqdm(json_list):
    output_json_path = make_output_path(input_dir, json_path, output_dir)
    with open(json_path, encoding='utf-8') as f:
        json_file = json.load(f)
    
    for obj in json_file['objects']:
        for atts in obj['attributes']:
            att_split = atts['values'][0]['value'].split('\n')
            for att in att_split:

                if len(att)>0 and att[-1] == ' ':
                    atts['values'][0]['value'] = att.rstrip()

                    error_file_list.append(json_path)
                
                    if len(att)>1 and att[-1] == '#':
                        att = att[:-2]
                    

    with open(output_json_path, 'w', encoding='utf-8') as o:
        json.dump(json_file, o, indent=2, ensure_ascii=False)
        
df = pd.DataFrame(error_file_list, columns=['error_filename'])
df.to_excel(f'{output_dir}/error_list.xlsx', index=False)