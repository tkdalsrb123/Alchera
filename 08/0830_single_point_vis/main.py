import cv2, json, os, sys
from collections import defaultdict
import numpy as np
import logging
from tqdm import tqdm


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

_, input_dir, output_dir = sys.argv

logger = make_logger('log.log')

json_dict = readfiles(input_dir, '.json')
img_dict = readfiles(input_dir, '.png')

for filename, img_path in tqdm(img_dict.items()):
    have_json = json_dict.get(filename)
    if have_json != None:
        json_path = json_dict[filename]

        root, file = os.path.split(img_path)
        mid = '\\'.join(root.split('\\')[len(input_dir.split('\\')):])
        folder = os.path.join(output_dir, mid)
        os.makedirs(folder, exist_ok=True)
        output_img_path = os.path.join(folder, file)
        
        logger.info(json_path)
        with open(json_path, encoding='UTF-8') as f:
            json_file = json.load(f)
            
        logger.info(img_path)
        img = read_img(img_path)
        color = (0, 0, 255) # 색상
        r = 3   # 원 반지름
        fontsize = 0.5  # 글씨 사이즈
        for point in json_file['points']:
            x = round(float(point['points']['x']))
            y = round(float(point['points']['y']))
            
            name = point['class']['name']

            cv2.circle(img, (x,y), r, color=color, thickness=-1)
            cv2.putText(img, name,(x,y), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=fontsize, color=color)

        result, encoded_img = cv2.imencode('.png', img)
        if result:
            with open(output_img_path, mode='w+b') as f:
                encoded_img.tofile(f)