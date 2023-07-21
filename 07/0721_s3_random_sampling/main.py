import boto3, os, sys
from config import access_key, secret_key, endpoint_url, region_name, bucket_name
import pandas as pd
import random
from tqdm import tqdm

def s3_file_down(file_list, bucket, wav_down_path, label_down_path):
    for wav_file in file_list:
        label_file = wav_file.replace('01.원천데이터', '02.라벨링데이터').replace('.wav', '.json')
        wav_mid_path, filename = os.path.split(wav_file)
        label_mid_path = wav_mid_path.replace('01.원천데이터', '02.라벨링데이터')
        wav_folder = os.path.join(wav_down_path, wav_mid_path)
        label_folder = os.path.join(label_down_path, label_mid_path)
        
        os.makedirs(wav_folder, exist_ok=True)
        os.makedirs(label_folder, exist_ok=True)
        
        to_down_wav_file = os.path.join(wav_folder, filename)
        to_down_label_file = os.path.join(label_down_path, label_file)
        
        s3client.download_file(bucket, wav_file, to_down_wav_file)
        print(to_down_wav_file, '저장!!')
        s3client.download_file(bucket, label_file, to_down_label_file)
        print(to_down_label_file, '저장!!')


_, excel_dir, wav_down_dir, label_down_dir = sys.argv

file_path_list = []
excel = pd.read_excel(excel_dir)

file_path_list.append(excel.apply(lambda x: ['/'.join(x.iloc[:8]), x.loc['Count']], axis=1))

file_path_list = file_path_list[0].tolist()

s3client = boto3.client('s3', region_name = region_name, endpoint_url = endpoint_url, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
paginator = s3client.get_paginator('list_objects_v2')

for file in tqdm(file_path_list):
    file_path = file[0]
    sample_count = file[1]
    
    response = paginator.paginate(Bucket=bucket_name, Prefix=f'{file_path}/', Delimiter='/')
    for res in response:
        s3_file_list = []
        for content in res['Contents']:
            s3_file_list.append(content['Key'])

        random_list = random.sample(s3_file_list, sample_count)
        
        s3_file_down(random_list, bucket_name, wav_down_dir, label_down_dir)