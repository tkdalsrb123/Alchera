import os, sys, cv2, json, logging
import numpy as np
from label import label
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


categories = {
       1  : "아스팔트 도로파임",
    
       2 : "콘크리트 도로파임",
    
       3 : "종방향균열",
   
       4 : "횡방향균열",
   
       5 : "거북등균열",
   
       6 : "줄눈부파손",
   
       7 : "십자파손",
   
       8 : "절삭보수부파손",
   
       9 : "긴급보수부파손",
   
       10 : "응력완화줄눈 화살표",
   
       11 : "응력완화줄눈 오각형",
   
       12 : "응력완화줄눈 삼각형",
   
       13 : "응력완화줄눈",
   
       14 : "신축이음부",
   
       15 : "차선",
   
       16 : "규제봉",
   
       17 : "맨홀",

       18 : "배수로" }
 

if __name__ == '__main__':
    _, img_dir, json_dir, output_dir = sys.argv
    
    logger = make_logger('log.log')

    img_dict = readfiles(img_dir, '.jpg')
    json_dict = readfiles(json_dir, '.json')
    
    for filename, json_path in tqdm(json_dict.items()):
        logger.info(json_path)
        img_path = img_dict[filename]

        output_img_path = makeOutputPath(img_path, img_dir, output_dir, 'jpg')
        data = readJson(json_path)
        img = read_img(img_path)
        
        annotations = data['annotations']

        if type(annotations) == dict:
            annotations = [annotations]
        
        for ann in annotations: 
            category_id = ann['category_id']
            bbox = ann.get('bbox')
            seg = ann.get('segmentation')
            category = categories.get(category_id)
            if bbox:
                x1 = round(bbox[0])
                y1 = round(bbox[1])
                x2 = x1 + round(bbox[2])
                y2 = y1 + round(bbox[3])
                cv2.rectangle(img, (x1,y1), (x2, y2), color=(0, 0, 255), thickness=3)
                if category:
                    img = label(img, category, 20, (255, 0, 0), (x1, y2), 0.5)
                
            if seg:
                points = [(round(seg[i]), round(seg[i+1])) for i in range(0, len(seg), 2)]
                points = np.array(points, np.int32)
                cv2.polylines(img, [points], isClosed=True, color=(0, 0, 255), thickness=3)
                if category:
                    img = label(img, category, 20, (255, 0, 0), points[0], 0.5)
            
        
        save_img(output_img_path, img, 'jpg')
        logger.info(output_img_path)