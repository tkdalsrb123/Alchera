import os, sys, json, cv2
from collections import defaultdict
import logging
from tqdm import tqdm
import numpy as np

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
img_dict = readfiles(input_dir, '.jpg')

for filename, json_path in tqdm(json_dict.items()):
    img_path = img_dict[filename]
    logger.info(filename)
    root, file = os.path.split(img_path)
    mid = '\\'.join(root.split('\\')[len(input_dir.split('\\')):])
    folder = os.path.join(output_dir, mid)
    os.makedirs(folder, exist_ok=True)
    output_img_path = os.path.join(folder, file)
    
    with open(json_path, encoding='UTF-8') as f:
        json_file = json.load(f)

    points_x_list = []         
    points_y_list = []         
    for points in json_file['points']:
        points_x_list.append(float(points['points']['x']))
        points_y_list.append(float(points['points']['y']))

    x_min = round(min(points_x_list))
    y_min = round(min(points_y_list))
    x_max = round(max(points_x_list))
    y_max = round(max(points_y_list))

    img = read_img(img_path)
    color = (255, 255, 255)
    
    cv2.rectangle(img, (x_min,y_min), (x_max, y_max), color=color, thickness=-1)

    result, encoded_img = cv2.imencode('.png', img)
    logger.info(f"{output_img_path} 저장!!")
    if result:
        with open(output_img_path, mode='w+b') as f:
            encoded_img.tofile(f)