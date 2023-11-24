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

def select_color(category_id):
    if category_id == 2:
        color = (255,255,0)
    elif category_id == 3:
        color = (255,0,0)
    elif category_id == 8:
        color = (173,255,47)
    elif category_id == 10:
        color = (108,0,255)
    elif category_id == 12:
        color = (255,187,80)
    elif category_id == 51:
        color = (255,0,255)
    elif category_id == 52:
        color = (0,0,255)
    elif category_id == 97:
        color = (0,255,255)
    elif category_id == 98:
        color = (255,255,255)
    elif category_id == 99:
        color = (255,160,207)
    elif category_id == 100:
        color = (0,128,0)
        
    return (color[2], color[1], color[0])

if __name__ == "__main__":
    _, input_dir, output_dir = sys.argv
    
    logger = make_logger('log.log')

    json_dict = readfiles(input_dir, '.json')
    img_dict = readfiles(input_dir, '.png')

    for filename, json_path in tqdm(json_dict.items()):
        logger.info(json_path)
        filename = os.path.splitext(filename)[0]
        img_path = img_dict[filename]

        output_img_path = makeOutputPath(img_path, input_dir, output_dir, 'png')

        data = readJson(json_path)
        
        img = read_img(img_path)
        for annotation in data['annotations']:
            _id = annotation['category_id']
            segmentation = annotation['segmentation']['coord']['points'][0][0]
            seg_coor = [[seg['x'], seg['y']] for seg in segmentation]
            seg_coor = np.array(seg_coor, dtype=np.int32)
            color = select_color(_id)
            cv2.polylines(img, [seg_coor], True, color, 2)
        
        save_img(output_img_path, img, 'png')