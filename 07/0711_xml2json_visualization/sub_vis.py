import cv2, os, sys, json
from collections import defaultdict
import numpy as np

def read_files(dir, Ext):
    file_dict = defaultdict(str)
    if Ext == 'img':
        for root, dirs, files in os.walk(dir):
            for file in files:
                filename, ext = os.path.splitext(file)
                if ext == '.jpg' or ext == '.png':
                    file_path = os.path.join(root, file)
                    
                    file_dict[filename] = file_path
    
        return file_dict

    elif Ext == 'json':
        for root, dirs, files in os.walk(dir):
            for file in files:
                filename, ext = os.path.splitext(file)
                if ext == '.json':
                    file_path = os.path.join(root, file)
                    
                    file_dict[filename] = file_path

        return file_dict

def read_img(img_path):
    img_array = np.fromfile(img_path, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img

_, json_dir, img_dir, output_dir = sys.argv

json_dict = read_files(json_dir, 'json')
img_dict = read_files(img_dir, 'img')

for filename, json_path in json_dict.items():
    img_path = img_dict[filename]
    print(img_path)
    root, file = os.path.split(img_path)
    mid = '\\'.join(root.split('\\')[len(img_dir.split('\\')):])
    folder = os.path.join(output_dir, mid)
    os.makedirs(folder, exist_ok=True)
    output_img_path = os.path.join(folder, file)

    with open(json_path, 'r', encoding='utf-8') as f:
        json_file = json.load(f)
        
    img = read_img(img_path)
    for obj in json_file['objects']:
        occlusion = obj['occlusion']
        truncation = obj['truncation']
        
        if occlusion != '0' or truncation != '0':
            text = f'{occlusion} {truncation}'
            xmin = obj['xmin']
            ymax = obj['ymax']
            
            cv2.putText(img, text, [xmin, ymax+10], cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,0,0), 1, cv2.LINE_AA)
        
    result, n = cv2.imencode('.png', img)
    
    if result:
        with open(output_img_path, mode='w+b') as f:
            n.tofile(f)        

        