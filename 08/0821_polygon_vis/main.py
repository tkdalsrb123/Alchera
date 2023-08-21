import json, os, sys, cv2
from collections import defaultdict
import numpy as np

def read_files(path, Ext):
    if Ext == 'json':
        file_dict = defaultdict(str)
        for root, dirs, files in os.walk(path):
            for file in files:
                filename, ext = os.path.splitext(file)
                if ext == '.json':
                    file_path = os.path.join(root, file)

                    file_dict[filename] = file_path
    elif Ext == 'img':
        file_dict = defaultdict(str)
        for root, dirs, files in os.walk(path):
            for file in files:
                filename, ext = os.path.splitext(file)
                if ext == '.png' or ext == '.jpg':
                    file_path = os.path.join(root, file)

                    file_dict[filename] = file_path
    
    return file_dict

def read_img(img_path):
    img_array = np.fromfile(img_path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img


_, input_dir, output_dir = sys.argv

json_dict = read_files(input_dir, 'json')
img_dict = read_files(input_dir, 'img')

for filename, img_filepath in img_dict.items():
    json_filepath = json_dict[filename]
    print(filename, '시각화!!')
    root, file = os.path.split(img_filepath)
    ext = os.path.splitext(img_filepath)[-1]
    mid = '\\'.join(root.split('\\')[len(input_dir.split('\\')):])
    folder = os.path.join(output_dir, mid)
    os.makedirs(folder, exist_ok=True)
    
    with open(json_filepath, encoding='UTF-8-SIG') as f:
        json_file = json.load(f)
        
    img = read_img(img_filepath)
    color = (255, 0, 0)
    for obj in json_file['objects']:
        for box in obj['boxes']:
            coor_list = []
            for coor in box['coords']:
                x = round(coor['x'])
                y = round(coor['y'])
                
                coor_list.append([x,y])
                
        points = np.array(coor_list, dtype=np.int32)
        cv2.polylines(img, np.int32([coor_list]), isClosed=True, color=color, thickness=1)
            
            
    result, n = cv2.imencode(ext, img)
    
    output_file_path = os.path.join(folder, file)
    if result:
        with open(output_file_path, mode='w+b') as f:
            n.tofile(f)