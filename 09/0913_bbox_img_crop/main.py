import os, sys, cv2, json
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

_, input_dir, output_dir = sys.argv

logger = make_logger('log.log')

json_dict = readfiles(input_dir, '.json')
img_dict = readfiles(input_dir, '.jpg')

for filename, img_path in tqdm(img_dict.items()):
    json_path = json_dict[filename]
    logger.info(json_path)
    root, file = os.path.split(img_path)
    filename, ext = os.path.splitext(file)
    mid = '\\'.join(root.split('\\')[len(input_dir.split('\\')):])
    folder = os.path.join(output_dir, mid)
    os.makedirs(folder, exist_ok=True)

    with open(json_path, encoding='utf-8') as f:
        json_file = json.load(f)
    
    img = read_img(img_path)
    i = 1
    for obj in json_file['objects']:
        x = round(obj['points'][0][0])
        y = round(obj['points'][0][1])

        w = round(obj['points'][1][0]) - x
        h = round(obj['points'][1][1]) - y

        file_num = str(i).zfill(3)
        output_img_path = os.path.join(folder, f'{filename}_{file_num}{ext}')
        
        cropped = img[y: y + h:, x: x + w]

        save_img(output_img_path, cropped)

        i += 1