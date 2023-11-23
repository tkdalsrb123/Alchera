import os, sys, logging, cv2, json
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

def select_color(index):
    if index == 0:
        color = (255, 255, 0)
    elif index%2 == 0:
        color = (0, 255, 0)
    elif index%2 == 1:
        color = (0, 255, 255)
        
    return color

def vis_skeleton(img, kp_list):
    key_dict = {}
    
    for idx, keypoints in enumerate(kp_list):
        key_dict[str(idx)] = keypoints
    
    head = [key_dict['4'], key_dict['2'], key_dict['0'], key_dict['1'], key_dict['3']]
    right_arm = [key_dict['6'], key_dict['8'], key_dict['10']]
    left_arm = [key_dict['5'], key_dict['7'], key_dict['9']]
    body = [key_dict['5'], key_dict['6'], key_dict['12'], key_dict['11'], key_dict['5']]
    right_leg = [key_dict['12'], key_dict['14'], key_dict['16']]
    left_leg = [key_dict['11'], key_dict['13'], key_dict['15']]
    
    line_vis_list = [head, right_arm, left_arm, body, right_leg, left_leg]

    for line in line_vis_list:
        pts = [[i[0]] for i in line if i[0] != [0, 0]]
        pts = np.array(pts)
        cv2.polylines(img, np.int32([pts]), False, (0,0,255))
    
    for idx, keypoints in enumerate(kp_list):
        if keypoints[1] == 0:
            pass
        elif keypoints[1] == 1:
            color = select_color(idx)
            cv2.circle(img, keypoints[0], 3, color=color, thickness=-1)
        elif keypoints[1] == 2:
            color = select_color(idx)
            cv2.circle(img, keypoints[0], 3, color=color, thickness=1)            
    
    
if __name__ == "__main__":
    _, input_dir, output_dir = sys.argv
    
    logger = make_logger('log.log')

    json_dict = readfiles(input_dir, '.json')
    img_dict = readfiles(input_dir, '.png')

    for filename, json_path in tqdm(json_dict.items()):
        filename = os.path.splitext(filename)[0]
        logger.info(json_path)
        img_path = img_dict[filename]

        output_img_path = makeOutputPath(img_path, input_dir, output_dir, 'png')
        data = readJson(json_path)

        annotations = data.get('annotations')

        img = read_img(img_path)

        if annotations:
            for ann in annotations:
                keypoints_list = [[[round(ann['keypoints'][idx]), round(ann['keypoints'][idx+1])], round(ann['keypoints'][idx+2])] for idx in range(0, len(ann['keypoints']), 3)]
                vis_skeleton(img, keypoints_list)
        
        save_img(output_img_path, img, 'png')