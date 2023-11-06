import cv2, json, os, sys
import numpy as np
import pandas as pd
import logging
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
    file_dict = defaultdict(str)
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
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
        
def readJson(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data

def get_textsize(text, font, fontscale):
    text_w, text_h = cv2.getTextSize(text, font, fontScale=fontscale, thickness=3)[0]
    
    return text_w, text_h


_, img_dir, json_dir, output_dir, font_size, alpha = sys.argv

logger = make_logger('log.log')

img_dict = readfiles(img_dir, '.jpg')
json_dict = readfiles(json_dir, '.json')

for filename, json_path in tqdm(json_dict.items()):
    img_path = img_dict[filename]
    output_img_path = makeOutputPath(img_path, img_dir, output_dir, 'jpg')

    data = readJson(json_path)

    bbox = data.get("bbox")
    polygon = data.get("polygon")
    
    draw_points = []
    text_info = []
    
    font = cv2.FONT_HERSHEY_PLAIN
    fontScale = int(font_size)
    alpha = float(alpha)
    if bbox:
        if type(bbox) == dict:
            bbox = [bbox]
        
        for box in bbox:
            codes = box["vienna_code"]
            points = box["vienna_points"][0]
            x1y1 = (round(points[0][0]), round(points[0][1]))
            x2y2 = (round(points[1][0]), round(points[1][1]))
            draw_points.append([x1y1, x2y2])
            for code in codes:
                tw, th = get_textsize(code, font, fontScale)
                text_background_points = (x1y1, (x1y1[0]+tw, x1y1[1]+th))
                text_points = (x1y1[0], x1y1[1]+th)
                text_info.append({'text_points':text_points, 'background_points':text_background_points, 'text':code})

    if polygon:
        if type(polygon) == dict:
            polygon = [polygon]
        
        for poly in polygon:
            code = poly["vienna_code"]
            points = poly["vienna_points"][0]
            points = [[round(i[0]), round(i[1])] for i in points]
            x1y1 = tuple(map(round, points[0]))
            pts = np.array(points, np.int32)
            draw_points.append([pts])
            
            for code in codes:
                tw, th = get_textsize(code, font, fontScale)
                text_points = (x1y1[0], x1y1[1]+th)
                text_background_points = (x1y1, (x1y1[0]+tw, x1y1[1]+th))
                text_info.append({'text_points':text_points, 'background_points':text_background_points, 'text':code})

 
    
    img = read_img(img_path)
    
    for draw in draw_points:
        if len(draw) == 2:
            cv2.rectangle(img, draw[0], draw[1], color=(0, 0, 255), thickness=3)
        else:
            cv2.polylines(img, draw, isClosed=True, color=(0, 0, 255), thickness=3)

    overlay = img.copy()
    for text in text_info:
        tp = text['text_points']
        bp = text['background_points']
        t = text['text']
        cv2.rectangle(overlay, bp[0], bp[1], color=(255,255,255), thickness=-1)
        cv2.putText(img, t, tp, fontFace=font, fontScale=fontScale, color=(0,0,0), thickness=1)
       
    img = cv2.addWeighted(img, 1-alpha, overlay, alpha, 1.0)
    
    save_img(output_img_path, img, 'jpg')
            
    
    