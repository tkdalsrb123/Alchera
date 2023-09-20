import json, os, sys
import pandas as pd
from collections import defaultdict
import logging
from tqdm import tqdm


def readfiles(dir):
    file_dict = defaultdict(str)
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext == '.json':
                file_path = os.path.join(root, file)
                file_dict[filename] = file_path
    
    return file_dict

def SortValue(x):
    if '.' in x[1]:
        sort_value = sorted(x, key=lambda v: float(v), reverse=True)
    elif '%' in x[1]:
        sort_value = sorted(x, key=lambda v: int(v[:-1]), reverse=True)
    elif ',' in x[1]:
        sort_value = sorted(x, key=lambda v: int(v.replace(',','')), reverse=True)
    else:
        sort_value = sorted(x, key=lambda v: int(v), reverse=True)

    return sort_value

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

_, input1_dir, input2_dir, output_dir = sys.argv

logger = make_logger('log.log')

json1_dict = readfiles(input1_dir)
json2_dict = readfiles(input2_dir)

error_list = []
for filename, json1_path in tqdm(json1_dict.items()):
    json_have = json2_dict.get(filename)

    logger.info(json1_path)
    root, file = os.path.split(json1_path)    
    mid = '\\'.join(root.split('\\')[len(input1_dir.split('\\')):])
    folder = os.path.join(output_dir, 'output', mid)
    os.makedirs(folder, exist_ok=True)
    
    output_json_path = os.path.join(folder, file)

    with open(json1_path, encoding='utf-8') as f1:
        json1_file = json.load(f1)
        
    if json_have != None:
        new_json = {}
        json2_path = json2_dict[filename]

        with open(json2_path, encoding='utf-8') as f2:
            json2_file = json.load(f2)
        
        obj_dict = json1_file['objects'][0]
        info = json1_file['info']

        [obj_dict['attributes'].append(att) for att in json2_file['objects'][0]['attributes']]

        new_json['objects'] = obj_dict
        new_json['info'] = info
        
        # for att in json2_file['objects'][0]['attributes']:
    #         if att['name'] == 'Y값 범위':
    #             values = att['values'][0]['value']
        
    #     value_list = values.split('\n')
    #     sort_val = []
    #     try:
    #         for value in value_list:
    #             split_val = value.split('#')
    #             split_val = [v.strip() for v in split_val]
    #             sort_val.append(SortValue(split_val))
    #     except:
    #         error_list.append([file, split_val])
    #         sort_val.append(split_val)
    #     json1_file['unit-range'] = sort_val

    #     with open(output_json_path, 'w', encoding='utf-8') as o:
    #         json.dump(json1_file, o, indent=2, ensure_ascii=False)

    #     logger.info(f'{output_json_path}  저장!!!')
        
    # else:
    #     json1_file['unit-range'] = [""]

        with open(output_json_path, 'w', encoding='utf-8') as o:
            json.dump(new_json, o, indent=2, ensure_ascii=False)

        logger.info(f'{output_json_path} "unit-range 공백 저장"!!!')
        
error_xlsx = os.path.join(output_dir, 'error_list.xlsx')
df = pd.DataFrame(error_list, columns = ['파일명', 'value'])
df.to_excel(error_xlsx, index=False)