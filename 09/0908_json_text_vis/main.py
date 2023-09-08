import cv2, json, os, sys
from collections import defaultdict
from label import label
import numpy as np

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

_, input_dir, output_dir = sys.argv

json_dict = readfiles(input_dir, '.json')
img_dict = readfiles(input_dir, '.jpg')

for filename , img_path in img_dict.items():
    have_json = json_dict.get(filename)
    if have_json != None:
        json_path = json_dict[filename]
        root, file = os.path.split(img_path)
        mid = '\\'.join(root.split('\\')[len(input_dir.split('\\')):])
        folder = os.path.join(output_dir, mid)
        os.makedirs(folder, exist_ok=True)
        output_img_path = os.path.join(folder, file)

        with open(json_path, encoding='utf-8') as f:
            json_file = json.load(f)
        
        id = json_file['annotations'][0]['category_id']
        quality = json_file['annotations'][0]['attributes']['quality']
        
        for cat in json_file['categories']:
            if cat['id'] == id:
                name = cat['name']
        
        text_color = (0, 0, 0)
        img = read_img(img_path)
        
        img = label(img, name, 70, text_color, (0, 0), 0.5)
        img = label(img, quality, 70, text_color, (0, 80), 0.5)
        
        result, encoded_img = cv2.imencode('.jpg', img)
        if result:
            with open(output_img_path, mode='w+b') as f:
                encoded_img.tofile(f)