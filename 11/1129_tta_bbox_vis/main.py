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

def makeOutputPath(file_path, file_dir, output_dir, Ext):
    root, file = os.path.split(file_path)
    filename, ext = os.path.splitext(file)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, f"{filename}.{Ext}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path

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
            
def readJson(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

if __name__ == "__main__":
    _, input_dir ,output_dir = sys.argv
    logger = make_logger('log.log')

    img_dict = readfiles(input_dir, '.jpg')
    json_dict = readfiles(input_dir, '.json')

    for filename, img_path in tqdm(img_dict.items()):
        json_path = json_dict.get(filename)
        if json_path:
            output_img_path = makeOutputPath(img_path, input_dir, output_dir, 'jpg')
            
            json_file = readJson(json_path)
            
            
            img = read_img(img_path)
            for obj in json_file['objects']:
                points = obj['points']
                name = obj['name']
                if name == '영역오류':
                    x1y1 = tuple([round(p) for p in points[0]])
                    x2y2 = tuple([round(p) for p in points[1]])

                    cv2.rectangle(img, x1y1, x2y2, color =(0, 0, 0), thickness=3)
            save_img(output_img_path, img)
