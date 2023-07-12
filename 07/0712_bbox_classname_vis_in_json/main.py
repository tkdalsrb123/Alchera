import json, os, sys
import pandas as pd
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont
import pybboxes.functional as pbf
from ast import literal_eval
import random

def random_color_generator():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)
             
_, input_dir, output_dir, surface_num = sys.argv

file_dict = defaultdict(list)
for root, dirs, files in os.walk(input_dir):
    for file in files:
        filename, ext = os.path.splitext(file)
        if ext == '.json':
            namekey = filename.split('-')[-1]
            path = os.path.join(root, file)
        elif ext == '.jpg':
            namekey = filename.split('-')[-1]
            path = os.path.join(root, file)
        
        file_dict[namekey].append(path)

for val in file_dict.values():
    for path in val:
        if '.json' in path:
            json_path = path
        elif '.jpg' in path:
            img_path = path

    with open(json_path, encoding='utf-8') as f:
        json_file = json.load(f)
    
    root, file = os.path.split(img_path)
    mid = '\\'.join(root.split('\\')[len(input_dir.split('\\')):])
    folder = os.path.join(output_dir, mid)
    os.makedirs(folder, exist_ok=True)
    output_img_dir = os.path.join(folder, file)
    
    
    img = Image.open(img_path)
    fontsize = 15
    fontpath = 'arial.ttf'
    font = ImageFont.truetype(fontpath, fontsize)
    draw = ImageDraw.Draw(img)
    
    if surface_num == '0':
        for ann in json_file['annotations']:
            random_color = random_color_generator()
            if ann['name'] != 'surface':
                coo_dict = literal_eval(ann['relative_coordinates'])
                center_x = coo_dict['center_x']
                center_y = coo_dict['center_y']
                width = coo_dict['width']
                height = coo_dict['height']
                text = ann['name']
                
                yolo_box = (center_x, center_y, width, height)
                x1, y1, x2, y2 = pbf.convert_bbox(yolo_box, from_type='yolo', to_type='voc', image_size=(1920, 1080))

                draw.rectangle((x1, y1, x2, y2), outline=random_color, width=3)
                draw.text((x1,y1-15), text, fill=random_color, font=font)
                
    elif surface_num == '1':
        for ann in json_file['annotations']:
            random_color = random_color_generator()
            if ann['name'] == 'surface':
                coo_dict = literal_eval(ann['relative_coordinates'])
                center_x = coo_dict['center_x']
                center_y = coo_dict['center_y']
                width = coo_dict['width']
                height = coo_dict['height']
                text = ann['name']
                
                yolo_box = (center_x, center_y, width, height)
                x1, y1, x2, y2 = pbf.convert_bbox(yolo_box, from_type='yolo', to_type='voc', image_size=(1920, 1080))

                draw.rectangle((x1, y1, x2, y2), outline=random_color)
                draw.text((x1,y1-10), text, fill=random_color)
        
 
    img.save(output_img_dir, 'JPEG')
    print(f'{output_img_dir} 저장!!!')
                