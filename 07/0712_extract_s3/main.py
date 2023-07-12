import boto3, os, sys
from config import access_key, secret_key, endpoint_url, region_name, bucket_name
import pandas as pd

_, excel_dir, s3_dir, save_dir = sys.argv

excel = pd.read_excel(excel_dir)
partfilename = excel['일부파일명'].tolist()