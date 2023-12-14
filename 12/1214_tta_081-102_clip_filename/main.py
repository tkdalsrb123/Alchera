import boto3, os, sys
from config import access_key, secret_key, endpoint_url, region_name, bucket_name
from tqdm import tqdm
import logging
import random
import pandas as pd
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

def down_file_path(output_dir, from_down_path, dir):
    mid, file = os.path.split(from_down_path)
    # mid = '/'.join(mid.split('/'))
    folder = os.path.join(output_dir, dir)
    os.makedirs(folder, exist_ok=True)
    
    output_file = os.path.join(folder, file)
    logger.info(output_file)
    s3client.download_file(bucket_name, from_down_path, output_file)

def extract_filename(path):
    filename = os.path.splitext(os.path.basename(path))[0]
    filename = '_'.join(filename.split('_')[:5])[:-3]
    return filename
    
def make_path(x):
    # path = '/'.join([i for i in x if type(i) != float])
    path_list.append('/'.join(x[:-2]))
    num = int(x[-1].split('_')[4][3:])
    path_num.append([extract_filename(x[-1]), num])
    
def response(path):
    res = paginator.paginate(Bucket=bucket_name, Prefix=f"{path}/", Delimiter='/')
    for r in res:
        prefixes = r.get('CommonPrefixes')
        contents = r.get('Contents')
        if prefixes:
            for pre in prefixes:
                response(pre['Prefix'][:-1])
        
        if len(contents) > 1:
            # [print(extract_filename(c['Key'])) for c in contents if os.path.split(c['key'])[-1] != '']
            [down_path_dict[extract_filename(c['Key'])].append(c['Key']) for c in contents if os.path.split(c['Key'])[-1] != '']
            
def make_range(i, m):
    min_num = i - 30
    max_num = i + 30
    
    if min_num < 1:
        min_num = 1
    if max_num > m:
        max_num = m
        
    return (min_num, max_num)
    
if __name__ == '__main__':
    _, excel_dir, output_dir = sys.argv
    
    logger = make_logger('log.log')
    
    path_num = []
    path_list = []
    excel = pd.read_excel(excel_dir)
    excel.apply(make_path, axis=1)
    
    s3client = boto3.client('s3', region_name = region_name, endpoint_url = endpoint_url, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    paginator = s3client.get_paginator('list_objects_v2')
    
    down_path_dict = defaultdict(list)
    path_list = list(set(path_list))
    for label_path in tqdm(path_list, desc='extract down file path'):
        try:
            response(label_path)
        except:
            print(label_path, '경로 존재 x')

    for folder_num in tqdm(path_num, desc='down files'):
        folder, num = folder_num
        down_path_list = down_path_dict.get(folder)
        if down_path_list:
            if len(down_path_list) < 60:
                for down_path in down_path_list:
                    down_file_path(output_dir, down_path, folder)
            else:
                min_n, max_n = make_range(num, len(down_path_list))
                for down_path in down_path_list[min_n:max_n]:
                    down_file_path(output_dir, down_path, folder)
                    
    