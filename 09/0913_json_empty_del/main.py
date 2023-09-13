import json, os, sys
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

for json_path in tqdm(json_list):
    output_json_path = make_output_path(input_dir, json_path, output_dir)
    with open(json_path, encoding='utf-8') as f:
        json_file = json.load(f)
    
    for obj in json_file['objects']:
        for att in obj['attributes']:
            att['values'][0]['value'] = att['values'][0]['value'].rstrip()

            if len(att['values'][0]['value'])>1 and att['values'][0]['value'][-1] == '#':
                att['values'][0]['value'] = att['values'][0]['value'][:-2]

    with open(output_json_path, 'w', encoding='utf-8') as o:
        json.dump(json_file, o, indent=2, ensure_ascii=False)