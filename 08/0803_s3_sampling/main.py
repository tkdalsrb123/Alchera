import boto3, os, sys
from config import access_key, secret_key, endpoint_url, region_name, bucket_name
import pandas as pd
from tqdm import tqdm

_, excel_dir, output_dir = sys.argv

path_list = []
excel = pd.read_excel(excel_dir)
excel.apply(lambda x: path_list.append('/'.join(list(x.dropna()))), axis=1)

s3client = boto3.client('s3', region_name = region_name, endpoint_url = endpoint_url, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
paginator = s3client.get_paginator('list_objects_v2')

# down file
for path in tqdm(path_list):
    mid, file = os.path.split(path)
    folder = os.path.join(output_dir, mid)
    os.makedirs(folder, exist_ok=True)
    
    output_file = os.path.join(folder, file)
    print(output_file)
    s3client.download_file(bucket_name, path, output_file)
