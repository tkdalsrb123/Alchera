import boto3, os, sys
from config import access_key, secret_key, endpoint_url, region_name, bucket_name
import pandas as pd
from collections import defaultdict
from tqdm import tqdm

_, excel_dir, s3_dir, save_dir = sys.argv

excel = pd.read_excel(excel_dir)
partfilename = excel['일부 파일명'].tolist()

s3client = boto3.client('s3', region_name = region_name, endpoint_url = endpoint_url, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
paginator = s3client.get_paginator('list_objects_v2')

response = paginator.paginate(Bucket=bucket_name, Prefix=s3_dir, Delimiter='/')

print('s3에서 이미지 불러오는 중..!')
img_dict = defaultdict(list)
for res1 in response:
    for common1 in res1['CommonPrefixes']:
        response2 = paginator.paginate(Bucket=bucket_name, Prefix=common1['Prefix'], Delimiter='/')
        for res2 in response2:
            for common2 in res2['CommonPrefixes']:
                response3 = paginator.paginate(Bucket=bucket_name, Prefix=common2['Prefix'], Delimiter='/')
                for res3 in response3:
                    print(res3['Prefix'])
                    for content in tqdm(res3['Contents']):
                        if os.path.splitext(content['Key'])[-1] == '.JPG':
                            img_dict[content['Key'].split('_')[-2]].append(content['Key'])
                            
print('-'*30, '이미지 저장 시작!!', '-'*30)
for filename in partfilename:
    folder = os.path.join(save_dir, filename)
    os.makedirs(folder, exist_ok=True)
    for img_path in img_dict[filename]:
        img_name = os.path.split(img_path)[-1]
        down_img_path = os.path.join(folder, img_name)
        s3client.download_file(bucket_name, img_path, down_img_path)
        print(down_img_path, '저장!!!')