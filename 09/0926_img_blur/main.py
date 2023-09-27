import json, cv2, os, sys
import logging
import numpy as np
from collections import defaultdict
from tqdm import tqdm

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

def makeOutputPath(file_path, file_dir, output_dir, type=None):
    root, file = os.path.split(file_path)
    filename, ext = os.path.splitext(file)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    # new_filename = f"blur_{filename}.jpg"
    # if type=='blur':
    #     output_path = os.path.join(output_dir, mid_dir, new_filename)
    # else:
    output_path = os.path.join(output_dir, mid_dir, file)
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path

_, json_dir, img_dir, output_dir = sys.argv

logger = make_logger('log.log')

img_dict = readfiles(img_dir, '.jpg')
json_dict = readfiles(json_dir, '.json')

for filename, img_path in tqdm(img_dict.items()):
    json_path = json_dict.get(filename)
    if json_path:
        output_img_path = makeOutputPath(img_path, img_dir, output_dir)
        # output_blur_img_path = makeOutputPath(img_path, img_dir, output_dir, type='blur')
        with open(json_path, encoding='utf-8') as f:
            json_file = json.load(f)
        
        img = read_img(img_path)
        # save_img(output_img_path, img)
        
        for obj in json_file['objects']:
            if len(obj['points']) > 1:
                x1 = round(obj['points'][0][0])
                y1 = round(obj['points'][0][1])
                width = round(obj['points'][1][0]) - x1
                height =round(obj['points'][1][1]) - y1
                
                roi = img[y1:y1+height, x1:x1+width]
                blur_img = cv2.GaussianBlur(roi, (51,51),0)

                img[y1:y1+height, x1:x1+width] = blur_img
            
        save_img(output_img_path, img)
            