import cv2, os, sys, json
import logging
import numpy as np
from tqdm import tqdm
from collections import defaultdict

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
            if ext == Ext:
                file_path = os.path.join(root, file)

                file_dict[filename] = file_path
    return file_dict

def read_img(img_path):
    img_array = np.fromfile(img_path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img

def save_img(img_path, img):
    result, encoded_img = cv2.imencode('.jpg', img)
    logger.info(f"{img_path} 저장!!")
    if result:
        with open(img_path, mode='w+b') as f:
            encoded_img.tofile(f)
            
_, img_dir, json_dir, output_dir = sys.argv

logger = make_logger('log.log')

img_dict = readfiles(img_dir, '.jpg')
json_dict = readfiles(json_dir, '.json')

for filename, img_path in tqdm(img_dict.items()):
    json_path = json_dict.get(filename)
    if json_path:
        logger.info(f'{json_path}')
        root, file = os.path.split(img_path)
        filename, ext = os.path.splitext(file)
        mid = '\\'.join(root.split('\\')[len(img_dir.split('\\')):])
        folder= os.path.join(output_dir, mid)
        os.makedirs(folder, exist_ok=True)
        
        with open(json_path, encoding='utf-8') as f:
            json_file = json.load(f)
        
        
        i = 1
        color = (0,0,255)
        for obj in json_file['objects']:
            img = read_img(img_path)
            points = obj['points']
            x1y1 = tuple([round(p) for p in points[0]])
            x2y2 = tuple([round(p) for p in points[1]])
            output_filename = f"{filename}_{i}{ext}"
            output_img_path = os.path.join(folder, output_filename)
            if i == 2:
                color = (0, 255, 255)
            cv2.rectangle(img, x1y1, x2y2, color =color, thickness=3)
            
            save_img(output_img_path, img)
            
            i += 1
