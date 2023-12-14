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

def extract_filename(path):
    filename = os.path.splitext(os.path.basename(path))[0]
    return filename
    
def make_path(x):
    path = '/'.join([i for i in x if type(i) != float])
    label_path_list.append('/'.join(x[:-2]).replace('1.원천데이터', '2.라벨링데이터'))
    path_dict[extract_filename(x[-1])] = path
        
def response(path):
    res = paginator.paginate(Bucket=bucket_name, Prefix=f"{path}/", Delimiter='/')
    for r in res:
        prefixes = r.get('CommonPrefixes')
        contents = r.get('Contents')
        if prefixes:
            for pre in prefixes:
                response(pre['Prefix'][:-1])
        
        if len(contents) > 1:
            [down_path_list.append(c['Key']) for c in contents]
            
    return down_path_list


if __name__ == '__main__':
    _, excel_dir, output_dir = sys.argv
    
    logger = make_logger('log.log')
    
    path_dict = {}
    label_path_list = []
    excel = pd.read_excel(excel_dir)
    excel.apply(make_path, axis=1)
    
    s3client = boto3.client('s3', region_name = region_name, endpoint_url = endpoint_url, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    paginator = s3client.get_paginator('list_objects_v2')
    
    down_path_list = []
    label_down_path_list = []
    label_path_list = list(set(label_path_list))
    for label_path in tqdm(label_path_list, desc='extract down file path'):
        try:
            label_down_path_list = response(label_path)
        except:
            print(label_path, '경로 존재 x')
    
    if label_down_path_list:

        label_dict = {'_'.join(extract_filename(path).split('_')[2:]): path for path in label_down_path_list if os.path.split(path)[-1] != ''}
        
        for filename, raw_path in tqdm(path_dict.items(), desc='download file'):
            label_path = label_dict.get(filename)
            if label_path:
                try:
                    down_file_path(output_dir, raw_path)
                except:
                    print(raw_path, '파일 x')
                try:
                    down_file_path(output_dir, label_path)
                except:
                    print(label_path, '파일 x')
            else:
                print(raw_path, label_path, '매칭 x')
    else:
        print(label_path, 'no file')