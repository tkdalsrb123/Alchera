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

def read_img(img_path):
    img_array = np.fromfile(img_path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img

_, img_dir, json_dir, output_dir, font_size = sys.argv

logger = make_logger('log.log')

img_dict = readfiles(img_dir, '.jpg')
json_dict = readfiles(json_dir, '.json')

count_list = []
for filename, img_path in tqdm(img_dict.items()):
    json_path = json_dict[filename]
    
    logger.info(json_path)
    root, file = os.path.split(img_path)
    mid = '\\'.join(root.split('\\')[len(img_dir.split('\\')):])
    folder= os.path.join(output_dir, mid)
    os.makedirs(folder, exist_ok=True)
    output_img_path = os.path.join(folder, file)

    with open(json_path, encoding='UTF-8') as f:
        json_file = json.load(f)

    img = read_img(img_path)
    font = cv2.FONT_HERSHEY_PLAIN
    fontScale = int(font_size)
    have_bbox = json_file.get('bbox')
    have_poly = json_file.get('polygon')
    bbox_count = 0
    poly_count = 0 
    if have_bbox != None and have_poly != None:
        vie_codes = json_file['bbox']['mid_vienna_codes']
        bbox_count = len(json_file['bbox']['points'])
        poly_count = len(json_file['polygon']['points'])
        for idx, points in enumerate(json_file['bbox']['points']):
            x1y1 = (round(points[0][1]), round(points[0][0]))
            x2y2 = (round(points[1][1]), round(points[1][0]))
            text = json_file['bbox']['mid_vienna_codes'][idx]
            text_w, text_h = cv2.getTextSize(text, font, fontScale=fontScale, thickness=3)[0]
            cv2.rectangle(img, x1y1, x2y2, color=(0, 0, 255), thickness=3)
            cv2.rectangle(img, x1y1, (x1y1[0]+text_w, x1y1[1]+text_h), color=(255,255,255), thickness=-1)
            cv2.putText(img, text, (x1y1[0], x1y1[1]+text_h), fontFace=font, fontScale=fontScale, color=(0,0,0), thickness=3)

        vie_codes = json_file['polygon']['mid_vienna_codes']
        for idx, points in enumerate(json_file['polygon']['points']):
            points = [[round(i[1]), round(i[0])] for i in points]
            x1y1 = tuple(map(round, points[0]))
            pts = np.array(points, np.int32)
            text = json_file['polygon']['mid_vienna_codes'][idx]
            text_w, text_h = cv2.getTextSize(text, font, fontScale=fontScale, thickness=3)[0]
            cv2.polylines(img, [pts], isClosed=True, color=(0, 0, 255), thickness=3)
            cv2.rectangle(img, x1y1, (x1y1[0]+text_w, x1y1[1]+text_h), color=(255,255,255), thickness=-1)
            cv2.putText(img, text, (x1y1[0], x1y1[1]+text_h), fontFace=font, fontScale=fontScale, color=(0,0,0), thickness=3)

    elif have_bbox != None:
        bbox_count = len(json_file['bbox']['points'])
        vie_codes = json_file['bbox']['mid_vienna_codes']
        for idx, points in enumerate(json_file['bbox']['points']):
            x1y1 = (round(points[0][1]), round(points[0][0]))
            x2y2 = (round(points[1][1]), round(points[1][0]))

            text = json_file['bbox']['mid_vienna_codes'][idx]
            text_w, text_h = cv2.getTextSize(text, font, fontScale=fontScale, thickness=3)[0]
            cv2.rectangle(img, x1y1, x2y2, color=(0, 0, 255), thickness=3)
            cv2.rectangle(img, x1y1, (x1y1[0]+text_w, x1y1[1]+text_h), color=(255,255,255), thickness=-1)
            cv2.putText(img, text, (x1y1[0], x1y1[1]+text_h), fontFace=font, fontScale=fontScale, color=(0,0,0), thickness=3)

    elif have_poly != None:
        poly_count = len(json_file['polygon']['points'])
        vie_codes = json_file['polygon']['mid_vienna_codes']
        for idx, points in enumerate(json_file['polygon']['points']):
            points = [[round(i[1]), round(i[0])] for i in points]
            x1y1 = tuple(map(round, points[0]))
            pts = np.array(points, np.int32)
            text = json_file['polygon']['mid_vienna_codes'][idx]
            text_w, text_h = cv2.getTextSize(text, font, fontScale=fontScale, thickness=3)[0]
            cv2.polylines(img, [pts], isClosed=True, color=(0, 0, 255), thickness=3)
            cv2.rectangle(img, x1y1, (x1y1[0]+text_w, x1y1[1]+text_h), color=(255,255,255), thickness=-1)
            cv2.putText(img, text, (x1y1[0], x1y1[1]+text_h), fontFace=font, fontScale=fontScale, color=(0,0,0), thickness=3)
                

    result, encoded_img = cv2.imencode('.jpg', img)
    logger.info(f"{output_img_path} 저장!!")
    if result:
        with open(output_img_path, mode='w+b') as f:
            encoded_img.tofile(f)
    
    count_list.append([filename, bbox_count, poly_count, bbox_count+poly_count])

df = pd.DataFrame(count_list, columns=['파일명', 'bbox', 'polygon', '합'])
df.to_excel(f'{output_dir}/count_list.xlsx', index=False)