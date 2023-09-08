import json, os, sys
import pandas as pd
from tqdm import tqdm
import logging

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
    file_list = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext == '.json':
                file_path = os.path.join(root, file)
            
                file_list.append(file_path)
    return file_list

_, input_dir, output_dir = sys.argv

logger = make_logger('log.log')

json_list = readfiles(input_dir)

df_list = []
for json_path in tqdm(json_list):
    root, file = os.path.split(json_path)
    depth_name = root.split('\\')[-4]
    
    logger.info(json_path)
    with open(json_path, encoding='UTF-8') as f:
        json_file = json.load(f)
    
    for obj in json_file['objects']:
        for att in obj['attributes']:
            if '스타일 정상 반영' in att['name']:
                for val in att['values']:
                    if val['selected'] == True:
                        point_1 = val['value'][0]
                        
            elif '원본 ID 유지' in att['name']:                    
                for val in att['values']:
                    if val['selected'] == True:
                        point_2 = val['value'][0]
                        
            elif '생성 영상 다양성' in att['name']:                   
                for val in att['values']:
                    if val['selected'] == True:
                        point_3 = val['value'][0]
                        
    labeler = json_file['info']['labeler']
    filename = json_file['info']['imageName']
    
    df_list.append([depth_name, labeler, filename, point_1, point_2, point_3])

df = pd.DataFrame(df_list, columns=['폴더명(depth2)', '작업자', 'filename', '스타일 정산 반영', 'ID 유지', '스타일 영상 다양성'])
df.to_excel(f'{output_dir}/json2xlsx.xlsx', index=False )