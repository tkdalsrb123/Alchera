import boto3, os, sys
from config import access_key, secret_key, endpoint_url, region_name, bucket_name
from tqdm import tqdm
import logging
import random
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

def down_file_path(output_dir, from_down_path):
    mid, file = os.path.split(from_down_path)
    mid = '/'.join(mid.split('/'))
    folder = os.path.join(output_dir, mid)
    os.makedirs(folder, exist_ok=True)
    
    output_file = os.path.join(folder, file)
    logger.info(output_file)
    s3client.download_file(bucket_name, from_down_path, output_file)

def make_path(x):
    path = '/'.join([i for i in x[:8] if type(i) != float])
    count = x[8]
    path_list.append([path, count])
        
def response(path):
    res = paginator.paginate(Bucket=bucket_name, Prefix=f"{path}/", Delimiter='/')
    return res

def revise_path(path, depth5, depth7, depth8, unique, Ext):
    root, file = os.path.split(path)
    root_split = root.split('/')
    filename, ext = os.path.splitext(file)
    filename_split = filename.split('_')
    filename_split[3] = unique
    new_filename = '_'.join(filename_split).replace(ext, Ext)
    
    root_split[4] = depth5
    root_split[6] = depth7
    root_split[7] = depth8
    
    new_path = '/'.join(root_split)

    new_file_path = '/'.join([new_path, new_filename])
    return new_file_path
    

def preprocessing(path):
    
    raw_lf = revise_path(path, '1.원천데이터', 'LWIR', 'LWIR_Front', 'LF', '.jpg')    
    raw_lr = revise_path(path, '1.원천데이터', 'Lidar', 'Lidar_Roof', 'LR', '.pcd')    
    label_fc = revise_path(path, '2.라벨링데이터', 'Camera', 'Camera_Front_Center', 'FC', '.json')    
    label_lf = revise_path(path, '2.라벨링데이터', 'LWIR', 'LWIR_Front', 'LF', '.json')    
    label_lr = revise_path(path, '2.라벨링데이터', 'Lidar', 'Lidar_Roof', 'LR', '.json')
            
    return [path, raw_lf, raw_lr, label_fc, label_lf, label_lr]
    

if __name__ == '__main__':
    _, excel_dir, raw_down_dir, label_down_dir = sys.argv
    
    logger = make_logger('log.log')
    
    path_list = []
    excel = pd.read_excel(excel_dir)
    excel.apply(make_path, axis=1)
    
    s3client = boto3.client('s3', region_name = region_name, endpoint_url = endpoint_url, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    paginator = s3client.get_paginator('list_objects_v2')
    
    down_path_list = []
    for data in tqdm(path_list, desc='extract down file path'):
        res = response(data[0])
        file_list = []
        for r in res:
            [file_list.append(c) for c in r['Contents']]
        
        con = random.sample(file_list, data[1])
        raw_file_list = [c['Key'] for c in con]
        [down_path_list.append(preprocessing(raw_file)) for raw_file in raw_file_list]
    
    for down_path in tqdm(down_path_list, desc='download file'):
        logger.info(down_path)
        for down in down_path:
            if '원천' in down:
                down_file_path(raw_down_dir, down)
            elif '라벨' in down:
                down_file_path(label_down_dir, down)