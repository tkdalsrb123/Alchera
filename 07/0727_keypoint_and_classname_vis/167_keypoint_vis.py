import os, sys, json
from collections import defaultdict
import cv2
import numpy as np
import random

def extract_file(path_list, ext):
    for path in path_list:
        if os.path.splitext(path)[-1] == ext:
            return path

def read_img(img_path):
    img_array = np.fromfile(img_path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img

def visualization(image, put_text, color, bbox, keypoints=[]):
    # keypoints 시각화
    for idx in range(0, len(keypoints), 3):
        x = keypoints[idx]
        y = keypoints[idx+1]
        point_text = str(keypoints[idx+2])
        cv2.circle(image, (x,y), 5, color=color, thickness=-1)
        cv2.putText(image, point_text, (x-5,y-10), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=0.5, color=color)

    # bbox 및 텍스트 시각화
    x1 = bbox[0]
    y1 = bbox[1]
    x2 = x1 + bbox[2]
    y2 = y1 + bbox[3]
    if len(keypoints) == 0:
        cv2.rectangle(image, (x1,y1), (x2,y2), color=color, thickness=2)

        if y1-10 > 1:
            cv2.putText(image, put_text, (x1,y1-10), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=0.5, color=color)
        else:   # 이미지 벗어날 경우 박스 하단에 시각화
            cv2.putText(image, put_text, (x1,y2+15), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=0.5, color=color)

_, input_dir, ouput_dir = sys.argv

# 파일 수집
matching_dict = defaultdict(list)
for root, dirs, files in os.walk(input_dir):
    for file in files:
        filename, ext = os.path.splitext(file)
        if ext == '.json':
            json_path = os.path.join(root, file)
            matching_dict[filename].append(json_path)
        
        elif ext == '.png':
            image_path = os.path.join(root, file)
            matching_dict[filename].append(image_path)

for path in matching_dict.values():
    json_path = extract_file(path, '.json')
    image_path = extract_file(path, '.png')
    
    print(image_path, '시각화!!')
    root, file = os.path.split(image_path)
    
    with open(json_path, 'r', encoding='utf-8') as f:
        json_file = json.load(f)
        
    action_name = json_file['annotationImageInfo']['action']
    
    img = read_img(image_path)
    for obj in json_file['annotationObjectInfo']:
        action_value = obj['actionValue']
        coordinates_keypoints = None
        if 'keypoints' in obj.keys():
            coordinates_keypoints = obj['keypoints']
        coordinates_BBox = obj['BBox']
        
        text = f'{action_name}/{action_value}'
        
        if action_value == True:
            # r = random.randint(0, 255)
            # g = random.randint(0, 255)
            # b = random.randint(0, 255)
            # select_color = (r, g, b)
            select_color = (0, 0, 255)
    
        elif action_value == False:
            select_color = (255, 0, 0)
        
        # keypoints가 존재하는 obj info 시각화
        if coordinates_keypoints is not None:
            visualization(img, text, select_color, coordinates_BBox, coordinates_keypoints)

        else:
            visualization(img, text, select_color, coordinates_BBox)
                
    mid = '\\'.join(root.split('\\')[len(input_dir.split('\\')):])
    folder = os.path.join(ouput_dir, mid)
    os.makedirs(folder, exist_ok=True)
    
    save_img_path = os.path.join(folder, file)
    
    result, encoded_img = cv2.imencode('.png', img)
    if result:
        with open(save_img_path, mode='w+b') as f:
            encoded_img.tofile(f)
        print(save_img_path, '저장!!')