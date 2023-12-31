import json, os, sys, cv2
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
    if Ext == 'img':
        for root, dirs, files in os.walk(dir):
            for file in files:
                filename, ext = os.path.splitext(file)
                if ext == '.jpg' or ext == '.jpeg':
                    file_path = os.path.join(root, file)

                    file_dict[filename] = file_path
    elif Ext == 'json':
        for root, dirs, files in os.walk(dir):
            for file in files:
                filename, ext = os.path.splitext(file)
                if ext == '.json':
                    file_path = os.path.join(root, file)

                    file_dict[filename] = file_path
    return file_dict

def read_img(img_path):
    img_array = np.fromfile(img_path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img

_, img_dir, json_dir, output_dir = sys.argv

logger = make_logger('log.log')

img_dict = readfiles(img_dir, 'img')
json_dict = readfiles(json_dir, 'json')

for filename, img_path in tqdm(img_dict.items()):
    json_path = json_dict[filename]
    
    root, file = os.path.split(img_path)
    mid = '\\'.join(root.split('\\')[len(img_dir.split('\\')):])
    folder= os.path.join(output_dir, mid)
    os.makedirs(folder, exist_ok=True)
    output_img_path = os.path.join(folder, file)
    
    with open(json_path, encoding='UTF-8') as f:
        json_file = json.load(f)
    
    img = read_img(img_path)
    font = cv2.FONT_HERSHEY_PLAIN
    fontScale = 3
    for img_data in json_file['imageDataList']:
        if os.path.splitext(img_data['imageName'])[0] == filename:
            for rect in img_data['rectangleEntries']:
                text = rect['name']
                points = rect['points']
                
                
                text_w, text_h = cv2.getTextSize(text, font, fontScale=fontScale, thickness=3)[0]
                cv2.rectangle(img, (points[0], points[1]), (points[2], points[3]), color=(0, 0, 255), thickness=3)
                cv2.rectangle(img, (points[0], points[1]),(points[0]+text_w, points[1]+text_h), color=(255,255,255), thickness=-1)
                cv2.putText(img, text, (points[0], points[1]+text_h), fontFace=font, fontScale=fontScale, color=(0,0,0), thickness=3)
            
    
    result, encoded_img = cv2.imencode('.jpg', img)
    logger.info(f"{output_img_path} 저장!!")
    if result:
        with open(output_img_path, mode='w+b') as f:
            encoded_img.tofile(f)
    
    
                
                