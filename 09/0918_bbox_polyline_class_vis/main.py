import cv2, os, sys, json
import logging
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

def save_img(img_path, img):
    result, encoded_img = cv2.imencode('.jpg', img)
    logger.info(f"{img_path} 저장!!")
    if result:
        with open(img_path, mode='w+b') as f:
            encoded_img.tofile(f)

def makeOutputPath(file_path, file_dir, output_dir):
    root, file = os.path.split(file_path)
    relpath = os.path.relpath(file_path, file_dir)
    mid_dir = os.path.split(relpath)[0]
    output_path = os.path.join(output_dir, mid_dir, file)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    return output_path

_, input_dir, output_dir, mode = sys.argv

logger = make_logger('log.log')

img_dict = readfiles(input_dir, '.png')
json_dict = readfiles(input_dir, '.json')

for filename, img_path in tqdm(img_dict.items()):
    json_path = json_dict[filename]

    output_img_path = makeOutputPath(img_path, input_dir, output_dir)

    with open(json_path, encoding='utf-8') as f:
        json_file = json.load(f)

    img = read_img(img_path)
    
    if mode == 'bbox':
        for ann in json_file['annotation']:
            id = ann['id']
            drivingtype = ann['DrivingType']
            cartegory = ann['cartegory']
            text = f'{id} / {cartegory} / {drivingtype}'
            
            if drivingtype == '정상':
                color = (0,0,255)
            elif drivingtype != '정상':
                color = (0,127,255)
                
            x1 = ann['bbox'][0]
            y1 = ann['bbox'][1]
            x2 = x1 + ann['bbox'][2]
            y2 = y1 + ann['bbox'][3]
                        
            cv2.rectangle(img, (x1,y1), (x2,y2), color=color, thickness=3)
            img = label(img, text, 10, color, (x1,y1-10), 0.5)
    
    elif mode == 'polyline':
        for ann in json_file['annotationImage']:
            lineId = ann['lineID']
            lineType = ann['lineType']
            lineColor = ann['lineColor']
            text = f'{lineId} / {lineType} / {lineColor}'

            if lineColor == '백색':
                color = (0,0,255)
            elif lineColor == '황색':
                color = (0,127,255)
            if len(ann['polyline']) > 0:
                polyline = [[poly['x'], poly['y']] for poly in ann['polyline']]
                x_mean = np.mean([poly[0] for poly in polyline])
                y_mean = np.mean([poly[1] for poly in polyline])
                img = label(img, text, 10, color, (x_mean,y_mean), 0.5)
                overlay = img.copy()
                alpha = 0.5
                cv2.polylines(overlay, np.int32([polyline]), False, color, 5, cv2.LINE_AA)
                img = cv2.addWeighted(img, alpha, overlay, 1-alpha, 0)

    save_img(output_img_path, img)
        
            