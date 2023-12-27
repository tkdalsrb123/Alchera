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
    path = '/'.join([i for i in x[:9] if type(i) != float])
    count = x[9]
    path_list.append([path, count])
        
def response(path):
    res = paginator.paginate(Bucket=bucket_name, Prefix=f"{path}/", Delimiter='/')
    return res

def matching_img_path(path):
    root, file = os.path.split(path)
    filename, ext = os.path.splitext(file)
    matching_filename = '-'.join(filename.split('-')[3:5])
    root_split = root.split('/')[:4]
    root_split.append('1.원천데이터')
    [root_split.append(i) for i in root.split('/')[-3:]]

    matching_root = '/'.join(root_split)
    file_list = []
    res = response(matching_root)
    for r in res:
        [file_list.append(c['Key']) for c in r['Contents'][1:] if matching_filename in c['Key']]
    return file_list
    
def preprocessing(path):
    img_list = matching_img_path(path)
    
    return [img_list, path]
    

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
            [file_list.append(c) for c in r['Contents'][1:]]
        
        con = random.sample(file_list, data[1])
        obj_file_list =[c['Key'] for c in con]
        
        [down_path_list.append(preprocessing(obj_file)) for obj_file in obj_file_list]

    for down_path in tqdm(down_path_list, desc='download file'):
        for img_path in down_path[0]:
            down_file_path(raw_down_dir, img_path)
        down_file_path(label_down_dir, down_path[1])



