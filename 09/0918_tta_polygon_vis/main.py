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

def makeOutputPath(file_path, file_dir, output_dir):
    root, file = os.path.split(file_path)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, file)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path

def select_color(n):
    if n == '11':
        color = (0,0,255)
    elif n == '12':
        color = (0,255,0)
    elif n == '13':
        color = (0,255,255)
    elif n == '14':
        color = (255,0,0)
    elif int(n) >= 21 and int(n) <= 41:
        color = (147,20,255)
    else:
        color = (0,0,0)
    
    return color

_, img_dir, json_dir, output_dir = sys.argv

logger = make_logger('log.log')

img_dict = readfiles(img_dir, '.jpg')
json_dict = readfiles(json_dir, '.json')

for filename, img_path in tqdm(img_dict.items()):
    json_path = json_dict[filename]

    output_img_path = makeOutputPath(img_path, img_dir, output_dir)
    with open(json_path, encoding='utf-8') as f:
        json_file = json.load(f)

    img = read_img(img_path)
    
    for ann in json_file['annotation_info']:
        color = select_color(ann['label_cd'])

        pts = ann['polygon_info']['points']
        pts = np.array(pts)
        cv2.polylines(img, np.int32([pts]), True, color, thickness=3)

    save_img(output_img_path, img)