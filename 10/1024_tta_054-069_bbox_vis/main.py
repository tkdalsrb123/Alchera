import os, sys, logging, cv2, json
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

    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            file_path = os.path.join(root, file)
            ext = ext.lower()
            if ext == Ext:
            
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

def visualization(img, eye_pts, vortex_pts, output_img_path):
    if eye_pts:
        x1 = eye_pts[0]
        y1 = eye_pts[1]
        x2 = x1 + eye_pts[2]
        y2 = y1 + eye_pts[3]
    elif vortex_pts:
        x1 = vortex_pts[0]["coor"][0]
        y1 = vortex_pts[0]['coor'][1]
        x2 = x1 + vortex_pts[0]["coor"][0]
        y2 = y1 + vortex_pts[0]["coor"][1]
    
    overlay = img.copy()
    
    cv2.rectangle(img, (x1,y1), (x2,y2), (255,0,0), -1)
    
    result = cv2.addWeighted(img, 0.5, overlay, 0.5, 1.0)
    
    save_img(output_img_path, result, 'png')
if __name__ == '__main__':
    _, input_dir, output_dir = sys.argv
    
    logger = make_logger('log.log')
    json_dict = readfiles(input_dir, '.json')
    img_dict = readfiles(input_dir, '.png')
    
    for filename, json_path in tqdm(json_dict.items()):
        logger.info(json_path)
        img_path = img_dict.get(filename)
        if img_path:
            logger.info(img_path)
            output_img_path = makeOutputPath(img_path, input_dir, output_dir, 'png')
            data = readJson(json_path)
            img = read_img(img_path)
            
            eye_bbox = data['horse_object'].get('eye_bbox')
            vortex_bbox = data['horse_object'].get('vortex_bbox')
            if eye_bbox or vortex_bbox:
                visualization(img, eye_bbox, vortex_bbox, output_img_path)
 