import cv2, json, os, sys
import numpy as np
import pandas as pd
import logging
import random
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

def select_color(i):
    if i == 0:
        color = (0, 0, 255)
    elif i == 1:
        color = (255, 0, 0)
    else:
        r = random.randrange(0,256)
        g = random.randrange(0,256)
        b = random.randrange(0,256)
        color = (b, g, r) 

    return color 

_, img_dir, json_dir, output_dir, font_size = sys.argv

logger = make_logger('log.log')

img_dict = readfiles(img_dir, '.jpg')
json_dict = readfiles(json_dir, '.json')

list2df = []
for filename, json_path in tqdm(json_dict.items()):
    img_path = img_dict[filename]
    output_img_path = makeOutputPath(img_path, img_dir, output_dir, 'jpg')

    data = readJson(json_path)

    bbox = data.get("bbox")
    polygon = data.get("polygon")
    
    draw_points = []
    text_info = []
    
    draw_dict = defaultdict(list)
    font = cv2.FONT_HERSHEY_PLAIN
    fontScale = int(font_size)
    bbox_count = 0
    poly_count = 0
    if bbox:        
        codes = bbox["vienna_code"]
        points_list = bbox["vienna_points"]
        for idx, points in enumerate(points_list):
            x1y1 = (round(points[0][0]), round(points[0][1]))
            x2y2 = (round(points[1][0]), round(points[1][1]))
            draw_dict[(x1y1, x2y2)].append(codes[idx])
            #     draw_points.append((x1y1, x2y2))
            bbox_count += 1
            # for code in codes:
            #     text_info.append(code)

    if polygon:
        codes = polygon["vienna_code"]
        points_list = polygon["vienna_points"]
        for idx, points in enumerate(points_list):
            points = [[round(i[0]), round(i[1])] for i in points]
            x1y1 = tuple(map(round, points[0]))
            pts = np.array(points, np.int32)
            draw_dict[x1y1].append((pts, codes[idx]))
                # draw_points.append([pts])
            poly_count += 1
            # for code in codes:
            #     text_info.append(code)

    list2df.append([filename, bbox_count, poly_count, bbox_count+poly_count])
    img = read_img(img_path)


    t = '000000'
    w, h = get_textsize(t, font, fontScale)
    text_coor = [5, h]
    i = 0
    for key, codes_list in draw_dict.items():
        color = select_color(i)
        if type(key[0]) == tuple:
            cv2.rectangle(img, key[0], key[1], color=color, thickness=2)
            for text in codes_list:
                cv2.putText(img, text, tuple(text_coor), fontFace=font, fontScale=fontScale, color=color, thickness=2)
                text_coor[1] += h+5
        else:
            for codes in codes_list:
                pts = codes[0]
                text = codes[1]
                cv2.polylines(img, [pts], isClosed=True, color=color, thickness=2)
                cv2.putText(img, text, tuple(text_coor), fontFace=font, fontScale=fontScale, color=color, thickness=2)
                text_coor[1] += h+5
        i += 1
    save_img(output_img_path, img, 'jpg')

df = pd.DataFrame(list2df, columns=['파일명', 'bbox', 'polygon', '합'])
df.to_excel(f"{output_dir}/vis_count.xlsx", index=False)