import os, sys, json, logging, cv2, random
import pandas as pd
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
            if Ext == '.png':
                if ext == Ext:
                    unique = root.split('\\')[-2]
                    file_path = os.path.join(root, file)
                
                    file_dict[unique].append(file_path)
            else:
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

def read_img(img_path):
    img_array = np.fromfile(img_path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img

def save_img(img_path, img, ext):
    result, encoded_img = cv2.imencode(f'.{ext}', img)
    if result:
        with open(img_path, mode='w+b') as f:
            encoded_img.tofile(f)

def make_path(x):
    path = os.path.join(img_dir, sequence, x['view'], x['FileName'])
    bbox_list = []
    for i in range(2, len(x.values), 4):
        if x.values[i] != 0:
            x1y1 = (x.values[i], x.values[i+1])
            x2y2=  (x.values[i+2], x.values[i+3])
            bbox_list.append([x1y1, x2y2])
    img_info_list.append((path, bbox_list))
            
if __name__ == "__main__":
    _, img_dir, csv_dir, output_dir = sys.argv
    
    csv_dict = readfiles(csv_dir, '.csv')
    
    for sequence, csv_path in tqdm(csv_dict.items(), desc="read csv", position=0):
        df = pd.read_csv(csv_path, encoding='utf-8')
        img_info_list = []
        df.apply(make_path, axis=1)
        
        for img_path, bbox_list in tqdm(img_info_list, desc="read img", position=1):
            
            output_img_path = makeOutputPath(img_path, img_dir, output_dir, 'png')
            img = read_img(img_path)
            for bbox in bbox_list:
                cv2.rectangle(img, bbox[0], bbox[1], (0, 0, 255), 2)
        
            save_img(output_img_path, img, 'png')


                    