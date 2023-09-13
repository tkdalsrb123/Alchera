import cv2, json, sys, os
from collections import defaultdict
import numpy as np
import logging
from tqdm import tqdm
import pandas as pd

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

def read_img(img_path):
    img_array = np.fromfile(img_path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img

def save_img(output_path, img):
    result, encoded_img = cv2.imencode('.jpg', img)
    logger.info(output_path)
    if result:
        with open(output_path, mode='w+b') as f:
            encoded_img.tofile(f)

def readfiles(dir, Ext):
    file_dict = defaultdict(str)
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext == Ext:
                file_path = os.path.join(root, file)
                
                file_dict[filename] = file_path
                
    return file_dict

def vis_skeleton(img, id, sk_info, output_path):
    key_dict = {}

    if id == '01':
        bbox_color = (0, 0, 255)
    elif id == '02':
        bbox_color = (0, 255, 255)

    x1 = round(sk_info['bbox'][0])
    y1 = round(sk_info['bbox'][1])
    x2 = round(sk_info['bbox'][2])
    y2 = round(sk_info['bbox'][3])
    
    for idx, keypoints in enumerate(sk_info['keypoints']):
        info_list.append(keypoints)
        key_dict[str(idx)] = [round(keypoints[0]), round(keypoints[1])]
        if keypoints[2] == 0:
            color = (255, 0, 0)
        elif keypoints[2] == 2:
            color = (0, 255, 255)
        elif keypoints[2] == 1:
            color = (0, 255, 0)
        cv2.circle(img, (round(keypoints[0]),round(keypoints[1])), 3, color=color, thickness=-1)
        cv2.putText(img, str(idx),(round(keypoints[0])-5,round(keypoints[1])-2), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=0.3, color=color)
    
    cv2.rectangle(img, (x1,y1), (x2,y2), color=bbox_color, thickness=3)

    head = [key_dict['4'], key_dict['2'], key_dict['0'], key_dict['1'], key_dict['3']]
    right_arm = [key_dict['6'], key_dict['8'], key_dict['10']]
    left_arm = [key_dict['5'], key_dict['7'], key_dict['9']]
    body = [key_dict['5'], key_dict['6'], key_dict['12'], key_dict['11'], key_dict['5']]
    right_leg = [key_dict['12'], key_dict['14'], key_dict['16']]
    left_leg = [key_dict['11'], key_dict['13'], key_dict['15']]
    
    line_vis_list = [head, right_arm, left_arm, body, right_leg, left_leg]

    for line in line_vis_list:
        pts = [[i[0], i[1]] for i in line]
        pts = np.array(pts)
        cv2.polylines(img, np.int32([pts]), False, (0, 69, 255))
    
    save_img(output_path, img)

_, img_dir, json_dir, output_dir = sys.argv

logger = make_logger('log.log')

json_dict = readfiles(json_dir, '.json')
img_dict = readfiles(img_dir, '.jpg')

df2list = []
for filename, img_path in tqdm(img_dict.items()):
    json_path = json_dict.get(filename)
    if json_path:
        json_path = json_dict[filename]
        
        root, file = os.path.split(img_path)
        mid = '\\'.join(root.split('\\')[len(img_dir.split('\\')):])
        folder = os.path.join(output_dir, mid)
        os.makedirs(folder, exist_ok=True)
        output_img_path = os.path.join(folder, file)
        logger.info(json_path)
        with open(json_path, encoding='utf-8') as f:
            json_file = json.load(f)

        img = read_img(img_path)
        if type(json_file[0]) == list:
            for info in json_file:
                info = info[0]
                key_dict = {}
                id = info['ID'][0]
                info_list = [filename, id]
                vis_skeleton(img, id, info, output_img_path)
                df2list.append(info_list)

        elif type(json_file[0]) == dict:
            id = json_file[0]['ID'][0]
            key_dict = {}
            info_list = [filename, id]
            vis_skeleton(img, id, json_file[0], output_img_path)
            df2list.append(info_list)

df = pd.DataFrame(df2list, columns=['filename', 'ID', 'BBox', 'nose', 'left eye', 'right eye', 'left ear', 'right ear', 'left shoulder',  'right shoulder', 'left wrist', 'right wrist', 'left hip', 'right hip', 'left knee', 'right knee', 'left ankle', 'right ankle'])
df.to_excel(f'{output_dir}/file_list.xlsx', index=False)