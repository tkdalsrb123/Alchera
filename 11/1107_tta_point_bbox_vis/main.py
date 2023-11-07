import os, sys, cv2, json, logging
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
    with open(path, 'r') as f:
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
        
if __name__ == '__main__':
    _, input_dir, output_dir, alpha = sys.argv

    logger = make_logger('log.log')
    
    json_dict = readfiles(input_dir, '.json')
    img_dict = readfiles(input_dir, '.jpg')
    
    for filename, json_path in tqdm(json_dict.items()):
        filename = '_'.join(filename.split('_')[:-1])
        logger.info(json_path)
        img_path = img_dict.get(filename)

        output_img_path = makeOutputPath(img_path, input_dir, output_dir, 'jpg')
        data = readJson(json_path)

        vis_list = []
        img = read_img(img_path)
        overlay = img.copy()
        alpha = float(alpha)
        acne_list = data['annotations'].get('acne')
        if acne_list: 
            for acne in acne_list:
                points = acne['points']
                x1y1 = (points[0]-50, points[1]-50)
                x2y2 = (points[0]+50, points[1]+50)
                vis_list.append((x1y1, x2y2))

            alpha = float(alpha)
            for vis in vis_list:
                cv2.rectangle(overlay, vis[0], vis[1], color=(0, 0, 0), thickness=2)
                
            img = cv2.addWeighted(img, alpha, overlay, 1-alpha, 1)

        save_img(output_img_path, img, 'jpg')
        logger.info(output_img_path)