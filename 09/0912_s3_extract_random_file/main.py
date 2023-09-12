import boto3, os, sys
from config import access_key, secret_key, endpoint_url, region_name, bucket_name
import pandas as pd
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

def down_file_path(output_dir, from_down_path):
    mid, file = os.path.split(from_down_path)
    folder = os.path.join(output_dir, mid)
    os.makedirs(folder, exist_ok=True)
    
    output_file = os.path.join(folder, file)

    s3client.download_file(bucket_name, from_down_path, output_file)
    


s3client = boto3.client('s3', region_name = region_name, endpoint_url = endpoint_url, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
paginator = s3client.get_paginator('list_objects_v2')