import boto3, os, sys
from config import access_key, secret_key, endpoint_url, region_name, bucket_name
from tqdm import tqdm
import logging
import random
from collections import defaultdict
import shutil

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

    s3client.download_file(bucket_name, from_down_path, output_file)

def readfiles(dir, Ext):
    if Ext == '.json':
        file_dict = defaultdict(lambda: defaultdict(str))
        for root, dirs, files in os.walk(dir):
            for file in files:
                filename, ext = os.path.splitext(file)
                if ext == Ext:
                    unique = root.split('\\')[-2]
                    file_path = os.path.join(root, file)
                    file_dict[unique][filename] = file_path
    elif Ext == '.JPG':
        file_dict = defaultdict(str)
        for root, dirs, files in os.walk(dir):
            for file in files:
                filename, ext = os.path.splitext(file)
                if ext == Ext:
                    file_path = os.path.join(root, file)
                    
                    file_dict[filename] = file_path
                
    return file_dict

def shutilFile(inputFile, outputDir, Ext):
    root, file = os.path.split(inputFile)
    copy_folder = os.path.join(outputDir, '031-041_image_all', Ext)
    os.makedirs(copy_folder, exist_ok=True)
    copy_file = os.path.join(copy_folder, file)
    logger.info(f"{copy_file} 복사")
    shutil.copy2(inputFile, copy_file)
    

_, s3_dir, folder_num, img_num, output_dir = sys.argv

logger = make_logger('log.log')

s3client = boto3.client('s3', region_name = region_name, endpoint_url = endpoint_url, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
paginator = s3client.get_paginator('list_objects_v2')

response = paginator.paginate(Bucket=bucket_name, Prefix=s3_dir, Delimiter='/')

path_list = []
for res in response:
    for prefixes in res['CommonPrefixes']:
        path_list.append(prefixes['Prefix'])

random_file_list = random.sample(path_list, int(folder_num))

for random_file in tqdm(random_file_list, desc='s3 파일 다운'):
    response = paginator.paginate(Bucket=bucket_name, Prefix=random_file, Delimiter='/')
    for res in response:
        for prefixes in res['CommonPrefixes']:
            response2 = paginator.paginate(Bucket=bucket_name, Prefix=prefixes['Prefix'], Delimiter='/')
            for res2 in response2:
                for contents in res2['Contents'][1:]:
                    logger.info(contents['Key'])
                    down_file_path(output_dir, contents['Key'])
                    
json_dict = readfiles(output_dir, '.json')
img_dict = readfiles(output_dir, '.JPG')

for file_dict in json_dict.values():
    for filename, json_path in tqdm(random.sample(list(file_dict.items()), int(img_num)), desc='파일 복사'):
        img_path = img_dict[filename]

        shutilFile(img_path, output_dir, 'image')
        shutilFile(json_path, output_dir, 'json')


    
        
    