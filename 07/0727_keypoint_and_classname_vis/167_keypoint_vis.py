import os, sys, json
from collections import defaultdict
import cv2
import numpy as np

def extract_file(path_list, ext):
    for path in path_list:
        if os.path.splitext(path)[-1] == ext:
            return path

def read_img(img_path):
    img_array = np.fromfile(img_path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img
        
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
    color = (0,0, 255)
    
    for obj in json_file['annotationObjectInfo']:
        action_value = obj['actionValue']
        coordinates_keypoints = obj['keypoints']
        coordinates_BBox = obj['BBox']
        
        text = f'{action_name}/{action_value}'
        
        # keypoints가 존재하는 obj info 시각화
        if len(coordinates_keypoints) > 0:
            # keypoints 시각화
            for idx in range(0, len(coordinates_keypoints), 3):
                x = coordinates_keypoints[idx]
                y = coordinates_keypoints[idx+1]
                cv2.circle(img, (x,y), 5, color=color, thickness=-1)

            # bbox 및 텍스트 시각화
            x1 = coordinates_BBox[0]
            y1 = coordinates_BBox[1]
            x2 = x1 + coordinates_BBox[2]
            y2 = y1 + coordinates_BBox[3]
            cv2.rectangle(img, (x1,y1), (x2,y2), color=color, thickness=2)
            cv2.putText(img, text, (x1,y1-10), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=0.5, color=color)
    
    mid = '\\'.join(root.split('\\')[len(input_dir.split('\\')):])
    folder = os.path.join(ouput_dir, mid)
    os.makedirs(folder, exist_ok=True)
    
    save_img_path = os.path.join(folder, file)
    
    result, encoded_img = cv2.imencode('.png', img)
    if result:
        with open(save_img_path, mode='w+b') as f:
            encoded_img.tofile(f)
        print(save_img_path, '저장!!')

    