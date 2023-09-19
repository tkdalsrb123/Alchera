import cv2, os, sys, json
import logging
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

def select_color(n):
    if n in [2, 5, 8, 9, 10, 15, 16, 17, 18, 19, 20]:
        color = (0,153,0)
    elif n in [3, 6, 11, 12, 13, 21, 22, 23, 24, 25, 26]:
        color = (0,128,255)
    elif n in [1, 4, 7, 14]:
        color = (0,255,255)
    return color

def select_skeleton_color(category):
    if category == 'left_arm' or category == 'left_leg':
        color = (0,153,0)
    elif category == 'body':
        color = (0,255,255)
    elif category == 'right_arm' or category == 'right_leg':
        color = (0,128,255)
    return color

_, img_dir, json_dir, output_dir, mode = sys.argv

logger = make_logger('log.log')

img_dict = readfiles(img_dir, '.jpg')
json_dict = readfiles(json_dir, '.json')

for filename, img_path in tqdm(img_dict.items()):
    json_path = json_dict[filename]

    output_img_path = makeOutputPath(img_path, img_dir, output_dir)
    with open(json_path, encoding='utf-8') as f:
        json_file = json.load(f)
    
    if mode == 'keypoint':
        skeleton_dict = {}

        for i, ann in enumerate(json_file['annotations']):
            img = read_img(img_path)
            
            if ann['player_id'] == 1:
                color = (0,0,255)
            elif ann['player_id'] == 2:
                color = (255,0,0)
            for idx, key in enumerate(range(0, len(ann['keypoints']),3)):
                skeleton_dict[idx+1]=ann['keypoints'][key:key+3]
                
            for num, keypoint in skeleton_dict.items():
                # color = select_color(num)
                visible = keypoint[2]
                if visible == 1:
                    cv2.circle(img, (keypoint[0], keypoint[1]), 3, color=color, thickness=1)
                elif visible == 2:
                    cv2.circle(img, (keypoint[0], keypoint[1]), 3, color=color, thickness=-1)       
                elif visible == 3:
                    cv2.circle(img, (keypoint[0], keypoint[1]), 3, color=(0,255,255), thickness=-1)
            if i == 0:
                new_image = img
            else:
                new_image = np.concatenate((new_image, img), axis=1)

        save_img(output_img_path, new_image)
            # left_arm = [skeleton_dict[7], skeleton_dict[8], skeleton_dict[9], skeleton_dict[10]]
            # left_leg = [skeleton_dict[14], skeleton_dict[15], skeleton_dict[16], skeleton_dict[17], skeleton_dict[18], skeleton_dict[19],  skeleton_dict[20]]
            # body = [skeleton_dict[1], skeleton_dict[4], skeleton_dict[7], skeleton_dict[14]]
            # right_arm = [skeleton_dict[7], skeleton_dict[11], skeleton_dict[12], skeleton_dict[13]]
            # right_leg = [skeleton_dict[14], skeleton_dict[21], skeleton_dict[22], skeleton_dict[23],  skeleton_dict[24],  skeleton_dict[25],  skeleton_dict[26]]

            # line_vis_list = [right_arm, left_arm, body, right_leg, left_leg]
            # line_vis_category = ['right_arm', 'left_arm', 'body', 'right_leg', 'left_leg']

            # for idx, line in enumerate(line_vis_list):
            #     pts = [[i[0], i[1]] for i in line]
            #     pts = np.array(pts)
            #     color = select_skeleton_color(line_vis_category[idx])
            #     cv2.polylines(img, np.int32([pts]), False, color)
    elif mode == 'bbox':
        player_dict = {}
        for player in json_file['players']:
            player_dict[player['id']] = player['description']

        for ann in json_file['annotations']:
            bar_color = player_dict[ann['player_id']]
            x1 = ann['bbox'][0]
            y1 = ann['bbox'][1]
            x2 = x1 + ann['bbox'][2]
            y2 = y1 + ann['bbox'][3]
            
            if bar_color == '홍샅바':
                color = (0,0,255)
            elif bar_color == '청샅바':
                color = (255,0,0)

            cv2.rectangle(img, (x1,y1), (x2,y2), color=color, thickness=3)
        
        save_img(output_img_path, img)