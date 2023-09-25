import json, cv2, os, sys
import logging
import numpy as np
from collections import defaultdict
from random import randint
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
_, img_dir, json_dir, save_dir = sys.argv

logger = make_logger('log.log')

img_dict = readfiles(img_dir, '.png')
json_dict = readfiles(json_dir, '.json')

for filename, img_path in tqdm(img_dict.items()):
    json_path = json_dict[filename]
    output_img_path = makeOutputPath(img_path, img_dir, save_dir)
    with open(json_path, encoding='utf-8') as f:
        json_file = json.load(f)
    
    horse_object = json_file.get('horse_object')
    img = read_img(img_path)
    if horse_object:
        font = cv2.FONT_HERSHEY_DUPLEX
        fontScale = 3     # 글씨 크기
        text_thickness = 5      # 글씨 굵기
        polygon_thickness = 10      # 폴리곤 선 굵기
        alpha = 0.5     # 배경 투명도 설정
        for polygon in horse_object['polygon']:
            text = polygon['category']
            coor = polygon['coor'][0]
            pts = [[coor[i], coor[i+1]] for i in range(0, len(coor), 2)]
            xmin = min([coor[i] for i in range(0, len(coor), 2)])
            ymin = min([coor[i+1] for i in range(0, len(coor), 2)])
            text_w, text_h = cv2.getTextSize(text, font, fontScale=fontScale, thickness=text_thickness)[0]
            pts = np.array(pts)

            overlay = img.copy()
            r = randint(0, 255)
            g = randint(0, 255)
            b = randint(0, 255)
            color = (r,g,b)
            cv2.fillPoly(overlay, [pts], color)
            cv2.rectangle(overlay, (xmin-10, ymin-10), (xmin+text_w+10, ymin+text_h+10), color=(255,255,255), thickness=-1)

            img = cv2.addWeighted(img, alpha, overlay, 1-alpha, 0)
            cv2.polylines(img, [pts], True, color, thickness=polygon_thickness)
            cv2.putText(img, text, (xmin, ymin+text_h), fontFace=font, fontScale=fontScale, color=(0,0,255), thickness=text_thickness)

            save_img(output_img_path, img)