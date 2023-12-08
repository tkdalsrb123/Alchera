import os, sys, cv2, json, logging
from collections import defaultdict
import numpy as np
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
    file_dict = defaultdict(list)

    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            ext = ext.lower()
            if ext in Ext:
                file_path = os.path.join(root, file)
            
                file_dict[filename] = file_path
    return file_dict

def makeOutputPath(file_path, file_dir, output_dir):
    root, file = os.path.split(file_path)
    filename, ext = os.path.splitext(file)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, f"{filename}{ext}")
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

def save_img(img_path, img):
    ext = os.path.splitext(img_path)[-1]
    result, encoded_img = cv2.imencode(f'{ext}', img)
    if result:
        with open(img_path, mode='w+b') as f:
            encoded_img.tofile(f)
            
if __name__ == '__main__':
    _, img_dir, json_dir, output_dir = sys.argv
    
    logger = make_logger('log.log')
    img_dict = readfiles(img_dir, ['.jpg', '.jpeg'])
    json_dict = readfiles(json_dir, ['.json'])
    
    for filename, json_path in tqdm(json_dict.items()):
        logger.info(json_path)
        img_path = img_dict[filename]
        output_img_path = makeOutputPath(img_path, img_dir, output_dir)
        data = readJson(json_path)
        
        cat_dict = {}
        for cat in data['Categories']:
            cat_dict[cat['id']] = cat['name']
        ann_dict = {}
        for ann in data['Annotations']:
            _id = ann['category_id']
            ann_dict[_id] = [round(b) for b in ann['bbox']]
        
        color = (0, 0, 255)
        img = read_img(img_path)
        for _id, bbox in ann_dict.items():
            text = cat_dict[_id]
            x1y1 = (bbox[0], bbox[1])
            x2y2 = (x1y1[0] + bbox[2], x1y1[1] + bbox[3])
            cv2.rectangle(img, x1y1, x2y2, color, 3)
            cv2.putText(img, text, (x1y1[0]+5, x1y1[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.3, color, 1)
        
        save_img(output_img_path, img)
            