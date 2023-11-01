import json, cv2, os, sys
import logging
import numpy as np
from collections import defaultdict
from tqdm import tqdm
from label import label

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
    file_dict = defaultdict(str)
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            ext = ext.lower()
            if ext == Ext:
                file_path = os.path.join(root, file)

                file_dict[filename] = file_path
    return file_dict

def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def read_img(img_path):
    img_array = np.fromfile(img_path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img

def save_img(img_path, img):
    result, encoded_img = cv2.imencode('.png', img)
    if result:
        with open(img_path, mode='w+b') as f:
            encoded_img.tofile(f)

def makeOutputPath(file_path, file_dir, output_dir):
    root, file = os.path.split(file_path)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, file)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path

if __name__ == "__main__":

    _, img_dir, json_dir, output_dir = sys.argv

    logger = make_logger('log.log')

    img_dict = readfiles(img_dir, '.jpg')
    json_dict = readfiles(json_dir, '.json')

    for filename, img_path in tqdm(img_dict.items()):
        json_path = json_dict.get(filename)
        logger.info(img_path)
        if json_path:
            logger.info(json_path)
            output_img_path = makeOutputPath(img_path, img_dir, output_dir)
            
            data = read_json(json_path)
            work = data['annotations'][0]['attributes']['work']
            part = data['annotations'][0]['attributes']['part']
            quality = data['annotations'][0]['attributes']['quality']

            img = read_img(img_path)

            org_h = 0
            text_size = 60
            for text in [work, part, quality]:
                img = label(img, text, text_size, (0,0,0), (0, org_h), 0.5)
                org_h += text_size+15
                
            save_img(output_img_path, img)