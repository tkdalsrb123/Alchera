import boto3, os, sys
import pandas as pd
from config import access_key, secret_key, endpoint_url, region_name, bucket_name
from tqdm import tqdm
import warnings


def s3_img_down(filename, bucket, down_path):
    pair1, pair2 = '_'.join(filename.split('_')[:3]), '_'.join(filename.split('_')[-3:])
    down_df = img_df[(img_df['filename'].str.contains(pair1)) & (img_df['filename'].str.contains(pair2))]
    down_mid = down_df['mid'].tolist()
    down_img_path = down_df['path'].tolist()
    for idx in range(down_df.shape[0]):
        folder = os.path.join(down_path, down_mid[idx])
        os.makedirs(folder, exist_ok=True)
        to_down_img_path = os.path.join(down_path, down_img_path[idx])
        s3client.download_file(bucket, down_img_path[idx], to_down_img_path)
        print(to_down_img_path, '저장!!!')
    

_, excel_dir, s3_dir, down_dir = sys.argv

warnings.filterwarnings('ignore')
tqdm.pandas()

excel = pd.read_excel(excel_dir)

s3client = boto3.client('s3', region_name = region_name, endpoint_url = endpoint_url, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
paginator = s3client.get_paginator('list_objects_v2')

response = paginator.paginate(Bucket=bucket_name, Prefix=s3_dir, Delimiter='/')

print('s3에서 파일 불러오는 중...')
img_list = []
for res in response:
    for common1 in res['CommonPrefixes']:
        common_res1 = paginator.paginate(Bucket=bucket_name, Prefix=common1['Prefix'], Delimiter='/')
        for pre1 in common_res1:
            for pre2 in pre1['CommonPrefixes']:
                common_res2 = paginator.paginate(Bucket=bucket_name, Prefix=pre2['Prefix'], Delimiter='/')
                for pre3 in common_res2:
                    for pre4 in tqdm(pre3['CommonPrefixes']):
                        common_res3 = paginator.paginate(Bucket=bucket_name, Prefix=pre4['Prefix'], Delimiter='/')
                        for pre5 in common_res3:
                            for content in pre5['Contents']:
                                img_path = content['Key']
                                
                                mid, filename = os.path.split(img_path)
                                img_list.append([mid, img_path, filename])

img_df = pd.DataFrame(img_list, columns=['mid', 'path', 'filename'])

print('파일 저장 시작!!!')
excel['filename'].progress_apply(s3_img_down, args=(bucket_name, down_dir))
print('파일 저장 끝!!!')
                                



