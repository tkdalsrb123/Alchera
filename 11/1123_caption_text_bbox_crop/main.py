import os, sys, json, cv2, logging
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
    file_dict = defaultdict(list)

    if Ext == 'img':
        for root, dirs, files in os.walk(dir):
            for file in files:
                filename, ext = os.path.splitext(file)
                ext = ext.lower()
                if ext in ['.png', '.jpg']:
                    file_path = os.path.join(root, file)
                
                    file_dict[filename] = file_path
    else:
        for root, dirs, files in os.walk(dir):
            for file in files:
                filename, ext = os.path.splitext(file)
                ext = ext.lower()
                if ext == Ext:
                    file_path = os.path.join(root, file)
                
                    file_dict[filename] = file_path

    return file_dict

def makeOutputPath(file_path, file_dir, output_dir, Ext):
    root, file = os.path.split(file_path)
    filename, ext = os.path.splitext(file)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, f"{filename}.{Ext}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path

def readJson(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def read_img(img_path):
    img_array = np.fromfile(img_path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img

def save_img(img_path, img, ext):
    result, encoded_img = cv2.imencode(f'.{ext}', img)
    if result:
        with open(img_path, mode='w+b') as f:
            encoded_img.tofile(f)

if __name__ == "__main__":
    _, img_dir, json_dir, output_dir = sys.argv
    
    img_dict = readfiles(img_dir, 'img')
    json_dict = readfiles(json_dir, '.json')

    
    for filename, json_path in tqdm(json_dict.items()):

        img_path = img_dict[filename]
        
        data = readJson(json_path)

        img = read_img(img_path)

        for obj in data['objects']:
            crop_filename = obj['id']
            name = obj['name']
            if obj['points']:
                x1 = round(obj['points'][0][0])
                y1 = round(obj['points'][0][1])
                w =  round(obj['points'][1][0]) - x1
                h =  round(obj['points'][1][1]) - y1

                output_img_folder = os.path.join(output_dir, name)
                os.makedirs(output_img_folder, exist_ok=True)
                output_img_path = os.path.join(output_img_folder, f"{crop_filename}.jpg")
                
                crop_img = img[y1:y1+h, x1:x1+w]
                save_img(output_img_path, crop_img, 'jpg')
            
        
        
        