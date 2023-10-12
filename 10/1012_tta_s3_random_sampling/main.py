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
    mid = '/'.join(mid.split('/')[-2:])
    folder = os.path.join(output_dir, mid)
    os.makedirs(folder, exist_ok=True)
    
    output_file = os.path.join(folder, file)
    logger.info(output_file)
    s3client.download_file(bucket_name, from_down_path, output_file)

def makePath(x):
    path = '/'.join(x.iloc[:7])
    name1 = x['case1']
    name2 = x['case2']
    count = x['count']
    
    data_list.append([path, name1, name2, count])

def response(path):
    res = paginator.paginate(Bucket=bucket_name, Prefix=f"{path}/", Delimiter='/')
    return res
    
_, excel_dir, down_dir = sys.argv

logger = make_logger('log.log')

data_list = []
excel = pd.read_excel(excel_dir)
excel.apply(makePath, axis=1)
    
s3client = boto3.client('s3', region_name = region_name, endpoint_url = endpoint_url, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
paginator = s3client.get_paginator('list_objects_v2')

for data in tqdm(data_list):
    path = data[0]
    name1 = data[1]
    name2 = data[2]
    count = data[3]
    res = response(path)
    
    file_list = []
    for r in res:
        for c in r['Contents']:
            filename = os.path.split(c['Key'])[-1]
            if name1 in filename and name2 in filename:
                file_list.append(c['Key'])
    random_content = random.sample(file_list, count)
    for file_path in random_content:
        down_file_path(down_dir, file_path)