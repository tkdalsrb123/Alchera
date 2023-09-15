import os, sys, shutil
from collections import defaultdict
from tqdm import tqdm
import logging
import chardet

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


def readfiles(dir, Ext):
    file_dict = defaultdict(list)
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext == Ext:
                new_filename = filename.split('_')[0]
                file_path = os.path.join(root, file)
                
                file_dict[new_filename].append(file_path)
                
    return file_dict

def copy_file(input_path, output_path):
    logger.info(input_path)
    root, file = os.path.split(input_path)
    mid = '\\'.join(root.split('\\')[len(root_dir.split('\\')):])
    folder = os.path.join(output_path, mid)
    os.makedirs(folder, exist_ok=True)
    output_img_path = os.path.join(folder, file)
    shutil.copy2(input_path, output_img_path)
    logger.info(f'{output_img_path} 저장!!!')
    
_, bookmark_dir, root_dir, output_dir, file_type = sys.argv

logger = make_logger('log.log')

img_dict = readfiles(root_dir, '.jpg')
json_dict = readfiles(root_dir, '.json')

file_list = []

bookmark_list = os.listdir(bookmark_dir)

for book in bookmark_list:
    bookmark_path = os.path.join(bookmark_dir, book)

    data = open(bookmark_path, 'rb').read()
    result = chardet.detect(data)
    enc = result['encoding']

    with open(bookmark_path, 'r', encoding=enc) as f:
        bookmarks = f.readlines()
        
    for bookmark in tqdm(bookmarks, desc='bookmark 읽는중'):
        file = os.path.split(bookmark)[-1]
        file = file.replace('\n', '')
        filename, ext = os.path.splitext(file)
        if ext == '.jpg' or ext == '.json':
            file_list.append(filename)
            
    if file_type == 'jpg':
        for filename in tqdm(file_list, desc='파일복사중'):
            img_paths = img_dict.get(filename)
            if img_paths:
                for img_path in img_paths:
                    copy_file(img_path, output_dir)
    elif file_type == 'json':
        for filename in tqdm(file_list, desc='파일복사중'):
            json_paths = json_dict.get(filename)
            if json_paths:
                for json_path in json_paths:
                    copy_file(json_path, output_dir)
