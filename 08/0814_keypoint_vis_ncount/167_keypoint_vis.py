import os, sys, json
from collections import defaultdict
import cv2
import numpy as np
from tqdm import tqdm

def extract_file(path_list, ext):
    for path in path_list:
        if os.path.splitext(path)[-1] == ext:
            return path

def read_img(img_path):
    img_array = np.fromfile(img_path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img

def bbox_vis(image, put_text, color, bbox):
    # bbox 및 텍스트 시각화
    x1 = bbox[0]
    y1 = bbox[1]
    x2 = x1 + bbox[2]
    y2 = y1 + bbox[3]
    cv2.rectangle(image, (x1,y1), (x2,y2), color=color, thickness=2)

    if y1-10 > 1:
        cv2.putText(image, put_text, (x1,y1-10), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=color)
    else:   # 이미지 벗어날 경우 박스 하단에 시각화
        cv2.putText(image, put_text, (x1,y2+15), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=color)
   

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

for path in tqdm(matching_dict.values()):
    json_path = extract_file(path, '.json')
    image_path = extract_file(path, '.png')
    
    print(image_path, '시각화!!')
    root, file = os.path.split(image_path)

    mid = '\\'.join(root.split('\\')[len(input_dir.split('\\')):])
    folder = os.path.join(ouput_dir, mid)
    os.makedirs(folder, exist_ok=True)
    
    with open(json_path, 'r', encoding='utf-8') as f:
        json_file = json.load(f)
   
    action_name = json_file['annotationImageInfo']['action']
    
    img = read_img(image_path)
    
    keypoint_in_obj = []
    for obj in json_file['annotationObjectInfo']:
        action_value = obj['actionValue']
        if 'keypoints' in obj.keys():
            keypoint_in_obj.append(obj['keypoints'])
        else:
            coordinates_BBox = obj['BBox']
        
        text = f'{action_name}/{action_value}'
        
        if action_value == True:
            select_color = (0, 0, 255)
    
        elif action_value == False:
            select_color = (255, 0, 0)
        
        bbox_vis(img, text, select_color, coordinates_BBox)

    # keypoints 시각화
    num = 1
    for keypoints in keypoint_in_obj:
        copy_img = img.copy()

        for idx in range(0, len(keypoints), 3):
            x = keypoints[idx]
            y = keypoints[idx+1]
            point_text = str(keypoints[idx+2])
            cv2.circle(copy_img, (x,y), 3, color=(0,255,255), thickness=-1)
            cv2.putText(copy_img, point_text, (x-5,y-10), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.4, color=(0,255,255))
        
        save_img_path = os.path.join(folder, f'{filename}_{num}.png')

        result, encoded_img = cv2.imencode('.png', copy_img)
        if result:
            with open(save_img_path, mode='w+b') as f:
                encoded_img.tofile(f)
            print(save_img_path, '저장!!')

        num += 1