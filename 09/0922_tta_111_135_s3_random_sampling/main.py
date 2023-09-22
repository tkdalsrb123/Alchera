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
    img_path_list.append({"img_path":'/'.join(list(x.iloc[:9].values)), "count":x.iloc[9]})


_, excel_dir, img_down_dir, label_down_dir = sys.argv

logger = make_logger('log.log')

img_path_list = []
excel = pd.read_excel(excel_dir)
excel.apply(makePath, axis=1)

for img_path_dict in tqdm(img_path_list):
    sample_count = img_path_dict['count']
    img_path = img_path_dict['img_path']
    json_path = img_path.replace('1.원천데이터', '2.라벨링데이터')

    s3client = boto3.client('s3', region_name = region_name, endpoint_url = endpoint_url, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    paginator = s3client.get_paginator('list_objects_v2')
    response = paginator.paginate(Bucket=bucket_name, Prefix=f"{img_path}/", Delimiter='/')
    for res in response:
        random_content = random.sample(res['Contents'][1:], sample_count)
        s3_img_path_list = [c['Key'] for c in random_content]
        for s3_img_path in s3_img_path_list:
            root, file = os.path.split(s3_img_path)
            filename, ext = os.path.splitext(file)
            s3_json_path = '/'.join([json_path, f"{filename}.json"])
            replace_json_name = '/'.join(['/'.join(s3_json_path.split('/')[:-2]), '/'.join(s3_json_path.split('/')[-2:]).replace('78', '79')])
            
            down_file_path(label_down_dir, replace_json_name)    
            down_file_path(img_down_dir, s3_img_path)
