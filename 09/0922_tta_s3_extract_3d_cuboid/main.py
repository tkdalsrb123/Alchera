import os, sys
import pandas as pd
from config import access_key, secret_key, endpoint_url, region_name, bucket_name
import boto3
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

def s3_download(down_img_path, output_folder):
    replace_name_list = [('Front_Left', 'FL'), ('Front_Right', 'FR'), ('Rear_Left', 'RL'), ('Rear_Right', 'RR')]
    for replace_name in replace_name_list:
        new_img_path = down_img_path.replace('Front_Center', replace_name[0]).replace('FC', replace_name[1])
        new_filename = os.path.split(new_img_path)[-1]
        output_file = os.path.join(output_folder, f"{new_filename}.jpg")
        logger.info(new_img_path)
        s3client.download_file(bucket_name, new_img_path, output_file)
    


_, s3_dir, excel_dir, output_dir = sys.argv

logger = make_logger('log.log')

df = pd.read_excel(excel_dir)
df = df.iloc[2:, 2:4]
df.columns = ['폴더명', '파일명']
df.reset_index(inplace=True)
df2dict = df.to_dict('records')

for i in tqdm(df2dict):
    folder_name = i['폴더명']
    file_name = i['파일명']
    
    folder = os.path.join(output_dir, folder_name)
    os.makedirs(folder, exist_ok=True)
    s3_path = os.path.join(s3_dir, folder_name)
    
    s3client = boto3.client('s3', region_name = region_name, endpoint_url = endpoint_url, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    paginator = s3client.get_paginator('list_objects_v2')

    response = paginator.paginate(Bucket=bucket_name, Prefix=f"{s3_path}/", Delimiter='/')
    for res in response:
        for prefixes in res['CommonPrefixes']:
            response2 = paginator.paginate(Bucket=bucket_name, Prefix=prefixes['Prefix'], Delimiter='/')
            for res2 in response2:
                for prefixes in res2['CommonPrefixes']:
                    response3 = paginator.paginate(Bucket=bucket_name, Prefix=prefixes['Prefix'], Delimiter='/')
                    for res3 in response3:
                        content = res3.get('Contents')
                        for con in content:
                            root, file = os.path.split(con['Key'])
                            filename, ext = os.path.splitext(file)
                            if ext == '.jpg' and filename == file_name:
                                down_img = con['Key']
                                output_file = os.path.join(folder, f"{file_name}.jpg")
                                logger.info(output_file)
                                s3client.download_file(bucket_name, down_img, output_file)
                                s3_download(down_img, folder)